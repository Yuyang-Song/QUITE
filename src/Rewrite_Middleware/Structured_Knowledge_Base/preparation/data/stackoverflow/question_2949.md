# Trouble writing recursive query
[Link to question](https://stackoverflow.com/questions/59743920/trouble-writing-recursive-query)
**Creation Date:** 1579050643
**Score:** 0
**Tags:** sql, recursion, teradata, recursive-query
## Question Body
<p>I apologize for how potentially cluttered the explanation to my problem might be. I've
included details so that things make as much sense as possible leading up to the main
obstacle I've come across.</p>

<p>I'm working within Teradata using two tables that look like the following</p>

<pre><code>Table Name             Fields
Sales                (ID, Sales)
Discounts       (ID, PromoNum, Discount)
</code></pre>

<p>The <code>PromoNum</code> field consists of 9 digit unique promotion numbers which correspond to coupons.
This helps track whenever a transaction includes a specific coupon that was used. Each 
transaction can have more than 1 coupon applied. </p>

<p>I'm trying to create a recursive query which pulls sales and discounts for a given set of coupons
in an iterative manner. The reason I'm doing so iteratively is because it is possible that a 
single transaction can have more than 1 coupon applied (for 1 or more items). If I was avoid the 
recursive query route and do an inner join on <code>ID</code> for example, it is possible that I could duplicate 
records unnecessarily where two or more promo numbers were used within the same transaction, resulting
in potentially greater sales or discounts than actual. On top of this, I only have read access
to the database.</p>

<p>I've created a temp table called <code>Promos</code> with 3 specific promotions that I want to run interatively 
and has the fields <code>PromoNum</code> and <code>PromoIndex</code>. <code>PromoIndex</code> is essentially the row number for each
promotion which I attempt to utilize in an interative manner below.</p>

<p>The recursive query I've writtens so far is as below. It doesn't work as expected due to the logic
behind the line I've commented. I need to rewrite this portion to make sure it simply runs for
the promotion number corresponding to the index at that specific iteration. For instance, when it
is at iteration 2, it will technically join on PromoIndex 1 and PromoIndex 2 when it should only run
for PromoIndex 2 if that makes sense. I've attempted to rewrite it while remaining within what's 
allowed in a recursive query and I can't figure it out.</p>

<pre><code>WITH RECURSIVE PromoData AS
(
SELECT 
  1 AS PromoIndex
  , 1 AS PromoNum --dummy column
  , 0 AS Sales --dummy column
  , 0 AS Discounts --dummy column
FROM 
Dummy Table

UNION ALL

SELECT 
  PromoData.PromoIndex + 1
  , PromoData.PromoNum
  , Sales.Sales
  , Discounts.Discounts --Edited here
FROM Sales
INNER JOIN Discounts on Sales.ID = Discounts.ID
INNER JOIN Promos on Promos.PromoNum = Discounts.PromoNum and Promos.PromoIndex = PromoData.PromoIndex --Problematic portion here
WHERE PromoData.PromoIndex &lt;= 3
)
SELECT *
FROM PromoData
</code></pre>

## Answers
### Answer ID: 59747043
<p>Recursive queries are normally used to resolve multiple layers of hierarchical rows, like those with a parent / child relationship.  I don't think that is needed in this case.</p>

<p>The main issue I see here is you're trying to relate sales and discounts, but I don't see a natural way to do that.  For example, if a transaction has $100 of sales and two discounts of $10 and $20 how much of the $100 gets attributed to each discount?  I think this is what you meant by "two or more promo numbers being used within the same transaction" causing inflated figures.</p>

<p>Assuming your <code>ID</code> field is used as a <code>transaction_ID</code>, you can try something like:</p>

<pre class="lang-sql prettyprint-override"><code>WITH coupons AS (
  SELECT 'PromoID1' AS PromoNum UNION ALL
  SELECT 'PromoID2' AS PromoNum UNION ALL
  SELECT 'PromoID3' AS PromoNum
)
SELECT 
  c.PromoNum, 
  COALESCE(info.sales, 0) sales, 
  COALESCE(info.discounts, 0) discounts
FROM coupons c -- get all specified coupons
LEFT JOIN (
  SELECT 
    MAX(s.sales) sales,
    SUM(d.discount) discounts, -- Get total discount for txn
    MAX(d.PromoNum) AS PromoNum -- Pick a single PromoNum
  FROM sales s -- Get all sales
  LEFT JOIN discounts d ON s.ID = d.ID -- Get any discounts applied to sales
  GROUP BY s.ID -- One row per txn (avoid double counting sales)
) info ON c.PromoNum = info.PromoNum -- Get related sales / discounts per PromoNum
</code></pre>

<p>The difference here is that in the case of a transaction with multiple discounts, all of the sales for that transaction will only be associated with a single PromoNum.  This way you won't get inflated sales numbers.  </p>

<p>Not sure if that's what you're after, but hope that helps.</p>

### Answer ID: 59743939
<p>From what you describe, you want:</p>

<pre><code>select s.*
from sales s
where exists (select 1
              from discounts d join
                   promos p
                   on d.promonum = p.promonum
              where d.id = s.id 
             );
</code></pre>

<p>I don't see what a recursive query has to do with the problem you have described.</p>

