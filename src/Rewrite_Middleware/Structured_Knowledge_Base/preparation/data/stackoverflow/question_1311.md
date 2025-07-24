# Transferring SQL query from with clause to without with clause
[Link to question](https://stackoverflow.com/questions/69762599/transferring-sql-query-from-with-clause-to-without-with-clause)
**Creation Date:** 1635470583
**Score:** 0
**Tags:** sql, database, with-statement
## Question Body
<p>Consider the query:</p>
<p>Find all departments where the total salary is greater than the average of the total salary at all departments</p>
<pre><code>with dept_total (dept_name, value) as
(
    select dept_name, sum(salary)
    from instructor
    group by dept_name
),
dept_total_avg(value) as
(
    select avg(value)
    from dept_total
)
select dept_name
from dept_total, dept_total_avg
where dept_total.value &gt;= dept_total avg.value;
</code></pre>
<p>Rewrite this query without using the with construct.</p>
<p>The query is based on University schema which is provided by The database system concept by Korth. I assume I need to consider only the instructor table to find the answer of the query.</p>
<p>Instructor (<strong>ID</strong>, name, dept_name, salary)</p>
<p>I can found the average of total salary of all dept</p>
<pre><code>SELECT AVG(salary) GROUP BY dept_name;
</code></pre>
<p>Then I lost. I did not find the way to proceed.</p>
<p>I found <a href="https://stackoverflow.com/questions/53111096/rewrite-sql-without-with-clause">that</a>. But I am looking for more explanation as I cannot understand it from this link.</p>
<p>Thank you for help.</p>

## Answers
### Answer ID: 69763217
<p>Here's a few ways to do it in a mySQL version that doesn't support CTEs (I'm assuming that's why they are having you rewrite the query to omit the with).  Also, you are calculating the average salary by department, but the question is asking to find the average TOTAL salary of each department, then return the ones that fall above that.</p>
<p><a href="https://dbfiddle.uk/?rdbms=mysql_5.5&amp;fiddle=fefea829cff3e20aea93634f9a4114d6" rel="nofollow noreferrer">https://dbfiddle.uk/?rdbms=mysql_5.5&amp;fiddle=fefea829cff3e20aea93634f9a4114d6</a></p>
<p>With a subquery:</p>
<pre><code>SELECT dept_name
FROM (
  SELECT dept_name, sum(salary) as salaries
  FROM instructor GROUP BY dept_name
) d

WHERE salaries &gt; (
  SELECT avg(salaries) as avgSalaries FROM (
    SELECT dept_name, sum(salary) as salaries
    FROM instructor GROUP BY dept_name
  ) z
)
</code></pre>
<p>With a join:</p>
<pre><code>SELECT dept_name
FROM (
  SELECT dept_name, sum(salary) as salaries
  FROM instructor GROUP BY dept_name
) d
CROSS JOIN (
  SELECT avg(salaries) as avgSalaries FROM (
    SELECT dept_name, sum(salary) as salaries
    FROM instructor GROUP BY dept_name
  ) z
) avgs
WHERE salaries &gt; avgs.avgSalaries
</code></pre>
<p>With a session variable (this is deprecated in later versions, but does still work):</p>
<pre><code>SELECT avg(salaries) INTO @avg FROM (
  SELECT dept_name, sum(salary) as salaries
  FROM instructor GROUP BY dept_name
) z;

SELECT @avg;

SELECT dept_name
FROM instructor GROUP BY dept_name
HAVING sum(salary) &gt; @avg;
</code></pre>
<p>All good techniques to understand.</p>

### Answer ID: 69762789
<p>Read your last question and found that you are using mysql5.8, then you can use the analysis function</p>
<pre class="lang-sql prettyprint-override"><code>select distinct t1.dept_name
  from (
select t1.*,
       sum(salary) over(partition by dept_name) val,
       sum(salary) over() / count(distinct dept_name) over() avg
  from Instructor t1
) t1
 where t1.val &gt; t1.avg
</code></pre>

