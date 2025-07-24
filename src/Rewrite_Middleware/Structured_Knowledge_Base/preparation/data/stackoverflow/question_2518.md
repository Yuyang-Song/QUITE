# Faster query performance for single table
[Link to question](https://stackoverflow.com/questions/38034101/faster-query-performance-for-single-table)
**Creation Date:** 1466900113
**Score:** 0
**Tags:** mysql, sql, query-optimization, query-performance
## Question Body
<p>I'm running queries on a single table. </p>

<p>example</p>

<pre><code>SELECT firstName, COUNT(*) as num_bob
FROM DataTable
WHERE firstName= "bob"
</code></pre>

<p>A query similar to the one above takes a long time.
The database/table does not use indexing and all the data is stored in a single table. Is there a way to rewrite this query to improve performance?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 38035379
<p>First of all if Group By is not required please remove it. If required use DISTINCT and ORDER BY instead of GROUP BY. See <a href="https://stackoverflow.com/questions/581521/whats-faster-select-distinct-or-group-by-in-mysql">this</a></p>

<p>You may check your ISOLATION LEVEL. If it is under Serializable then no worries. But if it is then stopping other quires to Datable will increase your performance.</p>

<p>Also See <a href="https://stackoverflow.com/questions/2710621/count-vs-count1-vs-countpk-which-is-better">this</a>. You are OK for this I think.</p>

### Answer ID: 38034627
<p>You can try</p>

<p>"create table  as ( your select query " ) and than select this table</p>

<p>This is faster than normal select.</p>

### Answer ID: 38034428
<p>Try removing GROUP BY...</p>

<pre><code>SELECT firstName, COUNT(*) as num_bob
FROM DataTable
WHERE firstName="bob";
</code></pre>

<p>It should give you the same results.</p>

