# SQL LIKE Operator doesn&#39;t work with Asian Languages (SQL Server 2008)
[Link to question](https://stackoverflow.com/questions/4698704/sql-like-operator-doesnt-work-with-asian-languages-sql-server-2008)
**Creation Date:** 1295080816
**Score:** 6
**Tags:** sql-server, select, unicode, collation, nvarchar
## Question Body
<p>I have a SQL Server database column that is of type NVarchar and is filled with standard Persian characters. when I'm trying to run a very simple query on it which incorporates the LIKE operator, the resultset becomes empty although I know the query term is present in the table. Here is the very simple example query which doesn't act correctly:</p>
<pre><code>SELECT * FROM T_Contacts WHERE C_ContactName LIKE '%ف%'
</code></pre>
<p>ف is a Persian character and the ContactName column contains multiple entries which contain that character.</p>
<p>Please tell me how should I rewrite the expression or what change should I apply. Note that my database's collation is <code>SQL_Latin1_General_CP1_CI_AS</code>.</p>
<p>Thank you very much</p>

## Answers
### Answer ID: 4698849
<p>Also, if those values are stored as <code>NVARCHAR</code> (which I hope they are!!), you should <strong>always</strong> use the <code>N'..'</code> prefix for any string literals to make sure you don't get any unwanted conversions back to non-Unicode <code>VARCHAR</code>.</p>

<p>So you should be searching:</p>

<pre><code>SELECT * FROM T_Contacts 
WHERE C_ContactName COLLATE Persian_100_CI_AS LIKE N'%ف%'
</code></pre>

### Answer ID: 4698847
<p>Shouldn't it be:</p>

<pre><code> SELECT * FROM T_Contacts WHERE C_ContactName LIKE N'%ف%'
</code></pre>

<p>ie, with the <code>N</code> in front of the comparing string, so it treats it like an <code>nvarchar</code>?</p>

