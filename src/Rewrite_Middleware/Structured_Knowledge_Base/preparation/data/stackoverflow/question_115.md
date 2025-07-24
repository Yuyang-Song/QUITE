# How can I get the SQL query object or parse tree in MySQL?
[Link to question](https://stackoverflow.com/questions/13471467/how-can-i-get-the-sql-query-object-or-parse-tree-in-mysql)
**Creation Date:** 1353408074
**Score:** 4
**Tags:** mysql
## Question Body
<p>I need to analyze the queries run against a MySQL database, in order to see which tables, columns etc are being accessed. Potentially I might do query rewriting too.</p>

<p>Does MySQL provide a callback/hook where it can give me the query information as a parsed object, instead of the raw string that gets logged to the files.</p>

<p>I read about the <a href="http://dev.mysql.com/doc/refman/5.5/en/writing-audit-plugins.html" rel="nofollow">Audit Plugin API</a> but it too passes the query as a string and not in a structured format.</p>

<p>Any help or pointers would be greatly appreciated.</p>

## Answers
### Answer ID: 53560466
<p>It sounds like what you need is an AQT: <a href="https://dev.mysql.com/worklog/task/?id=4533" rel="nofollow noreferrer">https://dev.mysql.com/worklog/task/?id=4533</a> .
But it only converts the MySQL query to a tree, and doesn't take your database in to consideration</p>

### Answer ID: 14685058
<pre><code>Does MySQL provide a callback/hook where it can give me the query information as a parsed object, instead of the raw string that gets logged to the files.
</code></pre>

<p>No, there is no such interface.</p>

<p>There is no abstract syntax tree either, the parser produces structures that are very coupled with the server runtime.</p>

