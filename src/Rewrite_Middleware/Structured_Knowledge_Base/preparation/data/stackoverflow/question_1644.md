# Problems when importing from Access database to Sql Server through Access queries
[Link to question](https://stackoverflow.com/questions/2480229/problems-when-importing-from-access-database-to-sql-server-through-access-querie)
**Creation Date:** 1269028857
**Score:** 2
**Tags:** sql, sql-server-2005, ms-access, import
## Question Body
<p>I have an Access database (in Access 2003) with several tables, and data must be imported to Sql Server 2005. Access data does not have the same structure as sql server database, so I created various queries which transforms it to format needed by Sql Server. Basically for each table in sql server I have two queries: a Select query which generates the fieldnames and types compatible with sql table, and an Append query which basically does</p>

<pre><code>Insert into [Sql_table] (field1, field2, ...)
Select [field1, field2, ...] from [Access_table]
</code></pre>

<p>Both Sql and original access tables have primary key Autoinc, and I include it in the query.</p>

<p>When I run the insert query and the source select query have not very many records (up to few hundreds) all works ok, the records are inserted ok, with the original identity</p>

<p>But when the source query have more records (I have few tables with over 10000 records), I have two situations:</p>

<ol>
<li><p>either Access reports the query cannot add any records to sql server due to primary key violation (but there is no violation at all). In this case I simply close access and restart it ... and I get to second situation</p></li>
<li><p>running the query Access tells me it cannot import x records (usually few, 10, 21, 32, usually seems random number up to 100 out of 10000+) due to primary key violation, but imports the rest. Again, there's no key violation anyway, all ID's are unique, as generated in original Access table by autoinc field. The strange thing is , if I delete sql data and run query again, I get different number of records not imported, sometimes few, sometimes more, but all in range of 10-50 out of 10000</p></li>
</ol>

<p>I tried with Access 2007 too, but the same thing happens.</p>

<p>The Sql server table has foreign key relation to a master table, but this relation is also satisfied by data I try to import.</p>

<p>Does anyone knows faced this problem and know for a solution?</p>

<p>Thanks</p>

<p>PS: I don't use sql server import wizard since there will be way to much work to convert access data through sql server - the access select queries are already made, they are quite complex, use some functions written in VBA, which would be difficult to rewrite to tsql just for this only purpose</p>

## Answers
### Answer ID: 2480311
<p>Is this a one time deal? If so, why not just use Access and export the tables and data to SQL server and then go in and clean up?  That's the way I've done it in the past</p>

<p><a href="http://office.microsoft.com/en-us/access/CH101759711033.aspx" rel="nofollow noreferrer">some info</a></p>

### Answer ID: 2480271
<p>I've run across things like this many time. Access's error messages are often misleading. I don't have a direct answer for you, but here's what I would do ..</p>

<p>Create an empty table matching the structure of the destination sql server table in sql server, but don't put any constraints on it.</p>

<p>Then copy the access data into that table instead.</p>

<p>Now use management studio (or your whatever sql interface you use) and do an insert from the fake table into the real one. If it works, then I'm not sure what to tell you. If it doesn't work, your management studio should give you a much better error message so you can figure out what's up.</p>

<p>-Don</p>

