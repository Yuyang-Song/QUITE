# MySQL 8 - Calculating Year-over-Year Metrics
[Link to question](https://stackoverflow.com/questions/63484498/mysql-8-calculating-year-over-year-metrics)
**Creation Date:** 1597831057
**Score:** 1
**Tags:** mysql, sql, sum, e-commerce, window-functions
## Question Body
<p>I've been trying to calculate year over year growth for monthly returns and have been rewriting the same queries for hours with no luck. I've seen solutions but they're all other database solutions.</p>
<p>I'm trying to basically achieve something like the following:</p>
<p><img src="https://cdn.sisense.com/wp-content/uploads/year-over-year-3.png" alt="Year over Year" /></p>
<p>And this is the query I've built, although I've never actually had it complete running (been running 15+ minutes) due to the sub-query runs per-row.</p>
<p>This table has 2m+ rows with good indexes, it's fast but subqueries kill it.</p>
<p>Could be totally wrong approach, but this is what I've got.</p>
<pre><code>SELECT
    YEAR(thisyear.trandte) AS `Year`,
    MONTH(thisyear.trandte) AS `YearMonth`,
    SUM(lastyear.totamount) AS LastYearSales,
    SUM(thisyear.totamount) AS ThisYearSales
FROM
    sync_invoice_lines thisyear
LEFT JOIN
    sync_invoice_lines lastyear ON
        MONTH(thisyear.trandte) = (MONTH(lastyear.trandte)) AND
        YEAR(thisyear.trandte) = (YEAR(lastyear.trandte) - 1)
WHERE
    thisyear.type = 'IN' AND
    lastyear.type = 'IN' AND
    thisyear.sync_active = 1 AND
    lastyear.sync_active = 1 AND
GROUP BY `Year`, `YearMonth`
</code></pre>

## Answers
### Answer ID: 63655772
<p>You can calculate the total separately for last year sales and this year sales with the CASE expression.
This is very simple.</p>
<p>The query is as follows:</p>
<pre><code>SELECT
    YEAR(CURRENT_DATE) AS `Year`,
    MONTH(trandte) AS `YearMonth`,
    SUM(CASE YEAR(trandte) WHEN YEAR(CURRENT_DATE)-1 THEN totamount END) AS LastYearSales,
    SUM(CASE YEAR(trandte) WHEN YEAR(CURRENT_DATE) THEN totamount END) AS ThisYearSales
FROM
    sync_invoice_lines
WHERE type = 'IN' AND sync_active = 1
GROUP BY `YearMonth`
ORDER BY `YearMonth`;
</code></pre>
<p><a href="https://www.db-fiddle.com/f/6NbwKqq4QmiKEwvd3sLsXV/1" rel="nofollow noreferrer">DB Fiddle</a></p>
<p>You can specify any year in the YEAR(CURRENT_DATE) part.</p>

### Answer ID: 63625411
<p>You can use pivot to display your sales for each month by year.</p>
<pre><code>with monthly_sales as  
(SELECT
    YEAR(trandte) AS year,
    MONTH(trandte) AS month,
    SUM(totamount) AS sales
FROM
    sync_invoice_lines 
WHERE
    type = 'IN' AND
    sync_active = 1
GROUP BY YEAR(trandte), MONTH(trandte)) 

Select * from 
(select month, year from monthly_sales)
pivot
(sum(sales) 
for month in (2013, 2014, 2015)
)
order by month
</code></pre>

### Answer ID: 63607801
<p>You can do that in a single table scan (without a join or CTE), and take in account possible missing month. For this, use <code>lag()</code> with a <code>range</code> clause that precisely targets the same month last year, like so:</p>
<pre><code>select
    year(trandte) as `year`,
    month(trandte) as `yearmonth`,
    lag(sum(totamount)) over(
        order by concat(year(trandte), '-', month(trandte), '-01') 
        range between interval 1 year preceding and interval 1 year preceding
    ) as lastyearsales,
    sum(totamount) as thisyearsales
from sync_invoice_lines
where type = 'IN' and sync_active = 1
group by year(trandte), month(trandte)
order by year(trandte), month(trandte)
</code></pre>

### Answer ID: 63564733
<p>Provided that you have data in the table for all months without any gaps, then all you need is the window function <code>LAG()</code> to fetch last year's sum of <code>totamount</code> for the same month:</p>
<pre><code>SELECT YEAR(trandte) AS Year, 
       MONTH(trandte) AS Month, 
       SUM(totamount) AS ThisYearSales,
       LAG(SUM(totamount), 12) OVER (ORDER BY YEAR(trandte), MONTH(trandte)) AS LastYearSales
FROM sync_invoice_lines 
WHERE type = 'IN' AND sync_active = 1
GROUP BY Year, Month
</code></pre>
<p>If there are gaps between the months then create a <code>CTE</code> from the above query and do a <code>LEFT</code> self join on it:</p>
<pre><code>WITH cte AS (
  SELECT YEAR(trandte) AS Year, 
         MONTH(trandte) AS Month, 
         SUM(totamount) AS Sales
  FROM sync_invoice_lines 
  WHERE type = 'IN' AND sync_active = 1
  GROUP BY Year, Month
)
SELECT c1.Year, 
       c1.Month,
       c1.Sales AS ThisYearSales,
       c2.Sales AS LastYearSales 
FROM cte c1 LEFT JOIN cte c2
ON c2.Year = c1.Year - 1 AND c2.Month = c1.Month
</code></pre>

### Answer ID: 63563956
<p>Step 1:  Calculate all monthly subtotals, no yr-over-yr <em>yet</em>:</p>
<pre><code>SELECT  LEFT(trandte, 7) AS yyyy_mm,
        SUM(totamount) AS sales
    FROM sync_invoice_lines
    WHERE ...
    GROUP BY 1;
</code></pre>
<p>First, see whether this gets the correct numbers, though not in the desired order.  And see how fast it goes.</p>
<p>That may be all you need.</p>
<p>Step 2:  This will be working with about 30 rows, so efficiency is not a problem.  Either put the above stuff in another table, or, since you have MySQL 8.0 (or MariaDB 10.2), use it in a <code>WITH</code> to do the rest of the work.  Step 2 is probably to compute the year over year, using a self-join.</p>
<p>Step 3:  The order of the output -- Or does the graphic package rearrange the data to get 12 sets of multiple years?</p>
<p>In the long run, consider building and maintaining a &quot;Summary table&quot;, perhaps of daily subtotals.  It would be like step 1, but thousands of rows, not millions or dozens.  With that, you could calculate monthly amounts quite fast.  Or weekly.  Or other ranges.  This way, the bulky task (step 1) is built in daily chunks, which will be a thousand times as fast.</p>
<p>More on subtotals:  <a href="http://mysql.rjweb.org/doc.php/summarytables" rel="nofollow noreferrer">http://mysql.rjweb.org/doc.php/summarytables</a></p>

