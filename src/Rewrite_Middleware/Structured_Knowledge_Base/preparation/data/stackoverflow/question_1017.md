# How can I convert/fix this WITH statement in SQL?
[Link to question](https://stackoverflow.com/questions/54936003/how-can-i-convert-fix-this-with-statement-in-sql)
**Creation Date:** 1551397522
**Score:** 1
**Tags:** mysql, sql, database, relational-database
## Question Body
<p>I have this query but apparently, the <code>WITH</code> statement has not been implemented in some database systems as yet. How can I rewrite this query to achieve the same result. </p>

<p>Basically what this query is supposed to do is to provide the branch names all of all the branches in a database whose deposit total is less than the average of all the branches put together.  </p>

<pre><code>WITH branch_total (branch_name, value) AS 
SELECT branch_name, sum (balance) FROM account
GROUP BY branch_name
WITH branch_total_avg (value) AS SELECT avg(value)
FROM branch_total SELECT branch_name
FROM branch_total, branch_total_avg
WHERE branch_total.value &lt; branch_total_avg.value;
</code></pre>

<p>Can this be written any other way without the <code>WITH</code>? Please help. </p>

## Answers
### Answer ID: 54936128
<p>Another way to rewrite this query:</p>

<pre><code>SELECT branch_name
  FROM account
 GROUP BY branch_name
HAVING SUM(balance) &lt; (SELECT AVG(value) 
                         FROM (SELECT branch_name, SUM(balance) AS value
                                 FROM account
                                GROUP BY branch_name) t1)
</code></pre>

<p>As you can see from this code the account table has nearly the same aggregate query run against it twice, once at the outer level and again nested two levels deep.</p>

<p>The benefit of the <code>WITH</code> clause is that you can write that aggregate query once give it a name and use it as many times as needed.  Additionally a smart DB engine will only run that subfactored query once but use the results as often as needed.</p>

### Answer ID: 54936085
<p><code>WITH</code> syntax was introduced as a new feature of MySQL 8.0. You have noticed that it is not supported in earlier versions of MySQL. If you can't upgrade to MySQL 8.0, you'll have to rewrite the query using subqueries like the following: </p>

<pre><code>SELECT branch_total.branch_name
FROM (
  SELECT branch_name, SUM(balance) AS value FROM account
  GROUP BY branch_name
) AS branch_total
CROSS JOIN (
  SELECT AVG(value) AS value FROM (
    SELECT SUM(balance) AS value FROM account GROUP BY branch_name 
  ) AS sums
) AS branch_total_avg
WHERE branch_total.value &lt; branch_total_avg.value;
</code></pre>

<p>In this case, the <code>WITH</code> syntax doesn't provide any advantage, so you might as well write it this way.</p>

<p>Another approach, which may be more efficient because it can probably avoid the use of temporary tables in the query, is to split it into two queries:</p>

<pre><code>  SELECT AVG(value) INTO @avg FROM (
    SELECT SUM(balance) AS value FROM account GROUP BY branch_name
  ) AS sums;

  SELECT branch_name, SUM(balance) AS value FROM account
  GROUP BY branch_name
  HAVING value &lt; @avg;
</code></pre>

<p>This approach is certainly easier to read and debug, and there's some advantage to writing more straightforward code, to allow more developers to maintain it without having to post on Stack Overflow for help.</p>

