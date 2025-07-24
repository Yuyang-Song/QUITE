# How to rewrite &quot;Recursive Query using WITH Clause&quot; in MySQL to fetch all levels of parent records for child record
[Link to question](https://stackoverflow.com/questions/12582076/how-to-rewrite-recursive-query-using-with-clause-in-mysql-to-fetch-all-levels)
**Creation Date:** 1348572713
**Score:** 2
**Tags:** mysql, sql, parent-child
## Question Body
<p>I am required to rewrite a query in MySQL which is originally written in MS SQL Server using the <code>WITH</code> clause. This is basically to fetch all levels of parent records for child records. Here, I am using the classic <code>EMPLOYEES</code> table of the <code>HR</code> schema in Oracle database as an example.</p>

<p>Originally data in <code>EMPLOYEES</code> table is in this format.</p>

<pre><code>select employee_id, manager_id
from employees
order by 1,2;

---------------------------------------------
EMPLOYEE_ID            MANAGER_ID             
---------------------- ---------------------- 
100                                           
101                    100                    
102                    100                    
103                    102                    
104                    103                    
107                    103                    
124                    100                    
141                    124                    
142                    124                    
143                    124                    
144                    124                    
149                    100                    
174                    149                    
176                    149                    
178                    149                    
200                    101                    
201                    100                    
202                    201                    
205                    101                    
206                    205
</code></pre>

<p>My requirement is to view all level of parent records for child records. I am able to achieve this using the following query in Oracle and MS SQL Server.</p>

<pre><code>WITH Asd(Child,
     Parent
    )
AS (SELECT Employee_Id,
           Manager_Id
      FROM Employees
    UNION ALL
    SELECT E.Employee_Id,
           A.Parent
      FROM Employees E, Asd A
      WHERE E.Manager_Id = A.Child
   )
SELECT Child,
       Parent
  FROM Asd
  WHERE Parent IS NOT NULL
  ORDER BY Child, Parent;

----------------------------------------------------------
CHILD                  PARENT                 
---------------------- -----------------------------------
101                    100                    
102                    100                    
103                    100                    
103                    102                    
104                    100                    
104                    102                    
104                    103                    
107                    100                    
107                    102                    
107                    103                    
124                    100                    
141                    100                    
141                    124                    
142                    100                    
142                    124                    
143                    100                    
143                    124                    
144                    100                    
144                    124                    
149                    100                    
174                    100                    
174                    149                    
176                    100                    
176                    149                    
178                    100                    
178                    149                    
200                    100                    
200                    101                    
201                    100                    
202                    100                    
202                    201                    
205                    100                    
205                    101                    
206                    100                    
206                    101                    
206                    205                    

36 rows selected
</code></pre>

<p>As you can see, I am bringing all the parents as well as grand parents under PARENT column in the query.</p>

<p>However, this approach does not work in MySQL as WITH clause is not supported.
Could anyone please help me on how to rewrite this query in MySQl?</p>

## Answers
### Answer ID: 12582264
<p>As for sept/2012, there is not direct substitute on MySQL for the <em>Common Table Expressions (CTE)</em> of MS SQL Server. You should rely on stored procedures.</p>

<p><a href="https://stackoverflow.com/questions/5291054/generating-depth-based-tree-from-hierarchical-data-in-mysql-no-ctes/5291159#5291159">Check this answer</a> to another identical question here in SO. It should answer all your doubts. I'm not copying any code as on the link everything is well detailed and explained.</p>

