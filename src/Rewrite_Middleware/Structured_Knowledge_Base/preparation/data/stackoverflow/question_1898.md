# SELECT query poor execution plan with &quot;WHERE A=1 OR A=2 clause&quot;
[Link to question](https://stackoverflow.com/questions/11519767/select-query-poor-execution-plan-with-where-a-1-or-a-2-clause)
**Creation Date:** 1342517721
**Score:** 1
**Tags:** sql-server, sql-server-2008, sql-server-2005, postgresql, sql-execution-plan
## Question Body
<p>We currently have a <code>LOGS</code> TABLE divided with multiple logbooks numbers (column <code>XLOG</code>), and accessed within a limited time range.</p>

<p>The table is declared with a clustered 'natural' primary key, where <code>XLOG</code> is logbook identifier, <code>XDATE</code> is the timestamp, and <code>XHW and XCELL</code> are hardware identifiers ensuring unicity of log events :</p>

<pre class="lang-sql prettyprint-override"><code> CREATE TABLE [dbo].[LOGS](
    [XDATE] [datetime] NOT NULL,
    [XHW] [nvarchar](3) NOT NULL,
    [XCELL] [nvarchar](3) NOT NULL,
    [XALIAS] [nvarchar](255) NULL,
    [XMESSAGE] [nvarchar](255) NULL,
    [XLOG] [int] NOT NULL,
 CONSTRAINT [PK_LOG] PRIMARY KEY CLUSTERED ([XLOG] ASC,[XDATE] ASC,[XHW] ASC,[XCELL] ASC)
</code></pre>

<p>The problem is a horrible execution plan occuring when accessing multiple logbooks with the same query (e.g. <code>XLOG = 1 OR XLOG = 1002</code> in the sample query below), request #1 :</p>

<pre class="lang-sql prettyprint-override"><code>SELECT TOP 100 XDATE, XHW, XCELL, XMESSAGE, XLOG FROM LOGS
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250'
AND (XLOG = 1 OR XLOG = 1002)
ORDER BY XDATE DESC, XLOG DESC
</code></pre>

<p><strong>Edit:</strong> the 100 rows needed are not only from logbook #1, but from both logbooks, mixed, date ordered. That is what both queries return.</p>

<p>Statistics were updated before the tests.</p>

<p>The actual execution plan basically uses clustered index seek to fetch million rows of data with a predicate on <code>XLOG</code> and <code>XDATE</code>, (where it might only fetch 100 first/last rows since we have XLOG= and we TOP order by XDATE) <img src="https://i.sstatic.net/dc7NM.png" alt="actual plan"></p>

<p>The details of the clustered index seek operation : <img src="https://i.sstatic.net/wzbGU.png" alt="tooltip"></p>

<p>The expected execution plan is <img src="https://i.sstatic.net/hDBsZ.png" alt="expected plan"></p>

<p>I tried to rewrite the query, but could not find another way except with <code>UNION ALL</code>. The resulting query returns the same results (with a correct plan !) but it feels over-complicated (and cannot be adapted with a JOIN on XLOG, but that is not the question) request #2 :</p>

<pre class="lang-sql prettyprint-override"><code>WITH A AS (SELECT TOP 100 XDATE,  XHW, XCELL, XMESSAGE, XLOG FROM LOGS
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250'
AND XLOG = 1
ORDER BY XDATE DESC),

B AS (SELECT TOP 100 XDATE,  XHW, XCELL, XMESSAGE, XLOG FROM LOGS
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250'
AND XLOG = 1002
ORDER BY XDATE DESC)

SELECT TOP 100 * FROM (
    SELECT * FROM A
    UNION ALL 
    SELECT * FROM B 
) A
ORDER BY XDATE DESC, XLOG DESC
</code></pre>

<p><strong>Question:</strong> What is wrong with request #1 ? how can it be rewritten/modified, to take the 'TOP' into account before attempting to sort millions of rows ? is another index, HINT, or some extra statistics needed to solve the problem ? am-I obliged to rewrite the queries like the request #2 ?</p>

<p><strong>Edit:</strong> Quantitatively this table holds a dozen of logbooks, some have as few as one event per month, when others have millions of events per month. </p>

<p>This kind of query is the most used against this table (there are other variants with extra filters but they are not relevant for this problem -- except for complexity when using request #2).</p>

<p><strong>Edit #2:</strong> I tried the solution of changing the clustered index to (XDATE,XLOG,...) instead of (XLOG,XDATE,...) -- nb: This composite primary key was designed this way because of the low selectivity of the column XLOG.</p>

<p>I tested this query on a copy of the production database, against a logbook with only a thousand of rows : the query plan generates LOTS OF I/O (it filters out only a few rows from that <code>XLOG=12</code> out of a wide range of <code>XDATE</code>s). So this particular solution is not ok.</p>

<pre class="lang-sql prettyprint-override"><code>SELECT TOP 100 XDATE, XHW, XCELL, XMESSAGE, XLOG FROM LOGS
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250'
AND (XLOG = 12 AND XALIAS LIKE 'KEYWORD%' )
ORDER BY XDATE DESC, XLOG DESC, XHW DESC, XCELL DESC
</code></pre>

<p><img src="https://i.sstatic.net/qxXld.png" alt="Nice query plan with lots of I/O"></p>

<p>PS: By the way, we have the same behaviour with <strong>PostgreSQL 9.1</strong> - so it is not database related, more probably a wrong query or a wrong table design.</p>

## Answers
### Answer ID: 11519871
<p>The issue is that the database does not know that the first 100 rows you want are all XLOG=1 so has to get all the possible XLOGS and then sort to find the first 100.</p>

<p>In your second case you have given more information or cut down the rows selected so the optimizer can just use the index for sorting.</p>

<p>Another way is to make the clustered index on XDATE DESC, XLOG DESC then the optimizer will know it does not have to sort and make the primary key a hash or other index. This ony makes sense if this query is the one most used.</p>

### Answer ID: 11521349
<p>Order by XDate is causing the issue.The data has to be sorted by xdate to get top 100 and that is why you have this sort. Best way would be to have an index on xdate,xlog.But that would add overhead.That should be the option when other things are not working. Try below method.</p>

<pre><code>SELECT TOP 100 XDATE, XHW, XCELL, XMESSAGE, XLOG
into #mytop100
FROM LOGS 
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250' 
AND (XLOG = 1) 
ORDER BY XDATE DESC
union all
SELECT TOP 100 XDATE, XHW, XCELL, XMESSAGE, XLOG FROM LOGS 
WHERE XDATE &gt; '2012-06-12T00:00:00' AND XDATE &lt; '2012-07-13T08:29:03.250' 
AND (XLOG = 1002) 
ORDER BY XDATE DESC

select TOP 100 XDATE, XHW, XCELL, XMESSAGE, XLOG from #mytop 100 ORDER BY XDATE DESC, XLOG DESC 
</code></pre>

<p>also try the main sql withwout into #mytop100 and see whether it picks up a good plan. I bet it would but still check that.</p>

