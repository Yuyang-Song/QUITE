# Optimal performing query for latest record for each N
[Link to question](https://stackoverflow.com/questions/7515354/optimal-performing-query-for-latest-record-for-each-n)
**Creation Date:** 1316697425
**Score:** 17
**Tags:** sql-server, performance, t-sql, greatest-n-per-group, database-performance
## Question Body
<p>Here is the scenario I find myself in.</p>

<p>I have a reasonably big table that I need to query the latest records from. Here is the create for the essential columns for the query:</p>

<pre><code>CREATE TABLE [dbo].[ChannelValue](
   [ID] [bigint] IDENTITY(1,1) NOT NULL,
   [UpdateRecord] [bit] NOT NULL,
   [VehicleID] [int] NOT NULL,
   [UnitID] [int] NOT NULL,
   [RecordInsert] [datetime] NOT NULL,
   [TimeStamp] [datetime] NOT NULL
   ) ON [PRIMARY]
GO
</code></pre>

<p>The ID column is a Primary Key and there is a non-Clustered index on VehicleID and TimeStamp</p>

<pre><code>CREATE NONCLUSTERED INDEX [IX_ChannelValue_TimeStamp_VehicleID] ON [dbo].[ChannelValue] 
(
    [TimeStamp] ASC,
    [VehicleID] ASC
)ON [PRIMARY]
GO
</code></pre>

<p>The table I'm working on to optimise my query is a little over 23 million rows and is only a 10th of the sizes the query needs to operate against.</p>

<p>I need to return the latest row for each VehicleID.</p>

<p>I've been looking through the responses to this question here on StackOverflow and I've done a fair bit of Googling and there seem to be 3 or 4 common ways of doing this on SQL Server 2005 and upwards.</p>

<p>So far the fastest method I've found is the following query:</p>

<pre><code>SELECT cv.*
FROM ChannelValue cv
WHERE cv.TimeStamp = (
SELECT
    MAX(TimeStamp)
FROM ChannelValue
WHERE ChannelValue.VehicleID = cv.VehicleID
)
</code></pre>

<p>With the current amount of data in the table it takes about 6s to execute which is within reasonable limits but with the amount of data the table will contain in the live environment the query begins to perform too slow.</p>

<p>Looking at the execution plan my concern is around what SQL Server is doing to return the rows.</p>

<p>I cannot post the execution plan image because my Reputation isn't high enough but the index scan is parsing every single row within the table which is slowing the query down so much.</p>

<p><img src="https://i36.photobucket.com/albums/e10/Sho-Gi/execplan.jpg" alt="Execution Plan"></p>

<p>I've tried rewriting the query with several different methods including using the SQL 2005 Partition method like this:</p>

<pre><code>WITH cte
AS (
    SELECT *,
    ROW_NUMBER() OVER(PARTITION BY VehicleID ORDER BY TimeStamp DESC) AS seq
     FROM ChannelValue
)

SELECT
   VehicleID,
   TimeStamp,
   Col1
FROM cte
WHERE seq = 1
</code></pre>

<p>But the performance of that query is even worse by quite a large magnitude.</p>

<p>I've tried re-structuring the query like this but the result speed and query execution plan is nearly identical:</p>

<pre><code>SELECT cv.*
FROM (
   SELECT VehicleID
    ,MAX(TimeStamp) AS [TimeStamp]
   FROM ChannelValue
   GROUP BY VehicleID
) AS [q]
INNER JOIN ChannelValue cv
   ON cv.VehicleID = q.VehicleID
   AND cv.TimeStamp = q.TimeStamp
</code></pre>

<p>I have some flexibility available to me around the table structure (although to a limited degree) so I can add indexes, indexed views and so forth or even additional tables to the database.</p>

<p>I would greatly appreciate any help at all here.</p>

<p><em>Edit</em> Added the link to the execution plan image.</p>

## Answers
### Answer ID: 7515391
<p>Depends on your data (how many rows are there per group?) and your indexes. </p>

<p>See <a href="http://www.sqlmag.com/article/departments/optimizing-top-n-per-group-queries">Optimizing TOP N Per Group Queries</a> for some performance comparisons of 3 approaches.</p>

<p>In your case with millions of rows for only a small number of Vehicles I would add an index on <code>VehicleID, Timestamp</code> and do </p>

<pre><code>SELECT CA.*
FROM   Vehicles V
       CROSS APPLY (SELECT TOP 1 *
                    FROM   ChannelValue CV
                    WHERE  CV.VehicleID = V.VehicleID
                    ORDER  BY TimeStamp DESC) CA  
</code></pre>

### Answer ID: 7515576
<p>Try this:</p>

<pre><code>SELECT SequencedChannelValue.* -- Specify only the columns you need, exclude the SequencedChannelValue
FROM
    (
        SELECT 
            ChannelValue.*,   -- Specify only the columns you need
            SeqValue = ROW_NUMBER() OVER(PARTITION BY VehicleID ORDER BY TimeStamp DESC)
        FROM ChannelValue
    ) AS SequencedChannelValue
WHERE SequencedChannelValue.SeqValue = 1
</code></pre>

<p>A table or index scan is expected, because you're not filtering data in any way.  You're asking for the latest TimeStamp for all VehicleIDs - the query engine HAS to look at every row to find the latest TimeStamp.</p>

<p>You can help it out by narrowing the number of columns being returned (don't use SELECT *), and by providing an index that consists of VehicleID + TimeStamp.</p>

### Answer ID: 7515507
<p>If your records are inserted sequentially, replacing <code>TimeStamp</code> in your query with <code>ID</code> may make a difference.</p>

<p>As a side note, how many records is this returning?  Your delay could be network overhead if you are getting hundreds of thousands of rows back.</p>

