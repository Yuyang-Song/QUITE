# Convert column dateformat inline with sql query
[Link to question](https://stackoverflow.com/questions/37263289/convert-column-dateformat-inline-with-sql-query)
**Creation Date:** 1463432924
**Score:** 0
**Tags:** android, sqlite, date-format, julian-date
## Question Body
<p>I have stored date in a column of android sqlite database in YYYY/MM/DD format . Now I want to use julianday function in sql query to select special rows of database however julianday uses date in YYYY-MM-DD format . How can I convert date format inline with sql query?</p>

<p>Please rewrite this sample query which "startdate" and "enddate" are stored in YYYY/MM/DD format not YYYY-MM-DD:</p>

<pre><code>select * from events where julianday(enddate)-julianday(startdate)&gt;1200
</code></pre>

## Answers
### Answer ID: 37263761
<p>SQL query accepts inline replace:</p>

<pre><code>select * from events where julianday(replace(enddate,'/','-'))-julianday(replace(startdate,'/','-'))&gt;1200
</code></pre>

<p>for more complex conversion use prepared SQL <strong><a href="http://www.w3schools.com/sql/func_convert.asp" rel="nofollow">convert()</a></strong> function</p>

