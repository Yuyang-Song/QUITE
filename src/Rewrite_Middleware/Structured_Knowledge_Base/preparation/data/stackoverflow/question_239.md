# Any idea why I am getting &#39;arguments are of the wrong type&#39; error when trying to insert to db with parameterized query?
[Link to question](https://stackoverflow.com/questions/17600148/any-idea-why-i-am-getting-arguments-are-of-the-wrong-type-error-when-trying-to)
**Creation Date:** 1373565076
**Score:** 1
**Tags:** sql, asp-classic, vbscript, parameterized-query
## Question Body
<p>I am attempting to insert some form data into an SQL database with parameterized queries in vbscript in classic asp (I have no experience with asp). I have tried several variations for declaring my parameters but everything is throwing an error. </p>

<pre><code>ADODB.Command error '800a0bb9'

Arguments are of the wrong type, are out of acceptable range, or are in conflict with one another
</code></pre>

<p>The table in my database won't allow a null for the ApplicationId field and is type int. The TimeStamp column is datetime. All the other fields are varchar(MAX)</p>

<p>Here is the more recent variation of my code please let me know if you can spot any errors etc</p>

<pre><code>Set conn = Server.CreateObject("ADODB.Connection")
conn.Mode = 3
conn.open "Provider=SQLOLEDB;Data Source=xxx.xxx.xxx.xxx,xxxx;database=db_example;uid=user;pwd=password;"

Dim oCmd 
set oCmd = Server.CreateObject("ADODB.Command")

Dim sSQL 
sSQL = "INSERT INTO tbl_Application (ApplicationNumber, Expenses, Name, Why) VALUES (?, ?, ?, ?);"

oCmd.CommandText = sSQL
oCmd.ActiveConnection= conn

Dim param1
Set param1 = oCmd.CreateParameter("ApplicationNumber",adInteger,adParamInput)     
param1.value = session.sessionId
oCmd.Parameters.Append param1
</code></pre>

<p>have tried assigning the value both before and after the Append</p>

<pre><code>Dim param2
Set param2 = oCmd.CreateParameter("Expenses",adChar,adParamInput,255) 
param2.value = session("Expenses")
oCmd.Parameters.Append param2

Dim param3
Set param3 = oCmd.CreateParameter("Name",adChar,adParamInput,255) 
param3.value = session("Name")
oCmd.Parameters.Append param3


Dim param4
Set param4 = oCmd.CreateParameter("Why",adChar,adParamInput,255) 
param4.value = session("Why")
oCmd.Parameters.Append param4

Dim oRS
Set oRS = oCmd.Execute()
</code></pre>

<p>also, the site was hacked so that is why I am rewriting the code with parameterized queries. Here is the original code which worked (but allowed for injection) in case I need to use the recordset or something</p>

<pre><code>Set conn = Server.CreateObject("ADODB.Connection")
conn.Mode = 3
conn.open "Provider=SQLOLEDB;Data Source=xxx.xxx.xxx.xxx,xxxx;database=db_example;uid=user;pwd=password;"

set rsAddEvent = server.createobject("adodb.recordset")
rsAddEvent.open "tbl_Application", conn, 2, 3
rsAddEvent.addnew

rsAddEvent("ApplicationNumber") = session.sessionId
rsAddEvent("TimeStamp") = now()
rsAddEvent("Applicant") = session("Applicant")
rsAddEvent("Email") = session("Email")
rsAddEvent("Pet") = session("Pet")
rsAddEvent("Address") = session("Address")
rsAddEvent("Postal") = session("Postal")
rsAddEvent("HomePhone")  = session("HomePhone")
rsAddEvent("WorkPhone") = session("WorkPhone")
rsAddEvent("Employed") = session("Employed")
rsAddEvent("Employer") = session("Employer")
rsAddEvent("Unemployment") = session("Unemployment")
rsAddEvent("FormerEmployer") = session("FormerEmployer")
rsAddEvent("Dependants") = session("Dependants")
rsAddEvent("Income") = session("Income")
rsAddEvent("OtherIncome") = session("OtherIncome")
rsAddEvent("Funds") = session("Funds")
rsAddEvent("Circumstance") = session("Circumstance")
rsAddEvent("Afford")  = session("Afford")
rsAddEvent("Spent") = session("Spent")
rsAddEvent("Expenses") = session("Expenses") 
rsAddEvent("Name") = session("Name")
rsAddEvent("Email") = session("Email")
rsAddEvent("Why") = session("Why")

rsAddEvent.update
rsAddEvent.movelast
</code></pre>

<p>Thanks so much for reading through this</p>

## Answers
### Answer ID: 17600542
<p>I think you forgot to include <code>adovbs.inc</code>, and thus the ADO constants such as <code>adChar</code> arent recognized.</p>

<p>Try put this at the top of your ASP page:</p>

<pre><code>&lt;!--#include virtual="/adovbs.inc"--&gt;
</code></pre>

<p>If that doesn't work, see this here which explains how to set up the inc file:</p>

<p><a href="https://web.archive.org/web/20210513005432/https://www.4guysfromrolla.com/webtech/faq/Beginner/faq7.shtml" rel="nofollow">https://web.archive.org/web/20210513005432/https://www.4guysfromrolla.com/webtech/faq/Beginner/faq7.shtml</a></p>

