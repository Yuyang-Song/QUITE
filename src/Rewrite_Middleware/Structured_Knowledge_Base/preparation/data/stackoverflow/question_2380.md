# Performance issue on selecting n newest rows in subselect
[Link to question](https://stackoverflow.com/questions/32093810/performance-issue-on-selecting-n-newest-rows-in-subselect)
**Creation Date:** 1439982554
**Score:** 1
**Tags:** sql, sql-server, group-by, top-n
## Question Body
<p>I have a database with courses. Each course contains a set of nodes, and some nodes contains a set of answers from students. The Answer table looks (simplified) like this:</p>

<p>Answer</p>

<pre><code>id  | courseId |  nodeId |  answer
------------------------------------------------
 1  |   1      |   1     |  &lt;- text -&gt;
 2  |   2      |   2     |  &lt;- text -&gt;
 3  |   1      |   1     |  &lt;- text -&gt;
 4  |   1      |   3     |  &lt;- text -&gt;
 5  |   2      |   2     |  &lt;- text -&gt;
..  |  ..      |   ..    |  ..
</code></pre>

<p>When a teacher opens a course (i.e. courseId = 1) I want to pick the node that have received the most answers lately. I can do this using the following query:</p>

<pre><code>with Answers as
(
   select top 50 id, nodeId from Answer A where courseId=1 order by id desc
)
select top 1 nodeId from Answers group by nodeId order by count(id) desc
</code></pre>

<p>or equally using this query:</p>

<pre><code>select top 1 nodeId from 
    (select top 50 id, nodeId from Answer A where courseId=1 order by id desc)
    group by nodeId order by count(id) desc
</code></pre>

<p>In both querys the newest 50 answers (with the highest ids) are selected and then grouped by nodeId so I can pick the one with the highest frequency. My problem is, however, that the query is very slow. If I only run the subselect, it takes less than a second, and grouping 50 rows should be fast, but when I run the entire query it takes about 10 seconds! My guess is that sql server does the select and grouping first, and afterwards does the top 50 and top 1, which in this case leads to terrible performance.</p>

<p>So, how can I rewrite the query to be efficient?  </p>

## Answers
### Answer ID: 32094745
<p>To be more insightful we'd need to see the indexes on that table and the execution plans you're getting <em>(one plan for the inner query on it's own, one plan for the full query)</em>.</p>

<p>I'd even recommend doing the same analysis again having added the index mentioned elsewhere on this page.</p>

<p>Without that information the only things we can recommend are trial and error.</p>

<p>For example, try avoiding using <code>TOP</code> <em>(this shouldn't matter, but we're guessing while we can't see your indexes and execution plans)</em></p>

<pre><code>WITH
    Answers AS
(
    SELECT
        ROW_NUMBER() OVER (ORDER BY id DESC)   AS rowId,
        id,
        nodeId
    FROM
        Answer
    WHERE
        courseId = 1
),
    top50 AS
(
    SELECT
        nodeId,
        COUNT(*)   AS row_count
    FROM
        Answers
    WHERE
        rowId &lt;= 50
    GROUP BY
        nodeId
),
    ranked AS
(
    SELECT
        ROW_NUMBER() OVER (ORDER BY row_count DESC, nodeId DESC)  AS ordinal,
        nodeID
    FROM
        top50
)
SELECT
    nodeID
FROM
    ranked
WHERE
    oridinal = 1
</code></pre>

<p>Which is massively over the top, but functionally the same as you have in your OP, but sufficiently different to <em>potentially</em> get a different execution plan.</p>

<p>Alternatively <em>(and not very nice)</em>, just put the results of your inner query in to a table variable, then run the outer query on the table variable.</p>

<p>I still expect, however, that adding the index will be the least-worst option.</p>

### Answer ID: 32093862
<p>You can add indexes to make your queries more efficient.  For this query:</p>

<pre><code>with Answers as (
      select top 50 id, nodeId
      from Answer A
      where courseId = 1
      order by id desc
     )
select top 1 nodeId
from Answers
group by nodeId
order by count(id) desc;
</code></pre>

<p>The best index is <code>Answer(courseId, id, nodeid)</code>.</p>

