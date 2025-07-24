# Column name in SQL query from request
[Link to question](https://stackoverflow.com/questions/53415217/column-name-in-sql-query-from-request)
**Creation Date:** 1542813619
**Score:** 1
**Tags:** c#, sql-server, oracle-database, sql-injection
## Question Body
<p>I was given a task to rewrite an old web API.</p>

<p>This API reads SQL queries from the database.</p>

<p>There's literally a view with "Queries" in the name which contains "SqlText" column.</p>

<pre><code>SELECT SqlText FROM Queries WHERE QueryID = 123
</code></pre>

<p>The "SqlText" contains only simple SQL queries in the format <code>SELECT [columns] FROM [table]</code> by convention.</p>

<p>The query is altered depending on the URL parameters in the request. The result of this query is then shown as result.</p>

<pre><code>string parsedColumns = ParseColumns(queryRow); //contains "Column1, Column2";
string parsedTable = ParseTable(queryRow); //contains "SomeTable"

string requestColumns = HttpContext.Request["columns"];
string sqlColumns = requestColumns ?? parsedColumns;

string col1Condition = HttpContext.Request["Column1"]
string col2Condition = HttpContext.Request["Column2"]

string sqlQuery = "SELECT " + sqlColumns 
                  + " FROM " + parsedTable 
                  + " WHERE Column1 = " + col1Condition 
                  + " AND Column2 = " + col2Condition;
</code></pre>

<p>This is obvious SQL injection issue so I started rewritting it.</p>

<p>Now there are three other problems.</p>

<ul>
<li>I cannot change the structure of the database or the convention</li>
<li>The database is either Oracle or SQL Server</li>
<li>I don't know how to correctly work with the "columns" URL parameter to avoid SQL injection.</li>
</ul>

<p>It's easy to convert the URL parameters in the WHERE clause to the SQL parameters for both SQL Server and Oracle.</p>

<p>SQL Server</p>

<pre><code>var sqlCommand = new SqlCommand("SELECT * FROM SomeTable WHERE Condition1 = @con1 AND Condition2 = @con2");
</code></pre>

<p>Oracle</p>

<pre><code>var oracleCommand = new OracleCommand("SELECT * FROM SomeTable WHERE Condition1 = :con1 AND Condition2 = :con2");
</code></pre>

<p><strong>Column identifiers</strong></p>

<p>The problem is with the <code>HttpContext.Request["columns"]</code>. I still need to somehow alter the SQL query string with URL parameters which I don't like at all. </p>

<p>To simplify the issue, let's consider a single column from URL request.</p>

<pre><code>string column = HttpContext.Request["column"];
var cmd = new SqlCommand($"SELECT {column} FROM ...");
</code></pre>

<p>I know that in SQL Server the identifier can be surrounded by braces. So my line of thinking is that I'm safe if I strip all braces from the column.</p>

<pre><code>string column = HttpContext.Request["column"];
column = column.Replace("[", "").Replace("]", "");
column = $"[{column}]";
var cmd = new SqlCommand($"SELECT {column} FROM ...");
</code></pre>

<p>Oracle uses quotation marks.</p>

<pre><code>string column = HttpContext.Request["column"];
column = column.Replace("\"", "");
column = $"\"{column}\"";
var cmd = new OracleCommand($"SELECT {column} FROM ...");
</code></pre>

<p><strong>The question</strong></p>

<ul>
<li>Is this sql-injection safe enough?</li>
<li>Or is this use case inherently sql-injection unsafe?</li>
</ul>

## Answers
### Answer ID: 53418142
<p>Since you are working with a basic program design that you cannot change what about just trying to add edits to the input to look for injection elements.  For example if the input is a column name it will need to have a maximum length of 30 (before 12.x) characters and should not contain a semicolon or the strings " OR" or " AND" in them.  While not a perfect solution this should be practical solution.</p>

