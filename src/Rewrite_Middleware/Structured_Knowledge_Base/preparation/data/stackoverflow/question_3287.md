# Using VB6 with ADO to access a MS SQLServer 2019 linked server
[Link to question](https://stackoverflow.com/questions/75195870/using-vb6-with-ado-to-access-a-ms-sqlserver-2019-linked-server)
**Creation Date:** 1674328006
**Score:** 1
**Tags:** sql-server, vb6, adodb, linked-server, sql-server-2019
## Question Body
<p>Note that both databases are MS SQL Server.</p>
<p>The SELECT works fine and the code doesn't break until it gets to <code>ADODB.Recordset.Update</code>. The SQL account has all of the necessary permissions. The table <code>[NASMSPAINT].[Ignition].[dbo].[booth_Styles]</code> is a linked server. The User account I am using has enough permissions because I am able to UPDATE the table using Python. This is on a secure isolated network so security is of very little concern, this just needs to work using VB6 with ADO. Long story short, this code is part of a large application still using VB6 and rewriting the code in Visual Studio is not an option.</p>
<p>Using <code>ADODB.Recordset.OPEN</code> using <code>adLockOptimistic</code> option, the following error occurs on the &quot;.Update&quot; line of the code:</p>
<blockquote>
<p>SQL server error message 16964 - for the optimistic cursor, timestamp columns are required if the update or delete targets are remote.</p>
</blockquote>
<p>Using <code>ADODB.Recordset.OPEN</code> using <code>adLockPessimistic</code> option, the following error occurs on the &quot;.Update&quot; line of the code:</p>
<blockquote>
<p>SQL Server Error Msg 16963 – You cannot specify scroll locking on a cursor that contains a remote table.</p>
</blockquote>
<p>I have found very little information on the internet concerning these errors. I have set the following server option properties on the linked server on the database:</p>
<pre>
Collation Compatible: TRUE
Data Access:TRUE
RPC:TRUE
RPC Out:TRUE
Use Remote Collation:FALSE
Collation Name:
Connection Timeout:0
Query Timeout:0
Distributor:FALSE
Publisher:FALSE
Subscriber:FALSE
Lazy Schema Validation:FALSE
Enable Promotion of Distributed Transaction:TRUE   
</pre>
<p>VB6 code:</p>
<pre class="lang-vb prettyprint-override"><code>sDBName = &quot;PROVIDER=SQLOLEDB.1;Data Source=192.168.2.70;User ID=xxxx;Password=xxxx;Persist Security Info=False&quot;

Dim Conn As ADODB.Connection
Dim rs As ADODB.Recordset

Set Conn = New ADODB.Connection
Conn.Open sDBName
Set rs = New ADODB.Recordset

With rs
    .Open &quot;SELECT * FROM [NASMSPAINT].[Ignition].[dbo].[booth_Styles] WHERE [Booth] = 'AdPro' ORDER BY  [StyleID]&quot;, Conn, adOpenDynamic, adLockOptimistic
    .MoveFirst
    nThisStyle = 1
    Do Until .EOF
        ![Plant_Number] = Style_Data(nThisStyle).PlantStyle
        ![Style_Number] = Style_Data(nThisStyle).FanucStyle
        ![Descript] = Style_Data(nThisStyle).StyleDesc
        ![Robots_Required] = Style_Data(nThisStyle).StyleRobotsReq
        .Update
        .MoveNext
        nThisStyle = nThisStyle + 1
    Loop
End With
</code></pre>
<p>The code breaks on the <code>.Update</code> line.</p>

