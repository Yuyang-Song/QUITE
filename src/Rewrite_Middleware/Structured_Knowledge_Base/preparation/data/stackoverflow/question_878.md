# Optimize slow aggregates in LATERAL join
[Link to question](https://stackoverflow.com/questions/48000013/optimize-slow-aggregates-in-lateral-join)
**Creation Date:** 1514419395
**Score:** 2
**Tags:** sql, postgresql, performance, optimization, postgresql-performance
## Question Body
<p>In my PostgreSQL 9.6.2 database, I've got a query that builds a table of calculated fields from some stock data. It calculates a moving average window of 1 through 10 years for each row in the table, and uses that in cyclical adjustments. CAPE, CAPB, CAPC, CAPS, and CAPD, specifically. </p>

<p>I.e., for each row, you calculate <code>avg(earnings)</code> for the past 1 through 10 years, then do the same for several other variables.</p>

<p>I'm currently using a lateral join to compute the aggregates for each row, but things are incredibly slow and I'm not entirely sure how to speed it up, whether it be indexing / rewriting the query, etc.</p>

<p>For instance when I stratify the query to only include ~ 25k rows, it takes 15 minutes to run which seems way too slow. (RDS on AWS Free Tier)</p>

<pre><code>-- Initialize Cyclical Adjustments
-- This query populates the database with numerous peak/min and CAPE type calculations.
-- We do this by selecting each valid row within the table by security then laterally
-- selecting the calculations for each of those rows. 'Valid' rows are determined by
-- date calculations that make sure every field that has insufficient data behind it
-- (several queries want 5+ years of time series data) is filled with NULL to avoid
-- inaccuracies.

WITH earliest_point AS (
    SELECT
      security_id,
      min(date) as min_date
    FROM bloomberg.security_data
    GROUP BY security_id
)
SELECT
  rec.record_id,
  rec.security_id,
  date,
  -- Each of these cases decides if we have enough data in the database to populate the field. If there are at least
  -- x years in the database (where x = 1:10) we do the price / aggregate computation. Otherwise, we shortcut to NULL.
  -- NOTE: The NULLIF prevents us from dividing by zero.
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.max_earnings, 0) ELSE NULL END AS price_to_peak_earnings,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.min_earnings, 0) ELSE NULL END AS price_to_minimum_earnings,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.max_book, 0) ELSE NULL END AS price_to_peak_book,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.min_book, 0) ELSE NULL END AS price_to_minimum_book,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.max_sales, 0) ELSE NULL END AS price_to_peak_sales,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.min_sales, 0) ELSE NULL END AS price_to_minimum_sales,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.max_cashflow, 0) ELSE NULL END AS price_to_peak_cashflow,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.min_cashflow, 0) ELSE NULL END AS price_to_minimum_cashflow,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.max_dividends, 0) ELSE NULL END AS price_to_peak_dividends,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.min_dividends, 0) ELSE NULL END AS price_to_minimum_dividends,
  CASE WHEN ep.min_date &lt; rec.date - '1 years'::INTERVAL  THEN price / NULLIF(ru.cap1_avg_earnings, 0) ELSE NULL END AS cape1,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_earnings, 0) ELSE NULL END AS cape2,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_earnings, 0) ELSE NULL END AS cape2,
  CASE WHEN ep.min_date &lt; rec.date - '3 years'::INTERVAL  THEN price / NULLIF(ru.cap3_avg_earnings, 0) ELSE NULL END AS cape3,
  CASE WHEN ep.min_date &lt; rec.date - '4 years'::INTERVAL  THEN price / NULLIF(ru.cap4_avg_earnings, 0) ELSE NULL END AS cape4,
  CASE WHEN ep.min_date &lt; rec.date - '5 years'::INTERVAL  THEN price / NULLIF(ru.cap5_avg_earnings, 0) ELSE NULL END AS cape5,
  CASE WHEN ep.min_date &lt; rec.date - '6 years'::INTERVAL  THEN price / NULLIF(ru.cap6_avg_earnings, 0) ELSE NULL END AS cape6,
  CASE WHEN ep.min_date &lt; rec.date - '7 years'::INTERVAL  THEN price / NULLIF(ru.cap7_avg_earnings, 0) ELSE NULL END AS cape7,
  CASE WHEN ep.min_date &lt; rec.date - '8 years'::INTERVAL  THEN price / NULLIF(ru.cap8_avg_earnings, 0) ELSE NULL END AS cape8,
  CASE WHEN ep.min_date &lt; rec.date - '9 years'::INTERVAL  THEN price / NULLIF(ru.cap9_avg_earnings, 0) ELSE NULL END AS cape9,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.cap10_avg_earnings, 0) ELSE NULL END AS cape10,
  CASE WHEN ep.min_date &lt; rec.date - '1 years'::INTERVAL  THEN price / NULLIF(ru.cap1_avg_book, 0) ELSE NULL END AS capb1,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_book, 0) ELSE NULL END AS capb2,
  CASE WHEN ep.min_date &lt; rec.date - '3 years'::INTERVAL  THEN price / NULLIF(ru.cap3_avg_book, 0) ELSE NULL END AS capb3,
  CASE WHEN ep.min_date &lt; rec.date - '4 years'::INTERVAL  THEN price / NULLIF(ru.cap4_avg_book, 0) ELSE NULL END AS capb4,
  CASE WHEN ep.min_date &lt; rec.date - '5 years'::INTERVAL  THEN price / NULLIF(ru.cap5_avg_book, 0) ELSE NULL END AS capb5,
  CASE WHEN ep.min_date &lt; rec.date - '6 years'::INTERVAL  THEN price / NULLIF(ru.cap6_avg_book, 0) ELSE NULL END AS capb6,
  CASE WHEN ep.min_date &lt; rec.date - '7 years'::INTERVAL  THEN price / NULLIF(ru.cap7_avg_book, 0) ELSE NULL END AS capb7,
  CASE WHEN ep.min_date &lt; rec.date - '8 years'::INTERVAL  THEN price / NULLIF(ru.cap8_avg_book, 0) ELSE NULL END AS capb8,
  CASE WHEN ep.min_date &lt; rec.date - '9 years'::INTERVAL  THEN price / NULLIF(ru.cap9_avg_book, 0) ELSE NULL END AS capb9,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.cap10_avg_book, 0) ELSE NULL END AS capb10,
  CASE WHEN ep.min_date &lt; rec.date - '1 years'::INTERVAL  THEN price / NULLIF(ru.cap1_avg_sales, 0) ELSE NULL END AS caps1,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_sales, 0) ELSE NULL END AS caps2,
  CASE WHEN ep.min_date &lt; rec.date - '3 years'::INTERVAL  THEN price / NULLIF(ru.cap3_avg_sales, 0) ELSE NULL END AS caps3,
  CASE WHEN ep.min_date &lt; rec.date - '4 years'::INTERVAL  THEN price / NULLIF(ru.cap4_avg_sales, 0) ELSE NULL END AS caps4,
  CASE WHEN ep.min_date &lt; rec.date - '5 years'::INTERVAL  THEN price / NULLIF(ru.cap5_avg_sales, 0) ELSE NULL END AS caps5,
  CASE WHEN ep.min_date &lt; rec.date - '6 years'::INTERVAL  THEN price / NULLIF(ru.cap6_avg_sales, 0) ELSE NULL END AS caps6,
  CASE WHEN ep.min_date &lt; rec.date - '7 years'::INTERVAL  THEN price / NULLIF(ru.cap7_avg_sales, 0) ELSE NULL END AS caps7,
  CASE WHEN ep.min_date &lt; rec.date - '8 years'::INTERVAL  THEN price / NULLIF(ru.cap8_avg_sales, 0) ELSE NULL END AS caps8,
  CASE WHEN ep.min_date &lt; rec.date - '9 years'::INTERVAL  THEN price / NULLIF(ru.cap9_avg_sales, 0) ELSE NULL END AS caps9,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.cap10_avg_sales, 0) ELSE NULL END AS caps10,
  CASE WHEN ep.min_date &lt; rec.date - '1 years'::INTERVAL  THEN price / NULLIF(ru.cap1_avg_cashflow, 0) ELSE NULL END AS capc1,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_cashflow, 0) ELSE NULL END AS capc2,
  CASE WHEN ep.min_date &lt; rec.date - '3 years'::INTERVAL  THEN price / NULLIF(ru.cap3_avg_cashflow, 0) ELSE NULL END AS capc3,
  CASE WHEN ep.min_date &lt; rec.date - '4 years'::INTERVAL  THEN price / NULLIF(ru.cap4_avg_cashflow, 0) ELSE NULL END AS capc4,
  CASE WHEN ep.min_date &lt; rec.date - '5 years'::INTERVAL  THEN price / NULLIF(ru.cap5_avg_cashflow, 0) ELSE NULL END AS capc5,
  CASE WHEN ep.min_date &lt; rec.date - '6 years'::INTERVAL  THEN price / NULLIF(ru.cap6_avg_cashflow, 0) ELSE NULL END AS capc6,
  CASE WHEN ep.min_date &lt; rec.date - '7 years'::INTERVAL  THEN price / NULLIF(ru.cap7_avg_cashflow, 0) ELSE NULL END AS capc7,
  CASE WHEN ep.min_date &lt; rec.date - '8 years'::INTERVAL  THEN price / NULLIF(ru.cap8_avg_cashflow, 0) ELSE NULL END AS capc8,
  CASE WHEN ep.min_date &lt; rec.date - '9 years'::INTERVAL  THEN price / NULLIF(ru.cap9_avg_cashflow, 0) ELSE NULL END AS capc9,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.cap10_avg_cashflow, 0) ELSE NULL END AS capc10,
  CASE WHEN ep.min_date &lt; rec.date - '1 years'::INTERVAL  THEN price / NULLIF(ru.cap1_avg_dividends, 0) ELSE NULL END AS capd1,
  CASE WHEN ep.min_date &lt; rec.date - '2 years'::INTERVAL  THEN price / NULLIF(ru.cap2_avg_dividends, 0) ELSE NULL END AS capd2,
  CASE WHEN ep.min_date &lt; rec.date - '3 years'::INTERVAL  THEN price / NULLIF(ru.cap3_avg_dividends, 0) ELSE NULL END AS capd3,
  CASE WHEN ep.min_date &lt; rec.date - '4 years'::INTERVAL  THEN price / NULLIF(ru.cap4_avg_dividends, 0) ELSE NULL END AS capd4,
  CASE WHEN ep.min_date &lt; rec.date - '5 years'::INTERVAL  THEN price / NULLIF(ru.cap5_avg_dividends, 0) ELSE NULL END AS capd5,
  CASE WHEN ep.min_date &lt; rec.date - '6 years'::INTERVAL  THEN price / NULLIF(ru.cap6_avg_dividends, 0) ELSE NULL END AS capd6,
  CASE WHEN ep.min_date &lt; rec.date - '7 years'::INTERVAL  THEN price / NULLIF(ru.cap7_avg_dividends, 0) ELSE NULL END AS capd7,
  CASE WHEN ep.min_date &lt; rec.date - '8 years'::INTERVAL  THEN price / NULLIF(ru.cap8_avg_dividends, 0) ELSE NULL END AS capd8,
  CASE WHEN ep.min_date &lt; rec.date - '9 years'::INTERVAL  THEN price / NULLIF(ru.cap9_avg_dividends, 0) ELSE NULL END AS capd9,
  CASE WHEN ep.min_date &lt; rec.date - '10 years'::INTERVAL THEN price / NULLIF(ru.cap10_avg_dividends, 0) ELSE NULL END AS capd10
FROM bloomberg.security_data rec
  -- Include the earliest point we have for this security in the record
  JOIN earliest_point ep ON ep.security_id = rec.security_id,
  -- LATERAL SELECT is executed for each row in the above query, with the row (rec) as a parameter
  LATERAL
  (
  SELECT
    -- Price to Peak/Minimum &lt;field&gt; calculations
    max(earnings)  AS max_earnings,
    min(earnings)  AS min_earnings,
    max(book)      AS max_book,
    min(book)      AS min_book,
    max(sales)     AS max_sales,
    min(sales)     AS min_sales,
    max(cashflow)  AS max_cashflow,
    min(cashflow)  AS min_cashflow,
    max(dividends) AS max_dividends,
    min(dividends) AS min_dividends,

    -- Each of the following computes the aggregates for the
    -- CAPE/B/S/C/D cyclical adjustments.
    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '1 years'::interval) AS cap1_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '1 years'::interval) AS cap1_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '1 years'::interval) AS cap1_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '1 years'::interval) AS cap1_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '1 years'::interval) AS cap1_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '2 years'::interval) AS cap2_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '2 years'::interval) AS cap2_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '2 years'::interval) AS cap2_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '2 years'::interval) AS cap2_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '2 years'::interval) AS cap2_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '3 years'::interval) AS cap3_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '3 years'::interval) AS cap3_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '3 years'::interval) AS cap3_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '3 years'::interval) AS cap3_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '3 years'::interval) AS cap3_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '4 years'::interval) AS cap4_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '4 years'::interval) AS cap4_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '4 years'::interval) AS cap4_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '4 years'::interval) AS cap4_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '4 years'::interval) AS cap4_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '5 years'::interval) AS cap5_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '5 years'::interval) AS cap5_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '5 years'::interval) AS cap5_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '5 years'::interval) AS cap5_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '5 years'::interval) AS cap5_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '6 years'::interval) AS cap6_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '6 years'::interval) AS cap6_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '6 years'::interval) AS cap6_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '6 years'::interval) AS cap6_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '6 years'::interval) AS cap6_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '7 years'::interval) AS cap7_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '7 years'::interval) AS cap7_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '7 years'::interval) AS cap7_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '7 years'::interval) AS cap7_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '7 years'::interval) AS cap7_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '8 years'::interval) AS cap8_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '8 years'::interval) AS cap8_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '8 years'::interval) AS cap8_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '8 years'::interval) AS cap8_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '8 years'::interval) AS cap8_avg_dividends,

    avg(earnings)  FILTER (WHERE date &gt;= rec.date - '9 years'::interval) AS cap9_avg_earnings,
    avg(book)      FILTER (WHERE date &gt;= rec.date - '9 years'::interval) AS cap9_avg_book,
    avg(sales)     FILTER (WHERE date &gt;= rec.date - '9 years'::interval) AS cap9_avg_sales,
    avg(cashflow)  FILTER (WHERE date &gt;= rec.date - '9 years'::interval) AS cap9_avg_cashflow,
    avg(dividends) FILTER (WHERE date &gt;= rec.date - '9 years'::interval) AS cap9_avg_dividends,

    avg(earnings)  AS cap10_avg_earnings,
    avg(book)      AS cap10_avg_book,
    avg(sales)     AS cap10_avg_sales,
    avg(cashflow)  AS cap10_avg_cashflow,
    avg(dividends) AS cap10_avg_dividends

  FROM bloomberg.security_data DATA
  WHERE security_id = rec.security_id
    AND date &gt;= rec.date - '10 years'::interval
    AND date &lt;= rec.date
  ) ru;
</code></pre>

<p>Any ideas on how to make this faster would be greatly appreciated as I'm new to PostgreSQL.</p>

<p>Here is the database setup for reference:</p>

<pre><code>CREATE SCHEMA bloomberg;

CREATE TABLE bloomberg.securities (
  security_id character varying(45) PRIMARY KEY,
  name_short character varying(45) NOT NULL,
  name character varying(45) NOT NULL,
  name_security character varying(45) NOT NULL
);

CREATE TABLE bloomberg.security_data (
  record_id bigserial PRIMARY KEY,
  date date NOT NULL,
  security_id character varying(45) NOT NULL,
  price double precision,
  total_return double precision,
  earnings double precision,
  book double precision,
  sales double precision,
  cashflow double precision,
  dividends double precision,
  CONSTRAINT security_id FOREIGN KEY (security_id)
  REFERENCES bloomberg.securities (security_id) MATCH SIMPLE
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE INDEX security_data_data on bloomberg.security_data (date);
CREATE INDEX security_data_security_id on bloomberg.security_data (security_id);
</code></pre>

## Answers
### Answer ID: 48001733
<p>This should be a faster variant with <code>LATERAL</code> subqueries. Untested.</p>

<pre><code>SELECT s.record_id, s.security_id, s.date
     , s.price / l.pmax   AS price_to_peak_earnings
     , s.price / l.pmin   AS price_to_minimum_earnings
  -- , ...
     , s.price / l.cape1  AS cape1
     , s.price / l.cape2  AS cape2
  -- , ...
     , s.price / l.cape10 AS cape10
     , s.price / l.capb1  AS capb1
     , s.price / l.capb2  AS capb2
  -- , ...
     , s.price / l.capb10 AS capb10
  -- , ...
FROM  (
   SELECT *
        , (date - interval  '1 y')::date AS date1
        , (date - interval  '2 y')::date AS date2
        -- ...
        , (date - interval '10 y')::date AS date10
   FROM  (
      SELECT *, min(date) OVER (PARTITION BY security_id) AS min_date
      FROM   security_data
      ) s1
   ) s
LEFT   JOIN LATERAL (
   SELECT CASE WHEN s.date10 &gt;= s.min_date THEN NULLIF(max(earnings)                               , 0) END AS pmax
        , CASE WHEN s.date10 &gt;= s.min_date THEN NULLIF(min(earnings)                               , 0) END AS pmin
        -- ...
        ,                                       NULLIF(avg(earnings) FILTER (WHERE date &gt;= s.date1), 0)     AS cape1   -- no case
        , CASE WHEN s.date2  &gt;= s.min_date THEN NULLIF(avg(earnings) FILTER (WHERE date &gt;= s.date2), 0) END AS cape2
        -- ...
        , CASE WHEN s.date10 &gt;= s.min_date THEN NULLIF(avg(earnings)                               , 0) END AS cape10  -- no filter

        ,                                       NULLIF(avg(book)     FILTER (WHERE date &gt;= s.date1), 0)     AS capb1
        , CASE WHEN s.date2  &gt;= s.min_date THEN NULLIF(avg(book)     FILTER (WHERE date &gt;= s.date2), 0) END AS capb2
        -- ...
        , CASE WHEN s.date10 &gt;= s.min_date THEN NULLIF(avg(book)                                   , 0) END AS capb10
        -- ...
   FROM   security_data 
   WHERE  security_id = s.security_id
   AND    date &gt;= s.date10
   AND    date &lt;  s.date
   ) l ON s.date1 &gt;= s.min_date  -- no computations if &lt; 1 year of trailing data
ORDER  BY s.security_id, s.date;
</code></pre>

<p>It's still not going to be blazingly fast, since every row needs multiple separate aggregations. The bottleneck here will be CPU.</p>

<p>Also see the follow up with an alternative approach (JOIN to generated calendar + window functions):</p>

<ul>
<li><a href="https://stackoverflow.com/questions/48016525/window-functions-filter-through-current-row/48017477#48017477">Window functions filter through current row</a></li>
</ul>

