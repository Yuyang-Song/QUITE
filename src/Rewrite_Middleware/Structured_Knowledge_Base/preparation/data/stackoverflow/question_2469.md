# Access pass through query
[Link to question](https://stackoverflow.com/questions/35922926/access-pass-through-query)
**Creation Date:** 1457629820
**Score:** 1
**Tags:** sql-server, ms-access, stored-procedures
## Question Body
<p>I have a very easy Stored Procedure in SQL (this is my first one!) and I can run it after researching how to accomplish this. Essentially, it deletes all the current records in a table and appends a new set of records. (I have read that having two queries in the same Stored Procedure may cause the problem I am having.)</p>

<p>This works very well the first time I run it. I make a change to the open table to see if it works the second time. It does not. I can even close the database, reopen and rerun the code and it still doesn't give me what I expect.</p>

<p>What I have figured out is that if I try to open the "CurrentProc" query in the Access window, I get an error that says "Pass-through query with ReturnsRecords property set to True did not return any records." That's fine, because after I hit "OK", the code will work again and give me the expected return.</p>

<p>My question is what can I do with the code below so that I can make whatever change I want to in a table, but have it all reset whenever I call the function without having to open the CurrentProc query and getting the error message. (Yes, I have tried opening the query with OpenQuery, but that didn't work either.)</p>

<p>Please understand that, while I have been an Access developer for (yikes!) nearly 20 years, this is my first time trying to use SQL stored procedures. Running this same query in Access takes about 45 minutes. Using the Stored procedure, it literally takes seconds! I will be adapting this for use with much larger recordsets and rewriting some Access code as SQL stored procedures to leverage this power, so any ideas you can provide will be greatly appreciated.</p>

<pre><code>Dim qdf As dao.QueryDef
Dim dbs As dao.Database
Dim rst As dao.Recordset
Dim sSQL As String


strConnect = "ODBC;DRIVER={SQL Server}" _
            &amp; ";SERVER=ourserver\equipment" _
            &amp; ";DATABASE=BDS"

Set dbs = CurrentDb
Set qdf = dbs.QueryDefs("CurrentProc")
qdf.Connect = strConnect
qdf.SQL = "exec AppendtoFRPbyModel1"
DoCmd.OpenTable "FRP by Model1"

Set rst = Nothing
Set qdf = Nothing
Set dbs = Nothing
</code></pre>

<p>Josetta</p>

## Answers
### Answer ID: 35925213
<p>Here's what worked:
I changed ReturnsRecords to "no" and that didn't do anything, HOWEVER, when I added "DoCmd.OpenQuery "CurrentProc" I did not receive an error (as I did before when I tried to run it outside of code) and I did get the expected results every time. Thank you!! </p>

