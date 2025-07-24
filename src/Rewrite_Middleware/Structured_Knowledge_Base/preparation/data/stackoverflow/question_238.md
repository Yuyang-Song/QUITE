# Rewriting sql query without subqueries
[Link to question](https://stackoverflow.com/questions/17597599/rewriting-sql-query-without-subqueries)
**Creation Date:** 1373556764
**Score:** -2
**Tags:** mysql, join, subquery
## Question Body
<p>I need some help with the followin MySQL Query</p>

<p>I want to rewrite my Query without any subqueries - but i dont know how..</p>

<p>It is a video rental store database ;)</p>

<pre><code>SELECT k.first_name, k.last_name, SUM(amount) AS profit 
FROM payment AS p 
JOIN (SELECT c.* FROM customer AS c 
 JOIN rental AS r ON c.customer_id = r.customer_id 
WHERE r.return_date IS NULL GROUP BY c.customer_id HAVING 
COUNT(*) &gt; '1') AS k ON p.customer_id = k.customer_id 
GROUP BY k.customer_id 
HAVING SUM(amount) &gt; 100 
ORDER BY profit DESC;
</code></pre>

<p>Thanks :)</p>

## Answers
### Answer ID: 17597799
<p>This this:</p>

<pre><code> SELECT c.first_name, c.last_name, c.customer_id,SUM(amount) AS profit 
 FROM payment AS p 
    INNER JOIN (customer c
        INNER join rental r
        ON c.customer_id=r.customer_id)
    ON p.customer_id = c.customer_id
 GROUP BY c.customer_id,c.last_name,c.first_name
 HAVING SUM(amount) &gt; 100 
 ORDER BY profit DESC;
</code></pre>

<p>using INNER JOIN will restrict this query to only those customers who have made payments.</p>

