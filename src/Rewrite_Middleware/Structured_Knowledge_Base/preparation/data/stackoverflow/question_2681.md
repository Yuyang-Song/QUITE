# Add aliases to each table in SQL query (programmatically)
[Link to question](https://stackoverflow.com/questions/47037501/add-aliases-to-each-table-in-sql-query-programmatically)
**Creation Date:** 1509459134
**Score:** 0
**Tags:** sql, .net, sql-server
## Question Body
<p>I need programmatically edit SQL commands in such way that each table in the SQL command will have an alias. The input is a schema for the database and an SQL command. The output should be an SQL query where every table and has an alias and it is always used when we reference an attribute of that table.</p>

<p>For example, let us have a database <code>person(id, name, salary, did)</code> and <code>department(did, name)</code> and the following SQL command:</p>

<pre><code>select id, t.did, maxs
from person
join (
  select did, max(salary) maxs
  from person
  group by did
) t on t.maxs = salary and person.did = t.did
</code></pre>

<p>The expected result for such input would be </p>

<pre><code>select p1.id, t.did, t.maxs
from person p1
join (
  select p2.did, max(p2.salary) maxs
  from person p2
  group by p2.did
) t on t.maxs = p1.salary and p1.did = t.did
</code></pre>

<p>I was considering using ANTLR4 for this, however, I was curious whether there is a simpler solution. I recently come across <a href="https://msdn.microsoft.com/en-us/library/microsoft.sqlserver.transactsql.scriptdom.tsqlparser.aspx" rel="nofollow noreferrer">TSqlParser</a>, is it possible to use this class to achieve such rewrite in some simple way?</p>

