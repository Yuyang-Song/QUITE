# Trouble exporting query to Excel from Access
[Link to question](https://stackoverflow.com/questions/34599358/trouble-exporting-query-to-excel-from-access)
**Creation Date:** 1451939600
**Score:** 0
**Tags:** excel, ms-access, vba
## Question Body
<p>I am attempting to export a query based on two combo boxes to excel.  Two weeks ago, this code worked.  I have moved the database, and updated the code.  Now, when I run it, it will open the query, and open excel, but it will NOT rewrite the excel file.  It just opens up the old data.</p>

<p>Access 2010</p>

<p>Code:</p>

<pre><code>Private Sub Command14_Click()

DoCmd.OpenQuery "rtnbymonth_qry", acViewNormal, acEdit
DoCmd.OutputTo acOutputQuery, "rtnbymonth_qry", acFormatXLS, "S:\Sales &amp; Use Tax\2016\export.xls"
DoCmd.Close acQuery, "rtnbymonth_qry", acSaveNo

'Open Excel
Call OpenSpecific_xlFile
End Sub
</code></pre>

<p>Also here is the code for the program to open excel:</p>

<pre><code>'mini program to open excel

Sub OpenSpecific_xlFile()
 '   Late Binding (Needs no reference set)
Dim oXL As Object
Dim oExcel As Object
Dim sFullPath As String
Dim sPath As String


 '   Create a new Excel instance
Set oXL = CreateObject("Excel.Application")


 '   Only XL 97 supports UserControl Property
On Error Resume Next
oXL.UserControl = True
On Error GoTo 0


 '   Full path of excel file to open
On Error GoTo ErrHandle
sFullPath = CurrentProject.Path &amp; "\export.xls"


 '   Open it
With oXL
    .Visible = True
    .Workbooks.Open (sFullPath)
End With


ErrExit:
    Set oXL = Nothing
    Exit Sub

ErrHandle:
    oXL.Visible = False
    MsgBox Err.Description
    GoTo ErrExit
End Sub
</code></pre>

## Answers
### Answer ID: 34600766
<p>Turns out that the location I was saving it to is different than the location where the database is stored.  The correct file was saved, just not in the location I was opening it.  Easy fix! Programmer error.</p>

