# need to rewrite this query without using a correlated subquery
[Link to question](https://stackoverflow.com/questions/24413127/need-to-rewrite-this-query-without-using-a-correlated-subquery)
**Creation Date:** 1403711029
**Score:** 2
**Tags:** python, mysql
## Question Body
<p>I know how <code>correlated subqueries</code> work and usually steer away from them.. but for what I was trying to do i couldn't find another way to write this query. I was ok with using it because I didn't have a bunch of records in the table I was using.. but now I need to do the same thing on some tables with > 100,000 records in them which will make this query take a long time. so I need some help with rewriting this query. </p>

<p><strong>INITIAL QUERY:</strong></p>

<pre><code>SELECT
DATE(m.Created_At) AS m_date,
COUNT(m.id) AS daily_count,
(
    SELECT
        COUNT(m1.id)
    FROM members_joined m1
    WHERE m1.has_verified = 1 and DATE(m1.Created_At) &lt;= m_date
) AS member_totals
FROM members_joined AS m
WHERE m.has_verified = 1 and m.Created_At BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
GROUP BY m_date;
</code></pre>

<p>what this query is doing is getting the total count of registered members up to 30 days ago.. and then for every day between the last 30 days its doing the total count again</p>

<pre><code>m_date      daily_count member_totals
2014-05-27      4           619
2014-05-29      1           620
2014-05-30      3           623
2014-06-02      4           627
2014-06-03      7           634
2014-06-04      10          644
2014-06-05      12          656
2014-06-06      4           660
2014-06-07      3           663
2014-06-08      3           666
2014-06-09      3           669
2014-06-10      5           674
2014-06-11      3           677
</code></pre>

<p>if you notice it is <strong>incrementing</strong> the count by <strong>each</strong> daily count.</p>

<p>this query itself only takes .036 seconds to run which isnt a big deal</p>

<p>but on some of the bigger tables it already takes 12 seconds and they are only going to get bigger.</p>

<p><strong>NOTE:</strong> can this be done without using a correlated subquery? assume you cannot use user-defined variables.</p>

<p>if this cant be done in mysql I can hit the database twice and do it in python, but I was hoping to find a solution in MySQL and not hit the database multiple times. </p>

<p>thanks for any pointers / help!</p>

## Answers
### Answer ID: 24413979
<p>EDIT : fix a mistake in the query</p>

<p>EDIT2 : proposal of a python way</p>

<p>You can rewrite it with an explicit auto-join, but I do not think it will be faster</p>

<pre><code>SELECT
DATE(m.Created_At) AS m_date,
COUNT(m.id) AS daily_count,
COUNT(m1.id) AS member_totals
FROM members_joined AS m
JOIN members_joined m1 ON m1.has_verified = 1 and DATE(m1.Created_At) &lt;= DATE(m.Created_At) 
WHERE m.has_verified = 1 and m.Created_At BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
GROUP BY m_date;
</code></pre>

<p>You are asking the database to get a quadratic number of rows.</p>

<p>As the autojoin do not improve performance, I think you should 2 simpler queries from your database, and then do the sums in Python.</p>

<pre><code>SELECT
DATE(m.Created_At) AS m_date,
COUNT(m.id) AS daily_count,
FROM members_joined AS m
WHERE m.has_verified = 1 and m.Created_At BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE()
GROUP BY m_date;
</code></pre>

<p>to get daily_count per date for the last 30 days, and </p>

<pre><code>SELECT
CURDATE() - INTERVAL 30 DAY AS m_date,
COUNT(m.id) AS member_totals,
FROM members_joined AS m
WHERE m.has_verified = 1 and m.Created_At &lt; CURDATE() - INTERVAL 30 DAY;
</code></pre>

<p>to get the cumulative member_totals for the day preceding the first of the other query</p>

<p>Python pseudo code, say second query initialized <code>member_total</code>, and then first query initialized rows (be it a cursor or a list or tuple obtained by <code>fetchall</code>)</p>

<pre><code>for row in rows:
    dat, daily_count = row
    member_totals += daily_count
    # use dat, daily_count, member_totals
</code></pre>

### Answer ID: 24414237
<p>This can hardly be done with pure SQL efficiently, but you can use MySQL-specific user defined variables. You will just need to compute counts for each day and accumulate counts for each row.</p>

<p>The main trick is to force MySQL update the variable in the correct order.</p>

<p>The query should look like the following (not sure that it is 100% correct):</p>

<pre><code>SELECT m_date, daily_count, @count:=(daily_count + @count) as member_totals
FROM
(SELECT DATE(Created_At) as m_date, COUNT(*) as daily_count
 FROM members_joined
 WHERE DATE(Created_At) &gt;= CURDATE() - INTERVAL 30 DAY AND has_verified = 1
 GROUP BY m_date
) as days,
(SELECT @count:=COUNT(*) as cnt0
 FROM members_joined
 WHERE DATE(Created_At) &lt; CURDATE() - INTERVAL 30 DAY 
   AND has_verified = 1) as init
ORDER BY m_date;
</code></pre>

