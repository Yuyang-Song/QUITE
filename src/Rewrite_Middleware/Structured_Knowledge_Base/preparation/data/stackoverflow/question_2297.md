# How does SQL Server handle the following query?
[Link to question](https://stackoverflow.com/questions/28151285/how-does-sql-server-handle-the-following-query)
**Creation Date:** 1422279983
**Score:** 2
**Tags:** sql, sql-server
## Question Body
<p>I have the following query I'd like to run on my database:</p>

<pre><code>SELECT 
    u.UserId, u.FullName, u.Location, csr.SponsorId
FROM 
    [User] u
LEFT JOIN 
    (SELECT 
         csr.SponsorId 
     FROM 
         ClubSponsorRelation csr 
     WHERE 
         csr.ClubId = @clubId) AS csr ON u.UserId = csr.SponsorId
WHERE 
    u.UserType = 'Sponsor'
    AND csr.SponsorId IS NULL
</code></pre>

<p>This is basically trying to run an excluding left join, all Users not in the ClubSponsorRelation table will be returned.</p>

<p>My question is in regards to the <code>WHERE u.UserType = 'Sponsor'</code> line. Will SQL Server take this into consideration before the Left Join, or after?</p>

<p>If it applies the <code>WHERE</code> after the Left Join, how can I rewrite this query that it will only apply the left join on Users with the UserType 'Sponsor'? IS a Left View even the most permanent way? The User and ClubSponsorRelation will become pretty big over time and the query is probably going to be run often.</p>

## Answers
### Answer ID: 28151580
<p>It is up to the DBMS how to execute your query. And as the order doesn't affect the results, you should not worry too much. Usually the optimizer will find the most efficient way. This can be one way or the other. Better just trust it to do a good job and only start to find workarounds when performance issues occur.</p>

<p>Your query already shows defensive thinking. You want to get users that are not sponsors for the given club. So why not use NOT IN or NOT EXISTS? This would be the straight-forward way (which would also be easier to read). The optimizer may decide to use an outer join internally, but why do you bother to think of such tricks before even getting into any issues with a normal query?</p>

<p>Having said this, I suggest to use NOT IN or NOT EXIST as long as they perform well.</p>

<pre><code>select userid, fullname, location
from [User]
where usertype = 'Sponsor'
and userid not in 
(
  select sponsorid 
  from clubsponsorrelation
  where clubid = @clubid
);
</code></pre>

<p>Or:</p>

<pre><code>select userid, fullname, location
from [User] u
where usertype = 'Sponsor'
and not exists
(
  select * 
  from clubsponsorrelation csr 
  where csr.clubid = @clubid 
  and csr.sponsorid = u.userid
);
</code></pre>

### Answer ID: 28151542
<p>Give this a try. Use <code>Not Exists</code> to find the users, since you want to find users who is not present in <code>ClubSponsorRelation</code> selecting <code>csr.SponsorId</code> doesn't make any sense to me.</p>

<pre><code>SELECT u.UserId,
       u.FullName,
       u.Location
FROM   [User] U
WHERE  NOT EXISTS (SELECT 1
                   FROM   ClubSponsorRelation csr
                   WHERE  u.UserId = csr.SponsorId
                   AND    csr.ClubId = @clubId)
       AND u.UserType = 'Sponsor' 
</code></pre>

### Answer ID: 28151440
<p>The other answers here have focused on query plans and I don't think that's what you're after. The WHERE clause will be applied to all of the rows created by the FROM clause, or after the JOIN in your words. If you want to apply your filter in the JOIN you can just add it as another condition;</p>

<pre><code>SELECT 
    u.UserId, 
    u.FullName, 
    u.Location, 
    csr.SponsorId
FROM 
    [User] u
        LEFT JOIN ClubSponsorRelation csr ON csr.SponsorId = u.UserId
                                         and csr.ClubId = @clubId
                                         and u.UserType = 'Sponsor'
WHERE 
    csr.SponsorId IS NULL
</code></pre>

### Answer ID: 28151321
<p>This is up to the execution engine. The easiest way to check is to let the server generate an execution plan for you - for example, in Management Studio, check <code>Include actual execution plan</code>. That will give you a good idea of how the query is actually going to be run, and why.</p>

<p>Note that the reasoning is quite complex, and in many cases might seem counter-intuitive - for example, if the statistics show that the query is going to touch most of the rows, it might ignore indices etc. If you want reasonable results, you want to run this on a realistic (and realistically scaled) data and on a properly maintained database.</p>

<p>And for a bit of code review - there's no need to join on a "subquery". Instead, just use a join with two conditions:</p>

<pre><code>left join ClubSponsorRelation csr on csr.ClubId = @clubId and u.UserId = csr.SponsorId
</code></pre>

<p>There's fewer reasons with each new MS SQL version to ever use subqueries. But of course, profiling is the king - there's too many variables to have reliable guesses in complex scenarios.</p>

<p>Another important thing to understand is that we're only talking about possible performance issues here - the statement must not depend on order of evaluations etc. That's part of the whole set/relational algebra SQL is built on.</p>

### Answer ID: 28151385
<p>Generally, DBMS will do its own query optimization for all of the query, which uses the algorithm it(DBMS) thinks is the fastest. So it's filtering, then joining.
But the best way is to see <code>Execution Plan</code>.</p>

