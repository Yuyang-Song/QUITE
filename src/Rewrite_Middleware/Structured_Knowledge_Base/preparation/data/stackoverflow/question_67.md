# SQL - Optimize date calculation for large table
[Link to question](https://stackoverflow.com/questions/11691216/sql-optimize-date-calculation-for-large-table)
**Creation Date:** 1343403749
**Score:** 4
**Tags:** sql, oracle-database, query-optimization
## Question Body
<p>Can this query below be optimized?</p>

<pre class="lang-sql prettyprint-override"><code>select
     max(date), sysdate - max(date)
 from
     table;
</code></pre>

<p>Query execution time ~5.7 seconds</p>

<p>I have another approach
</p>

<pre><code>select
    date, sysdate - date
from
    (select * from table order by date desc)
where
    rownum = 1;
</code></pre>

<p>Query execution ~7.9 seconds</p>

<p>In this particular case, table has around 17,000,000 entries.</p>

<p>Is there a more optimal way to rewrite this?</p>

<p><strong>Update</strong>: Well, I tried the hint a few of you suggested in a database development, although with a smaller subset than the original (approximately 1,000,000 records). Without the index the queries runs slower than with the index.</p>

<p>The first query, without index: ~0.56 secs, with index: ~0.2 secs. The second query, without index: ~0.41 secs, with index: ~0.005 secs. (This surprised me, I thought the first query would run faster than the second, maybe it's more suitable for smaller set of records).</p>

<p>I suggested to DBA this solution and he will change the table structure to accommodate this, and then i will test it with the actual data. Thanks</p>

## Answers
### Answer ID: 11691287
<p>That query is simple enough that there's likely nothing that can be done to optimize it beyond adding an index on the date column. What database is this? And is sysdate another column of the table?</p>

### Answer ID: 11691266
<p>Is there an index on the date column?</p>

