# Error: input query is too long
[Link to question](https://stackoverflow.com/questions/37890081/error-input-query-is-too-long)
**Creation Date:** 1466196054
**Score:** 0
**Tags:** sql, powershell
## Question Body
<p>I have converted an HTML table from <a href="https://support.microsoft.com/en-us/lifecycle?c2=1044&amp;wa=wsignin1.0" rel="nofollow">this site</a> to an XML file.</p>

<p>I am trying to run a SQL query in PowerShell to copy the data from from the XML file to a database table.  If I run the query within SSMS, it runs fine.  However when I try to run the following code in Powershell, I get:</p>

<blockquote>
  <p>Error: input query is too long</p>
</blockquote>

<pre><code>[string] $dbCommand =
@"
Truncate table DB_NAME.dbo.SQL_LIFE_CYCLE_UPLOAD_IC

DECLARE @Data XML
SELECT  @Data = BulkColumn
FROM    OPENROWSET(BULK 'D:\Powershell\Temp\SQL_Life_Cycle.XML', SINGLE_BLOB) AS x  
INSERT INTO DB_NAME.dbo.SQL_LIFE_CYCLE_UPLOAD_IC
(PRODUCT_RELEASED,LIFECYCLE_START_DATE,MAINSTREAM_SUPPORT_END_DATE,EXTENDED_SUPPORT_END_DATE,SERVICE_PACK__SUPPORT_END_DATE,NOTES)
 Select max(case when col=1 then value else '' end) as PRODUCT_RELEASED,
        max(case when col=2 then value else '' end) as LIFECYCLE_START_DATE,
        max(case when col=3 then value else '' end) as MAINSTREAM_SUPPORT_END_DATE,
        max(case when col=4 then value else '' end) as EXTENDED_SUPPORT_END_DATE,
        max(case when col=5 then value else '' end) as SERVICE_PACK__SUPPORT_END_DATE,
        max(case when col=6 then value else '' end) as NOTES
  from      
  (SELECT
         x.y.value('Col[1]', 'int') AS [Col],
         x.y.value('Row[1]', 'int') AS [Row],
         x.y.value('Value[1]', 'VARCHAR(200)') AS [Value]
         FROM @data .nodes('//DocumentElement/TableData') AS x ( y )
 ) rawTableData
 group by row
 having row &gt;0
 order by row
"@

OSQL.EXE -E -Q $dbCommand
</code></pre>

<p>Any suggestions on how to rewrite this script where it will work?</p>

## Answers
### Answer ID: 37890289
<p>I am assuming it is too long because you are using <code>OSQL.exe</code> and passing it as a <code>command line parameter</code>. Seeing you are using <code>powershell</code> I would just use built in .net capabilities and execute the query in that manner.  If you need more info just search the internet for <code>.net SQL</code> <code>ExecuteNonQuery</code> and it will give you a lot of results.</p>

<p>The basics of it are as follows:</p>

<pre><code># Instantiate new SqlConnection object. 
$Connection = New-Object System.Data.SQLClient.SQLConnection 

# Set the SqlConnection object's connection string to the passed value. 
$Connection.ConnectionString = "place a connection string here"

# Open the connection to the database. 
$Connection.Open() 

# Instantiate a SqlCommand object. 
$Command = New-Object System.Data.SQLClient.SQLCommand 

# Set the SqlCommand's connection to the SqlConnection object above. 
$Command.Connection = $Connection 

# Set the SqlCommand's command text to the query value passed in. 
# this is where you pass the query string you wrote to
$Command.CommandText = $dbCommand

# Execute the command against the database without returning results (NonQuery). 
$Command.ExecuteNonQuery() 

# Close the currently open connection. 
$Connection.Close() 
</code></pre>

<p>I have written this code a few times but I did just grab it from this script which is available on Microsoft's Technet gallery <a href="https://gallery.technet.microsoft.com/scriptcenter/Perform-ExecuteNonQuery-a05eb40a" rel="nofollow">https://gallery.technet.microsoft.com/scriptcenter/Perform-ExecuteNonQuery-a05eb40a</a></p>

