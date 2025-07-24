# Oracle 11.2.0.1.0_GROUP BY without aggregate functions doesn&#39;t raise error?
[Link to question](https://stackoverflow.com/questions/42709027/oracle-11-2-0-1-0-group-by-without-aggregate-functions-doesnt-raise-error)
**Creation Date:** 1489112473
**Score:** 0
**Tags:** sql, oracle-database, oracle11g
## Question Body
<p>Today I face a very weird problem that I have searched with no luck. In one of our procedure I meet this query:</p>

<pre><code>select count(*) into b_count 
from (
    select col1, col2, col3 
    from table_name 
    where col_id = b_id and col3 = b_col3 
    group by col1, col2);
</code></pre>

<p>Let's not talk about this poor query that we could rewrite without using subquery. </p>

<p>The problem here is in our development database, oracle didn't raise <code>ORA-00979 not a GROUP BY expression</code> and we could run the procedure normally (no control, no if else,....). And in our real database it did raise error.</p>

<p>Did someone ever meet this before? Could someone explain this to me?</p>

<p>As trying to reproduce the problem, I write this query and it run fine in our developement db (result count(*) = 2 not 3), and yes error 00979 in our real db:</p>

<pre><code>WITH table_name AS 
(
    SELECT 1 col1, 2 col2, 3 col3 FROM DUAL UNION ALL
    SELECT 1, 3, 4 FROM DUAL UNION ALL
    SELECT 2, 7, 8 FROM DUAL 
)
SELECT COUNT(*)
FROM (
    SELECT col1, col2, col3
    FROM table_name
    GROUP BY col1
);
</code></pre>

<p>P/S: our dev db:</p>

<blockquote>
  <p>Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production</p>
</blockquote>

<p>Our real db:</p>

<blockquote>
  <p>Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production</p>
</blockquote>

<p>Did 11.2.0.1.0's query optimizer be "smarter" that is omitted the SELECT statement in subquery and only use the SELECT COUNT(*) in main query? Or it's some setup in Oracle that I don't know?</p>

<p>And this is query plan in the dev db, it seems not different from a running query like <code>SELECT SUM(col3) FROM (SELECT col1, MAX(col3) col3 FROM table_name GROUP BY col1)</code>
<a href="https://i.sstatic.net/D4wTD.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/D4wTD.png" alt="enter image description here"></a></p>

