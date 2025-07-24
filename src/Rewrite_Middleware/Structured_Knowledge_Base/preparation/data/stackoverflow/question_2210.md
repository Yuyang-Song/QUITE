# MS Access - Editing a query&#39;s sql with vba - change &quot;SELECT Top n&quot;
[Link to question](https://stackoverflow.com/questions/23995862/ms-access-editing-a-querys-sql-with-vba-change-select-top-n)
**Creation Date:** 1401716059
**Score:** 2
**Tags:** sql, ms-access, vba
## Question Body
<p>Context - I'm building an access database that keeps track of sailboat races and calculates overall season scores as well as smaller "series" of scores. However, in a "series" not every race is counted. For example, if a series has 10 races, I only want to count the top 7 races of each individual person. </p>

<p>I have a separate query that is able to calculate the number of races actually counted based on the total number in each series. The query I am working on now calculates each individual's score by adding up their points for their top "n" races in that series. I don't have an extensive knowledge in sql or vba, but I was able to figure out how to use the "SELECT Top n" to filter each individual's top scores and then use a SUM to get the total. </p>

<p>The problem I have now is that the "n" has to be adaptable because the series could have any number of races. After some research, I learned that the only way to alter "SELECT TOP" is to use vba to rewrite the query's definition. I'm not exactly sure how to accomplish this- I don't even know where to put the code to alter the query in vba. </p>

<p>Again, I don't have much experience in vba, but I'm eager to learn in order to accomplish what I need. Any help is appreciated and I can show my sql if needed.</p>

## Answers
### Answer ID: 23996144
<p>So, I think you want to store the value of the number of races in a series into a variable, and use that variable in your <code>Top N</code> query.</p>

<pre><code>Dim Db As DAO.Database
Dim rs As DAO.Recordset
Dim series As Integer

Set db = CurrentDb
Set rs = db.OpenRecordset("YourTableNameOrQueryName")
'Here we can open the Table and store the number of series into a variable.

series = rs!YourSeriesCountFieldInTableOrQuery

Dim SQL As String
SQL = "SELECT Top " &amp; series &amp; " races FROM YourTable"
' You can ensure you have the right number of series by setting a break point or
' Using Debug.Print (SQL) to see the SQL in the output window.

db.Execute "SQL", dbFailOnError

'The SQL string would be your query that you have working, as posted in your OP.
'The only difference would be the string concatenation of the number of series that is dynamic


rs.Close
Set rs = Nothing
</code></pre>

