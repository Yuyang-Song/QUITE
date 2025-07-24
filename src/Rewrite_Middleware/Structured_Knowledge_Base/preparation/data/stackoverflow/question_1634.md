# How to avoid nested SQL query in this case?
[Link to question](https://stackoverflow.com/questions/2132905/how-to-avoid-nested-sql-query-in-this-case)
**Creation Date:** 1264429812
**Score:** 1
**Tags:** sql, mysql, subquery
## Question Body
<p>I have an SQL question, related to <a href="https://stackoverflow.com/questions/284984/sql-query-without-nested-queries">this</a> and <a href="https://stackoverflow.com/questions/855970/avoiding-a-nested-subquery-in-sql">this</a> question (but different). Basically I want to know how I can avoid a nested query.</p>

<p>Let's say I have a huge table of jobs (<code>jobs</code>) executed by a company in their history. These jobs are characterized by year, month, location and the code belonging to the tool used for the job. Additionally I have a table of tools (<code>tools</code>), translating tool codes to tool descriptions and further data about the tool. Now they want a website where they can select year, month, location and tool using a dropdown box, after which the matching jobs will be displayed. I want to fill the last dropdown with only the relevant tools matching the before selection of year, month and location, so I write the following nested query:</p>

<pre><code>SELECT c.tool_code, t.tool_description
FROM (
 SELECT DISTINCT j.tool_code
 FROM jobs AS j
 WHERE j.year = ....
        AND j.month = ....
 AND j.location = ....
) AS c
LEFT JOIN tools as t
ON c.tool_code = t.tool_code
ORDER BY c.tool_code ASC
</code></pre>

<p>I resorted to this nested query because it was much faster than performing a JOIN on the complete database and selecting from that. It got my query time down a lot. But as I have recently read that <a href="http://www.selikoff.net/2008/12/10/memo-avoid-nested-queries-in-mysql-at-all-costs/" rel="nofollow noreferrer">MySQL nested queries should be avoided at all cost</a>, I am wondering whether I am wrong in this approach. Should I rewrite my query differently? And how?</p>

## Answers
### Answer ID: 2132935
<p>No, you shouldn't, your query is fine.</p>

<p>Just create an index on <code>jobs (year, month, location, tool_code)</code> and <code>tools (tool_code)</code> so that the <code>INDEX FOR GROUP-BY</code> can be used.</p>

<p>The article your provided describes the subquery predicates (<code>IN (SELECT ...)</code>), not the nested queries (<code>SELECT FROM (SELECT ...)</code>).</p>

<p>Even with the subqueries, the article is wrong: while <code>MySQL</code> is not able to optimize all subqueries, it deals with <code>IN (SELECT …)</code> predicates just fine.</p>

<p>I don't know why the author chose to put <code>DISTINCT</code> here:</p>

<pre><code>SELECT  id, name, price
FROM    widgets
WHERE   id IN
        (
        SELECT  DISTINCT widgetId
        FROM    widgetOrders
        )
</code></pre>

<p>and why do they think this will help to improve performance, but given that <code>widgetID</code> is indexed, <code>MySQL</code> will just transform this query:</p>

<pre><code>SELECT  id, name, price
FROM    widgets
WHERE   id IN
        (
        SELECT  widgetId
        FROM    widgetOrders
        )
</code></pre>

<p>into an <code>index_subquery</code></p>

<p>Essentially, this is just like <code>EXISTS</code> clause: the inner subquery will be executed once per <code>widgets</code> row with the additional predicate added:</p>

<pre><code>SELECT  NULL
FROM    widgetOrders
WHERE   widgetId = widgets.id
</code></pre>

<p>and stop on the first match in <code>widgetOrders</code>.</p>

<p>This query:</p>

<pre><code>SELECT  DISTINCT w.id,w.name,w.price
FROM    widgets w
INNER JOIN
        widgetOrders o
ON      w.id = o.widgetId
</code></pre>

<p>will have to use <code>temporary</code> to get rid of the duplicates and will be much slower.</p>

### Answer ID: 2132951
<p>You could avoid the subquery by using <code>GROUP BY</code>, but if the subquery performs better, keep it.</p>

<p>Why do you use a <code>LEFT JOIN</code> instead of a <code>JOIN</code> to join <code>tools</code>?</p>

