# Optimize run speed on for next loops vba
[Link to question](https://stackoverflow.com/questions/51897019/optimize-run-speed-on-for-next-loops-vba)
**Creation Date:** 1534514355
**Score:** 0
**Tags:** excel, vba, for-loop, ms-query
## Question Body
<p>TLDR: I'm trying to make this macro run faster.</p>

<p>Macro overview: Refresh a query tied to an order database. The query refreshes a month's worth of data in about 9 seconds. A filter is used to copy only values from the selected <code>DateVal</code> and copies it to the first report page (with some formatting).</p>

<p>Next is where it bogs down. Applying this <code>averageifs()</code> formula to each row takes a while. Then after that it goes through each row and removes orders within the acceptable variance range. This also takes a while. I tried applying the <code>averageifs()</code> formula inside the query itself but I don't believe MSQuery can do that calculation. So the first loop takes about 10 minutes and the second loop takes another 10 minutes per month of data.</p>

<p>Any ideas to optimize the two <code>for i next i</code> loops below? I'd really like to be able to use 2 months of data, but it adds so much time to complete the macro.</p>

<p>Here is the full vba:</p>

<pre><code>Option Explicit
Public wb As Workbook
Public ws0, ws1, ws2 As Worksheet
Public i, t As Long
Public lRow, lCol As Long
Public DateVal, MinVar, MinMul, CritMul As Long

Sub ExceptionReport()
'This Macro is designed for call center to highlight potential keying errors.
'The criteria are fairly simple logic and are on the second tab (ws0).
'This backs up against a query file (.dqy).
'It uses the following tables: RMORHP, RMORDP, RMCUSP, and RMITMP.
'If any of these tables aren't getting fresh information, none of this wil work.
'General logic steps are to:
'(1) Refresh query
'(2) Copy query data to the report tab
'(3) Set up some qualifiers
'(4) Remove unqualified rows


'Some initial setup
Set wb = ThisWorkbook
Set ws0 = wb.Sheets("Setup")
Set ws1 = wb.Sheets("Report")
Set ws2 = wb.Sheets("Query")

'Store user filter criteria from setup tab
DateVal = ws0.Range("B4").Value
MinVar = ws0.Range("B5").Value
MinMul = ws0.Range("B6").Value
CritMul = ws0.Range("B7").Value

'In case someone messed with the refresh settings, this will delay macro until query refresh.
With wb.Connections("Order Table").ODBCConnection
    .BackgroundQuery = False
End With

'Refresh Query &amp; request parameter input
wb.RefreshAll

'Completely rewrite the Report page in case someone messed it up
ws1.Activate
ws1.Cells.Delete shift:=xlUp
ws1.Range("A1:L1").Merge
ws1.Range("A1:L1").Font.Bold = True
ws1.Range("A2:L2").Merge
With ws1.Range("A1:L2")
    .HorizontalAlignment = xlCenter
    .VerticalAlignment = xlBottom
    .WrapText = False
    .Orientation = 0
    .AddIndent = False
    .IndentLevel = 0
    .ShrinkToFit = False
    .ReadingOrder = xlContext
End With

ws1.Range("A1:K1").Value = "Order Entry Exception Report"
ws1.Range("A2:K2").Value = "Exception Report " &amp; Format(Now, "mm/dd/yy hh:Nn")
ws1.Range("K4").Value = "Avg Units Ordered"
ws1.Range("L4").Value = "Var From Avg"

'Find Out how large the Query dataset is
'We know the dataset is 10 columns
lCol = 10
lRow = ws2.Cells(Rows.Count, 1).End(xlUp).Row

'Copy Query (ws2) to Report (ws1) tab with a filter/unfilter on the query table
ws2.ListObjects("Table_Order_Table").Range.AutoFilter Field:=2, Criteria1:=DateVal
ws2.Range(ws2.Cells(1, 1), ws2.Cells(lRow, lCol)).SpecialCells(xlCellTypeVisible).Copy
ws1.Range(ws1.Cells(4, 1), ws1.Cells(lRow + 3, lCol)).PasteSpecial xlPasteValues
ws2.ListObjects("Table_Order_Table").Range.AutoFilter Field:=2

'Remove all rows that don't have specified date
'The above filter/unfilter make these lines obsolete. Improved runtime by about 15min per month of data.
'For i = lRow + 3 To 5 Step -1
'    If ws1.Range("B" &amp; i).Value &lt;&gt; DateVal Then ws1.Range("B" &amp; i).EntireRow.Delete
'Next i

'Relalc lRow
lRow = ws1.Cells(Rows.Count, 1).End(xlUp).Row

'Add the average units per order and variance amount
For i = 5 To lRow
    ws1.Range("K" &amp; i).Formula = "=+IFERROR(ROUND(AVERAGEIFS(Table_Order_Table[Units Ordered],Table_Order_Table[Product],Report!H" &amp; i &amp; ",Table_Order_Table[Customer Number],Report!D" &amp; i &amp; ",Table_Order_Table[Order Number],""&lt;&gt;""&amp;Report!A" &amp; i &amp; "),0),0)"
    ws1.Range("L" &amp; i).Formula = "=abs(K" &amp; i &amp; "-J" &amp; i &amp; ")"
Next i

'Copy/Paste to improve calculation speed by removing formulas
ws1.Range(ws1.Cells(5, 11), ws1.Cells(lRow, 12)).Copy
ws1.Range(ws1.Cells(5, 11), ws1.Cells(lRow, 12)).PasteSpecial xlPasteValues

'Remove rows that aren't outside acceptable variance
For i = lRow To 5 Step -1
    If ws1.Range("L" &amp; i) &lt; MinVar Or ws1.Range("K" &amp; i).Value * MinMul &gt;= ws1.Range("J" &amp; i).Value Then ws1.Range("L" &amp; i).EntireRow.Delete
Next i

'Delete rows in the Query to make the file smaller
lRow = ws2.Cells(Rows.Count, 1).End(xlUp).Row
ws2.Range(ws2.Cells(2, 1), ws2.Cells(lRow, lCol)).EntireRow.Delete

'Some more formatting
ws1.Activate
ActiveWindow.Zoom = 100
ws1.Cells.EntireColumn.AutoFit
ws1.Range("A4:L4").Font.Bold = True
ws1.Range("A4:L4").Font.Underline = xlUnderlineStyleSingle
ws1.Range("A1").Select

End Sub
</code></pre>

<p>Here is the SQL Query:</p>

<pre><code>XLODBC 1 DRIVER=SQL Server;

SERVER=*OMIT*;

UID=*OMIT*;

Trusted_Connection=Yes;

APP=Microsoft Office 2010;

WSID=*OMIT*;

DATABASE=*OMIT*
SELECT DISTINCT RMORHP.ORHORDNUM AS 'Order Number',
                RMORHP.ORHCRTDTE AS 'Order Create Date',
                RMORHP.ORHCRTUSR AS 'Created By',
                CONCAT(RMORHP.ORHCUSCHN, '-', RMORHP.ORHCUSNUM) AS 'Customer Number',
                RMORHP.ORHCUSCHN AS 'Chain ID',
                RMORHP.ORHCUSNUM AS 'Cust ID',
                RMCUSP.CUSCUSNAM AS 'Customer Name',
                RMORDP.ORDITMNUM AS 'Product',
                RMITMP.ITMLNGDES AS 'Product Name',
                RMORDP.ORDADJQTY AS 'Units Ordered'
FROM *OMIT*.RMORHP RMORHP,
     *OMIT*.RMCUSP RMCUSP,
     *OMIT*.RMORDP RMORDP,
     *OMIT*.RMITMP RMITMP
WHERE (RMORHP.ORHCRTDTE BETWEEN ? AND ?)
  AND RMCUSP.CUSCUSCHN = RMORHP.ORHCUSCHN
  AND RMCUSP.CUSCUSNUM = RMORHP.ORHCUSNUM
  AND RMORHP.ORHORDNUM = RMORDP.ORDORDNUM
  AND RMORDP.ORDITMNUM = RMITMP.ITMITMNUM
  AND RMCUSP.CUSDFTDCN = 505 enter
  START date "yyyymmdd" enter END date "yyyymmdd"
</code></pre>

## Answers
### Answer ID: 51898133
<p>I modify the code, not test yet! Hope it helps. Just disable update, then enable:</p>

<pre><code>Option Explicit
Public wb As Workbook
Public ws0, ws1, ws2 As Worksheet
Public i, t As Long
Public lRow, lCol As Long
Public DateVal, MinVar, MinMul, CritMul As Long

Sub ExceptionReport()
'This Macro is designed for call center to highlight potential keying errors.
'The criteria are fairly simple logic and are on the second tab (ws0).
'This backs up against a query file (.dqy).
'It uses the following tables: RMORHP, RMORDP, RMCUSP, and RMITMP.
'If any of these tables aren't getting fresh information, none of this wil work.
'General logic steps are to:
'(1) Refresh query
'(2) Copy query data to the report tab
'(3) Set up some qualifiers
'(4) Remove unqualified rows


'Some initial setup
Set wb = ThisWorkbook
Set ws0 = wb.Sheets("Setup")
Set ws1 = wb.Sheets("Report")
Set ws2 = wb.Sheets("Query")

'Store user filter criteria from setup tab
DateVal = ws0.Range("B4").Value
MinVar = ws0.Range("B5").Value
MinMul = ws0.Range("B6").Value
CritMul = ws0.Range("B7").Value

'In case someone messed with the refresh settings, this will delay macro until query refresh.
With wb.Connections("Order Table").ODBCConnection
    .BackgroundQuery = False
End With

'Refresh Query &amp; request parameter input
wb.RefreshAll

'Completely rewrite the Report page in case someone messed it up
ws1.Activate
ws1.Cells.Delete shift:=xlUp
ws1.Range("A1:L1").Merge
ws1.Range("A1:L1").Font.Bold = True
ws1.Range("A2:L2").Merge
With ws1.Range("A1:L2")
    .HorizontalAlignment = xlCenter
    .VerticalAlignment = xlBottom
    .WrapText = False
    .Orientation = 0
    .AddIndent = False
    .IndentLevel = 0
    .ShrinkToFit = False
    .ReadingOrder = xlContext
End With

ws1.Range("A1:K1").Value = "Order Entry Exception Report"
ws1.Range("A2:K2").Value = "Exception Report " &amp; Format(Now, "mm/dd/yy hh:Nn")
ws1.Range("K4").Value = "Avg Units Ordered"
ws1.Range("L4").Value = "Var From Avg"

'Find Out how large the Query dataset is
'We know the dataset is 10 columns
lCol = 10
lRow = ws2.Cells(Rows.Count, 1).End(xlUp).Row

'Copy Query (ws2) to Report (ws1) tab with a filter/unfilter on the query table
ws2.ListObjects("Table_Order_Table").Range.AutoFilter Field:=2, Criteria1:=DateVal
ws2.Range(ws2.Cells(1, 1), ws2.Cells(lRow, lCol)).SpecialCells(xlCellTypeVisible).Copy
ws1.Range(ws1.Cells(4, 1), ws1.Cells(lRow + 3, lCol)).PasteSpecial xlPasteValues
ws2.ListObjects("Table_Order_Table").Range.AutoFilter Field:=2

'Remove all rows that don't have specified date
'The above filter/unfilter make these lines obsolete. Improved runtime by about 15min per month of data.
'For i = lRow + 3 To 5 Step -1
'    If ws1.Range("B" &amp; i).Value &lt;&gt; DateVal Then ws1.Range("B" &amp; i).EntireRow.Delete
'Next i

'Relalc lRow
lRow = ws1.Cells(Rows.Count, 1).End(xlUp).Row

'DISABLE ALL

Application.ScreenUpdating = False
Application.Calculation = xlCalculationManual
Application.EnableEvents = False

'Add the average units per order and variance amount
For i = 5 To lRow
    ws1.Range("K" &amp; i).Formula = "=+IFERROR(ROUND(AVERAGEIFS(Table_Order_Table[Units Ordered],Table_Order_Table[Product],Report!H" &amp; i &amp; ",Table_Order_Table[Customer Number],Report!D" &amp; i &amp; ",Table_Order_Table[Order Number],""&lt;&gt;""&amp;Report!A" &amp; i &amp; "),0),0)"
    ws1.Range("L" &amp; i).Formula = "=abs(K" &amp; i &amp; "-J" &amp; i &amp; ")"
Next i

'Copy/Paste to improve calculation speed by removing formulas
ws1.Range(ws1.Cells(5, 11), ws1.Cells(lRow, 12)).Copy
ws1.Range(ws1.Cells(5, 11), ws1.Cells(lRow, 12)).PasteSpecial xlPasteValues

'Remove rows that aren't outside acceptable variance
For i = lRow To 5 Step -1
    If ws1.Range("L" &amp; i) &lt; MinVar Or ws1.Range("K" &amp; i).Value * MinMul &gt;= ws1.Range("J" &amp; i).Value Then ws1.Range("L" &amp; i).EntireRow.Delete
Next i

'Delete rows in the Query to make the file smaller
lRow = ws2.Cells(Rows.Count, 1).End(xlUp).Row
ws2.Range(ws2.Cells(2, 1), ws2.Cells(lRow, lCol)).EntireRow.Delete

'ENABLE
Application.ScreenUpdating = True
Application.Calculation = xlCalculationAutomatic
Application.EnableEvents = True

'Some more formatting
ws1.Activate
ActiveWindow.Zoom = 100
ws1.Cells.EntireColumn.AutoFit
ws1.Range("A4:L4").Font.Bold = True
ws1.Range("A4:L4").Font.Underline = xlUnderlineStyleSingle
ws1.Range("A1").Select

End Sub
</code></pre>

