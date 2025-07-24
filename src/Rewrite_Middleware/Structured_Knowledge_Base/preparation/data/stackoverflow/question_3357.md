# How to more efficiently write multiple EXISTS subquery in Postgresql
[Link to question](https://stackoverflow.com/questions/77092159/how-to-more-efficiently-write-multiple-exists-subquery-in-postgresql)
**Creation Date:** 1694547004
**Score:** -1
**Tags:** sql, postgresql, subquery
## Question Body
<p>I'm querying my database where a workflow has multiple of a specific property in a related table. I've managed to write a query that correctly gets the results but it is using multiple subqueries, and I'm sure there's a more efficient way to write it.</p>
<pre><code>SELECT *
FROM   workflow w
WHERE  EXISTS (SELECT ti.id
               FROM   task_instance ti
                      left join workflow_task_instance wti
                             ON ti.id = wti.task_instance_id
               WHERE  ti.task_type = 'TASK_ONE'
                      AND wti.workflow_id = w.id)
       AND EXISTS (SELECT ti.id
                   FROM   task_instance ti
                          left join workflow_task_instance wti
                                 ON ti.id = wti.task_instance_id
                   WHERE  ti.task_type = 'TASK_TWO'
                          AND wti.workflow_id = w.id); 
</code></pre>
<p>How can I rewrite this to use just one subquery, or joins instead of subqueries?</p>

## Answers
### Answer ID: 77101173
<p>You can calculate which workflow_ids have both task_types using a  single subquery that uses a <code>GROUP BY</code> clause and a subsequent <code>HAVING</code> clause. Whist you could continue to use EXISTS with this single subquery approach; an <code>INNER JOIN</code> seems the more direct route.</p>
<pre><code>SELECT w.*
FROM workflow w
INNER JOIN (
    SELECT wti.workflow_id
    FROM task_instance ti
    INNER JOIN workflow_task_instance wti ON ti.id = wti.task_instance_id
    WHERE ti.task_type IN ('TASK_ONE', 'TASK_TWO')
    GROUP BY wti.workflow_id
    HAVING COUNT(DISTINCT ti.task_type) = 2
    ) subquery ON w.id = subquery.workflow_id
</code></pre>
<p><strong>nb</strong></p>
<ul>
<li>there is no point using a left join inside the subquery because unmatched rows (producing NULL in the workflow_id column) will be ignored anyway.</li>
<li>because the subquery groups by workflow_id there will only be one row per workflow_id in the result, hence joining the subquery to the workflow table will not multiply the resultant rows (therefore removing a key advantage of using EXISTS).</li>
</ul>

