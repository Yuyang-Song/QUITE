# What Does *= means in WHERE Clause in TSQL?
[Link to question](https://stackoverflow.com/questions/17439701/what-does-means-in-where-clause-in-tsql)
**Creation Date:** 1372825807
**Score:** 5
**Tags:** sql, sql-server, t-sql
## Question Body
<p>some one have asked me the output of below query.</p>

<pre><code>Select      *    
from        TableA t1, TableB t2
where       t1.Id *= t2.Id
</code></pre>

<p>Can anyone explain me, if such type of any query exists, if so then how its works. Because i have never seen such type of query Thanks.<br />
<strong>UPDATE:</strong> 
<br />
Also when i run this query in SQL Server, i get this;</p>

<pre><code>The query uses non-ANSI outer join operators ("*=" or "=*"). 
To run this query without modification, please set the compatibility level 
for current database to 80, using the SET COMPATIBILITY_LEVEL option 
of ALTER DATABASE. 
It is strongly recommended to rewrite the query using ANSI outer join 
operators (LEFT OUTER JOIN, RIGHT OUTER JOIN). 
In the future versions of SQL Server, non-ANSI join operators will 
not be supported even in backward-compatibility modes.
</code></pre>

## Answers
### Answer ID: 17439740
<p>Using asterisk in a <code>WHERE</code> is an old <code>non-ANSI</code> compliant syntax for <code>OUTER JOIN</code>ing tables and therefore should not be used anymore.</p>

<p>Here's the <a href="http://sqlmag.com/sql-server/old-join-syntax-vs-new" rel="noreferrer">link</a>.</p>

### Answer ID: 17439747
<p>The asterisk in the where condition is actually part of a <code>non-ANSI outer join operator</code>, it is used to define an implicit outer join.</p>

<p>It will cause trouble in modern databases as this operator has been obsolete since 1992.</p>

<p>Essentially the below are the same:</p>

<pre><code>  SELECT * FROM TableA LEFT OUTER JOIN TableB ON t1.Id = t2.Id

  SELECT * FROM TableA , TableB WHERE t1.Name *= t2.Name
</code></pre>

### Answer ID: 17439714
<p>The <code>*=</code> operator means <code>LEFT OUTER JOIN</code>.</p>

