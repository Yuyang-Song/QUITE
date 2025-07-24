# Can I create a pass-through query via VBA to call a parameterized tSQL UDF and send it a dynamic parameter to return results to Access?
[Link to question](https://stackoverflow.com/questions/26789986/can-i-create-a-pass-through-query-via-vba-to-call-a-parameterized-tsql-udf-and-s)
**Creation Date:** 1415310305
**Score:** 0
**Tags:** vba, ms-access, parameter-passing, user-defined-functions
## Question Body
<p>I currently have a SQL 2008 R2 database backend with an Access 2013 accdb front end with ODBC DSN-less connection and linked tables. In SQL I have many parameterized tSQL UDFs created to feed data into reports (currently working well in my Access 2010 adp frontend). The reports are complicated: multiple tSQL UDFs run calculations and then feed into a final UDF that feeds the respective report. I would like to keep the UDFs on the server – rewriting into Access queries would be a poor solution.
My problem is that I have not been able to figure out how to write the VBA correctly to send a pass-through query to call the tSQL UDF and give it a parameter, which would change for each report. I know pass-through queries are read-only, that’s ok. I’ve read that I can call a stored procedure (SP) from VBA, but can I call the UDF rather than having to convert each to a SP or create a SP just to call the UDF so that I could call the SP from VBA. Based on my research, I think I might have to either create a SP to call the UDF or convert the UDF to a SP to get the VBA to work (i.e., return results without error). Is this correct?</p>

<p>I found this discussion: <a href="https://social.msdn.microsoft.com/Forums/office/en-US/898933f5-73f9-44e3-adb9-6aa79ebc948f/calling-a-sql-udf-from-access?forum=accessdev" rel="nofollow noreferrer">https://social.msdn.microsoft.com/Forums/office/en-US/898933f5-73f9-44e3-adb9-6aa79ebc948f/calling-a-sql-udf-from-access?forum=accessdev</a> , but it has conflicting statements “You can't call a tSql udf from Access.”, and “You can use a passthrough query to call UDF's or stored procedures or anything else written in tsql.” Also, their code is written in ADO instead of DOA so it’s a bit cryptic to me since I’ve only written DAO so far, but the general gist that I got was they converted their UDF to a SP.</p>

<p>I found this article a great read, but again did not get a clear “yes” to my question:
<a href="http://technet.microsoft.com/en-us/library/bb188204(v=sql.90).aspx" rel="nofollow noreferrer">http://technet.microsoft.com/en-us/library/bb188204(v=sql.90).aspx</a></p>

<p>It may be possible to remove the parameter from the Server side and add it to the Access side similar to this <a href="https://stackoverflow.com/questions/3200470/access-2007-forms-with-parameterized-recordsource">Access 2007 forms with parameterized RecordSource</a> , but wouldn't that cause Access to load the entire dataset before filtering, instead of processing on the Server side – possibly causing performance issues?</p>

<p>I can successfully create a pass-through query in the Access interface if I supply it with a constant parameter, for example “Select * from udf_FinalReport(2023)”, but what I really need is to be able to pass a dynamic parameter. For example, the parameter would be from Forms!Control![txtboxValue]. Can I do this? The following code is what I’m using– it works if I use a table name in the SQL (ex, “SELECT * FROM Table WHERE tblYear = “&amp;intYear ) in line 9 so I feel like I have everything coded right, but when I put my UDF in the SQL like below I get the error #3131 “Syntax error in FROM clause.” (I did verify that I should not use the prefix schema (dbo.) – this gives error 3024 “could not find file”.) Is this user error or just plain telling me I can’t call a UDF this way?</p>

<pre><code>1 Sub AnnualSummary()
2 Dim dbs As DAO.Database
3  Dim qdfPoint As DAO.QueryDef
4  Dim rstPoint As DAO.Recordset
5  Dim intYear As Integer
6  intYear = Reports!Annual_Delineation_Summary!txtYear
7 Set dbs = OpenDatabase("", False, False, "ODBC;DRIVER=sql server;SERVER=******;APP=Microsoft 
8 Office 2010;DATABASE=*******;Network=DBMSSOCN")
9 Set qdfPoint = dbs.CreateQueryDef("", "Select * from udf_AnnualReport(" &amp; intYear&amp; ")")
10 GetPointTemp qdfPoint
11 ExitProcedure:
12  On Error Resume Next
13    Set qdfPoint = Nothing
14    Set dbs = Nothing
15    Set rstPoint = Nothing
16 Exit Sub
17 End Sub
18
19 Function GetPointTemp(qdfPoint As QueryDef)
20  Dim rstPoint As Recordset
21  With qdfPoint
22   Debug.Print .Name
23   Debug.Print " " &amp; .SQL
24   Set rstPoint = .OpenRecordset(dbOpenSnapshot)
25   With rstPoint
26     .MoveLast
27     Debug.Print " Number of records = " &amp; _
28      .RecordCount
29     Debug.Print
30     .Close
31   End With
32  End With
33 End Function
</code></pre>

<p>I also tried writing the code a little differently, using the following instead of lines 5, 6, and 9. This also works when I use a table name in the select statement, but I get error #3131 when I use a UDF name:</p>

<pre><code> Set qdfPoint = dbs.CreateQueryDef("", "Parameters year int; Select * from Point_Info where 
 year(Sample_Date) = year")
 qdfPoint.Parameters("year").Value = intYear
</code></pre>

<p>Both code variations also work if I try use the name of a SQL View in the tSQL SELECT statement.</p>

## Answers
### Answer ID: 43683773
<p>I don't know if it's the most efficient method of passing a variable parameter through a pass-through query into a function and returning the results to Access, as I am still relatively new to Access, but I came across this earlier when I was attempting a similar problem.
I managed it by creating a couple of pass-through queries that executed functions in SQL server and returned a result. I then made a small VBA script that re-wrote the pass-through queries with the new variable every time I wanted to change it, and executed them.</p>

<p>I got the result back out using OpenRecordset, and stored it as a string to use in the rest of my code.</p>

### Answer ID: 26986715
<p>My consensus is using ADO language instead of DAO to write the pass-through query works well.  But, I have found that it is still probably better to execute a stored procedure than to try to call the UDF.  Here is the code that ended up working most smoothly for me:  (my ADO Connection uses Public variables strUID and strPWD) </p>

<pre><code>   Dim cn As ADODB.Connection
   Dim rs As ADODB.Recordset
   Dim strPoint As String

   strPoint = Forms!FRM_Vegetation_Strata!Point_ID

   Set cn = New ADODB.Connection

   cn.Open "Provider = sqloledb;Data Source=imperialis.inhs.illinois.edu;" &amp; _
           "Initial Catalog=WetlandsDB_SQL;User Id=" &amp; strUID &amp; ";Password=" &amp; strPWD

   Set rs = New ADODB.Recordset
   With rs
      Set .ActiveConnection = cn
      .Source = "sp_Report_VegWorksheet '" &amp; strPoint &amp; "'"
      .LockType = adLockOptimistic
      .CursorType = adOpenKeyset
      .CursorLocation = adUseClient
      .Open
   End With

   Set Me.Recordset = rs
</code></pre>

<p>On a side note I found that to get set the .Recordset to fill a subform put this code in the "Open" event of the subform.  </p>

<p>Then to clean up your connection:</p>

<pre><code>Private Sub Form_Unload(Cancel As Integer)  'use "unload", not "close"
   'Close the ADO connection we opened
   Dim cn As ADODB.Connection
   Dim rs As ADODB.Recordset
   Set cn = Me.Recordset.ActiveConnection
   cn.Close
   Set cn = Nothing
   Set rs = Nothing
   Set Me.Recordset = Nothing

End Sub
</code></pre>

<p>This approach does not work for populating a report.  "Set Me.Recordset" only works for forms.  I believe I will have to call a stored procedure then populate a temp table to use as the report recordset.</p>

<p>EDIT: I have found that I can call a SQL UDF or SP from VBA in Access using DOA.  This is particularly helpful when one wants to pull the data from a complicated SQL function/procedure and put it into an Access-side temp table.   See Juan Soto's blog <a href="https://accessexperts.com/blog/2012/01/10/create-temp-tables-in-access-from-sql-server-tables/#comment-218563" rel="nofollow">https://accessexperts.com/blog/2012/01/10/create-temp-tables-in-access-from-sql-server-tables/#comment-218563</a> This code puts the info into a temp table, which is what I wanted to populate my reports.  I used his code example and the following to call the sub:
To execute as SP: <code>CreateLocalSQLTable "testTBL","exec dbo.sp_Report_WetDet_point '1617-1-1A'",False</code>
To call a UDF: <code>CreateLocalSQLTable "testTBL","Select * from dbo.QryReport_Main('1617-2-2A')",False</code></p>

