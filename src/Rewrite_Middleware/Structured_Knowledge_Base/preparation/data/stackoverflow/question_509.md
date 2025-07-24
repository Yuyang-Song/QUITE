# different estimated rows on same index operation?
[Link to question](https://stackoverflow.com/questions/29117042/different-estimated-rows-on-same-index-operation)
**Creation Date:** 1426666760
**Score:** 2
**Tags:** sql-server, sql-server-2008-r2, histogram, optimization, sql-server-performance
## Question Body
<p><strong>Introduction and Background</strong></p>

<p>I had to optimize a simple query (example below). After rewriting it several times I recognized that the estimated row count on the one and same index operation differs depending on the way the query is written.</p>

<p>Originally the query did a clustered index scan, as the table in production contains a binary column the table is quite large (about 100 GB) and the full table scan takes too much time to execute.</p>

<p><strong>Question</strong></p>

<p>Why is the estimated row count different on the same index operation (example will show)? What is the optimizer doing here?</p>

<p><strong>the example database - I am using SQL Server 2008 R2</strong></p>

<p>I tried to create a very simplyfied version of my production tables that shows the behaviour.</p>

<pre><code>-- CREATE THE SAMPLE TABLES
----------------------------
CREATE TABLE dbo.MasterTable(
    MasterId    smallint NOT NULL,
    Name        varchar(5) NOT NULL,
    CONSTRAINT PK_MasterTable PRIMARY KEY CLUSTERED (MasterId ASC)
) ON  [PRIMARY]

GO

CREATE TABLE dbo.DetailTable(
    DetailId    bigint IDENTITY(1,1) NOT NULL,
    MasterId    smallint NOT NULL,
    Name        nvarchar(50) NOT NULL,
    CreateDate  datetime NOT NULL,
    CONSTRAINT PK_DetailTable PRIMARY KEY CLUSTERED (DetailId ASC)
) ON  [PRIMARY]

GO

ALTER TABLE dbo.DetailTable
    ADD  CONSTRAINT FK1
    FOREIGN KEY(MasterId) REFERENCES dbo.MasterTable (MasterId)

GO

CREATE NONCLUSTERED INDEX IX_DetailTable
    ON dbo.DetailTable( MasterId ASC, Name ASC )

GO

-- INSERT SOME SAMPLE DATA
----------------------------
SET NOCOUNT ON
GO

-- These are some Codes. In our system we always use these codes to search for "types" of data.

INSERT INTO dbo.MasterTable (MasterId, Name)
VALUES (1, 'N1'), (2, 'N2'), (3, 'N3'), (4, 'N4'), (5, 'N5'), (6, 'N6'), (7, 'N7'), (8, 'N8')

GO

-- ADD ROWS TO THE DETAIL TABLE
-- Takes about 1 minute to run
-- Don't care about the logic, it's just to get a distribution similar to production system
----------------------------
declare @x int = 1
DECLARE @MasterID INT
while (@x &lt;= 400000)
begin
    SET @MasterID = ABS(CHECKSUM(NEWID())) % 8 + 1

    INSERT INTO dbo.DetailTable(MasterId,Name,CreateDate)
    VALUES(
        CASE
            WHEN @MasterID IN (1, 3, 4) AND @x % 20 != 0 THEN 2
            WHEN @MasterID IN (5, 6) AND @x % 20 != 0 THEN 7
            WHEN @MasterID = 8 AND @x % 100 != 0 THEN 7
            ELSE @MasterID
        END,
        NEWID(),
        DATEADD(DAY, - ABS(CHECKSUM(NEWID())) % 1000, GETDATE())
)

SET @x = @x + 1
end

go
-- DO THE INDEX AND STATISTIC MAINTENANCE
----------------------------
alter index all on dbo.DetailTable reorganize
alter index all on dbo.MasterTable reorganize
update statistics dbo.DetailTable WITH FULLSCAN
update statistics dbo.MasterTable WITH FULLSCAN
go
</code></pre>

<p><strong>Preparation is done, let's start with the query</strong></p>

<p>Let's have a look at the statistics first, look at <code>RANGE_HI_KEY=8</code>, there are 489 EQ_ROWS</p>

<pre><code>-- CHECK THE STATISTICS
----------------------------
dbcc show_statistics ('dbo.DetailTable', IX_DetailTable)
GO
</code></pre>

<p>Now we do the query. The first one is the original query I had to optimize.
Please activate the current execution plan when executing.
 Have a look at the operation "index seek (nonclustered) [DetailTable].[IX_DetailTable]"</p>

<pre><code>-- ORIGINAL QUERY
----------------------------
SELECT d.DetailId
FROM dbo.DetailTable d
INNER JOIN dbo.MasterTable m ON d.MasterId = m.MasterId
WHERE m.Name = 'N8'
AND d.CreateDate &gt; '20150312 11:00:00'

GO

-- FORCESEEK
----------------------------
SELECT d.DetailId
FROM dbo.DetailTable d WITH (FORCESEEK)
INNER JOIN dbo.MasterTable m ON d.MasterId = m.MasterId
WHERE m.Name = 'N8'
AND d.CreateDate &gt; '20150312 11:00:00'

GO

-- Actual: 489, Estimated 50.000


-- TABLE VARIABLE
----------------------------
DECLARE @MasterId AS TABLE( MasterId SMALLINT )
INSERT INTO @MasterId (MasterId)
SELECT MasterID FROM dbo.MasterTable WHERE Name = 'N8'
SELECT d.DetailId
FROM dbo.DetailTable d WITH (FORCESEEK)
INNER JOIN @MasterId m ON d.MasterId = m.MasterId
WHERE d.CreateDate &gt; '20150312 11:00:00'

GO

-- Actual: 489, Estimated 40.000

-- TEMP TABLE
----------------------------
CREATE TABLE #MasterId( MasterId SMALLINT )
INSERT INTO #MasterId (MasterId)
    SELECT MasterID FROM dbo.MasterTable WHERE Name = 'N8'

SELECT d.DetailId
FROM dbo.DetailTable d --WITH (FORCESEEK)
INNER JOIN #MasterId m ON d.MasterId = m.MasterId
WHERE d.CreateDate &gt; '20150312 11:00:00'

-- Actual 489, Estimated 489

DROP TABLE #MasterId

GO
</code></pre>

<p><strong>Analyse and final question(s)</strong></p>

<p>Please have a look at the operation "index seek (nonclustered) [DetailTable].[IX_DetailTable]"</p>

<p>The comments in the script above show you the values I got for estimated and actual row count.</p>

<p>In our production environment this table has 33 million rows, the estimated rows in the queries above differ from 3 million to 16 million.</p>

<p><strong>To summarize:</strong></p>

<ol>
<li><p>when a join between the DetailTable and the MasterTable is made, the estimated rowcount is 12,5% (there are 8 values in the master table, it makes sense, kind of...)</p></li>
<li><p>when a join between the DetailTable and the table variable is made, the estimated rowcount is 10%</p></li>
<li><p>when a join between the DetailTable and the temp table is made, the estimated rowcount is exactly the same as the actual row count</p></li>
</ol>

<p>The question is why do these values differ?</p>

<p>The statistics are up to date and making an estimation should really be easy.</p>

<p>I just would like to understand this.</p>

## Answers
### Answer ID: 29207053
<p><strong>As nobody answer i ll try to give answer :</strong></p>

<p>Please don`t force optimizer to follow you</p>

<p><strong>(1) Explanation about you original query :</strong></p>

<pre><code>SELECT d.DetailId
FROM dbo.DetailTable d
INNER JOIN dbo.MasterTable m ON d.MasterId = m.MasterId
WHERE m.Name = 'N8'
AND d.CreateDate &gt; '20150312 11:00:00'
</code></pre>

<p>Why this query is slow ?</p>

<p><em>this query is slow because your indexes are not covering this query,
both query are using index scan and than joining with "Hash join":</em></p>

<p><img src="https://i.sstatic.net/1txvg.png" alt="enter image description here"></p>

<p><em>WHY scanning entire row for mastertable ?</em>
Because index on Master table is on column MasterId , not on column Name. </p>

<p>WHY scanning entire row for Detailtable? Because here as well index is  on 
(DETAILID) "CLUSTERED" AND ( MasterId ASC, Name ASC ) "NON CLUSTERED"<br>
 not on Createdate column.</p>

<p>having one NONCLUSTERED index will help this query ON column (CREATEDATE,MasterId ) for this particular Query.</p>

<p>If your Master table is huge as well you can create NONCLUSTERED index on (Name) column.</p>

<p><strong>(2) Explanation on FORCESEEK :</strong></p>

<h2>-- FORCESEEK</h2>

<pre><code>SELECT d.DetailId
FROM dbo.DetailTable d WITH (FORCESEEK)
INNER JOIN dbo.MasterTable m ON d.MasterId = m.MasterId
WHERE m.Name = 'N8'
AND d.CreateDate &gt; '20150312 11:00:00'
GO
</code></pre>

<p><img src="https://i.sstatic.net/98QOc.png" alt="enter image description here"></p>

<p>Why optimizer estimated 50,000 row ?</p>

<p>Here you are joining on column d.MasterId = m.MasterId and you are FORCING optimizer to choose seek on Detail table, so
optizer using  INDEX IX_DetailTable () to join your Mastertable using LOOP join . </p>

<p>Since Optimizer chooosing Loop join to join all rows (Actually ONE) of MAster table to Detail table 
so it will choose one key from master table then seek for entire  index and then pass the matching value to further iterator.</p>

<p>so optimizer chooses Average of rows per value .
8 unique values in column 40000 table cardinality (rows) so
40000 / 8 Is   50,000 rows estimated (fair enough).</p>

<h2>(3) -- TABLE VARIABLE</h2>

<p>Here is your query :</p>

<pre><code>DECLARE @MasterId AS TABLE( MasterId SMALLINT )
INSERT INTO @MasterId (MasterId)
SELECT MasterID FROM dbo.MasterTable WHERE Name = 'N8'
SELECT d.DetailId
FROM dbo.DetailTable d WITH (FORCESEEK)
INNER JOIN @MasterId m ON d.MasterId = m.MasterId
WHERE d.CreateDate &gt; '20150312 11:00:00'

GO
</code></pre>

<p><img src="https://i.sstatic.net/l0Mb8.png" alt="enter image description here"></p>

<p>Statatictic does not maintain on table variable so optimzer has no idia how many rows( so it estimate 1 row )it gonaa deal with to produce a good plan, 
here as well estimated rows are 1 and actual row 1  aswell congrates!!</p>

<p>but how optimizer  Estimated "40.000" ROWS</p>

<p>Personally i never checked this and because of this question i did servels testing, but have no idia how optimzer calculating estimated  rows, so it will be great if someone come up and enlight us.</p>

<p><strong>(4) -- TEMP TABLE</strong></p>

<p>Your Query </p>

<pre><code>CREATE TABLE #MasterId( MasterId SMALLINT )
INSERT INTO #MasterId (MasterId)
    SELECT MasterID FROM dbo.MasterTable WHERE Name = 'N8'

SELECT d.DetailId
FROM dbo.DetailTable d --WITH (FORCESEEK)
INNER JOIN #MasterId m ON d.MasterId = m.MasterId
WHERE d.CreateDate &gt; '20150312 11:00:00'

-- Actual 489, Estimated 489
DROP TABLE #MasterId
</code></pre>

<p><img src="https://i.sstatic.net/YxUZZ.png" alt="enter image description here"></p>

<p>here as well optimizer is choosing same query plan as was choosing in table variable but diffrence is
Statistics does maintain on temp tables, So Here in query optimizer has a fair idia what row it actually going to join. 
 "N8" key has 8, and 8`s estimated rows in dbo.DetailTable  is 489.</p>

