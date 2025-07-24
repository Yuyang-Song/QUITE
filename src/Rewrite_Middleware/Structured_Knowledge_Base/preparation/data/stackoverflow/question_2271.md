# Strong loop studio with SQL Server
[Link to question](https://stackoverflow.com/questions/26995606/strong-loop-studio-with-sql-server)
**Creation Date:** 1416317553
**Score:** 1
**Tags:** node.js, strongloop
## Question Body
<p>I am trying to use strong loop studio to build an api for a SQL Server database. Almost all the functions are working but if I want to find after id like this <code>localhost:3000/api/tableName/1</code> where 1 is the id, I get a syntax error. </p>

<blockquote>
  <p>Incorrect syntax near the keyword 'null'</p>
</blockquote>

<p>Using SQL Server Profiler I got the query that is executed and I got this: </p>

<pre><code>SELECT 
    [id], [name], [description], [application], 
FROM 
    (SELECT 
        [id], [name], [description], [application], ROW_NUMBER() OVER (null) AS RowNum
     FROM [dbo].[tableName]) AS S
WHERE 
    S.RowNum &gt; 0 AND S.RowNum &lt;= 1
</code></pre>

<p>What could be the problem? Can I override this method in some way and rewrite the query? 
Actually i tried this on multiple tables and I get the same error.</p>

## Answers
### Answer ID: 28772127
<p>That null comes from the order by clause in the SQL that StrongLoop creates. If it doesn't get an order, it seems to just use null. 
<a href="https://github.com/strongloop/loopback-connector-mssql/blob/master/lib/mssql.js#L667" rel="nofollow">https://github.com/strongloop/loopback-connector-mssql/blob/master/lib/mssql.js#L667</a></p>

<p>You can fix this by using an order in the default scope in your model.
<a href="http://docs.strongloop.com/display/public/LB/Model+definition+JSON+file#ModeldefinitionJSONfile-Defaultscope" rel="nofollow">http://docs.strongloop.com/display/public/LB/Model+definition+JSON+file#ModeldefinitionJSONfile-Defaultscope</a></p>

<pre><code>  "scope": {
    "order": "id"
  },
</code></pre>

