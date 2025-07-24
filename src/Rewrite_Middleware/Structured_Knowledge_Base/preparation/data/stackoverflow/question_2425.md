# Optimizing sql condition to apply condition to all dependent rows
[Link to question](https://stackoverflow.com/questions/33635861/optimizing-sql-condition-to-apply-condition-to-all-dependent-rows)
**Creation Date:** 1447176080
**Score:** 1
**Tags:** sql, postgresql
## Question Body
<p>I have the following query, split up into a view for readability:</p>

<pre><code>CREATE TEMPORARY VIEW task_depcount AS
SELECT
    t.*,
    COUNT(p.id) AS unfinished_dep_count
FROM
    task t
    LEFT JOIN taskdependency d on t.id = d.task_id
    LEFT JOIN task p on  d.parent_task_id = p.id and p.status != 'SUCCESS'
GROUP BY t.id;

SELECT   t.id, t.task_type, t.status
FROM     task_depcount t
WHERE    t.status = 'READY' AND t.unfinished_dep_count = 0;
</code></pre>

<p>Now If we're looking at the <code>EXPLAIN ANALYZE</code> output, this is obviously very inefficient, as we cannot really do index scans over a COUNT() result. Rewriting into a single query with <code>HAVING</code> would also not improve it.</p>

<p>So here's the question: Is there a way to write this query so that the database isn't forced to do sequence scans all over? Database is PostgreSQL 9.2, with no option to upgrade to newer versions.</p>

<p>Or, to state the intended result in plain english: I need all the tasks where either all it's dependencies are of status "success", or there are no dependencies at all.</p>

## Answers
### Answer ID: 33637016
<pre><code>create temporary view task_depcount as
select t.*
from
    task t
    left join
    taskdependency d on t.id = d.task_id
    left join
    task p on d.parent_task_id = p.id
group by t.id
having not bool_or(p.status != success) or not bool_or(d.task_id is not null)
;

select t.id, t.task_type, t.status
from task_depcount t
where t.status = 'READY'
</code></pre>

### Answer ID: 33635927
<p>You can use <code>not exists</code>:</p>

<pre><code>SELECT t.*
FROM task t
WHERE NOT EXISTS (SELECT 1
                  FROM taskdependency d JOIN 
                       task p
                       ON d.parent_task_id = p.id 
                  WHERE t.id = d.task_id AND p.status &lt;&gt; 'SUCCESS'
                 );
</code></pre>

<p>With the right indexes, this should be much faster.</p>

<p>The use of an aggregation function such as <code>COUNT()</code> -- whether in a view, subquery, or CTE -- requires processing all the data.  With <code>NOT EXISTS</code>, the processing can stop for each at the first unsuccessful one (if any) and not have to do any aggregation.</p>

