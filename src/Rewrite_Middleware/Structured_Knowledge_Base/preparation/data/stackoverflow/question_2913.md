# Is it possible to put vba code behind BarTender Design and have it run a delete query in access
[Link to question](https://stackoverflow.com/questions/58305476/is-it-possible-to-put-vba-code-behind-bartender-design-and-have-it-run-a-delete)
**Creation Date:** 1570628260
**Score:** 0
**Tags:** ms-access, vbscript, bartender
## Question Body
<pre><code>  1.Public sub test()
  2.dim cn, rs, cmd
  3.Set cn = createobject("ADODB.Connection")
  4.Set rs = createobject("ADODB.Recordset")
  5.Set cmd = createobject("ADODB.Command")
  6.connectionString = "Provider=Microsoft.ACE.OLEDB.12.0;
DataSource=C:\Users\text\Documents\PrintCenterForm\PrintCernter_v1.accdb;"
  7.cn.Open connectionString
  8.cmd.ActiveConnection = cn
  9.cmd.Execute
  10.End sub
</code></pre>

<p>Sorry Guys, I posted a picture of my code and error yesterday but for some odd reason they deleted it?</p>

<p>But anyways I am getting an error On Line 8 Stating:"Command text was not set for the command object."</p>

<p>I have also tried rewriting this code as it is doing no good just sitting here waiting for a response but I have also tried this way too but cannot seem to get this to work</p>

<pre><code> 1.Set accessApp = GetObject("C:\Users\texthere\Documents\PrintCenterForm\PrintCernter_v1.accdb")
 3.Set accessApp = createObject("Access.Applicaiton")
 4.accessApp.visible = true
 5.accessApp.UserControl = true 
 6.accessApp.OpenCurrentDataBase
("C:\Users\texthere\Documents\PrintCenterForm\PrintCernter_v 
 1.accdb"),false
 7.accessApp.Run "Qry_DeletePrinted"
 8.End Sub
</code></pre>

<p>I am getting a error on line 1 on the bottom code stating: "ActiveX component can't create object: 'Access.Application' I am more than likely not going to use this code unless you guys see that it would be easier to work with? I also, changed the OnPrintJobStart to OnNewRecord to see if this approach work but first I need to come through the coding issue.</p>

<p>My end result I would just like some code that will kick off a delete query in Access to delete records whenever they are printed from Bartender.</p>

<p>I have a delete query already in Access call "Qry_DeletePrinted".</p>

<p>This database is located on my C:Drive DataSource=C:\Users\text\Documents\PrintCenterForm\PrintCernter_v1.accdb</p>

<p>Just to clarify, I am using MS Access 2013</p>

<p>As you both can see I am nowhere near familiar to VB Script    </p>

## Answers
### Answer ID: 58557629
<p>BELOW IS WHAT THESE GUYS HELPED ME ACCOMPLISH AND IT WORKS LIKE A CHARM!</p>

<pre><code> Dim cn, rs, cmd
   set cn = CreateObject("ADODB.Connection")
   set rs = CreateObject("ADODB.Recordset")
   set cmd = CreateObject("ADODB.Command")
   ConnectionString = "Provider=Microsoft.ACE.OLEDB.12.0;Data 
   Source=\\NetworkDriveName\PrintCernter_v1.accdb;"
   cn.Open ConnectionString 
   sql = "Qry_DeletePrinted" 
   '+ Format.NamedSubStrings("Printed_User").Value
   cmd.ActiveConnection = cn
   cmd.CommandText = sql
   cmd.execute
   cn.close
</code></pre>

### Answer ID: 58318011
<p>Yes you can, there is a <strong>VBScript Type of Data Source</strong> in <strong>Bartender Software</strong>.
Create a new VBScript Data Source and set the Script Type as Event Control Scripts.</p>

<p><a href="https://i.sstatic.net/cbkAq.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/cbkAq.png" alt="Bartender VBScript Data Source"></a></p>

<p>Inside the <code>Edit with Script Assistant..</code> choose the <code>OnPrintStart</code> and inject your VBScript connection and delete statement code. It will run everytime a label is started to print.</p>

<p><a href="https://i.sstatic.net/AAK4W.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/AAK4W.png" alt="Bartender Script Assistant"></a></p>

<p><strong>First, you need to open your Access Database through Bartender in VBScript:</strong>
Source: <a href="https://www.connectionstrings.com/access-2013/" rel="nofollow noreferrer">Access 2013 Connection String</a></p>

<pre><code>Dim cn, rs, cmd
set cn = CreateObject("ADODB.Connection")
set rs = CreateObject("ADODB.Recordset")
set cmd = CreateObject("ADODB.Command")

connectionScring = "Provider=Microsoft.ACE.OLEDB.12.0;
    Data Source=C:\Users\text\Documents\PrintCenterForm\PrintCernter_v1.accdb;"
cn.Open connectionScring 
</code></pre>

<p><strong>Second, you can prepare your SQL statement:</strong> </p>

<p><em>Note: <code>Value</code> in this script means the Value assigned to this VBScript Data Source</em></p>

<p>You can choose to get other dataSource value by caling this: <code>Format.NamedSubStrings("OtherDataSource").Value</code></p>

<pre><code>sql = "delete from yourTable where key = '" &amp; Value &amp; "'"
cmd.ActiveConnection = cn
cmd.CommandText = sql
cmd.execute
cn.Close    
</code></pre>

### Answer ID: 58407468
<p>While I don't have a lot of experience with VBscript. I did create something to delete records from a firebird Databse some time ago. It looks to me you don't give a correct command to execute the query / procedure. Below the coding I used with a procedure and which works.</p>

<pre><code>Const Connection = "DRIVER=Firebird/InterBase(r) driver;UID=SYSDBA;PWD=masterkey;DBNAME=C:\DB\Database.FDB;" 
SQL = "execute procedure NameOfProcedure " + Format.NamedSubStrings("TELLER").Value
Set dbconn = CreateObject("ADODB.Connection")
dbconn.Open connection
dbconn.Execute(SQL)
dbconn.Close
</code></pre>

<p>the important part is the "SQL". the procedure has the code to remove the printed line from the database and BarTender just calls the procedure. Of course we need to tell it which line it needs to delete. I use a named datascource for this "Teller". This is linked with the database field ID.</p>

