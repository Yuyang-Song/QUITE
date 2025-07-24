# T-SQL query to return results into single table
[Link to question](https://stackoverflow.com/questions/37750348/t-sql-query-to-return-results-into-single-table)
**Creation Date:** 1465567614
**Score:** 2
**Tags:** sql-server, t-sql
## Question Body
<p>I am running a query against all databases within an instance. There are a few hundered databses with identical schema (tables and all).</p>

<p>This is the query:</p>

<pre><code>EXEC sp_MSforeachdb 'Use ? SELECT top 1  Column1, Column2 from [TableName]where Column3 = ''SpecificValue'' order by Column4 desc'
</code></pre>

<p>The query works alright and returns the results which I want, but not in a way I want them. </p>

<p>After I run this query, in the results pane I get one mini table per database so I end up with a few hundered mini tables. It's very impractical, and it forces me to copy results one by one. </p>

<p><a href="https://i.sstatic.net/3ArbU.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/3ArbU.jpg" alt="enter image description here"></a></p>

<p>Is there a way to rewrite this query so that it returns all results inone table with 2 columns. I would like each row to be like</p>

<p>value of column 1 from db 1    \   value of column2 dfrom db1</p>

<p>value of column 1 from db 2    \   value of column2 dfrom db2</p>

<p>value of column 1 from db 3    \   value of column2 dfrom db3</p>

<p>and so on...</p>

## Answers
### Answer ID: 37754558
<p>Although there are cases where a global temp table, i.e. "##", may be warranted, I try to stray away from them. Instead, you could still use a single session-based temp table, i.e. "#", or a table variable and just take a dynamic SQL approach to the problem.</p>

<p>Here's an alternative:</p>

<ul>
<li>Create a temp table, e.g. <code>#tmp</code>. </li>
<li>Create a single executable string of SQL to be run. This string will include a query for each database.</li>
<li>Then simply execute the SQL string.</li>
</ul>

<p>Here is the code:</p>

<pre><code>create table #tmp (
    database_id int,
    database_name varchar(128),
    object_id int,
    object_name varchar(128));

declare
    @Sql varchar(max) = (
        select 'insert #tmp (database_id, database_name, object_id, object_name) select ' + convert(varchar(128), database_id) + ', ''' + name + ''', object_id, name from ' + name + '.sys.objects;'
        from sys.databases
        where name in ('master', 'msdb', 'tempdb')
        for xml path(''));

exec (@Sql);

select
    database_name,
    object_count = count(*)
from #tmp
group by
    database_name
order by
    1;
</code></pre>

<p>Below are the results from the group by above:</p>

<pre>
database_name         object_count
--------------------- ------------
master                116
msdb                  1194
tempdb                81
</pre>

### Answer ID: 37751003
<p>You can use a global temp table for this:</p>

<pre><code>CREATE TABLE ##tmpTable(DBName VARCHAR(MAX),Content VARCHAR(MAX));
EXEC sp_MSforeachdb 'Use ? INSERT INTO ##tmpTable SELECT TOP 1 ''?'', TABLE_NAME FROM INFORMATION_SCHEMA.TABLES'
SELECT * FROM ##tmpTable;
GO
DROP TABLE ##tmpTable;
</code></pre>

