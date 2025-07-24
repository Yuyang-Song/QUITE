# Occasional failure of sub-query on SQL Server using ADO - properties not supported
[Link to question](https://stackoverflow.com/questions/20265777/occasional-failure-of-sub-query-on-sql-server-using-ado-properties-not-support)
**Creation Date:** 1385640419
**Score:** 1
**Tags:** sql-server, delphi, ado
## Question Body
<p>I have a Delphi program (D2010) that accesses a local SQL Server 2005 Express database using the ADO components (TADOConnection and TADOQuery). At program startup I use a correlated sub-query to identify the maximum of a specific field for a range of values. This works well in all our testing.</p>

<p>However, on some customer systems we have seen that if our program is shutdown and restarted immediately, the program fails when running this subquery with an EOleException 'The requested properties cannot be supported'. Subsequent restarts of the program repeat this error, until the PC is rebooted. In this state, all other database access in the program seems OK; this is the only use of a correlated sub-query in the program.</p>

<p>The correlated sub-query is:</p>

<pre><code>SELECT p1.*
FROM Packs p1
WHERE p1.MachID = :MachID
AND p1.BuildID &lt;= :MaxPosID
AND p1.PackID = 
(
SELECT MAX(p2.PackID)
FROM packs p2
WHERE p2.BuildID = p1.BuildID
and p2.MachID = p1.MachID
)
ORDER BY BuildID
</code></pre>

<p>The MachID and MaxPosID fields do not change on an individual system, so the query is the same in any run of the program. The only difference with the customer systems is that they may be running with larger databases (typ. 1GB).</p>

<p>I have added some code to iterate over the database connection properties, and seen that on our working systems the 'Subquery Support' property has a value of 31H, which according to<br>
<a href="http://msdn.microsoft.com/en-us/library/office/aa140022%28v=office.10%29.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/office/aa140022(v=office.10).aspx</a> means that correlated subqueries are supported. </p>

<p>I assume that when the problem occurs on customer sites the property does not have the same value set for some reason. </p>

<p>One workaround was to open a command prompt, and use sqlcmd to just 'USE (our database name)'. If this command prompt is left open, then our program starts normally. I have no idea how this would affect the running of our program, or the value of the properties returned by the connection object.</p>

<p>Any ideas about why the supported properties change, or why program shutdown/startup should see this change?</p>

<p>I can rewrite the code to replace the use of the correlated subquery with a slower search through the table until I find all the required values, and this would probably not be affected by the problem, but I would like to understand what is happening.</p>

<p>Edit: the connection string is:</p>

<pre><code>Provider=SQLNCLI.1;Integrated Security=SSPI;Persist Security Info=False;Initial Catalog=TQSquality
</code></pre>

<p>The connection string is modified at runtime to add 'OLE DB Services = -2', to switch off connection pooling. </p>

<p>The query is executed by:</p>

<pre><code>SetCnx(LastPackIDQry, CnxQuality);
LastPackIDQry.Parameters[0].Value := GetMachNo;
LastPackIDQry.Parameters[1].Value := TQS.PosRange.Last;
QryOpen(LastPackIDQry);
try
  while not Eof do
  begin
</code></pre>

<p>...process the data</p>

<p>QryOpen is a utility that just calls .Open on the input query, but provides some logging on errors. As I mentioned, the two parameters are fixed for a specific machine, so I cannot believe the problem is with the query; has to be something to do with the connection or the database.</p>

<p>TIA Ian</p>

