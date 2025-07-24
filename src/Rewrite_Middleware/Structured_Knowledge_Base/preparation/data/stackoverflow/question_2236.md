# Sql server which is better &quot;Rank&quot; or &quot;Left join with own table&quot; to filter latest records
[Link to question](https://stackoverflow.com/questions/25488607/sql-server-which-is-better-rank-or-left-join-with-own-table-to-filter-latest)
**Creation Date:** 1408978214
**Score:** 0
**Tags:** sql, sql-server, sql-server-2008
## Question Body
<p>I have the following table in database with around 10 millions records (it will increase in future may be double in 1 year):</p>

<pre><code>create table PropertyOwners (
    [Key] int not null primary key,
    PropertyKey int not null, 
    BoughtDate DateTime, 
    OwnerKey int not null
)
go
</code></pre>

<p>Above table contains all the property owned by an owner at certain time, I want to get the owners which owns more than certain amount of properties at a current time, lets say more then 1000 properties at a time. I have written two different queries one using "Rank" and other using "Left join with own table".</p>

<p><strong>Using Rank (Taking around 4 sec):</strong></p>

<pre><code>select OwnerKey, COUNT(1) PropertyCount 
from (
    select PropertyKey, OwnerKey, BoughtDate,
        RANK() over (partition by PropertyKey order by BoughtDate desc) as [Rank]
    from dbo.PropertyOwners 
) result
where [Rank]=1
group by OwnerKey
having COUNT(1)&gt;1000
</code></pre>

<p>Using left join with same table (Taking around 10sec):</p>

<pre><code>select OwnerKey, COUNT(1) PropertyCount 
from (
    select po.PropertyKey, po.OwnerKey, po.BoughtDate
    from dbo.PropertyOwners po
    left join dbo.PropertyOwners lo on lo.PropertyKey = po.PropertyKey
    and lo.BoughtDate &gt; po.BoughtDate
    where lo.PropertyKey is null
) result
group by OwnerKey
having COUNT(1)&gt;1000
</code></pre>

<p>Both of the query times are unacceptable as taking so much time, can anyone help me with the query to rewrite. My table has following index:</p>

<pre><code>CREATE NONCLUSTERED INDEX [IX_PropertyKey_BounghtDate] ON [dbo].[PropertyOwners] 
(
    [PropertyKey] ASC,
    [BoughtDate] DESC
)
INCLUDE ( [OwnerKey]) WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
GO
</code></pre>

## Answers
### Answer ID: 25499911
<p>Grouping is never fast. You may look into indices that SQL Server will suggest if you run your queries sufficient amount of times; google diagnostic queries that involve <code>sys.dm_db_index_usage_stats</code>, they will be of some help.</p>

<p>Another option, already suggested before, is building a summary table. Slightly more lightweight solution will be an indexed view, but you have to understand implications that will come into play if you will create it.</p>

### Answer ID: 25489582
<p>You have a fair amount of data and a lot that has to be counted.  <a href="http://sqlperformance.com/2012/12/t-sql-queries/left-anti-semi-join" rel="nofollow">This</a> analysis by Aaron Bertrand isn't exactly your problem, but it might help you.</p>

<p>With your supporting index, I would recommend trying the <code>not exists</code> approach:</p>

<pre><code>select OwnerKey, count(*) as PropertyCount
from PropertyOwners po
where not exists (select 1
                  from PropertyOwners po2
                  where po2.PropertyKey = po.PropertyKey and
                        po2.BoughtDate &gt; po.BoughtDate
                 )
group by OwnerKey
having count(*) &gt; 1000;
</code></pre>

<p>If you can't get the query to work sufficiently fast, you may need to either upgrade your hardware or use triggers to keep a summary table up-to-date.</p>

### Answer ID: 25489005
<p>You could rewrite this as (which might improve performance)</p>

<pre><code>select OwnerKey, COUNT(1) PropertyCount 
from (
    select PropertyKey, MAX( BoughtDate) BoughtDate
    from dbo.PropertyOwners 
    Group by PropertyKey
) result INNER JOIN dbo.PropertyOwners po ON po.PropertyKey=result.PropertyKey and PO.boughtDate=result.boughtdate
group by OwnerKey
having COUNT(1)&gt;1000
</code></pre>

