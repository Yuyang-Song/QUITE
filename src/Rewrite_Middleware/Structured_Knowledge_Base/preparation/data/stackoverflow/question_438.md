# SQL Server 2014 execution plan creation takes a long time (fast in older versions)
[Link to question](https://stackoverflow.com/questions/26177480/sql-server-2014-execution-plan-creation-takes-a-long-time-fast-in-older-version)
**Creation Date:** 1412332836
**Score:** 5
**Tags:** sql-server, t-sql, sql-server-2014
## Question Body
<p>I've encountered a problem with a query in SQL Server 2014. The first time this query is run, it takes ages for the execution plan to be generated.</p>

<p>The strange thing is that it has worked just fine in all previous versions of SQL Server (2012, 2008 R2, 2008, etc.).
It seems to be related to a unique index on one of the involved tables, combined with a certain amount of subqueries in the main query.</p>

<p>Here are the involved tables in the query. I've simplified the tables a lot compared to the originals, but the problem persists. Note the unique constraint on table2, this seems to be what is causing the issue. It does not matter if it is a unique constraint, unique index, or even primary key on Table2, the result is the same.</p>

<pre><code>IF OBJECT_ID('Table2') IS NOT NULL DROP TABLE [Table2]
IF OBJECT_ID('Table1') IS NOT NULL DROP TABLE [Table1]
CREATE TABLE [dbo].[Table1] ( [ReferencedColumn] [int] NOT NULL PRIMARY KEY)
CREATE TABLE [dbo].[Table2] ( [ReferencedColumn] [int] NOT NULL FOREIGN KEY REFERENCES [Table1] ([ReferencedColumn]), [IntColumn] [int] NOT NULL, [AnotherIntColumn] [int] NULL )
CREATE UNIQUE NONCLUSTERED INDEX [IX_Table2] ON [dbo].[Table2] ([ReferencedColumn], [IntColumn])
</code></pre>

<p>If I then do some subqueries from the table with the index in a select statement, it takes ages to complete the first time (more than 30 seconds in my tests).</p>

<pre><code>SELECT  (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 1 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 2 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 3 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 4 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 5 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 6 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 7 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 8 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 9 ),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 10),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 11),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 12),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 13),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 14),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 15),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 16),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 17),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 18),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 19),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 20),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 21),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 22),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 23),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 24),
        (SELECT F2.IntColumn FROM Table2 F2 WHERE F2.[ReferencedColumn] = F.[ReferencedColumn] AND F2.IntColumn = 25)
FROM    Table1 F
</code></pre>

<p>Since the tables have no rows in them, and since the query runs instantly after the first run, it seems to me that it must be the execution plan that takes a long time to generate.</p>

<p>However, if you do one of the changes listed below, the execution plan is generated instantly instead.</p>

<ul>
<li>Remove the index</li>
<li>Remove the UNIQUE part of the index</li>
<li>Add AnotherIntColumn to the index</li>
<li>Set the compatibility level on the database to SQL Server 2012</li>
</ul>

<p>It is worth noting that the execution plan that is generated is the same across the versions, only the time to generate it changes. The plan includes many "Compute Scalar" operations, but I don't see how can be a problem, when the same plan is generated instantly in 2012/2008.</p>

<p>I've only tested it on a couple of instances of SQL Server 2014 Enterprise and Web editions, but I assume the same behavior will occur on other editions of 2014.</p>

<p>I already have several ways of solving the problem (modify the index, change compatibility level, rewrite the query), but I am curious why there is such a big drop in performance compared to the older versions of SQL Server?</p>

## Answers
### Answer ID: 26180823
<p>SQL Server 2014 had a <a href="http://blogs.msdn.com/b/saponsqlserver/archive/2014/01/16/new-functionality-in-sql-server-2014-part-2-new-cardinality-estimation.aspx" rel="nofollow">brand new Query Optimizer</a>. Cardinality Estimation (guessing how many rows a statement will return) is much more aggressive in than in past versions. There are bugs and edge cases where the new optimizer will take longer to find the optimal query plan. Setting a lower compatibility level falls back to the previous Query Optimizer.</p>

<p>Your query is pretty much a torture test. There are better ways to write it. But I think you exposed a bug in the new Query Optimizer. File a bug report on <a href="https://connect.microsoft.com/SQLServer" rel="nofollow">SQL Connect</a>.</p>

