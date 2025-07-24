# Mysql reporting - Can&#39;t get numbers to match up
[Link to question](https://stackoverflow.com/questions/19793141/mysql-reporting-cant-get-numbers-to-match-up)
**Creation Date:** 1383666934
**Score:** 3
**Tags:** mysql, sql
## Question Body
<p>I think I've been staring at this problem for too long. We took over maintenance of a system and are trying to fix one of the reports in it. For some reason, all of the numbers are correct except for one in this report and I'm not having any luck with the issue.</p>

<p>The following query shows that there are 1014 transactions in the database:</p>

<pre><code>SELECT COUNT(DISTINCT(store_orders_id))
FROM transactions, store_orders_products
WHERE store_orders_products.store_orders_id = transactions.id
AND transactions.date &gt;= '2013-10-01 00:00:00'
AND transactions.date &lt;= '2013-10-31 23:59:59'
AND store_orders_products.category_name &lt;&gt; ''
</code></pre>

<p>The DISTINCT() call is necessary because store_orders_products contains one line for each product ordered so for orders with multiple products, store_orders_id will have duplicates. The above query produces the correct outcome. There are in fact 1014 transactions between those dates.</p>

<p>Here is where the issue is. When we run the full reporting query, the total returned is 1030.</p>

<pre><code>SELECT COUNT(DISTINCT(store_orders_id)) as transactions,
SUM(store_orders_products.total + store_orders_products.coupon) as total,
SUM(store_orders_products.coupon) as coupon,
SUM(store_orders_products.shipping) as shipping,
SUM(store_orders_products.tax) as tax, store_orders_products.category_name
FROM transactions, store_orders_products
WHERE store_orders_products.store_orders_id = transactions.id
AND transactions.date &gt;= '2013-10-01 00:00:00'
AND transactions.date &lt;= '2013-10-31 23:59:59'
AND store_orders_products.category_name &lt;&gt; ''
GROUP BY store_orders_products.category_name
ORDER BY store_orders_products.category_name ASC
</code></pre>

<p>This produces a report like the following:</p>

<pre><code>Transactions | Total    | Coupon | Shipping | Tax    | Category Name
483          | 17863.15 | 0.00   | 1493.50  | 260.56 | Category 1
547          | 21541.47 | 0.00   | 1594.80  | 194.03 | Category 2
</code></pre>

<p>As you can see, the sum of those transactions is 1030, and not the 1014 that we would expect.</p>

<p>The problem appears to occur when we simply add a second selected column. For example, changing from <code>SELECT COUNT(DISTINCT(store_orders_id))</code> to <code>SELECT COUNT(DISTINCT(store_orders_id)), store_orders_products.category_name</code> in the first query block posted above results in a jump from 1014 results to 1030 results.</p>

<p>I hope I've provided enough information to be useful. I'm sure this is a problem with the query but as I said, we've just taken this project over and are still getting used to things so we're trying not to rewrite anything from scratch right now.</p>

## Answers
### Answer ID: 19793820
<p>It looks like you're assuming that the categories are mutually exclusive and therefore adding up the category totals will yield the grand total, but they really aren't.  There are some (16) transactions that are associated with both categories.</p>

