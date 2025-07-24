# Getting General error: 4004 General SQL Server error:
[Link to question](https://stackoverflow.com/questions/36428649/getting-general-error-4004-general-sql-server-error)
**Creation Date:** 1459865026
**Score:** 2
**Tags:** php, sql-server, pdo, laravel-5
## Question Body
<p>I am trying to fetch data from my database in Laravel, however I am getting a "General error: 4004 General SQL Server error:"</p>

<p>I'm using Laravel-5 with MSSQL.
If I use the DB object to fetch data from MSSQL I am not able to fetch xml and nvarchar fields, </p>

<p>I found a usefull link below, but to implement this I have to rewrite all my queries. Is there any other way?</p>

<p><a href="https://gullele.wordpress.com/2010/12/15/accessing-xml-column-of-sql-server-from-php-pdo" rel="nofollow">https://gullele.wordpress.com/2010/12/15/accessing-xml-column-of-sql-server-from-php-pdo</a></p>

## Answers
### Answer ID: 57196498
<p>The most important information for everybody else is the answer to the question: <strong>What does the error 4004 (severity 16) mean?</strong></p>

<blockquote>
  <p><em>Error 4004:</em> Unicode data in a Unicode-only collation or ntext data cannot be sent to clients using DB-Library (such as ISQL) or ODBC version 3.7 or earlier. </p>
</blockquote>

<p>(<a href="http://www.sql-server-helper.com/error-messages/msg-4001-5000.aspx" rel="nofollow noreferrer">Source</a>)</p>

<p>In my case, I had to cast a <code>STUFF()</code> clause to <code>VARCHAR(MAX)</code> to resolve the error, after migrating to SQL Server 2016 and setting <code>tds version = 7.4</code>.</p>

### Answer ID: 36449205
<p>Please try :</p>

<pre><code> $handle = getHandle();
 $handle-&gt;exec('SET QUOTED_IDENTIFIER ON');
 $handle-&gt;exec('SET ANSI_WARNINGS ON');
 $handle-&gt;exec('SET ANSI_PADDING ON');
 $handle-&gt;exec('SET ANSI_NULLS ON');
 $handle-&gt;exec('SET CONCAT_NULL_YIELDS_NULL ON');
</code></pre>

<p>OR</p>

<p>You can also check the server configuration:
check the "/etc/freetds.conf " file and change the tds version and add client charset then in php.ini please check mssql.charset and default_charset</p>

<p>in /etc/freetds.conf :</p>

<pre><code>;tds version = 4.2
tds version = 8.0
client charset = UTF-8
</code></pre>

<p>In php.ini :</p>

<pre><code>mssql.charset = "UTF-8"
default_charset = "utf-8"
</code></pre>

