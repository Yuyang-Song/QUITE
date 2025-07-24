# Join two different types of databases together
[Link to question](https://stackoverflow.com/questions/8116353/join-two-different-types-of-databases-together)
**Creation Date:** 1321234243
**Score:** 0
**Tags:** sql-server, vb.net, ms-access
## Question Body
<p>I have two databases, one MSSQL and the other in Access.</p>

<p>Right now, inside the access file, the mssql tables are set up as linked tables so queries can be written using tables from both databases. (e.g. <code>"select * db1.table1 where db1.table1.somevalue not in db2.table1"</code>, or select into tables like that one)</p>

<p>These queries need to be moved into a VB.NET project, but still be linked to the access file.</p>

<p>I think what I am needing is a Database object that can have tables from 2 different connections, (ie the SqlClient and OleDb connections)</p>

<p>Is this possible? If so, how? Or do I need to rewrite the queries using loops or something?</p>

## Answers
### Answer ID: 8117081
<p>I'm pretty sure you can just connect to the Access database. All the internal objects--including the links to SQL Server tables--should be accessible to your vb.net project.</p>

### Answer ID: 8117058
<p>THere is no reason you can't create an MS Access .mdb with Links to your MS Access Database and your SQL Server database</p>

<p>Access Db #1 Contains Access Tables and Data.</p>

<p>SQL Db Contains your MS SQL Tables. </p>

<p>Access Db #2 contains links to the tables in Access DB #1 as well as links to the tables in your SQL Server Db. This .mdb files ALSO contains your query defs required by your vb.net project. </p>

### Answer ID: 8116419
<p>What I would do is query your access database to get some result set and that pass that result set as a parameter to a stored procedure in your MS SQL database.  You would just have to transform your results from access into XML to be passed as a xml variable as a parameter.  And then in your stored procedure you can convert the XML to be a table variable and you can use it just like a regular table.</p>

