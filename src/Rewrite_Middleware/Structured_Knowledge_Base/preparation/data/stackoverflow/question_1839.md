# Why doesn&#39;t this sub-query seem to work?
[Link to question](https://stackoverflow.com/questions/9845503/why-doesnt-this-sub-query-seem-to-work)
**Creation Date:** 1332531528
**Score:** 5
**Tags:** sql-server-2008, t-sql
## Question Body
<p>Before anything, I am not looking for a re-write. This was presented to me, and I can't seem to figure out if this is a bug in general or some kind of syntactic craziness that occurs due to the peculiarity of the script. Okay with that said on with the setup:</p>

<ul>
<li><p>Microsoft SQL Server Standard Edition (64-bit)</p></li>
<li><p>Version 10.50.2500.0</p></li>
</ul>

<p><strong>On a table located in a generic database, defined as:</strong></p>

<pre><code>CREATE TABLE [dbo].[Regions](
    [RegionID] [int] NOT NULL,
    [RegionGroupID] [int] NOT NULL,
    [IsDefault] [bit] NOT NULL,
 CONSTRAINT [PK_Regions] PRIMARY KEY CLUSTERED
(
    [RegionID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
</code></pre>

<p><strong>insert some values:</strong></p>

<pre><code>INSERT INTO [dbo].[Regions]
([RegionID],[RegionGroupID],[IsDefault])
VALUES
(0,1,0),
(1,1,0),
(2,1,0),
(3,2,0),
(4,2,0),
(5,2,0),
(6,3,0),
(7,3,0),
(8,3,0)
</code></pre>

<p><strong>Now run the query</strong> (to select a single from each group, remember no rewrite suggestions!):</p>

<pre><code>SELECT RXXID FROM (
   SELECT
       RXX.RegionID as RXXID,
       ROW_NUMBER() OVER (PARTITION BY RXX.RegionGroupID ORDER BY RXX.RegionGroupID) AS RXXNUM
   FROM Regions as RXX
) AS tmp
WHERE tmp.RXXNUM = 1
</code></pre>

<p><strong>You should get:</strong></p>

<pre><code>RXXID
-----------
0
3
6
</code></pre>

<p><strong>Now stick that inside an update statement</strong> (with a preset to 0 and a select all after):</p>

<pre><code>UPDATE Regions SET IsDefault = 0

UPDATE Regions
SET IsDefault = 1
WHERE RegionID IN (
    SELECT RXXID FROM (
       SELECT
           RXX.RegionID as RXXID,
           ROW_NUMBER() OVER (PARTITION BY RXX.RegionGroupID ORDER BY RXX.RegionGroupID) AS RXXNUM
       FROM Regions as RXX
    ) AS tmp
    WHERE tmp.RXXNUM = 1
)


SELECT * FROM Regions
ORDER BY RegionGroupID
</code></pre>

<p><strong>and get this result:</strong></p>

<pre><code>RegionID    RegionGroupID IsDefault
----------- ------------- ---------
0           1             1
1           1             1
2           1             1
3           2             1
4           2             1
5           2             1
6           3             1
7           3             1
8           3             1
</code></pre>

<p><strong>zomg wtf lamaz?</strong></p>

<p>While I don't claim to be a SQL guru, this seems neither proper nor correct.  And to make things more crazy, if you drop the primary key it seems to work:</p>

<p><strong>Drop primary key:</strong></p>

<pre><code>IF  EXISTS (SELECT * FROM sys.indexes WHERE object_id = OBJECT_ID(N'[dbo].[Regions]') AND name = N'PK_Regions')
ALTER TABLE [dbo].[Regions] DROP CONSTRAINT [PK_Regions]
</code></pre>

<p><strong>And re-run update statement set, result:</strong></p>

<pre><code>RegionID    RegionGroupID IsDefault
----------- ------------- ---------
0           1             1
1           1             0
2           1             0
3           2             1
4           2             0
5           2             0
6           3             1
7           3             0
8           3             0
</code></pre>

<p><strong>Isn't that a b?</strong></p>

<p>Does anyone have any clue what is going on here? My guess is some kind of sub-query caching and is this a bug? It sure doesn't seem like what SQL <em>should</em> be doing?</p>

## Answers
### Answer ID: 9845643
<p>Just update as a CTE directly:</p>

<pre><code>WITH tmp AS (
SELECT 
       RegionID as RXXID,
       RegionGroupID,
       IsDefault,
       ROW_NUMBER() OVER (PARTITION BY RegionGroupID ORDER BY RegionID) AS RXXNUM
   FROM Regions

) 
UPDATE tmp SET IsDefault = 1 WHERE RXXNUM = 1
select * from Regions
</code></pre>

<p>Added more columns to illustrate. You can see this on <a href="http://sqlfiddle.com/#!3/03913/9" rel="nofollow noreferrer">http://sqlfiddle.com/#!3/03913/9</a></p>

<p>Not 100% sure what is going on in your example, but since you partition and order by the same column, you're not really certain to get the same order back, since they are all tied. Shouldn't you order by RegionID or some other column, as i did on sqlfiddle?</p>

<hr>

<p>Back to your question:</p>

<p>If you change your UPDATE (with the clustered index) to a SELECT, you'll get all 9 rows back.
If you drop the PK, and do the SELECT, you only get 3 rows. Back to your update statement. Inspecting the execution plans show that they differ slightly:</p>

<p><img src="https://i.sstatic.net/yVMiJ.png" alt="First (PK) Execution plan">
<img src="https://i.sstatic.net/TnS1b.png" alt="Second (No PK) Execution plan"></p>

<p>What you can see here is that in the first (with PK) query, you'll scan the clustered index for the outer reference, note that it does not have the alias RXX. Then for each row in the top, do a lookup to the RXX. And yes, because of your row number ordering, every RegionID can be row_number() 1 for each RegionGroupID. SQL Server would know this based on your PK, i guess, and can say that For every RegionID, this RegionID can be row number 1. Therefore the statement is rather valid.</p>

<p>In the second query, there is no index, and you get a table scan on Regions, then it builds a probe table using the RXX, and joins differently (single pass, ROW_NUMBER() can only be 1 for one row per regiongroupid now). This way in that scan, every RegionID has only one ROW_NUMBER(), though you cannot be 100% certain it'll be the same every time.</p>

<p>This means:
Using your subquery which doesn't have a deterministic order for every execution, you should avoid using a multiple pass (NESTED LOOP) join type, but a single pass (MERGE OR HASH) join.</p>

<p>To fix this without changing the structure of your query, add OPTION (HASH JOIN) or OPTION (MERGE JOIN) to the first UPDATE:</p>

<p>So, you'll need the following update statement (when you have the PK):</p>

<pre><code>UPDATE Regions SET IsDefault = 0

UPDATE Regions 
SET IsDefault = 1 
WHERE RegionID IN (
    SELECT RXXID FROM (
       SELECT 
           RXX.RegionID as RXXID,
           ROW_NUMBER() OVER (PARTITION BY RXX.RegionGroupID ORDER BY RXX.RegionGroupID) AS RXXNUM
       FROM Regions as RXX
    ) AS tmp
    WHERE tmp.RXXNUM = 1 
)
OPTION (HASH JOIN)

SELECT * FROM Regions
ORDER BY RegionGroupID
</code></pre>

<p>Here are the execution plans using these two join types (note actual number of rows: 3 in the properties):</p>

<p><img src="https://i.sstatic.net/xoE4q.png" alt="Using MERGE JOIN">
<img src="https://i.sstatic.net/BWt23.png" alt="Using HASH JOIN"></p>

### Answer ID: 9845878
<p>Your query in plain language is something like:<br>
For each row in <code>Regions</code> check if <code>RegionID</code> exists in some sub query. Meaning that the sub query is executed for each row in <code>Regions</code>. (I know that is not the case but it is the semantics of the query).</p>

<p>Since you are using <code>RegionGroupID</code> as order and partition you really have no idea what <code>RegionID</code> will be returned so it might very well be a new ID for each time the sub-query is checked against.</p>

<p><strong>Update:</strong></p>

<p>Doing the update with a <strong>join</strong> against the derived table instead instead of using <strong>in</strong> changes the semantics of the query and it changed the result as well.</p>

<p>This works as expected:</p>

<pre><code>UPDATE R 
SET IsDefault = 1
FROM Regions as R
  inner join 
      (
        SELECT RXXID FROM (
           SELECT 
               RXX.RegionID as RXXID,
               ROW_NUMBER() OVER (PARTITION BY RXX.RegionGroupID ORDER BY RXX.RegionGroupID) AS RXXNUM
           FROM Regions as RXX
        ) AS tmp
        WHERE tmp.RXXNUM = 1 
      ) as C
    on R.RegionID = C.RXXID
</code></pre>

