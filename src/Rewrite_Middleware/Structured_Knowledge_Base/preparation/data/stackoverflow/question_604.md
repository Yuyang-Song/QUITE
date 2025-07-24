# How do We Transform sql server 2012 query syntax into postgresql or standard sql
[Link to question](https://stackoverflow.com/questions/33299142/how-do-we-transform-sql-server-2012-query-syntax-into-postgresql-or-standard-sql)
**Creation Date:** 1445592870
**Score:** -2
**Tags:** sql-server, database-migration, greenplum
## Question Body
<p><strong>We tried to transposing of data using unpivot operator in sql server 2012.same thing we have to output using postgres database. so,we have to rewrite given syntax into postgresql.</strong></p>

<p>We have also tried on postgresql :
uncrosstab() function using given query structure.</p>

<pre><code>select * from uncrosstab( select * from tablename) as ct()
</code></pre>

<p><strong>ie Our input sql server 2012  syntax is :</strong></p>

<pre><code>select Name,budget,CASE WHEN bmon='BudMnt1' THEN CONVERT(DATE, '01-JAN-2015')
WHEN bmon='BudMnt2' THEN CONVERT(DATE, '01-FEB-2015')
WHEN bmon='BudMnt3' THEN CONVERT(DATE, '01-MAR-2015')
WHEN bmon='BudMnt4' THEN CONVERT(DATE, '01-APR-2015')
WHEN bmon='BudMnt5' THEN CONVERT(DATE, '01-MAY-2015')
WHEN bmon='BudMnt6' THEN CONVERT(DATE, '01-JUN-2015')
WHEN bmon='BudMnt7' THEN CONVERT(DATE, '01-JUL-2015')
WHEN bmon='BudMnt8' THEN CONVERT(DATE, '01-AUG-2015')
WHEN bmon='BudMnt9' THEN CONVERT(DATE, '01-SEP-2015')
WHEN bmon='BudMnt10' THEN CONVERT(DATE, '01-OCT-2015')
WHEN bmon='BudMnt11' THEN CONVERT(DATE, '01-NOV-2015')
WHEN bmon='BudMnt12' THEN CONVERT(DATE, '01-DEC-2015')
END AS bmon from tablename
UNPIVOT
(
       budget
       FOR bmon IN (BudMnt1,
BudMnt2,
BudMnt3,
BudMnt4,
BudMnt5,
BudMnt6,
BudMnt7,
BudMnt8,
BudMnt9,
BudMnt10,
BudMnt11,
BudMnt12)
) p 
</code></pre>

<p>Any help would be much appreciated ?</p>

## Answers
### Answer ID: 33350037
<p>PIVOT and UNPIVOT are non-ANSI standard SQL commands that I am not familiar with.  I also don't have your full table definition so I am having a hard time just understanding your SQL.  So, I turned to Microsoft's site and found an example to work with.</p>

<p><a href="https://technet.microsoft.com/en-us/library/ms177410(v=sql.105).aspx" rel="nofollow">https://technet.microsoft.com/en-us/library/ms177410(v=sql.105).aspx</a></p>

<p>Using their UNPIVOT example, I came up with two solutions.  First, let's create a table in Greenplum and insert some values.</p>

<pre><code>CREATE TABLE pvt (VendorID int, Emp1 int, Emp2 int, Emp3 int, Emp4 int, Emp5 int)
distributed by (vendorid);

INSERT INTO pvt VALUES (1,4,3,5,4,4);
INSERT INTO pvt VALUES (2,4,1,5,5,5);
INSERT INTO pvt VALUES (3,4,3,5,4,4);
INSERT INTO pvt VALUES (4,4,2,5,5,4);
INSERT INTO pvt VALUES (5,5,1,5,5,5);
</code></pre>

<p>The unsupported Microsoft UNPIVOT example:</p>

<pre><code>SELECT VendorID, Employee, Orders
FROM 
   (SELECT VendorID, Emp1, Emp2, Emp3, Emp4, Emp5
   FROM pvt) p
UNPIVOT
   (Orders FOR Employee IN 
      (Emp1, Emp2, Emp3, Emp4, Emp5)
)AS unpvt;
GO
</code></pre>

<p>Solution 1</p>

<pre><code>select vendorid, 'emp1' as employee, emp1 from pvt
union all
select vendorid, 'emp2' as employee, emp2 from pvt
union all
select vendorid, 'emp3' as employee, emp3 from pvt
union all
select vendorid, 'emp4' as employee, emp4 from pvt
union all
select vendorid, 'emp5' as employee, emp5 from pvt;
</code></pre>

<p>This is simple and easy to write but each query is run sequentially.  It also means you are scanning the pvt table 5 times but it might be the right solution for you.  </p>

<p>Solution 2</p>

<pre><code>select vendorid, 
       split_part(unpivot, ',', 1) as employee, 
       split_part(unpivot, ',', 2) as orders
from    (
        select vendorid, unnest(employee) as unpivot
        from    (
                select vendorid, 
                       array['emp1,' || emp1, 
                             'emp2,' || emp2, 
                             'emp3,' || emp3, 
                             'emp4,' || emp4, 
                             'emp5,' || emp5] as employee 
                from pvt
                ) as sub
        ) as sub2;
</code></pre>

<p>Solution 2 is a little "cooler" as it passes through the pvt table only once and converts the distinct columns into array elements.  I concatenated the name of the column so I could have a index to each array element.  I then used unnest to convert the array elements to rows.  Finally, I used split_part to split each array index + value into separate columns.  For fun, I called this "unpivot".  :)</p>

<p>Lastly, I suggest you store the data so that is easy to use.  That recommendation is valid for any database too.  If you often want to see the data that is the result of UNPIVOT, store the data that way.  Don't make analysis harder than it should be.</p>

