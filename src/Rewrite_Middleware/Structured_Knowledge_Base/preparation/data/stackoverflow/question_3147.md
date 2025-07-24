# Is it possible to improve the performance of query with distinct?
[Link to question](https://stackoverflow.com/questions/68727706/is-it-possible-to-improve-the-performance-of-query-with-distinct)
**Creation Date:** 1628602112
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>There is following query:</p>
<pre><code>        &quot;SELECT DISTINCT LEVEL, ID, R1, R2, R3, R4, R5&quot; +
        &quot; FROM custom_table +
        &quot; WHERE fromDate=:startDate 
        &quot; AND toDate=:endDate, 
        &quot; AND AccountIds=[ :accountIds ]
        &quot; AND LEVEL IN (:Levels)&quot;
</code></pre>
<p>Some columns of the table (exclude dates and other non-important columns for us):</p>
<pre><code>ID INTEGER NOT NULL,
LEVEL INTEGER,
R1 VARCHAR(50),
R2 VARCHAR(50),
R3 VARCHAR(50),
R4 VARCHAR(50),
R5 VARCHAR(50)
</code></pre>
<p>Simple data:</p>
<pre><code>ID,LEVEL,R1,R2,R3,R4,R5
id1,1,TOTAL,null,null,null,null
id1,2,TOTAL,A,null,null,null
id1,2,TOTAL,B,null,null,null
id2,1,TOTAL,null,null,null,null
id2,2,TOTAL,A,null,null,null
id2,3,TOTAL,B,C,null,null
</code></pre>
<p>Current query is running more than 1s, usually it returns between 100 and 1000 records, I want to improve the performance of this query. I have tried to rewrite it with <code>GROUP BY</code> clause but it is overkill because there are no aggregation and it is redundant, I think.</p>
<p>Maybe there are ways to improve this query to fetch data a bit faster? I hope I've provided enough information here. Database is custom, NO_SQL giant under the hood but syntax of our database bridge is very similar to MySQL.</p>

## Answers
### Answer ID: 68730294
<p>You would seem to want an index on:  <code>(fromDate, toDate, accountId, levels)</code>.</p>
<p>The first three columns are all used for <code>=</code> comparisons, so they can be in any order.</p>

