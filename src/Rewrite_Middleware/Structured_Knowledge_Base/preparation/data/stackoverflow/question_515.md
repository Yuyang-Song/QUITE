# Optimizing ROW_NUMBER() in SQL Server
[Link to question](https://stackoverflow.com/questions/2960104/optimizing-row-number-in-sql-server)
**Creation Date:** 1275500562
**Score:** 7
**Tags:** sql-server, sql-server-2005, t-sql, optimization, query-optimization
## Question Body
<p>We have a number of machines which record data into a database at sporadic intervals.  For each record, I'd like to obtain the time period between <em>this</em> recording and the <em>previous</em> recording.</p>

<p>I can do this using ROW_NUMBER as follows:</p>

<pre><code>WITH TempTable AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Machine_ID ORDER BY Date_Time) AS Ordering
    FROM dbo.DataTable
)

SELECT [Current].*, Previous.Date_Time AS PreviousDateTime
FROM TempTable AS [Current]
INNER JOIN TempTable AS Previous 
    ON [Current].Machine_ID = Previous.Machine_ID
    AND Previous.Ordering = [Current].Ordering + 1
</code></pre>

<p>The problem is, it goes <em>really</em> slow (several minutes on a table with about 10k entries) - I tried creating separate indicies on Machine_ID and Date_Time, and a single joined-index, but nothing helps.</p>

<p>Is there anyway to rewrite this query to go faster?</p>

## Answers
### Answer ID: 2961466
<p>How does it compare to this version?:</p>

<pre><code>SELECT x.*
    ,(SELECT MAX(Date_Time)
      FROM dbo.DataTable
      WHERE Machine_ID = x.Machine_ID
          AND Date_Time &lt; x.Date_Time
    ) AS PreviousDateTime
FROM dbo.DataTable AS x
</code></pre>

<p>Or this version?:</p>

<pre><code>SELECT x.*
    ,triang_join.PreviousDateTime
FROM dbo.DataTable AS x
INNER JOIN (
    SELECT l.Machine_ID, l.Date_Time, MAX(r.Date_Time) AS PreviousDateTime
    FROM dbo.DataTable AS l
    LEFT JOIN dbo.DataTable AS r
    ON l.Machine_ID = r.Machine_ID
        AND l.Date_Time &gt; r.Date_Time
    GROUP BY l.Machine_ID, l.Date_Time
) AS triang_join
ON triang_join.Machine_ID = x.Machine_ID
    AND triang_join.Date_Time = x.Date_Time
</code></pre>

<p>Both would perform best with an index on Machine_ID, Date_Time and for correct results, I'm assuming that this is unique.</p>

<p>You haven't mentioned what is hidden away in * and that can sometimes means a lot since a Machine_ID, Date_Time index will not generally be covering and if you have a lot of columns there or they have a lot of data, ...</p>

### Answer ID: 2960159
<p>The given ROW_NUMBER() partition and order require an index on <code>(Machine_ID, Date_Time)</code> to satisfy in one pass:</p>

<pre><code>CREATE INDEX idxMachineIDDateTime ON DataTable (Machine_ID, Date_Time);
</code></pre>

<p>Separate indexes on Machine_ID and Date_Time will help little, if any.</p>

### Answer ID: 2960198
<p>I have had some strange performance problems using CTEs in SQL Server 2005.  In many cases, replacing the CTE with a real temp table solved the problem.</p>

<p>I would try this before going any further with using a CTE.</p>

<p>I never found any explanation for the performance problems I've seen, and really didn't have any time to dig into the root causes.  However I always suspected that the engine couldn't optimize the CTE in the same way that it can optimize a temp table (which can be indexed if more optimization is needed).</p>

<p><strong>Update</strong></p>

<p>After your comment that this is a view, I would first test the query with a temp table to see if that performs better.</p>

<p>If it does, and using a stored proc is not an option, you might consider making the current CTE into an indexed/materialized view.  You will want to read up on the subject before going down this road, as whether this is a good idea depends on a lot of factors, not the least of which is how often the data is updated.</p>

### Answer ID: 2960812
<p>If the number of rows in dbo.DataTable is large then it is likely that you are experiencing the issue due to the CTE self joining onto itself.  There is a blog post explaining the issue in some detail <a href="http://sqlblogcasts.com/blogs/tonyrogerson/archive/2008/05/17/non-recursive-common-table-expressions-performance-sucks-1-cte-self-join-cte-sub-query-inline-expansion.aspx" rel="nofollow noreferrer" title="here">here</a></p>

<p>Occasionally in such cases I have resorted to creating a temporary table to insert the result of the CTE query into and then doing the joins against that temporary table (although this has usually been for cases where a large number of joins against the temp table are required - in the case of a single join the performance difference will be less noticable)</p>

### Answer ID: 2960323
<p>If you require this data often, rather than calculate it each time you pull the data, why not add a column and calculate/populate it whenever row is added?</p>

<p>(Remus' compound index will make the query fast; running it only once should make it faster still.)</p>

### Answer ID: 2960165
<p>What if you use a trigger to store the last timestamp an subtract each time to get the difference?</p>

