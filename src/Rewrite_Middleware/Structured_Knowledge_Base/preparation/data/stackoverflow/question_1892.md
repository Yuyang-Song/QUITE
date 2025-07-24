# What database strategy to choose for a large web application
[Link to question](https://stackoverflow.com/questions/11277530/what-database-strategy-to-choose-for-a-large-web-application)
**Creation Date:** 1341089051
**Score:** 0
**Tags:** sql, database, architecture, hadoop, redis
## Question Body
<p>I have to rewrite a large database application, running on 32 servers. The hardware is up to date, each machine has two quad core Xeon and 32 GByte RAM.</p>

<p>The database is multi-tenant, each customer has his own file, around 5 to 10 GByte each. I run around 50 databases on this hardware. The app is open to the web, so I have no control
on the load. There are no really complex queries, so SQL is not required if there is a better solution. </p>

<p>The databases get updated via FTP every day at midnight. The database is read-only. 
C# is my favourite language and I want to use ASP.NET MVC. </p>

<p>I thought about the following options:</p>

<ul>
<li><p>Use two big SQL servers running SQL Server 2012 to serve the 32 servers with data. On the 32 servers running IIS hosting providing REST services.</p></li>
<li><p>Denormalize the database and use Redis on each webserver. Use booksleeve as a Redis client.</p></li>
<li><p>Use a combination of SQL Server and Redis </p></li>
<li><p>Use SQL Server 2012 together with Hadoop</p></li>
<li><p>Use Hadoop without SQL Server</p></li>
</ul>

<p>What is the best way for a read-only database, to get the best performance without loosing maintainability? Does Map-Reduce make sense at all in such a scenario? </p>

<p>The reason for the rewrite is, the old app written in C++ with ISAM technology is too slow, the interfaces are old fashioned and not nice to use from an website, especially when using ajax.</p>

<p>The app uses a relational datamodel with many tables, but it is possible to write one accerlerator table where all queries can be performed on, and all other information from the other tables are possible by a simple key lookup.</p>

## Answers
### Answer ID: 11278520
<p>This question is almost an opinion piece.  I'd personally prefer an Oracle RAC with TimesTen for caching if performance is of the utmost importance, and if volume of concurrent reads is high during the day.</p>

<p>There's a white paper here...</p>

<p><a href="http://www.oracle.com/us/products/middleware/timesten-in-memory-db-504865.pdf" rel="nofollow">http://www.oracle.com/us/products/middleware/timesten-in-memory-db-504865.pdf</a></p>

<p>The specs of the disk subsystem and organization of indexes and data files across physical disks is probably the most important factor though.  </p>

### Answer ID: 11277719
<p>Few questions.  What problems have come up that you're rewriting this?  What do the query patterns look like?  It sounds like you would be most comfortable with a SQLServer + caching (memcached) to address whatever issues that are causing you to rewrite this.  Redis is good, but you won't need the data structure features with the db handling queries, and you don't need persistance if it's only being used as a cache.  Without knowing more about the problem, I guess I'd look at MongoDB to handle data sharding, redundant storage, and caching all in one solution.  There are no special machines in this setup, redundancy can be configured, and the load should balance well. </p>

