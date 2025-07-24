# Different results when querying with OleDb compared to directly in Access
[Link to question](https://stackoverflow.com/questions/18337302/different-results-when-querying-with-oledb-compared-to-directly-in-access)
**Creation Date:** 1377008020
**Score:** 1
**Tags:** .net, vb.net, ms-access, ado.net, oledb
## Question Body
<p>We currently use ADO.Net in a couple of internal products, and one of those products must query a Microsoft Access database with OleDB. The problem we have right now is that one of the query does not produce the same results when executed by <code>OleDbDataAdapter.Fill</code> and when executed directly in Microsoft Access' SQL View.</p>
<p>The query looks like this:</p>
<pre><code>SELECT DISTINCT t1.* 
FROM tableOne AS t1 
INNER JOIN tableTwo AS t2 ON t2.tableOne_no = t1.tableOne_no 
WHERE t1.status = 'A' 
AND t2.tableThree_no = @p_tableThree_no
AND t2.status = 1 
AND (t2.startDate IS NULL OR (YEAR(t2.startDate) &lt;= @p_year AND MONTH(t2.startDate) &lt;= @p_month)) 
AND (t2.endDate IS NULL OR (YEAR(t2.endDate) &gt;= @p_year AND MONTH(t2.endDate) &gt;= @p_month))
</code></pre>
<p>We query the database with the following code, using Microsoft ACE OLEDB 12 and ADO.Net:</p>
<pre><code>Dim oDataSet As New DataSet()
    
Using oSqlConnection As New OleDbConnection(&quot;Provider=Microsoft.ACE.OLEDB.12.0;Data Source=\\NetworkDrive\database.mdb;User Id=admin;Password=password;&quot;)

    Using oSqlCommand As New OleDbCommand(p_sQuery, oSqlConnection)

        oSqlCommand.Parameters.AddWithValue(&quot;@p_tableThree_no&quot;, 1111)
        oSqlCommand.Parameters.AddWithValue(&quot;@p_year&quot;, 2013)
        oSqlCommand.Parameters.AddWithValue(&quot;@p_month&quot;, 7)
        oSqlCommand.CommandType = CommandType.Text

        Using oDataAdapter As New OleDbDataAdapter()

            oDataAdapter.SelectCommand = oSqlCommand

            oSqlConnection.Open()
            oDataAdapter.Fill(oDataSet)

        End Using

    End Using

End Using
</code></pre>
<p>Somehow, executing the query from OleDB doesn't give the same number of results than executing the same query in Microsoft Access (Access having the correct number of results). When executing the same query with different <code>@p_tableThree_no</code> values, everything seems okay. Is it possible that specific values from some Text field would cause OleDB to ignore rows in that specific case? There is no error message and the code runs successfully, only with wrong results.</p>
<p>Searching for this problem on Google and StackOverflow provided little to no help, as the only solutions I found are for problems with <code>LIKE</code> statements (using % instead of *) and with parameters names conflicts, which are not relevant to my situation.</p>
<p>Am I missing something? Is the query too complex for OleDB? Should I wrap something in parentheses? I have no idea what I'm doing wrong.</p>
<h1>Edit &amp; Solution</h1>
<p>Turns out the query was wrong to begin with, and nobody (including myself) pinpointed it at first glance. I was rewriting the query from stratch when I noticed that <code>MONTH(t2.startDate) &lt;= @p_month</code> didn't make any sense if the date is, for example, 2012-11 compared to 2013-07. I still don't know why the query results were &quot;wrongly correct&quot; when executing it directly in Access and providing parameters in popup windows, but that's another mystery I'm not willing to solve. I'm accepting @HansUp 's answer since he did provide me a query that was the same on both sides and he was the one that made me doubt about the SQL itself.</p>

## Answers
### Answer ID: 18339827
<p>Define the parameters within the SQL statement, then supply the values from your code as before.  </p>

<p>Don't fret about the parameter names in <code>Parameters.AddWithValue</code>.  OleDb ignores the parameter names ... you could do <code>.AddWithValue("Hello World!", 1111)</code> and it wouldn't change anything.  However you must supply the parameters in the order Access expects, and I'm hopeful adding a <code>PARAMETERS</code> clause will avoid confusion there.  </p>

<pre class="lang-sql prettyprint-override"><code>PARAMETERS
    p_tableThree_no Long,
    p_year Long,
    p_month Long;
SELECT DISTINCT t1.* 
FROM
    tableOne AS t1 
    INNER JOIN
    tableTwo AS t2
    ON t2.tableOne_no = t1.tableOne_no 
WHERE
        t1.status = 'A' 
    AND t2.tableThree_no = p_tableThree_no
    AND t2.status = 1 
    AND (t2.startDate IS NULL
         OR (YEAR(t2.startDate) &lt;= p_year AND MONTH(t2.startDate) &lt;= p_month)) 
    AND (t2.endDate IS NULL
         OR (YEAR(t2.endDate) &gt;= p_year AND MONTH(t2.endDate) &gt;= p_month))
</code></pre>

### Answer ID: 18339243
<p>ACE.OLEDB ignores parameter names, so perhaps the OleDb query is getting confused because the <code>@p_year</code> and <code>@p_month</code> parameters are repeated in the SQL command but they are only specified once in the <code>OleDbCommand.Parameters</code> collection. I'd be inclined to try using <code>?</code> as the parameter placeholder and repeat the last two parameters (i.e.,  using five <code>AddWithValue</code> statements instead of three).</p>

