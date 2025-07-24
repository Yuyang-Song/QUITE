# LINQ Join between datatables, two untyped fields
[Link to question](https://stackoverflow.com/questions/22104086/linq-join-between-datatables-two-untyped-fields)
**Creation Date:** 1393615417
**Score:** 0
**Tags:** vb.net, linq, system.data.datatable
## Question Body
<p>I'm querying two databases and trying to join the result sets and query out of them using LINQ.  It seems it would be an easy task, but without doing an explicit join I'm having major performance issues.  When I do the explicit join, I am having trouble with VB syntax for making things explicit types.  Working Code, Cleaned:</p>

<pre><code>        For Each CurrRow In ResultsA.Tables(15).Rows
            CurrDate = CurrRow("Date")
            CurrID = CurrRow("ID")
            CurrVal = CurrRow("Val")
            Dim ResultsB = From SMW In DataSetA.Tables(0).AsEnumerable() _
                           Where SMW("ID") = CurrScheduleID And SMW("Time") = CurrProfileDate _
                           Select UTC_TS = SMW("Time"), Value = (SMW("VALUE") / 1000), Time_Zone = SMW("Time_Zone"), ID = SMW("ID")

            Dim CurrentResult As Object
            Dim boolSchedDateFound As Boolean = False
            For Each CurrentResult In ResultsB
                If CurrentResult.Value &lt;&gt; CurrVal Then
                    'LogIntegrityCheckErrorRow()
                End If
                boolSchedDateFound = True
            Next
        Next
</code></pre>

<p>This takes FOREVER to run with 100,000 rows.</p>

<p>I've been trying to rewrite this as:</p>

<pre><code>        Dim MismatchRows = From TableAData In DataSetA.Tables(0).AsEnumerable() Join TableBData In DataSetB.Tables(15).AsEnumerable() _
                On New With {.TableAID = Convert.ToInt32(TableAData("ID")), .TableATime = Convert.ToDateTime(TableAData("Date"))} _
                Equals New With {.TableBDID = Convert.ToInt32(TableBData("ID")), .TableBTime = Convert.ToDateTime(TableBData("Time"))} _
            Select ..................  (Hard to clean up, but this isn't the part that's failing)
</code></pre>

<p>And I'm having a bear of a time with it.  The fundamental problem is the lack of strong typing.  I've looked, but there seems to be little advice because most people doing this build EF on the data.  Which isn't a terrible idea, but would require a bunch of re-engineering.  So.  Problem in front of me, how do I remove the error:</p>

<pre><code>'Equals' cannot compare a value of type '&lt;anonymous type&gt; (line 2641)' with a value of type '&lt;anonymous type&gt; (line 2642)'.
</code></pre>

<p>Thank you so much for your help.</p>

## Answers
### Answer ID: 22148499
<pre><code>    db.tb_DeviceGeFenceDetail.Join(db.tb_InventoryLog, Function(gfd) gfd.DeviceID, Function(il) il.deviceId, Function(gfd, il) New From { _
gfd.GeFenceLat1, _
gfd.GeFenceLng1, _
gfd.GeFenceLat2, _
gfd.GeFenceLng2, _
il.deviceName, _
il.DeviceIcon, _
gfd.DeviceID, _
il.id _
}).ToList().Where(Function(y) intValues.Contains(y.id))
</code></pre>

<p>you can try joining tables something like this.</p>

### Answer ID: 22122866
<p>Have you tried this?</p>

<pre><code>Dim MismatchRows = From TableAData In ei _
    Join TableBData In e2 On _
        TableAData("ID") Equals TableBData("ID") And TableAData("Data") Equals TableBData("Time")
    Select .......
</code></pre>

