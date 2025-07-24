# Slow subquery IN clause?
[Link to question](https://stackoverflow.com/questions/8718513/slow-subquery-in-clause)
**Creation Date:** 1325624291
**Score:** 3
**Tags:** sql, sql-server, llblgenpro
## Question Body
<p>I'm having a number of slow prefetch queries in LLBL. Here's a simplified version of the generated SQL:</p>

<pre><code>SELECT DISTINCT 
    Column1
FROM 
    Table1
WHERE 
Table1.Table2ID IN 
(
    SELECT Table2.Table2ID AS Table2ID 
    FROM 
        Table2  
        INNER JOIN Table1 ON  Table2.Table2ID=Table1.Table2ID
        INNER JOIN 
        (
            SELECT DISTINCT 
                Table1.Table2ID AS Table2ID, 
                MAX(Table1.EffectiveDate) AS EffectiveDate 
            FROM Table1  
            WHERE Table1.EffectiveDate &lt;= '2012-01-03 00:00:00:000'
            GROUP BY Table1.Table2ID
        ) MaxEffective  
        ON  
            MaxEffective.Table2ID = Table1.Table2ID 
            AND MaxEffective.EffectiveDate = Table1.EffectiveDate
)
</code></pre>

<p>What I'm finding is that the subquery executes fast and if I replace that subquery with the actual results, the outer query is fast. But together, they are slow.</p>

<p>I have ran the Database Engine Tuning Adviser which helped a bit, but it's still quite slow. </p>

<p>I'm not very skilled in understanding the execution plans, but it appears the vast majority of time is spent doing an index seek on Table1. </p>

<p>I expected this to run faster since it's a non-correlated subquery. Is there something I'm just not seeing? </p>

<p>If it were just straight SQL, I'd rewrite the query and do a join, but I'm pretty much stuck with LLBL. Are there any settings I can use to force it to do a join? Is there a reason SQL Server isn't generating the same execution plan as it does for a join?</p>

<p>Edit for actual query...</p>

<pre><code>SELECT DISTINCT 
    ResidentialComponentValues.ResidentialComponentValueID AS ResidentialComponentValueId, 
    ResidentialComponentValues.ResidentialComponentTypeID AS ResidentialComponentTypeId, 
    ResidentialComponentValues.Value, 
    ResidentialComponentValues.Story, 
    ResidentialComponentValues.LastUpdated, 
    ResidentialComponentValues.LastUpdatedBy, 
    ResidentialComponentValues.ConcurrencyTimestamp, 
    ResidentialComponentValues.EffectiveDate, 
    ResidentialComponentValues.DefaultQuantity 
FROM 
ResidentialComponentValues  
WHERE 
ResidentialComponentValues.ResidentialComponentTypeID IN 
(
    SELECT ResidentialComponentTypes.ResidentialComponentTypeID AS ResidentialComponentTypeId 
    FROM 
        ResidentialComponentTypes  INNER JOIN ResidentialComponentValues  
        ON  ResidentialComponentTypes.ResidentialComponentTypeID=ResidentialComponentValues.ResidentialComponentTypeID
        INNER JOIN 
        (
            SELECT DISTINCT 
                ResidentialComponentValues.ResidentialComponentTypeID AS ResidentialComponentTypeId, 
                MAX(ResidentialComponentValues.EffectiveDate) AS EffectiveDate 
            FROM ResidentialComponentValues  
            WHERE ResidentialComponentValues.EffectiveDate &lt;= '2012-01-03 00:00:00:000'
            GROUP BY ResidentialComponentValues.ResidentialComponentTypeID
        ) LPA_E1  
        ON  
            LPA_E1.ResidentialComponentTypeId = ResidentialComponentValues.ResidentialComponentTypeID 
            AND LPA_E1.EffectiveDate = ResidentialComponentValues.EffectiveDate
)
</code></pre>

<p>Edit for create statements:</p>

<pre><code>/****** Object:  Table [dbo].[ResidentialComponentTypes]    Script Date: 01/03/2012 13:49:06 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[ResidentialComponentTypes](
    [ResidentialComponentTypeID] [int] IDENTITY(1,1) NOT NULL,
    [ComponentTypeName] [varchar](255) NOT NULL,
    [LastUpdated] [datetime] NOT NULL,
    [LastUpdatedBy] [varchar](50) NOT NULL,
    [ConcurrencyTimestamp] [timestamp] NOT NULL,
    [Active] [bit] NOT NULL,
 CONSTRAINT [PK_ResidentialComponentTypes] PRIMARY KEY CLUSTERED 
(
    [ResidentialComponentTypeID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[ResidentialComponentValues]    Script Date: 01/03/2012 13:49:06 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[ResidentialComponentValues](
    [ResidentialComponentValueID] [int] IDENTITY(1,1) NOT NULL,
    [ResidentialComponentTypeID] [int] NOT NULL,
    [Value] [decimal](18, 3) NOT NULL,
    [Story] [varchar](255) NOT NULL,
    [LastUpdated] [datetime] NOT NULL,
    [LastUpdatedBy] [varchar](50) NOT NULL,
    [ConcurrencyTimestamp] [timestamp] NOT NULL,
    [EffectiveDate] [datetime] NOT NULL,
    [DefaultQuantity] [int] NOT NULL,
 CONSTRAINT [PK_ResidentialComponentPrices] PRIMARY KEY CLUSTERED 
(
    [ResidentialComponentValueID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING OFF
GO
CREATE NONCLUSTERED INDEX [_dta_index_ResidentialComponentValues_71_56543435__K1] ON [dbo].[ResidentialComponentValues] 
(
    [ResidentialComponentValueID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [_dta_index_ResidentialComponentValues_71_56543435__K1_2_3_4_5_6_7_8_9] ON [dbo].[ResidentialComponentValues] 
(
    [ResidentialComponentValueID] ASC
)
INCLUDE ( [ResidentialComponentTypeID],
[Value],
[Story],
[LastUpdated],
[LastUpdatedBy],
[ConcurrencyTimestamp],
[EffectiveDate],
[DefaultQuantity]) WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [_dta_index_ResidentialComponentValues_71_56543435__K2_K1] ON [dbo].[ResidentialComponentValues] 
(
    [ResidentialComponentTypeID] ASC,
    [ResidentialComponentValueID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [_dta_index_ResidentialComponentValues_71_56543435__K2_K8_K1] ON [dbo].[ResidentialComponentValues] 
(
    [ResidentialComponentTypeID] ASC,
    [EffectiveDate] ASC,
    [ResidentialComponentValueID] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
CREATE NONCLUSTERED INDEX [_dta_index_ResidentialComponentValues_71_56543435__K2_K8_K1_3_4_5_6_7_9] ON [dbo].[ResidentialComponentValues] 
(
    [ResidentialComponentTypeID] ASC,
    [EffectiveDate] ASC,
    [ResidentialComponentValueID] ASC
)
INCLUDE ( [Value],
[Story],
[LastUpdated],
[LastUpdatedBy],
[ConcurrencyTimestamp],
[DefaultQuantity]) WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
/****** Object:  ForeignKey [FK_ResidentialComponentValues_ResidentialComponentTypes]    Script Date: 01/03/2012 13:49:06 ******/
ALTER TABLE [dbo].[ResidentialComponentValues]  WITH CHECK ADD  CONSTRAINT [FK_ResidentialComponentValues_ResidentialComponentTypes] FOREIGN KEY([ResidentialComponentTypeID])
REFERENCES [dbo].[ResidentialComponentTypes] ([ResidentialComponentTypeID])
GO
ALTER TABLE [dbo].[ResidentialComponentValues] CHECK CONSTRAINT [FK_ResidentialComponentValues_ResidentialComponentTypes]
GO
</code></pre>

<p><img src="https://i.sstatic.net/X6wu8.jpg" alt="enter image description here"></p>

## Answers
### Answer ID: 8719367
<p>It's not clear to me from reading your queries what you're actually trying to achieve.  Is your outer query trying to select only the most recently effective ResidentialComponentValues records for each ResidentialComponentType?</p>

<p>The <code>DISTINCT</code> on the inner-most query seems unnecessary and may cause the database some difficulty in optimizing the query.  You're only selecting 2 columns, and you are grouping by one and aggregating the other, therefore I'm sure that the results will already be distinct.  You're not helping the database execute this query more efficiently by specifying <code>DISTINCT</code>, though perhaps the query optimizer would ignore it.</p>

<p>Similarly, the first <code>INNER JOIN</code> to ResidentialComponentValues on the inner query seems like it is unnecessary.</p>

<p>The <code>ON</code> condition for your second <code>INNER JOIN</code> in your subquery (shown below) confuses me. It seems like this is simply joining your LPA_E1 result with the ResidentialComponentValues  table from the first <code>INNER JOIN</code> in your subquery, but I think what you're really trying to do is join it with the ResidentialComponentValues table from the outer query.</p>

<pre><code>ON  
    LPA_E1.ResidentialComponentTypeId = ResidentialComponentValues.ResidentialComponentTypeID 
    AND LPA_E1.EffectiveDate = ResidentialComponentValues.EffectiveDate
</code></pre>

<hr>

<p>My guess is that below is the query that you really want, though I don't think that it produces the same results as your original.  This selects only the most recently effective ResidentialComponentValue records for each ResidentialComponentType.</p>

<pre><code>declare @endDate datetime
set @endDate = '2012-01-03 00:00:00:000'

SELECT
    ResidentialComponentValues.ResidentialComponentValueID AS ResidentialComponentValueId, 
    ResidentialComponentValues.ResidentialComponentTypeID AS ResidentialComponentTypeId, 
    ResidentialComponentValues.Value, 
    ResidentialComponentValues.Story, 
    ResidentialComponentValues.LastUpdated, 
    ResidentialComponentValues.LastUpdatedBy, 
    ResidentialComponentValues.ConcurrencyTimestamp, 
    ResidentialComponentValues.EffectiveDate, 
    ResidentialComponentValues.DefaultQuantity 
FROM 
    ResidentialComponentValues  
WHERE
    -- the effective date for this ResidentialComponentValue record has already passed
    ResidentialComponentValues.EffectiveDate &lt;= @endDate
    -- and there does not exist any other ResidentialComponentValue record for the same ResidentialComponentType that is effective more recently
    and not exists (
        select 1
        from ResidentialComponentValues LPA_E1
        where
            LPA_E1.ResidentialComponentTypeID = ResidentialComponentValues.ResidentialComponentTypeID
            and LPA_E1.EffectiveDate &lt;= @endDate
            and LPA_E1.EffectiveDate &gt; ResidentialComponentValues.EffectiveDate
    )
</code></pre>

<p>Side Note: My guess is that this query would benefit from a 2-column index on the ResidentialComponentValues table for columns (ResidentialComponentTypeID, EffectiveDate).</p>

<p><hr>
Additionally, I think that this query shown below will probably produce the same results as your original, and my guess is that it will execute faster.</p>

<pre><code>SELECT
    ResidentialComponentValues.ResidentialComponentValueID AS ResidentialComponentValueId, 
    ResidentialComponentValues.ResidentialComponentTypeID AS ResidentialComponentTypeId, 
    ResidentialComponentValues.Value, 
    ResidentialComponentValues.Story, 
    ResidentialComponentValues.LastUpdated, 
    ResidentialComponentValues.LastUpdatedBy, 
    ResidentialComponentValues.ConcurrencyTimestamp, 
    ResidentialComponentValues.EffectiveDate, 
    ResidentialComponentValues.DefaultQuantity 
FROM 
    ResidentialComponentValues  
WHERE
    -- show any ResidentialComponentValue records where there is any other currently effective ResidentialComponentValue record for the same ResidentialComponentType
    exists (
        select 1
        from ResidentialComponentValues LPA_E1
        where
            LPA_E1.ResidentialComponentTypeID = ResidentialComponentValues.ResidentialComponentTypeID
            and LPA_E1.EffectiveDate &lt;= @endDate
    )
</code></pre>

<p><hr>
Given the following test data, the first query returns records 2 and 4.  The second query returns records 1, 2, 3, 4, and 5.</p>

<pre><code>insert into ResidentialComponentTypes values (1)
insert into ResidentialComponentTypes values (2)
insert into ResidentialComponentTypes values (3)

insert into ResidentialComponentValues (ResidentialComponentValueID, ResidentialComponentTypeID, Value, Story, LastUpdated, LastUpdatedBy, EffectiveDate, DefaultQuantity)
          select 1, 1, 'One',   'Blah', getdate(), 'Blah', '2012-01-01', 1
union all select 2, 1, 'Two',   'Blah', getdate(), 'Blah', '2012-01-02', 1
union all select 3, 1, 'Three', 'Blah', getdate(), 'Blah', '2012-01-04', 1
union all select 4, 2, 'Four',  'Blah', getdate(), 'Blah', '2012-01-02', 1
union all select 5, 2, 'Five',  'Blah', getdate(), 'Blah', '2012-01-04', 1
union all select 6, 3, 'Six',   'Blah', getdate(), 'Blah', '2012-01-04', 1
</code></pre>

### Answer ID: 8719258
<p>The inner subquery does not need the <code>DISTINCT</code> as you already <code>GROUP BY ResidentialComponentTypeID</code>:</p>

<pre><code>    (
        SELECT DISTINCT 
            ResidentialComponentValues.ResidentialComponentTypeID 
              AS ResidentialComponentTypeId, 
            MAX(ResidentialComponentValues.EffectiveDate) 
              AS EffectiveDate 
        FROM ResidentialComponentValues 
        WHERE ResidentialComponentValues.EffectiveDate 
              &lt;= '2012-01-03 00:00:00:000'
        GROUP BY ResidentialComponentValues.ResidentialComponentTypeID
    ) LPA_E1 
</code></pre>

<p>Not sure if SQL-Server will recognize this and optimize but you can rewrite to be sure:</p>

<pre><code>    (
        SELECT 
            rcv.ResidentialComponentTypeID 
            MAX(rcv.EffectiveDate) AS EffectiveDate 
        FROM ResidentialComponentValues  AS rcv
        WHERE rcv.EffectiveDate 
              &lt;= '2012-01-03 00:00:00:000'
        GROUP BY rcv.ResidentialComponentTypeID
    ) LPA_E1 
</code></pre>

<hr>

<p>And if I am not wrong, you also need neither the other <code>DISTINCT</code> in the query nor the extra subquery nesting. Check if this rewrite gives the same results:</p>

<pre><code>SELECT 
    v.ResidentialComponentValueID, 
    v.ResidentialComponentTypeID, 
    v.Value, 
    v.Story, 
    v.LastUpdated, 
    v.LastUpdatedBy, 
    v.ConcurrencyTimestamp, 
    v.EffectiveDate, 
    v.DefaultQuantity 
FROM 
        ResidentialComponentTypes  AS t
    INNER JOIN ResidentialComponentValues  AS v
        ON  t.ResidentialComponentTypeID=v.ResidentialComponentTypeID
    INNER JOIN 
        (
            SELECT 
                rcv.ResidentialComponentTypeID 
                MAX(rcv.EffectiveDate) AS EffectiveDate 
            FROM ResidentialComponentValues  AS rcv
            WHERE rcv.EffectiveDate 
                  &lt;= '2012-01-03 00:00:00:000'
            GROUP BY rcv.ResidentialComponentTypeID
        ) LPA_E1 
        ON  
            LPA_E1.ResidentialComponentTypeId = v.ResidentialComponentTypeID 
            AND LPA_E1.EffectiveDate = v.EffectiveDate
</code></pre>

<hr>

<p>You also do not need to join the <code>ResidentialComponentTypes</code> as there is a <code>Foreign Key</code> constraint from the <code>ResidentialComponentValues</code> to it but perhaps you have that join to be used in other reports.</p>

<hr>

<p>No idea how that would be done in LLBL but if you can remove any of the <code>DISTINCT</code> from the code generated - especially the first one - or the extra nesting (or the extra join), it will probably help the confused optimizer. </p>

