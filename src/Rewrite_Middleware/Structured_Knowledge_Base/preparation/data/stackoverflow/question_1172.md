# How to convert this existing query to retrieve the same information from a table located in a database on a linked server?
[Link to question](https://stackoverflow.com/questions/61929494/how-to-convert-this-existing-query-to-retrieve-the-same-information-from-a-table)
**Creation Date:** 1590046372
**Score:** 0
**Tags:** sql-server, t-sql, linked-server
## Question Body
<p>I am using <code>SQL Server 2014</code> and I have the following <code>T-SQL</code> query which gives me some nice information about any table on the database.</p>

<pre><code>USE [MyDatabase]

SELECT COLUMN_NAME,* 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Table1' AND TABLE_SCHEMA='dbo'
</code></pre>

<p>I would like to modifiy this query so that I get the same information from a table residing on a database on a linked server. </p>

<p>Assuming the full schema of the table is [xxx.xx.x.xx].Database2.dbo.[Table1], how do I rewrite my existing query?</p>

<p>I had a look at this <code>Stackoverflow</code> question but the answers do not meet my requirements: <a href="https://stackoverflow.com/questions/40917635/how-to-list-all-tables-columns-names-of-a-linked-server-database-in-sql-server">How to list all tables &amp; columns names of a linked-server database in SQL Server?</a></p>

## Answers
### Answer ID: 61930492
<p>Use a 4 parts identifier:</p>

<p><code>[server].[database].[information_Schema].[columns]</code></p>

<p><code>[server]</code> being the linked server name,<br>
<code>[database]</code> being the relevant database in the linked server.</p>

