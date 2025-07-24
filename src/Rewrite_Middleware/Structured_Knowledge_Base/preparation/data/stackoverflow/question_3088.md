# Using a recordset without blocking resources
[Link to question](https://stackoverflow.com/questions/66105754/using-a-recordset-without-blocking-resources)
**Creation Date:** 1612802727
**Score:** 0
**Tags:** sql-server, vbscript, asp-classic, ado, recordset
## Question Body
<p>I am dealing with some performance issues on an older codebase here.
The issues appear in the Sql Server. Either the queries time out or  <code>The request limit for the database is 2000 and has been reached</code>. This error message occurs earlier than I think it should when doing load testing.</p>
<p>The code is executing vbscript database queries by using this code</p>
<pre><code>  Dim cmd, i, rsx
  Set cmd = Server.CreateObject(&quot;ADODB.Command&quot;)
  cmd.CommandText = querytext
  ' 1 -&gt; adCmdText
  cmd.CommandType = 1
  For i = 0 To UBound(parameters)
    cmd.Parameters.Append(create_variant_input_parameter(cmd, &quot;&quot;, parameters(i)))    
  Next
  Set cmd.ActiveConnection = connection 
  Set rsx = cmd.Execute()
</code></pre>
<p>and then using it like this</p>
<pre><code>do while not rsx.eof
    Test = Test &amp; rsx(&quot;Test&quot;) &amp; &quot;,&quot;
rs.movenext : loop
rs.close : set rs = nothing
</code></pre>
<p>I read that the recordset object maintains a connection to the server, is this blocking database workers unnecessarily while looping through the recordset? These loops are also nested a lot of times, so this here is a very simple example.</p>
<p>If yes, how could I just save the result in a recordset that does not maintain the connection without having to rewrite the entire codebase?</p>

## Answers
### Answer ID: 66111453
<p>Try using a &quot;firehose cursor&quot; with ADODB.Recordset.</p>
<p>Here's how to build one in VBA:</p>
<pre><code>Dim rs As ADODB.Recordset
Set rs = New ADODB.Recordset

With rs
    .CursorLocation = adUseServer
    .CursorType = adOpenForwardOnly
    .LockType = adLockReadOnly
End With
</code></pre>
<p>These are server-side, forward-only, read-only cursors that push data directly from the server to the client recordset that you can then loop. Fetch the data and then be sure to close the recordset to free the resources on the server.</p>
<p>It's worth noting that you can also play with the recordset's <code>CacheSize</code> to modify performance.</p>
<p>You can adapt this example to your VBScript requirement.</p>

