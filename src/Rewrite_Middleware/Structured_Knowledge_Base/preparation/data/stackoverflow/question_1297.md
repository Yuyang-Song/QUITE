# Writing Common Table Expressions in SQL (Snowflake)
[Link to question](https://stackoverflow.com/questions/69209917/writing-common-table-expressions-in-sql-snowflake)
**Creation Date:** 1631801037
**Score:** 0
**Tags:** sql, snowflake-cloud-data-platform, common-table-expression
## Question Body
<p>Just learning how to use common table expressions, I wish I was writing like this from the gate.</p>
<p>I've converted all of my queries in my database to a CTE format using <code>WITH ... AS</code> but this one and I am struggling .</p>
<p>So there are two tables:</p>
<p><strong>Table 1. customers</strong></p>
<ul>
<li>customer_id: unique id for each customer</li>
<li>full_name: customer full name</li>
</ul>
<p><strong>Table 2. subscriptions</strong></p>
<ul>
<li>subscription_id: unique id for subscription</li>
<li>customer_id: id for customer who subscribed to subscription</li>
<li>title: name of subscription</li>
</ul>
<p>The following query is used to return how many subscriptions each of your customers has:</p>
<pre><code>SELECT c.customer_id, c.full_name,
(
SELECT COUNT(*)
FROM subscriptions s
WHERE s.customer_id = c.customer_id
GROUP BY s.customer_id
) subscriptions_count
FROM customers c
</code></pre>
<p>How can I rewrite this as a Common Table Expression?</p>

## Answers
### Answer ID: 69210101
<p>If you really want to use <code>CTE</code> here is one way. You can rewrite it to use <code>left join</code> if you wish to show customers with no counts</p>
<pre><code>with cte as

(select customer_id, count(*) as counts
from subscriptions
group by customer_id) 

select c.customer_id, c.full_name, s.counts
from customers c
join cte s on s.customer_id=c.customer_id;
</code></pre>

### Answer ID: 69210098
<p>Sure. You can calculate the aggregate first, then join with <code>customers</code>:</p>
<pre><code>WITH cte AS (
    SELECT customer_id
         , COUNT(*) AS n
      FROM subscriptions
     GROUP BY customer_id
     )
SELECT c.*
     , COALESCE(cte.n, 0) AS n
  FROM      customers AS c
  LEFT JOIN cte
    ON c.customer_id = cte.customer_id
;
</code></pre>

