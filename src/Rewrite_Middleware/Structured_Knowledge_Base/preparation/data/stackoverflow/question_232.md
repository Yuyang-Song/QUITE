# Windows Azure SQL database. Sharding Complete Tables to limit DB Size
[Link to question](https://stackoverflow.com/questions/17322942/windows-azure-sql-database-sharding-complete-tables-to-limit-db-size)
**Creation Date:** 1372256929
**Score:** 0
**Tags:** azure-sql-database, sharding
## Question Body
<p>I am moving my web app from on-premise to windows azure. In my app, I have two DBs which are setup on same SQL Server and so I can query one database from the other easily using fully qualified name in my query. Now moving to cloud, I am facing limitation where I can't query tables in One DB from another DB. I can't change my queries because it requires a complete change in web app. I was thinking to merge these DBs into one to save the web app rewrite. But my DBs are huge(40 GB each) and have heavy load(millions of hits per day). 
Now my question is, </p>

<ul>
<li>Windows Azure SQL database is good enough to handle this number of
hits and huge DBs?</li>
<li>Is it a good idea to merge two huge DBs into one? Here I was thinking
to shard all tables in the second db so that all the data will be
saved in second instance.</li>
<li>What else I can do?</li>
</ul>

<p>Sorry If problem is vague and unclear. </p>

## Answers
### Answer ID: 17333240
<p>You also have the option of not using SQLAzure and use the new Azure IAAS where you can spin up a SQL Server instance that is closer to more traditional SQL Server. You can also control the instance size more easily this way. Here is some info <a href="http://blogs.msdn.com/b/windowsazure/archive/2013/04/24/sql-server-in-windows-azure-infrastructure-services-updated-documentation-and-best-practices-for-ga-upcoming-blogs.aspx" rel="nofollow">http://blogs.msdn.com/b/windowsazure/archive/2013/04/24/sql-server-in-windows-azure-infrastructure-services-updated-documentation-and-best-practices-for-ga-upcoming-blogs.aspx</a></p>

