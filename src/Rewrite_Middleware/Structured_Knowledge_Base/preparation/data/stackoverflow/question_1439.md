# Poor Performance of Table Driven Parameterized View due to poor cardinality estimation
[Link to question](https://stackoverflow.com/questions/76524115/poor-performance-of-table-driven-parameterized-view-due-to-poor-cardinality-esti)
**Creation Date:** 1687355896
**Score:** 0
**Tags:** sql, performance, view, sql-server-2019
## Question Body
<p>We are trying to create a number of views which return data which is filtered by parameters stored in a parameter table.</p>
<p>This is so that a large number of views do not need to be redeployed in the scenario that some filtering criteria changes and means we don't need to update reports / front end code if some filtering criteria changes - it is all data driven by changing the parameters in the parameter table.</p>
<p>Below is a StackOverflow2010 database example representative of what is in place</p>
<p>Create a parameters table and add some values</p>
<pre><code>CREATE TABLE Parameters
(
    ID INT IDENTITY(1,1) PRIMARY KEY,
    GroupName NVARCHAR(30),
    ParameterName NVARCHAR(30),
    ParameterValue NVARCHAR(255),
)

INSERT INTO Parameters VALUES ('Filtering Rules','LocationEqualityFilter','Paris, France')
INSERT INTO Parameters VALUES ('Filtering Rules','TitleLikeFilter','sql')
</code></pre>
<p>Create some covering indexes for the view</p>
<pre><code>CREATE INDEX IX_Location ON Users
(
    [Location]
)
INCLUDE
(
    DisplayName,
    Reputation
)

CREATE INDEX IX_Title ON Posts
(
    Title
)
INCLUDE
(
    Tags,
    OwnerUserId
)
</code></pre>
<p>Create our view - this looks up posts whos titles start with a given string by users in a given location</p>
<pre><code>CREATE OR ALTER VIEW vw_PostsByLocationWithTitle
AS
SELECT  u.DisplayName,
        u.Reputation,
        pos.tags
FROM    Users u
        JOIN Parameters p
            ON u.Location = p.ParameterValue AND
                p.ParameterName = 'LocationEqualityFilter'
        JOIN Posts pos
            ON pos.OwnerUserId = u.Id
        JOIN Parameters p1
            ON pos.Title LIKE p1.ParameterValue + N'%' AND
                p1.ParameterName = N'TitleEqualityFilter' 
</code></pre>
<p>Select from the view:</p>
<pre><code>SET STATISTICS IO ON
SELECT * FROM vw_PostsByLocationWithTitle
</code></pre>
<p>The actual plan is <a href="https://www.brentozar.com/pastetheplan/?id=S1nit_eu3" rel="nofollow noreferrer">here</a> and the logical reads are</p>
<pre><code>Table 'Users'. Scan count 7, logical reads 1873, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Parameters'. Scan count 2, logical reads 4, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Worktable'. Scan count 0, logical reads 0, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Posts'. Scan count 1, logical reads 222, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Workfile'. Scan count 0, logical reads 0, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Worktable'. Scan count 0, logical reads 0, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
</code></pre>
<p>If I run the equivalent query with hardcoded literals, I get a much simpler plan, built on far better estimates:</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation,
        p.Tags
FROM    Users u
        JOIN posts p
            ON p.OwnerUserId = u.Id
WHERE   Location = N'Paris, France' AND
        p.Title LIKE N'SQL%'
</code></pre>
<p><a href="https://www.brentozar.com/pastetheplan/?id=Sy0squgun" rel="nofollow noreferrer">Plan</a></p>
<pre><code>Table 'Workfile'. Scan count 0, logical reads 0, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Worktable'. Scan count 0, logical reads 0, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Posts'. Scan count 1, logical reads 222, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
Table 'Users'. Scan count 1, logical reads 10, physical reads 0, page server reads 0, read-ahead reads 0, page server read-ahead reads 0, lob logical reads 0, lob physical reads 0, lob page server reads 0, lob read-ahead reads 0, lob page server read-ahead reads 0.
</code></pre>
<p>Even the far simpler</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
        JOIN Parameters p
            ON u.Location = p.ParameterValue AND
                p.ParameterName = N'LocationEqualityFilter'
</code></pre>
<p>has <a href="https://www.brentozar.com/pastetheplan/?id=B1pViOgd3" rel="nofollow noreferrer">pretty terrible estimations</a> vs <a href="https://www.brentozar.com/pastetheplan/?id=Bylui_x_3" rel="nofollow noreferrer">its literal counterpart</a> below</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
WHERE   Location = N'Paris, France'
</code></pre>
<p>We are having a number of performance issues when users use views with this pattern and in each case, this can be tracked down to this poor estimation which can be fixed by replacing with literals</p>
<p>I can fix the estimate on this simpler query in two ways:</p>
<p><a href="https://www.brentozar.com/pastetheplan/?id=Bylui_x_3" rel="nofollow noreferrer">Using a variable:</a></p>
<pre><code>DECLARE @Location NVARCHAR(100) = (SELECT ParameterValue FROM Parameters WHERE ParameterName = N'LocationEqualityFilter')

SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
WHERE   Location = @Location
</code></pre>
<p><a href="https://www.brentozar.com/pastetheplan/?id=H1tmhulO2" rel="nofollow noreferrer">Using a temp table</a></p>
<pre><code>SELECT  ParameterValue 
INTO    #Location
FROM    Parameters 
WHERE   ParameterName = N'LocationEqualityFilter'

SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
        JOIN #Location l
            ON u.Location = l.ParameterValue

DROP TABLE #Location
</code></pre>
<p>I believe the reason these fix the estimate is that in the original query, SQL Server can estimate how many rows in <code>Parameters</code> match <code>N'LocationEqualityFilter'</code> but it doesn't know what the value for the <code>ParameterValue</code> column is so cannot use that for the histogram lookup required to estimate the number of rows in <code>Users</code> that match that value. However, declaring a variable means SQL Server can use the value of that variable for the histogram lookup and the temp table variant means SQL Server knows the <code>ParameterValue</code> by means of statistics on the temp table to be able to use it for the Histogram lookup on <code>Users</code></p>
<p>Whilst both of these fixes solve the problem, neither are permitted in views.</p>
<p>I also tried this pattern which also gives <a href="https://www.brentozar.com/pastetheplan/?id=rympdYgOn" rel="nofollow noreferrer">estimation issues</a></p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
WHERE   Location = (SELECT CAST(ParameterValue AS NVARCHAR(100)) FROM Parameters WHERE ParameterName = N'LocationEqualityFilter')
</code></pre>
<p>Finally, I tried to create an indexed view which returns the parameter value for<code>LocationEqualityFilter</code></p>
<pre><code>CREATE OR ALTER VIEW dbo.LocationEqualityFilter
WITH SCHEMABINDING AS
SELECT  ParameterValue
FROM    dbo.Parameters
WHERE   ParameterName = N'LocationEqualityFilter' 
GO

CREATE UNIQUE CLUSTERED INDEX IX_LocationEqualityFilter ON dbo.LocationEqualityFilter
(
    ParameterValue
)
</code></pre>
<p>The Optimizer indeed <a href="https://www.brentozar.com/pastetheplan/?id=SkanYhbun" rel="nofollow noreferrer">scans the index</a> but the estimation on the Users table seek is still off.</p>
<p>I can see that the stats that were created for this view represent that the view returns one row and shows us the value:</p>
<p><a href="https://i.sstatic.net/YBnXr.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/YBnXr.png" alt="enter image description here" /></a></p>
<p>In the same way the temp table solution does however, I can see that the plan does not load this stat:</p>
<p><a href="https://i.sstatic.net/Q6V96.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Q6V96.png" alt="enter image description here" /></a></p>
<p>The same is true if I rewrite my view to reference the new Indexed view explicitly:</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
        JOIN LocationEqualityFilter p
            ON u.Location = p.ParameterValue
</code></pre>
<p>However, If I add the WITH (NOEXPAND) hint. It does then get the correct estimate</p>
<p>Is there a way to fix this estimation in the view or some other method to create this data driven parameterisation?</p>
<p>The only options I can think of are:</p>
<ul>
<li>Break each <code>ParameterName</code> into its own table, to replicate the temp table fix. There would have to be a trigger on the <code>Parameters</code> table to update this new table as records change</li>
<li>Create the views with literal values, alter the view definition each time the relevant value in the <code>Parameters</code> table is updated (by means of a trigger)</li>
<li>Create a scalar UDF which returns the literal value of the <code>ParameterValue</code> and use in the WHERE clause and update this definition by a trigger each time the Parameter table is updated. (Assuming SQL Server 2019 and scalar function inlining)</li>
<li>Indexed views as above</li>
</ul>

## Answers
### Answer ID: 76532005
<p>You are probably best off creating <a href="https://learn.microsoft.com/en-us/sql/relational-databases/views/create-indexed-views?view=sql-server-ver16" rel="nofollow noreferrer"><strong>indexed views</strong></a>. Given that you only have inner join that should be no problem.</p>
<p>Add the primary/unique keys of <code>Users</code> and <code>Posts</code> to the view, and create an index on those columns. The reason to use those columns is so that the compiler can efficiently locate them in the indexed view to update them when the base tables are updated.</p>
<pre><code>CREATE UNIQUE CLUSTERED INDEX ux ON dbo.vw_PostsByLocationWithTitle
  (UserId, PostId);
</code></pre>
<p>This hopefully should allow the server to create statistics on the actual values, at the obvious cost of actually storing and maintaining all that data a second time.</p>
<hr />
<p>Note that you should <a href="https://sqlperformance.com/2015/12/sql-performance/noexpand-hints" rel="nofollow noreferrer">always</a> query such views using the <code>WITH (NOEXPAND)</code> hint, even on Enterprise Edition. To enforce that, you may wish to create <em>another</em> view which queries <em>this</em> view using <code>NOEXPAND</code>, and only allow the user to use <em>that</em> view.</p>
<p>Also note that indexed views have many restrictions. Among the most notable:</p>
<ul>
<li>Particular <code>SET</code> options (such as <code>ANSI_NULLS</code>) must be enabled when querying the view, or <strong>modifying the base tables</strong>. Older clients may not have these options set by default.</li>
<li>Only <code>INNER JOIN</code> is allowed, no <code>LEFT</code> <code>RIGHT</code> <code>FULL</code> or <code>APPLY</code>.</li>
<li>No <code>TOP</code> or <code>OFFSET</code>.</li>
<li>No <code>DISTINCT</code> <code>UNION</code> or other set operators.</li>
<li><code>GROUP BY</code> is allowed, but only if the index covers all the non-aggregated columns, and a <code>COUNT_BIG</code> is included. The only other aggregation function allowed is <code>SUM</code>. <code>HAVING</code> is not allowed.</li>
</ul>

### Answer ID: 76524236
<blockquote>
<p>This is so that a large number of views do not need to be redeployed in the scenario that some filtering criteria changes</p>
</blockquote>
<p>That's just not a very good idea.  Instead consider regenerating the views when the filtering criteria change with proper hard-coded column names and column values. eg</p>
<pre><code>CREATE OR ALTER VIEW vw_PostsByLocationWithTitle
AS
SELECT  u.DisplayName,
        u.Reputation,
        pos.tags
FROM    Users u
        JOIN Posts pos
            ON pos.OwnerUserId = u.Id
WHERE u.Location = 'whatever'
  and pos.Title like '%whatever'
</code></pre>
<p>And you can also embed the scalar subquery in the SELECT in the view</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
WHERE   Location = (SELECT cast(ParameterValue as varchar(20)) FROM Parameters WHERE ParameterName = N'LocationEqualityFilter')
</code></pre>
<p>or</p>
<pre><code>SELECT  u.DisplayName,
        u.Reputation
FROM    Users u
WHERE   Location = dbo.fn_getVarcharParameter(N'LocationEqualityFilter')
</code></pre>
<p>Neither of which can return more than one row.</p>

