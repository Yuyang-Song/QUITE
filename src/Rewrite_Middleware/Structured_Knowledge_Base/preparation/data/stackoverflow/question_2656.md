# Excel SQL import - Error 3704 Operation not allowed when object is closed
[Link to question](https://stackoverflow.com/questions/45083997/excel-sql-import-error-3704-operation-not-allowed-when-object-is-closed)
**Creation Date:** 1499956975
**Score:** 1
**Tags:** sql, excel, vba
## Question Body
<p>When trying to execute a sub in an Excel model I receive an error message saying: </p>

<blockquote>
  <p><em>Operation not allowed when object is closed.</em></p>
</blockquote>

<p>I have written code like this before in order to import data from a SQL database and never had any problems. I'm guessing the issue with this sub is that the sql query is making a temporary table, with a result from a stored procedure, of which I just want the 4 most recent data points.</p>

<p>The sub looks like this:</p>

<pre class="lang-vb prettyprint-override"><code>Sub sqlImport()

Dim dbConn As ADODB.connection
Set dbConn = New ADODB.connection

dbConn.ConnectionString = "Provider=SQLOLEDB;Integrated Security=SSPI;Network=dbmssocn;Initial Catalog=Funds;Data Source=" &amp; Data_Source_Prod02
dbConn.CursorLocation = adUseServer
dbConn.Open

'Define cell - top left in table
Dim startCell As Range
Set startCell = Import.Range("tableTopLeft")

'Clear the table
Range(startCell, startCell.End(xlDown).End(xlToRight)).ClearContents

'Setup SQL import
Dim CmdSP As New ADODB.Command
CmdSP.CommandType = adCmdText
CmdSP.CommandText = "CREATE TABLE #tmpBus2 (FundID INT, PortfolioDate date, TotalFundValueBillionSEK float, NAVSEK float, FundShares float)" &amp; _
                    "INSERT INTO #tmpBus2 EXEC Funds.Analysi.Fund_Size @FundId = 4235 " &amp; _
                    "SELECT TOP 4 PortfolioDate, NAVSEK, FundShares FROM #tmpBus2 ORDER BY PortfolioDate DESC"
CmdSP.ActiveConnection = dbConn

'Execute command
Dim dbList As ADODB.Recordset
Set dbList = CmdSP.Execute

'Print table data
Dim row As Integer, col As Integer
row = 1
While Not dbList.EOF
    For col = 0 To dbList.Fields.Count - 1
        startCell.Offset(row, col) = dbList(col)
    Next col

    dbList.MoveNext
    row = row + 1
Wend

dbConn.Close

End Sub
</code></pre>

<p>The error occurs at</p>

<pre><code>While Not dbList.EOF
</code></pre>

<p>Anyone have a solution?</p>

<p>I can't rewrite the stored procedure. And the result I get from the stored procedure is quite a big dataset, that's why I want to just select the top 4 rows.</p>

