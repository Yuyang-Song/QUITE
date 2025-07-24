# Get top salary by department without using any subquery
[Link to question](https://stackoverflow.com/questions/67260914/get-top-salary-by-department-without-using-any-subquery)
**Creation Date:** 1619411981
**Score:** 0
**Tags:** sql, common-table-expression, window-functions
## Question Body
<p>Let's say we have 2 database tables - <code>emp</code> and <code>dept</code>, which consists of the following columns</p>
<p><code>emp</code>: empid, deptid, salary</p>
<p><code>dept</code>: deptid, deptname</p>
<p>The deptid column in <code>emp</code> can be joined with deptid column in <code>dept</code> column. Note that some departments don't have any employee. For those cases, the deptid in <code>dept</code> table won't exist in <code>emp</code> table.
We need to find top salary in each department. For departments that don't have any employee, we need to assign them the highest salary from <code>emp</code> table. One requirement is that we can NOT use subquery, but CTE (common table expression) is allowed.</p>
<p>Below is the query I built:</p>
<pre><code>with cte as 
(Select d.deptid, e.salary, row_number() over (partition by d.deptid order by e.salary desc) as rnk,
row_number() over(order by e.salary desc) as salary_rank    
from emp e 
join dept d on e.deptid = dept.deptid),

top_salary as 
(Select d.deptid, e.salary 
from emp e 
join dept d on e.deptid = dept.deptid
order by e.salary desc
limit 1)


(Select d.deptid, cte.salary 
from cte 
join dept d on d.deptid = cte.deptid
where cte.rnk = 1) as t1

UNION 

(Select d.deptid, ts.salary  
from dept d 
left join cte on cte.deptid = d.deptid 
left join top_salary ts on ts.deptid = cte.deptid 
where cte.salary is null
)
</code></pre>
<p>But I am not sure if I did it correctly, especially in cases where the departments don't have any employees. I am also not sure if the 2 queries I wrote surrounding the <code>UNION</code> clause are considered subqueries. If they are indeed subqueries, then is there a way I can rewrite that query without using any subquery?</p>

## Answers
### Answer ID: 67266530
<blockquote>
<p>We need to find top salary in each department. For departments that don't have any employee, we need to assign them the highest salary from emp table.</p>
</blockquote>
<p>Your attempt seems overly complicated:</p>
<pre><code>with edmax as (
      select e.deptid, max(e.salary) as max_salary
      from emp
      group by e.deptid
     ),
     emax as (
      select max(e.salary) as max_salary
     )
select d.*, max(edmax.max_salary, emax.max_salary) as max_salary
from dept d left join
     edmax
     on d.deptid = edmax.deptid cross join
     emax;
</code></pre>
<p>The basic idea is to calculate the maximum salary for each department and then &quot;default&quot; to the overall maximum.</p>
<p>By the way, you <em>could</em> do this only with joins:</p>
<pre><code>select d.deptid, d.name,
       coalesce(max(de.salary), max(d.salary))
from emp e cross join
     dept d left join
     dept de
     on de.deptid = e.deptid
group by d.deptid, d.name;
</code></pre>
<p>I don't recommend this approach but you might want to understand it.</p>

