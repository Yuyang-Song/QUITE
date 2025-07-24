# Excel VBA UpdatePivotCache results in Error 438 - Object Doesn&#39;t support Property or method
[Link to question](https://stackoverflow.com/questions/40228478/excel-vba-updatepivotcache-results-in-error-438-object-doesnt-support-propert)
**Creation Date:** 1477347566
**Score:** 1
**Tags:** excel, excel-2013, vba
## Question Body
<p>I have a spreadsheet that generates a summary of a Database query as Pivot Charts. This database query was written by a 3rd party and works very well, except that it deletes everything in the worksheet and rewrites all of the data in that same sheet. To work with this, I've written a macro to do some minor re-arranging of the data, and then update the cache of the Pivot Tables. I would like the Pivot Tables themselves to persist, as the filters and parameters of the Pivot Tables will not change between updates.</p>

<p>Here's the code that I wrote to accomplish this:</p>

<pre><code>Dim wb As Workbook
Dim sh As Worksheet
Dim sht As Worksheet
Dim pvtCache As PivotCache
Dim pvt As PivotTable
Dim SrcData As String

Set wb = ThisWorkbook
Set sh = wb.Sheets("Data")

'Find Last Row of Data
Lastrow = sh.Range("D" &amp; Rows.Count).End(xlUp).Row    
' STEP 2 - Update Pivot Tables

' Set Source Data
SrcData = sh.Name &amp; "!" &amp; sh.Range("$A1:$CS" &amp; Lastrow).Address(ReferenceStyle:=xlR1C1)
Set pvtCache = wb.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=SrcData, Version:=xlPivotTableVersion15)

' Change Pivot Cache to current Range and Refresh for all Pivot tables in Sheet
For Each sht In wb.Worksheets
    For Each pvt In sht.PivotTables
' ERROR 438 - Object Doesn't support Property or method
        pvt.ChangePivotCache (pvtCache)
        'sht.PivotTables(pvt).ChangePivotCache (pvtCache) ' Attempt 2
        'sht.PivotTables(pvt).ChangePivotCache (wb.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=SrcData, Version:=xlPivotTableVersion15)) ' Attempt 2 - Longhand pvtCache
' ERROR 1004 - Method 'PivotTables' of object '_Worksheet' failed
        pvt.PivotCache.Refresh
    Next pvt
Next sht
</code></pre>

<p>The error occurs on the line:</p>

<pre><code> pvt.ChangePivotCache (pvtCache)
</code></pre>

<p>Every reference I've seen says that this should be a legitimate way to change the Pivot Cache, but it gives me an "Error 438 - Object Doesn't support Property or Method" every time. I've also tried to do it outside the loop with this code:</p>

<pre><code>    ' Update WeekStops
Set sht = wb.Sheets("Stops by Week")
sht.PivotTables("WeekStops").ChangePivotCache (wb.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=SrcData, Version:=xlPivotTableVersion15))
sht.PivotTables("WeekStops").PivotCache.Refresh
</code></pre>

<p>The Error 438 still occurs on the ChangePivotCache command. </p>

<p>Could it be related to the Error 1004 that happens on the next line</p>

<pre><code>pvt.PivotCache.Refresh
</code></pre>

<p>when I comment out the line above it?</p>

<p>Thanks and Best Regards,</p>

<p>John</p>

## Answers
### Answer ID: 40239840
<p>The Issue was in the creation of pvtCache external to the ChangePvtCache command, as well as using parentheses in ChangePivotCache.</p>

<p>The working code looks like: </p>

<pre><code>pvt.ChangePivotCache wb.PivotCaches.Create(SourceType:=xlDatabase, SourceData:=SrcData, Version:=xlPivotTableVersion15)
</code></pre>

<p>Thanks everyone for your help.</p>

