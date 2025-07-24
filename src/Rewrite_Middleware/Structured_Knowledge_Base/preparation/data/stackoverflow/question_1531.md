# SQL Server Query Performance, Large where statements vs. queries
[Link to question](https://stackoverflow.com/questions/870809/sql-server-query-performance-large-where-statements-vs-queries)
**Creation Date:** 1242420567
**Score:** 1
**Tags:** sql, sql-server
## Question Body
<p>I am wondering which is a more efficent method to retrieve data from the database. </p>

<p>ex.
One particular part of my application can have well over 100 objects. Right now I have it setup to query the database twice for each object. This part of the application periodically refreshes itself, say every 2 minutes, and this application will probably end of being installed on 25-30 pc's. I am thinking that this is a large number of select statements to make from the database, and I am thinking about trying to optimize the procedure. I have to pull the information out of several tables, and both queries are using join statements.</p>

<p>Would it be better to rewrite the queries so that I am only executing the queries twice per update instead of 200 times? For example using a large where statement to include each object, and then do the processing of the data outside of the object, rather than inside each object?</p>

<p>Using SQL Server, .net No indexes on the tables, size of database is less than 10-5th</p>

## Answers
### Answer ID: 870843
<p>The default answer for optimization must always be: don't optimize until you have a demonstrated need for it.  The followup is: once you have a demonstrated need for it, and an alternative approach: try both ways to determine which is faster.  You can't predict which will be faster, and we certainly can't.  KM's answer is good - fewer queries tends to be better - but the way to <em>know</em> is to test.</p>

### Answer ID: 870827
<p>all things being equal, many statements with few rows is usually worse than few statements with many rows.</p>

<p>show the actual code and get better answers.</p>

