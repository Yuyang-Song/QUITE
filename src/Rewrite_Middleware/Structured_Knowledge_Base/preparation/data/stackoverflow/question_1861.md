# SQL Server Dynamic SQL to select the same columns from multiple similarly-named tables
[Link to question](https://stackoverflow.com/questions/10331993/sql-server-dynamic-sql-to-select-the-same-columns-from-multiple-similarly-named)
**Creation Date:** 1335437757
**Score:** 0
**Tags:** sql-server, sql-server-2005
## Question Body
<p>I have multiple tables that are updated (fairly infrequently) which creates new tables in my database. I then have to update my reports to query these historic tables, using the case function. Given the number of reports I have to provide, this is a lengthy exercise, and one which probably means my reports are underperforming due to lengthy case statements &amp; full outer joins. I was hoping to use some sort of a wildcard, to look through these similarly-named tables to extract the data (the columns I require all have the same name), so that every time the database is updated, I don't need to rewrite all my queries. e.g. </p>

<pre><code>Table1.PaymentStatus
Table1.Amount
Table2.PaymentStatus
Table2.Amount
....
TableX.PaymentStatus
TableX.Amount
</code></pre>

<p>Are the fields I would need -></p>

<pre><code>Payment Status   Amount
All Data         All Data   
</code></pre>

<p>Hopefully I could create some sort of dynamic sql including Union All, and then link this sort of subquery to the rest of my tables. I don't have much experience with dynamic SQL, &amp; found this query on the forum &amp; am trying to adapt it (and learn at the same time!) but am not having much luck. </p>

<pre><code>declare @columns table (idx int identity(1,1), table_name varchar(100), column_name varchar(50)) 

insert into @columns (table_name, column_name)  
select table_name, column_name 

from INFORMATION_SCHEMA.COLUMNS 

where table_name like '%Special%' 

declare @sql nvarchar(4000) 

declare @i int 
declare @cnt int 

declare @col varchar(100) 
declare @table varchar(100) 

select @i = 0, @cnt = max(idx), @sql = '' from @columns 

select *
from @columns

while @i &lt; @cnt 
begin 
    select @i = @i + 1 

    select @col = column_name, @table = table_name from @columns where idx = @i 

    if len(@sql) &gt; 0 
        select @sql = @sql + ', ' 

    select @sql = @sql + '[' + @table + '].[' + @col + '] as [' + @table + '_' + @col + ']' 
end 

select @sql = 'select ' + @sql + ' from *' 

exec sp_executesql @sql
</code></pre>

<p>I've had another suggestion about creating a view and linking my queries to this view so I only have to update this view every time an update occurs, but was wondering whether there was a more automatic solution. I don't have control over the way these copies are created unfortunately.</p>

<p>Thanks!</p>

## Answers
### Answer ID: 10332075
<p>Create a view a view that wraps the table and then write a query that drops and recreates the view using the latest table.</p>

<p>You can then run that query once whenever the tables change.</p>

<p>You can get a list of tables by querying sys.tables.</p>

