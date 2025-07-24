# Rewrite the MS Access query to less number of lines
[Link to question](https://stackoverflow.com/questions/58173008/rewrite-the-ms-access-query-to-less-number-of-lines)
**Creation Date:** 1569866511
**Score:** 1
**Tags:** sql, ms-access
## Question Body
<p>So there's a database from which I regularly pull data for 200 Quarters. The Quarters are named as column Q0r, Q1r, Q2r,.....,Q200r.</p>

<p>So my query goes as 
Select Q0r, Q1r, Q2r, Q3r....., Q199r, Q200r from testdata where [condition];</p>

<p>I was wondering if there's an easy way to rewrite this query so I don't have to literally do counting from 0 to 200 in the select statement.</p>

## Answers
### Answer ID: 58180797
<p>Create a function to build the SQL and write it to the query:</p>

<pre class="lang-vb prettyprint-override"><code>Public Function CreateQuery()

    Dim Query           As DAO.QueryDef
    Dim SqlMaster       As String
    Dim Sql             As String
    Dim Id              As Integer
    Dim Names(0 To 200) As String

    Set Query = CurrentDb.QueryDefs("QueryQuarters")

    SqlMaster = "Select {0} From YourTable"

    For Id = LBound(Names) To UBound(Names)
        Names(Id) = "Q" &amp; CStr(Id) &amp; "r"
    Next

    Sql = Replace(SqlMaster, "{0}", Join(Names, ","))
    Query.Sql = Sql

    Debug.Print Sql

End Function
</code></pre>

### Answer ID: 58173057
<p>You can use an asterisk to select all columns:</p>

<pre><code>SELECT *
FROM tablename
</code></pre>

