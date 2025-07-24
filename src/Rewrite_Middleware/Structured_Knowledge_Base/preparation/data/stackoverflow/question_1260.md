# How to improve SQL query performance containing partially common subqueries
[Link to question](https://stackoverflow.com/questions/66994155/how-to-improve-sql-query-performance-containing-partially-common-subqueries)
**Creation Date:** 1617829883
**Score:** 1
**Tags:** sql, postgresql, window-functions, postgresql-performance, conditional-aggregation
## Question Body
<p>I have a simple table <code>tableA</code> in PostgreSQL 13 that contains a time series of event counts. In stylized form it looks something like this:</p>
<pre><code>event_count     sys_timestamp

100             167877672772
110             167877672769
121             167877672987
111             167877673877
...             ...
</code></pre>
<p>With both fields defined as <code>numeric</code>.</p>
<p>With the help of answers from stackoverflow I was able to create a query that basically counts the number of positive and negative excess events within a given time span, conditioned on the current event count. The query looks like this:</p>
<pre><code>SELECT t1.*,

    (SELECT COUNT(*) FROM tableA t2 
        WHERE t2.sys_timestamp &gt; t1.sys_timestamp AND 
        t2.sys_timestamp &lt;= t1.sys_timestamp + 1000 AND
        t2.event_count &gt;= t1.event_count+10)
    AS positive, 

    (SELECT COUNT(*) FROM tableA t2 
       WHERE t2.sys_timestamp &gt; t1.sys_timestamp AND 
       t2.sys_timestamp &lt;= t1.sys_timestamp + 1000 AND
       t2.event_count &lt;= t1.event_count-10) 
    AS negative 

FROM tableA as t1
</code></pre>
<p>The query works as expected, and returns in this particular example for each row a count of positive and negative excesses (range + / - 10) given the defined time window (+ 1000 [milliseconds]).</p>
<p>However, I will have to run such queries for tables with several million (perhaps even 100+ million) entries, and even with about 500k rows, the query takes a looooooong time to complete. Furthermore, whereas the time frame remains always the same within a given query [but the window size can change from query to query], in some instances I will have to use maybe 10 additional conditions similar to the positive / negative excesses in the same query.</p>
<p>Thus, I am looking for ways to improve the above query primarily to achieve better performance considering primarily the size of the envisaged dataset, and secondarily with more conditions in mind.</p>
<p>My concrete questions:</p>
<ol>
<li><p>How can I reuse the common portion of the subquery to ensure that it's not executed twice (or several times), i.e. how can I reuse this within the query?</p>
<pre><code> (SELECT COUNT(*) FROM tableA t2 
  WHERE t2.sys_timestamp &gt;  t1.sys_timestamp
  AND   t2.sys_timestamp &lt;= t1.sys_timestamp + 1000)
</code></pre>
</li>
<li><p>Is there some performance advantage in turning the <code>sys_timestamp</code> field which is currently <code>numeric</code>, into a timestamp field, and attempt using any of the PostgreSQL Windows functions? (Unfortunately I don't have enough experience with this at all.)</p>
</li>
<li><p>Are there some clever ways to rewrite the query aside from reusing the (partial) subquery that materially increases the performance for large datasets?</p>
</li>
<li><p>Is it perhaps even faster for these types of queries to run them outside of the database using something like Java, Scala, Python etc. ?</p>
</li>
</ol>

## Answers
### Answer ID: 66996704
<p>You have the right idea.
The way to write statements you can reuse in a query is &quot;with&quot; statements (AKA subquery factoring). The &quot;with&quot; statement runs once as a subquery of the main query and can be reused by subsequent subqueries or the final query.</p>
<p>The first step includes creating parent-child detail rows - table multiplied by itself and filtered down by the timestamp.</p>
<p>Then the next step is to reuse that same detail query for everything else.</p>
<p>Assuming that event_count is a primary index or you have a compound index on event_count and sys_timestamp, this would look like:</p>
<pre><code>with baseQuery as
(
   SELECT distinct t1.event_count as startEventCount, t1.event_count+10 as pEndEventCount 
   ,t1.eventCount-10 as nEndEventCount, t2.event_count as t2EventCount
   FROM tableA t1, tableA t2 
   where t2.sys_timestamp between t1.sys_timestamp AND t1.sys_timestamp + 1000
), posSummary as
(
   select bq.startEventCount, count(*) as positive
   from baseQuery bq
   where t2EventCount between bq.startEventCount and bq.pEndEventCount
   group by bq.startEventCount 
), negSummary as
(
   select bq.startEventCount, count(*) as negative
   from baseQuery bq
   where t2EventCount between bq.startEventCount and bq.nEndEventCount
   group by bq.startEventCount 
)
select t1.*, ps.positive, nv.negative
from tableA t1 
inner join posSummary ps on t1.event_count=ps.startEventCount
inner join negSummary ns on t1.event_count=ns.startEventCount
</code></pre>
<p>Notes:</p>
<ol>
<li>The distinct for baseQuery may not be necessary based on your actual keys.</li>
<li>The final join is done with tableA but could also use a summary of baseQuery as a separate &quot;with&quot; statement which already ran once. Seemed unnecessary.</li>
</ol>
<p>You can play around to see what works.</p>
<p>There are other ways of course but this best illustrates how and where things could be improved.</p>
<p>With statements are used in multi-dimensional data warehouse queries because when you have so much data to join with so many tables(dimensions and facts), a strategy of isolating the queries helps understand where indexes are needed and perhaps how to minimize the rows the query needs to deal with further down the line to completion.
For example, it should be obvious that if you can minimize the rows returned in baseQuery or make it run faster (check explain plans), your query improves overall.</p>

### Answer ID: 66995827
<blockquote>
<p>How can I reuse the common portion of the subquery ...?</p>
</blockquote>
<p>Use conditional aggregates in a single <code>LATERAL</code> subquery:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT t1.*, t2.positive, t2.negative
FROM   tableA t1
CROSS  JOIN LATERAL (
   SELECT COUNT(*) FILTER (WHERE t2.event_count &gt;= t1.event_count + 10) AS positive
        , COUNT(*) FILTER (WHERE t2.event_count &lt;= t1.event_count - 10) AS negative
   FROM   tableA t2 
   WHERE  t2.sys_timestamp &gt;  t1.sys_timestamp
   AND    t2.sys_timestamp &lt;= t1.sys_timestamp + 1000
   ) t2;
</code></pre>
<p>It can be a <code>CROSS JOIN</code> because the subquery always returns a row. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/35374860/join-select-ue-on-1-1/35375634#35375634">JOIN (SELECT ... ) ue ON 1=1?</a></li>
<li><a href="https://stackoverflow.com/questions/28550679/what-is-the-difference-between-lateral-join-and-a-subquery-in-postgresql/28557803#28557803">What is the difference between LATERAL JOIN and a subquery in PostgreSQL?</a></li>
</ul>
<p>Use conditional aggregates with the <code>FILTER</code> clause to base multiple aggregates on the same time frame. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/27136251/aggregate-columns-with-additional-distinct-filters/27141193#27141193">Aggregate columns with additional (distinct) filters</a></li>
</ul>
<p><code>event_count</code> should probably be <code>integer</code> or <code>bigint</code>. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/33836749/postgresql-using-uuid-vs-text-as-primary-key/33838373#33838373">PostgreSQL using UUID vs Text as primary key</a></li>
<li><a href="https://stackoverflow.com/questions/33583490/is-there-any-difference-in-saving-same-value-in-different-integer-types/33584708#33584708">Is there any difference in saving same value in different integer types?</a></li>
</ul>
<p><code>sys_timestamp</code> should probably be <code>timestamp</code> or <code>timestamptz</code>. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/9571392/ignoring-time-zones-altogether-in-rails-and-postgresql/9576170#9576170">Ignoring time zones altogether in Rails and PostgreSQL</a></li>
</ul>
<p>An index on <code>(sys_timestamp)</code> is minimum requirement for this. A multicolumn index on <code>(sys_timestamp, event_count)</code> typically helps some more. If the table is vacuumed enough, you get index-only scans from it.</p>
<p>Depending on exact data distribution (most importantly how much time frames overlap) and other db characteristics, a tailored procedural solution may be faster, yet. Can be done in any client-side language. But a server-side PL/pgsql  solution is superior because it saves all the round trips to the DB server and type conversions etc. See:</p>
<ul>
<li><a href="https://stackoverflow.com/questions/18173412/window-functions-or-common-table-expressions-count-previous-rows-within-range">Window Functions or Common Table Expressions: count previous rows within range</a></li>
<li><a href="https://stackoverflow.com/questions/7510092/what-are-the-pros-and-cons-of-performing-calculations-in-sql-vs-in-your-applica/7518619#7518619">What are the pros and cons of performing calculations in sql vs. in your application</a></li>
</ul>

