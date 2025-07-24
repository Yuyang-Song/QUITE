# ADODB Command Parameters Refresh doesn&#39;t retrieve parameters
[Link to question](https://stackoverflow.com/questions/41574385/adodb-command-parameters-refresh-doesnt-retrieve-parameters)
**Creation Date:** 1484068088
**Score:** 0
**Tags:** sql-server, sql-server-2008, iis, vbscript, adodb
## Question Body
<p>I have an old web application, built with VBScript on an IIS6 Server with a SQL Server 2008 database. It is in the processed of being moved to a new server, on IIS8.</p>

<p>Every queries in the app work with stored procedures, with which we never had a problem. But on the new server, it doesn't seem to work. I found it it's because the <code>Command.Parameters.Refresh</code> doesn't return the parameters properly.</p>

<p>Consider this code:</p>

<pre class="lang-vb prettyprint-override"><code>Set cmd = Server.CreateObject("ADODB.Command")
cmd.ActiveConnection = conn
cmd.CommandType = 4
cmd.CommandText = v_strSpName
cmd.CommandTimeout = 0
cmd.Parameters.Refresh

For i = LBound(v_arrParameters) To UBound(v_arrParameters)
    If m_bReplaceEmptyToNull Then
        v_arrParameters(i)(1) = ReplaceEmpty(v_arrParameters(i)(1))
    End If

    cmd.Parameters(v_arrParameters(i)(0)).value = v_arrParameters(i)(1)
Next
</code></pre>

<p>Everything in <code>v_arrParameters</code> exists, but I tried iterating in Parameters.name after the refresh, the parameters are not returned (but they are on the production server).</p>

<p>Also worth noting, the SQL Profiler does receive the query and return the parameters:</p>

<pre class="lang-none prettyprint-override"><code>exec [Database]..sp_procedure_params_rowset N'get_company',1,N'dbo',NULL
</code></pre>

<p>According to <a href="https://support.microsoft.com/en-us/kb/174223" rel="nofollow noreferrer">this page</a>, it is a known issue, I just want to make sure it doesn't come from this problem, and find a solution or an alternative that doesn't imply a full rewriting of the application.</p>

<p>Also, no I can not update the SQL Server version, switch to VB.NET, there is always the issue that there is a client that won't pay for this problem.</p>

## Answers
### Answer ID: 41622264
<p>So we managed to make it work this way:</p>

<ul>
<li>Opening the Applications Pools section in IIS Manager.</li>
<li>Going in the Advanced Settings of the Default App Pool (its name here, maybe not for everyone, I don't know)</li>
<li>Setting <code>Enable 32-bits apps</code> to <code>True</code></li>
</ul>

<p>This is on a 64-bit Windows Server 2012 R2, with Microsoft SQL Server 2008 (SP4) - 10.0.6241.0 (X64) .</p>

