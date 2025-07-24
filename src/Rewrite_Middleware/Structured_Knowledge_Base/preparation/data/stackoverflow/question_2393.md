# Improving performances of nodejs and MySql
[Link to question](https://stackoverflow.com/questions/32564919/improving-performances-of-nodejs-and-mysql)
**Creation Date:** 1442233941
**Score:** 0
**Tags:** mysql, node.js, performance
## Question Body
<p>I'm rewriting a php application in nodejs.</p>

<p>I'm facing an issue with performances when querying a mysql database.</p>

<p>I'm executing the following query:</p>

<pre><code>START TRANSACTION;

SELECT id
FROM stock
WHERE id IN (
  SELECT id
  FROM stock
  WHERE warehouse = 1
) ORDER BY id
FOR UPDATE;

DELETE FROM stock WHERE warehouse = 1;

LOAD DATA LOCAL INFILE '/tmp/28718734728601.csv'
INTO TABLE stock FIELDS
TERMINATED BY ';'
ENCLOSED BY '"'
(sku, qty, warehouse);

COMMIT;
</code></pre>

<p>Running it in PHP using PDO it takes around 3 seconds.
Running it in Nodejs using <a href="https://github.com/felixge/node-mysql/" rel="nofollow">mysql</a> or <a href="https://github.com/sidorares/node-mysql2" rel="nofollow">mysql2</a> it takes around 5 seconds.</p>

<p>The query is locking rows on the <code>stock</code> table and a 2/3 seconds lock is ok, but 5 or more is too much in my context.</p>

<p>Does anyone have any suggestion/idea on how to improve performances for this?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 32575198
<ul>
<li><p>Don't use that subquery in the SELECT.  It is (1) inefficient, and (2) unnecessary.</p></li>
<li><p>Don't even have the SELECT -- You are not getting any values from it, and the DELETE will lock the rows promptly anyway.</p></li>
</ul>

<p>How many rows are in warehouse #1?  Is the LOAD reloading all the #1 values?</p>

