# MySQL: Getting the MIN and the MAX of a table and both of their titles
[Link to question](https://stackoverflow.com/questions/28504881/mysql-getting-the-min-and-the-max-of-a-table-and-both-of-their-titles)
**Creation Date:** 1423847162
**Score:** 0
**Tags:** mysql, inner-join, min
## Question Body
<p>I have a large database of products. It has a one to many relationship to another table of prices. I can easily get, with one query, the MIN, MAX and AVG of a particular category.</p>

<pre><code>SELECT 
  MIN(gbp.price) AS min,
  ROUND(AVG(gbp.price),2) AS ave,
  MAX(gbp.price) AS max
FROM sku AS s
  INNER JOIN price gbp ON gbp.sid = s.id
</code></pre>

<p>However, I also want to be able to get the title of the product it relates to as well - I cannot get this resolved despite multiple searches and rewrites.</p>

<p>My data is similar to...</p>

<pre><code>prod_id | title
===============
1       | prod1
2       | prod2
3       | prod3
4       | prod4
5       | prod5
6       | prod6
7       | prod7

price_id | prod_id | price | price_date
=======================================
1        | 1       | 2.99  | 2015/02/01
2        | 1       | 3.99  | 2015/02/12
3        | 2       | 12.99 | 2015/02/01
4        | 3       | 15.99 | 2015/02/01
5        | 4       | 29.99 | 2015/02/01
6        | 5       | 29.99 | 2015/02/01
7        | 5       | 24.99 | 2015/02/12
8        | 6       | 2.99  | 2015/02/01
9        | 7       | 99.99 | 2015/02/01
10       | 7       | 89.99 | 2015/02/12
</code></pre>

<p>I am going to presume that other people may want a query writing similar to this, so I am going to ask for two answers. </p>

<p><strong>First one "simply" to return this...</strong></p>

<pre><code>min  | min_title | ave   | max   | max_title
============================================
2.99 | prod1     | 31.39 | 99.99 | prod7 
</code></pre>

<p>However, the real answer I want (despite the fact I cannot even solve the above) is where it gets even trickier.</p>

<p>The actual results I want is in the table below...</p>

<pre><code>min  | min_title | ave   | max   | max_title
============================================
2.99 | prod6     | 25.85 | 89.99 | prod7 
</code></pre>

<p>The <code>min</code> is <code>2.99</code> for <code>prod6</code> as the <code>2.99</code> price for <code>prod1</code> has expired.</p>

<p>The <code>max</code> is <code>89.99</code> for <code>prod7</code> as the <code>99.99</code> price for <code>prod7</code> has expired.</p>

<p>The <code>ave</code> is <code>25.85</code> because of above and because the price for <code>prod5</code> is <code>24.99</code>.</p>

<p>I am not expecting answers for everything, just answering the first question (in bold) will likely lead me to the answer for the second part (as I have similar queries that get the latest price etc).</p>

## Answers
### Answer ID: 28506110
<p>This is essentially two different queries (or three if you count the average). The cross join is just horizontally splicing together the two results for min and max. They could all obviously be separated and executed individually.</p>

<pre><code>with current_prices as (
    select price_id, prod_id, price
    from prices
    where price_date = (
        select max(price_date)
        from prices as prices2
        where prices2.prod_id = prices.prod_id
    )
),
min_current_prices as (
    select price, min(prod_id) as prod_d /* arbitrary selected representative */
    from current_prices
    where price = (
        select min(price)
        from current_prices
    )
    group by price
),
max_current_prices as (
    select price, min(prod_id) as prod_id /* arbitrary selected representative */
    from current_prices
    where price = (
        select max(price)
        from current_prices
    )
    group by price
)
select
    m1.price, prod1.title,
    (select avg(price) from current_prices) as ave,
    m2.price, prod2.title
from
    min_current_prices as m1 inner join products as prod1 on prod1.prod_id = m1.prod_id
    max_current_prices as m2 inner join products as prod2 on prod2.prod_id = m2.prod_id
</code></pre>

<p>I feel that this seems too complicated and yet you're asking for something very unusual. There clearly could be products with the same min/max price so this is going to cause problems when there is more than one at either end.</p>

<p>If your platform doesn't support <code>WITH</code> then just substitute the full query instead:</p>

<pre><code>select
    min_current_price.price as min_price, min_prod.title as min_title,
    (
        select avg(price)
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
        )
    ) as ave,
    max_current_price.price as max_price, max_prod.title as max_title
from
(
    select price, min(prod_id) as prod_id /* arbitrarily selected representative */
    from (
        select *
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
            )
        ) as current_prices
    where price = (
        select min(price)
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
            )
        )
    group by price
) as min_current_price

cross join

(
    select price, min(prod_id) as prod_id /* arbitrarily selected representative */
    from (
        select *
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
            )
        ) as current_prices
    where price = (
        select max(price)
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
            )
        )
    group by price
) as max_current_price

inner join products as min_prod on min_prod.prod_id = min_current_price.prod_id
inner join products as max_prod on max_prod.prod_id = max_current_price.
</code></pre>

<p>Here's a hack for doing it in mysql using limits and sorting methods:</p>

<pre><code>select
    minprice.price as min_price, minprod.title as min_title,
    (
        select avg(price)
        from prices
        where price_date = (
            select max(price_date)
            from prices as prices2
            where prices2.prod_id = prices.prod_id
        )
    ) as ave,
    maxprice.price as max_price, maxprod.title as max_title
from
(
    select price_id, price, prod_id
    from prices
    where not exists ( /* another way of excluding expired prices */
        select 1 from prices as p2
        where p2.prod_id = prices.prod_id and p2.price_date &gt; prices.prod_id
    )
    order by price asc
    limit 0, 1
) as minprice,

(
    select price_id, price, prod_id
    from prices
    where not exists (
        select 1 from prices as p2
        where p2.prod_id = prices.prod_id and p2.price_date &gt; prices.prod_id
    )
    order by price desc
    limit 0, 1
) as maxprice

inner join prod as minprod on minprod.prod_id = minprice.prod_id
inner join prod as maxprod on min.prod_id = maxprice.prod_id
</code></pre>

### Answer ID: 28505934
<p>To solve your first output just use join to get those values:</p>

<pre><code>SELECT min, mint.title, ave, max, maxt.title
FROM (
    SELECT 
      MIN(gbp.price) AS min,
      ROUND(AVG(gbp.price),2) AS ave,
      MAX(gbp.price) AS max
    FROM (SELECT price 
          FROM price AS gbp 
          INNER JOIN sku s2 ON gbp.sid = s2.id 
          ORDER BY prdate DESC 
          LIMIT 0, 1) AS s
    INNER JOIN price gbp ON gbp.sid = s.id
) inq
JOIN price minp ON inq.min = minp.price
JOIN price maxp on inq.max = maxp.price
JOIN prod mint ON minp.prod_id = mint.prod_id
JOIN prod maxt ON maxp.prod_id = maxt.prod_id
</code></pre>

<p>I don't understand the rules for your second output.</p>

### Answer ID: 28506248
<pre><code>SELECT t1.min, s.title AS min_title, t1.ave, t1.max, s2.title AS max_title
FROM (SELECT 
        MIN(gbp.price) AS min,
        ROUND(AVG(gbp.price),2) AS ave,
        MAX(gbp.price) AS max
    FROM sku AS s
        INNER JOIN price gbp ON (gbp.sid = s.id)
) t1
  INNER JOIN (SELECT gbp.price, MAX(gbp.prod_id) AS MaxProdID
    FROM price gbp
    WHERE NOT EXISTS(
        SELECT p2.price_id 
        FROM price p2 
        WHERE p2.price_id &gt; gbp.price_id 
        AND p2.prod_id = gpb.prod_id
    )
    GROUP BY gbp.price
  ) minprice ON (minprice.price = t1.min)
  INNER JOIN sku s ON (s.id = minprice.MaxProdID)
  INNER JOIN (SELECT gbp.price, MAX(gbp.prod_id) AS MaxProdID
    FROM price gbp
    WHERE NOT EXISTS(
        SELECT p2.price_id 
        FROM price p2 
        WHERE p2.price_id &gt; gbp.price_id 
        AND p2.prod_id = gpb.prod_id
    )
    GROUP BY gbp.price
  ) maxprice ON (maxprice.price = t1.max)
  INNER JOIN sku s2 ON (s2.id = maxprice.MaxProdID)
</code></pre>

