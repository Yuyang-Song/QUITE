# SQL Server 2012 Database Slowness
[Link to question](https://stackoverflow.com/questions/49559924/sql-server-2012-database-slowness)
**Creation Date:** 1522337423
**Score:** 0
**Tags:** sql, sql-server-2012, subquery
## Question Body
<p>So we have a system that uses two columns as the unique ID the userid as well as the a date. We have to keep every record that has ever been associated with a particular subject so there are no deleted records. So one subject can have 50 records. The database designer created views to get the latest row for a subject. Database is really not that huge in terms of record count we are roughly at 750000 records.</p>

<p>The view is written for every table very similar to:</p>

<pre><code>Select Username, 
UserID 
From users 
where USerID = 000 
and UserUpdatedDate = (
    Select MAX(UserUpdatedDate) 
    FROM 
    users a 
    WHERE a.USerID = UserID 
)
</code></pre>

<p>We are seeing a major slowness, any suggestions would be welcomed?</p>

<p>We are rewriting some queries using temp tables, it seems to be quicker. Is this a good thing or bad in long haul</p>

## Answers
### Answer ID: 49559945
<p>Replace this subquery 
<code>(Select MAX(UserUpdatedDate) FROM users a WHERE a.USerID = UserID )</code> with a join - subqueries are slow</p>

