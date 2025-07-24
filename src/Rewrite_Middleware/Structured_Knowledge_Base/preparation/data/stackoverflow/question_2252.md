# How to I stop a return parameter from a stored procedure from being truncated at 4000 characters
[Link to question](https://stackoverflow.com/questions/26044041/how-to-i-stop-a-return-parameter-from-a-stored-procedure-from-being-truncated-at)
**Creation Date:** 1411664053
**Score:** 1
**Tags:** ms-access, adodb
## Question Body
<p>The question asked here:-</p>

<p><a href="https://stackoverflow.com/questions/24408250/how-long-does-access-keep-unflushed-transactions-locally">How long does Access keep unflushed transactions locally?</a></p>

<p>is about problems with some invoice generation, which is still causing problems.  I am now trying to rewrite the same code to work entirely on the backend SQL Server databases using ADODB, specifically ADODB.Command and a some stored procedures.</p>

<p>One problem I am trying to resolve is that in the old system I created a local table (called <code>tmpUKRepeatInvoices</code>) in the client.  I am making a similar table on the server.  However the fields of this table are created from a join across two separate databases.</p>

<p>It is easier with my new system to populate the equivalent table on the server associated with the invoicing with a stored procedure and using a <code>FOR XML PATH('')</code> clause in that stored procedure return a comma separated list of customerIDs (the keys to the other database) using a query like so</p>

<pre><code>SELECT @Subs = (SELECT ''''+SubsID+''',' FROM InvoicingData WHERE SessionID = @SessionID FOR XML PATH(''),TYPE).value('.','NVARCHAR(MAX)')
SELECT @Customers = LEFT(@Subs,LEN(@Subs)-1)
</code></pre>

<p>@Customers is an output parameter for this stored procedure of type NVARCHAR(MAX) and will contain the text I will use in the next query</p>

<p>I can run the stored procedure in Sql Server Management studio and It returns a string of 42000 characters</p>

<p>The next query then will be like so. and can be used to populate the working table with the number of items against each customer.</p>

<pre><code>SQL = "SELECT COUNT(*) As NoItems, CustomerID FROM CustomerItems WHERE CustomerID IN(" &amp; Customers &amp; " )"
</code></pre>

<p>So I create the call in my Access VBA to run the stored procedure like so</p>

<pre><code>    Dim Customers As String
    With cmd
        Set .ActiveConnection = Conn
        .CommandType = adCmdStoredProc
        .CommandText = "CreateInvoicingData"
        .Parameters.Append .CreateParameter("@SessionID", adVarWChar, adParamInput, 25, TempVars!SessionID)
        .Parameters.Append .CreateParameter("@InvoiceDate", adDate, adParamInput, , Form_Company.InvoiceDate)
        .Parameters.Append .CreateParameter("@Currency", adVarWChar, adParamInput, 15, "Pounds")
        .Parameters.Append .CreateParameter("@Customers", adVarWChar, adParamOutput, 1000000000)
        .Execute
        Customers = .Parameters("@FleetCustomers").Value
    End With
</code></pre>

<p>The problem that I am having is that the Customers string is truncated to 4000 characters.  I tried setting the @Customers parameter to type adLongVarWChar instead but an error was thrown at the .Execute statement that said that "Data type Ox63  is a depreciated large object or LOB, but is marked as an Output parameter. Depreciated Large Objects are not supported as output parameters. Use Current Large Objects instead."</p>

<p>What type should I use for the @Customers Parameter so it won't get truncated or regarded as depreciated?. Note: I tried setting the size of this parameter to -1 but that just failed with an inconsistent parameter error message.</p>

