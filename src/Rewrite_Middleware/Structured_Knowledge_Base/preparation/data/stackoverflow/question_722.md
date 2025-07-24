# UNION that filters by a Table
[Link to question](https://stackoverflow.com/questions/38933932/union-that-filters-by-a-table)
**Creation Date:** 1471100049
**Score:** 0
**Tags:** postgresql
## Question Body
<p>I'm missing something fundamental in my query.
I have three transaction tables (expenses, bills, income) that I want to sum by their category type (categories) in a given time period.</p>

<p>I've joined three selects by a UNION and they return category sums, but the query returns duplicate categories from each select.</p>

<p>Here is a quick gist of the query - <a href="https://gist.github.com/telagraphic/2e3af3c39211a761af37fe9ba4aceddf" rel="nofollow noreferrer">https://gist.github.com/telagraphic/2e3af3c39211a761af37fe9ba4aceddf</a></p>

<p>How would I get each category to sum for all selects in the UNION?</p>

<p>Query:</p>

<p>I have 28 categories that I would like to sum all transaction amounts for by a given time period.
When I run each select statement for each table by itself, I get the 28 rows per each category.
When I use the UNION for all three tables, I get more than 28 records.
It includes the 'duplicate' category when there is a amount for that category.
I know that UNION will not include duplicates...
I need to rewrite this query to return expenses, bills and income summed against each category.
I would prefer to do this in the database than using some reduce on the client.</p>

<p>I have tried several re-writes, but any suggestions on how to write a query would be helpful.
Still not seeing the solution...</p>

<pre><code>SELECT cat.name AS category, SUM(ex.amount) AS weekly_total, trx.id    AS type
FROM categories cat
FULL OUTER JOIN expenses ex ON (cat.id = ex.categorytype)
AND date_trunc('month', ex.trxdate) = date_trunc('month', current_date)
INNER JOIN transaction_type trx ON (cat.transactiontype = trx.id)
GROUP BY cat.name, trx.id
UNION
SELECT cat.name AS category, SUM(bl.amount) AS weekly_total, trx.id AS type
FROM categories cat
FULL OUTER JOIN bills bl ON (cat.id = bl.categorytype)
AND date_trunc('month', bl.paiddate) = date_trunc('month', current_date)
INNER JOIN transaction_type trx ON (cat.transactiontype = trx.id)
GROUP BY cat.name, trx.id
UNION
SELECT cat.name AS category, SUM(inc.netamount) AS weekly_total, trx.id AS type
FROM categories cat
FULL OUTER JOIN income inc ON (cat.id = inc.categorytype)
AND date_trunc('month', inc.payday) = date_trunc('month', current_date)
INNER JOIN transaction_type trx ON (cat.transactiontype = trx.id)
GROUP BY cat.name, trx.id;
</code></pre>

<p>This returns duplicates for each select:</p>

<p><a href="https://i.sstatic.net/Mfk7v.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Mfk7v.png" alt="enter image description here"></a></p>

<p>I would the query to return by each category like this</p>

<p><a href="https://i.sstatic.net/DDNCL.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/DDNCL.png" alt="enter image description here"></a></p>

## Answers
### Answer ID: 38933995
<p>You can do something like this:</p>

<pre><code>select category, sum(amount)
from ((select category, amount from expenses) union all
      (select category, amount from bills) union all
      (select category, amount from income)
     ) c
group by category;
</code></pre>

<p>Note:  It is better to put the image directly in the question -- or better yet, to put the query in <em>as text</em>.  That way, people who are answering can use your query as the basis for the answer.</p>

