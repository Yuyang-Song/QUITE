# How to speed up a slow MariaDB SQL query that has a flat BNL join?
[Link to question](https://stackoverflow.com/questions/73193600/how-to-speed-up-a-slow-mariadb-sql-query-that-has-a-flat-bnl-join)
**Creation Date:** 1659356580
**Score:** 2
**Tags:** sql, mariadb, query-optimization
## Question Body
<p>I'm having problems with a slow SQL query running on the following system:</p>
<ul>
<li>Operating system: Debian 11 (bullseye)</li>
<li>Database: MariaDB 10.5.15 (the version packaged for bullseye)</li>
</ul>
<p>The table schemas and some sample data (no DB Fiddle as it doesn't support MariaDB):</p>
<pre class="lang-sql prettyprint-override"><code>DROP TABLE IF EXISTS item_prices;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS item_orders;

CREATE TABLE item_orders
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ordered_date DATE NOT NULL
) Engine=InnoDB;

CREATE TABLE prices
(
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    selected_flag TINYINT UNSIGNED NOT NULL
) Engine=InnoDB;

CREATE TABLE item_prices
(
    item_order_id INT UNSIGNED NOT NULL,
    price_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (item_order_id, price_id),
    FOREIGN KEY (item_order_id) REFERENCES item_orders(id),
    FOREIGN KEY (price_id) REFERENCES prices(id)
) Engine=InnoDB;

INSERT INTO item_orders VALUES (1, '2022-01-01');
INSERT INTO item_orders VALUES (2, '2022-02-01');
INSERT INTO item_orders VALUES (3, '2022-03-01');

INSERT INTO prices VALUES (1, 0);
INSERT INTO prices VALUES (2, 0);
INSERT INTO prices VALUES (3, 1);

INSERT INTO prices VALUES (4, 0);
INSERT INTO prices VALUES (5, 0);

INSERT INTO prices VALUES (6, 1);

INSERT INTO item_prices VALUES (1, 1);
INSERT INTO item_prices VALUES (1, 2);
INSERT INTO item_prices VALUES (1, 3);

INSERT INTO item_prices VALUES (2, 4);
INSERT INTO item_prices VALUES (2, 5);

INSERT INTO item_prices VALUES (3, 6);
</code></pre>
<p>A high-level overview of the table usage is:</p>
<ol>
<li>For any given month, there will be thousands of rows in item_orders.</li>
<li>A row in item_orders will link to zero or more rows in item_prices (item_orders.id = item_prices.item_order_id).</li>
<li>A row in item_prices will have exactly one linked row in prices (item_prices.price_id = prices.id).</li>
<li>For any given row in item_orders, there will be zero or one row in prices where the selected_flag is 1 (item_orders.id = item_prices.item_order_id AND item_prices.price_id = prices.id AND prices.selected_flag = 1). This is enforced by the application rather than the database (i.e. it's not defined as a CONSTRAINT).</li>
</ol>
<p>What I want to get, in a single query, are:</p>
<ol>
<li>The number of rows in item_orders.</li>
<li>The number of rows in item_orders where the related selected_flag is 1.</li>
</ol>
<p>At the moment I have the following query:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT
    COUNT(item_orders.id) AS item_order_count,
    SUM(CASE WHEN prices.id IS NOT NULL THEN 1 ELSE 0 END) AS item_order_selected_count
FROM
    item_orders
LEFT JOIN prices ON prices.id IN (
    SELECT price_id
    FROM item_prices
    WHERE
        item_prices.item_order_id = item_orders.id)
    AND prices.selected_flag = 1
</code></pre>
<p>This query returns the correct data (item_order_count = 3, item_order_selected_count = 2), however it takes a long time (over 10 seconds) to run on a live dataset, which is too slow for users (it is a heavily-used report, refreshed repeatedly through the day). I think the problem is the subquery in the LEFT JOIN, as removing the LEFT JOIN and the associated SUM reduces the query time to around 0.1 seconds. Also, the EXPLAIN output for the join has this in the Extra column:</p>
<p>Using where; Using join buffer (flat, BNL join)</p>
<p>Searching for 'flat BNL join' reveals a lot of information, of which the summary seems to be: 'BNL joins are slow, avoid them if you can'.</p>
<p>Is it possible to rewrite this query to return the same information, but avoiding the BNL join?</p>
<p>Things I've considered already:</p>
<ol>
<li><p>All the ID columns are indexed (item_orders.id, prices.id, item_prices.item_order_id, item_prices.price_id).</p>
</li>
<li><p>Splitting the query in two - one for item_order_count (no JOIN), the other for item_order_selected_count (INNER JOIN, as I only need rows which match). This works but isn't ideal as I want to build up this query to return more data (I've stripped it back to the minimum for this question). Also, I'm trying to keep the query output as close as possible to what the user will see, as that makes debugging easier and makes the database (which is optimised for that workload) do the work, rather than the application.</p>
</li>
<li><p>Changing the MariaDB configuration: Some of the search results for BNL joins suggest changing configuration options, however I'm wary of doing this as there are hundreds of other queries in the application and I don't want to cause a regression (e.g. speed up this query but accidentally slow down all the others).</p>
</li>
<li><p>Upgrading MariaDB: This would be a last resort as it would involve using a version different to that packaged with Debian, might break other parts of the application, and the system has just been through a major upgrade.</p>
</li>
</ol>

## Answers
### Answer ID: 74030041
<p>I came back to this question this week as the performance got even worse as the number of rows increased, to the point where it was taking over 2 minutes to run the query (with around 100,000 rows in the item_orders table, so hardly 'big data').</p>
<p>I remembered that it was possible to list multiple tables in the FROM clause and wondered if the same was true of a LEFT JOIN. It turns out this is the case and the query can be rewritten as:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT
    COUNT(item_orders.id) AS item_order_count,
    SUM(CASE WHEN prices.id IS NOT NULL THEN 1 ELSE 0 END) AS item_order_selected_count
FROM
    item_orders
LEFT JOIN (item_prices, prices) ON
    item_prices.item_order_id = item_orders.id
    AND prices.id = item_prices.price_id
    AND prices.selected_flag = 1
</code></pre>
<p>This returns the same results but takes less than a second to execute. Unfortunately I don't know any relational algebra to prove this, but effectively what I am saying is 'only LEFT JOIN where everything matches on both item_prices and prices'.</p>

### Answer ID: 73336389
<p>Not sure whether this will be any faster but worth a try (table joins on indexed foreign keys are fast and sometimes simplicity is king...)</p>
<pre><code>SELECT 
    (SELECT COUNT(*) FROM item_orders) AS item_order_count,
    (SELECT COUNT(*)
     FROM item_orders io
     JOIN item_prices ip
     ON io.id = ip.item_order_id
     JOIN prices p
     ON ip.price_id = p.id
     WHERE p.selected_flag = 1) AS item_order_selected_count;
</code></pre>

