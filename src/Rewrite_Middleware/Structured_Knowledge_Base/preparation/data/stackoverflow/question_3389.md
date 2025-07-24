# OLEDBDataAdaptor.Fill method runs incredibly slowly
[Link to question](https://stackoverflow.com/questions/78274144/oledbdataadaptor-fill-method-runs-incredibly-slowly)
**Creation Date:** 1712236790
**Score:** 0
**Tags:** sql, vb.net, ms-access, query-optimization, oledb
## Question Body
<p>I have a complex SQL query that runs instantly in MS Access.</p>
<p>When I run the same query in VB.Net the <code>OLEDB.Fill</code> method hangs for up to 10 minutes. I eventually get back the same 1500 records returned in Access but it is too slow.</p>
<p>The query returns invoices that have an outstanding balance.</p>
<p>Lines on the invoices are stored in the <code>Entries</code> table that are joined to the <code>Journal</code> table, that is joined to the <code>Invoices</code> table. To work out whether an invoice has been paid or not we need to add all the invoice cost centre entries and the payment entries. The query text can also be modified for example to find invoices for any particular supplier, but this just changes the WHERE clause without affecting the SELECT.</p>
<p>The <code>Entries</code> table has around 370.000 rows, the <code>Journal</code> table around 150.000 and around 65.000. There are <code>indexes</code> on the tables for every field used in the join statements. I've already done multiple compact and repairs on the database. I need the whole datatable to display the results in a datagridview so a datareader would not work?</p>
<p>I am rewriting the software using C# instead of VB and using SQL server instead of Access, however that is going to take some time and I need a solution in the interim.</p>
<p>Here is the query:</p>
<pre><code>SELECT invoices.id,
       jobs.id AS [Job ID],
       jobs.datestart AS [Job Date],
       locations.locationname AS LOCATION,
       invoices.invoicedate,
       invoices.duedate,
       invoices.invoiceno,
       Clients.entityname AS Client,
       xinvoicetype.description AS TYPE,
       Payers.entityname AS Payer,
       Payees.entityname AS Payee,
       xinvoicestatus.description AS Status,
       Costs.[nett],
       Costs.tax AS GST,
       Costs.nett + Costs.tax AS Total,
       Iif(Isnull(Payments.paid), 0, Payments.paid) AS Paid,
       Costs.nett + Costs.tax - Iif(Isnull(Payments.paid), 0, Payments.paid) AS Balance,
       xdoctypes.description AS [Next Doc],
       invoices.nextdocdue
FROM ((((((((((invoices
               INNER JOIN entities AS Payers ON invoices.payerid = Payers.id)
              INNER JOIN entities AS Payees ON invoices.payeeid = Payees.id)
             INNER JOIN xinvoicetype ON invoices.invoicetype = xinvoicetype.id)
            INNER JOIN xinvoicestatus ON invoices.status = xinvoicestatus.id)
           INNER JOIN xdoctypes ON invoices.nextdoctype = xdoctypes.id)
          LEFT JOIN
            (SELECT invoiceid,
                    Sum(amount) AS Nett,
                    Sum(gst) AS Tax
             FROM entries
             INNER JOIN journal ON entries.journalid = journal.id
             WHERE entrytype &lt; 6 GROUP  BY invoiceid) AS Costs ON Costs.invoiceid = invoices.id)
         LEFT JOIN
           (SELECT invoiceid,
                   Sum(amount * -1) AS Paid
            FROM entries
            INNER JOIN journal ON entries.journalid = journal.id
            WHERE entrytype BETWEEN 7 AND 8 GROUP  BY invoiceid) AS Payments ON Payments.invoiceid = invoices.id)
        LEFT JOIN jobs ON invoices.jobid = jobs.id)
       LEFT JOIN entities AS Clients ON jobs.clientid = Clients.id)
      LEFT JOIN sessions ON jobs.sessionid = sessions.id)
LEFT JOIN locations ON sessions.locationid = locations.id
WHERE NOT(Costs.nett + Costs.tax - Iif(Isnull(Payments.paid), 0, Payments.paid) BETWEEN -0.011 AND .0099);
</code></pre>
<p>Here is the code:</p>
<pre><code>Using cnn = New OleDb.OleDbConnection(&quot;Provider=Microsoft.Jet.OLEDB.4.0;Data Source=&quot; &amp; gstrConnectionMain &amp; &quot;;Persist Security Info=False&quot;)
    Using dt As DataTable = New DataTable
        Using da As OleDb.OleDbDataAdapter = New OleDb.OleDbDataAdapter(strSQL, cnn)
            Dim unused = da.Fill(dt)
            grd.DataSource = dt
        End Using
    End Using
End Using
</code></pre>
<p>As mentioned, the query works instantly in Ms-Access but abysmally slowly in VB. Any pointers gratefully received.</p>

