# Jdbc update statement in spark
[Link to question](https://stackoverflow.com/questions/63038823/jdbc-update-statement-in-spark)
**Creation Date:** 1595434964
**Score:** 0
**Tags:** apache-spark, jdbc, databricks
## Question Body
<p>I am connected to a database using JDBC and I am trying to run an update query. First I am typing the query, then I am executing it (in the same way I do the SELECT which works perfectly fine).</p>
<pre><code>caseoutputUpdateQuery = &quot;(UPDATE dbo.CASEOUTPUT_TEST SET NOTIFIED = 'YES') alias_output &quot;
spark.read.jdbc(url=jdbcUrl, table=caseoutputUpdateQuery, properties=connectionProperties) 
</code></pre>
<p>When I run this I have the following error:</p>
<p><code>A nested INSERT, UPDATE, DELETE, or MERGE statement must have an OUTPUT clause.</code></p>
<p>I tried to fix this in different ways but there is always another error. For example, I tried to rewrite the query in the following way:</p>
<pre><code>caseoutputUpdateQuery = &quot;(UPDATE dbo.CASEOUTPUT_TEST SET NOTIFIED = 'YES' OUTPUT DELETED.*, INSERTED.* FROM dbo.CASEOUTPUT_TEST) alias_output &quot; 
</code></pre>
<p>but I encounter this error:
<code>A nested INSERT, UPDATE, DELETE, or MERGE statement is not allowed in a SELECT statement that is not the immediate source of rows for an INSERT statement.</code></p>
<p>The other way I tried to rewrite it was:</p>
<pre><code>caseoutputUpdateQuery = &quot;(INSERT INTO dbo.UpdateOutput(OldCaseID,NotifiedOld) SELECT * FROM( UPDATE dbo.CASEOUTPUT_TEST SET NOTIFIED = 'YES' OUTPUT deleted.OldCaseID,DELETED.NotifiedOld ) AS tbl) alias_output &quot; 
</code></pre>
<p>but I've got this error:</p>
<p><code>A nested INSERT, UPDATE, DELETE, or MERGE statement is not allowed inside another nested INSERT, UPDATE, DELETE, or MERGE statement.</code></p>
<p>I've literally tried everything I found on the internet but without luck. Do you have any suggestion on how I can fix this and run my update statement?</p>

## Answers
### Answer ID: 71682184
<p>spark.read under the covers does a select * from the source jdbc table.  if you pass a query, spark translates it to</p>
<p>select your query
from ( their query select *)</p>
<p>Sql complains because you are trying to do an update on a view &quot;select * from&quot;</p>

### Answer ID: 63040074
<p>I think Spark is not designed for that UPDATE statement use case. That's not the scenario where Spark can help to deal with RDBMS. I suggest to use a direct connection using a JDBC from the code you are writing (I mean calling that JDBC directly). If you are using Scala you can use as suggested <a href="http://guyharrison.squarespace.com/blog/2014/4/30/best-practices-for-accessing-oracle-from-scala-using-jdbc.html" rel="nofollow noreferrer">here</a> (for example, but there are other multiple ways) or from Python as explained <a href="https://www.oracletutorial.com/python-oracle/updating-data/" rel="nofollow noreferrer">here</a>. Those samples reach Oracle engine, but please change the driver/connector if you are using MySQL, SQL Server, Postgres or any other RDMBS</p>

