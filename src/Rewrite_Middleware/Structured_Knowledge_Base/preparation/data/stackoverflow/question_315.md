# SQL Server queries with datetime
[Link to question](https://stackoverflow.com/questions/20395320/sql-server-queries-with-datetime)
**Creation Date:** 1386233356
**Score:** 0
**Tags:** sql, sql-server, ms-access
## Question Body
<p>I have old program with access database. I want rewrite it to MS ACCESS. In queries u have text value <code>mm/yyyy</code> in query how to convert it to datetime from string?</p>

## Answers
### Answer ID: 20395380
<pre><code>DECLARE @a nvarchar(100)
SET @a = '12052013'

SELECT CONVERT(DATETIME,LEFT(@a,2) + '/' + 
       SUBSTRING(@a,3,2) + '/' + RIGHT(@a,4),101)
</code></pre>

<p>outputs this</p>

<pre><code> --2013-12-05 00:00:00.000
</code></pre>

