# Optimize a query with IN() clauses
[Link to question](https://stackoverflow.com/questions/10143568/optimize-a-query-with-in-clauses)
**Creation Date:** 1334330194
**Score:** 2
**Tags:** mysql
## Question Body
<p>Reading <a href="http://forge.mysql.com/wiki/Top10SQLPerformanceTips" rel="nofollow">this wiki article</a>, I found out that the SELECT performance is killed if using IN() clauses with indexed columns in a MySQL database. My question is, how can I rewrite my query so that it won't use any IN() clause while still keeping its functionality?</p>

<p>My query is:</p>

<pre><code>SELECT 
    `Route`.`route_id`, `Route`.`order`, `Route2`.`order` 
FROM 
    `routes` AS `Route` 
INNER JOIN 
    `routes` AS `Route2` 
ON `Route`.`route_id` = `Route2`.`route_id` 
WHERE 
    `Route`.`station_line_id` IN ([10 values]) AND 
    `Route2`.`station_line_id` IN ([10 values]) AND 
    `Route`.`order` &lt;= `Route2`.`order` 
GROUP BY `
    `Route`.`station_line_id`, `Route2`.`station_line_id`, (`Route2`.`order` - `Route`.`order`)
</code></pre>

<p>and I have indexed all columns (route_id, station_line_id, station_id and line_id), with the id column being the primary key (the table is just read-only once generated, so no worries for indexing everything). The <code>[10 values]</code> in the IN() clause are comma separated, like: <code>IN(1, 2, ..., 10)</code>.</p>

<p>Basically, I self join the table routes table and group the results to get the desired records. The other joins are used for retrieving associated data. </p>

<p>Performance-wise, using InnoDB storage engine, I execute a similar query in >30seconds. Using MyISAM, I get >5seconds. But I believe results can be fetched even faster. I have ~4.5 million records in the table.</p>

## Answers
### Answer ID: 10143814
<p>You'll get the best performance in a query like this using a 'Hash index'. The 'standard' index is a B+ tree, which allows you to lookup entries in log(n) time where n is the number of rows in the table. They also maintain sorted order, so you can efficiently do queries like <code>... WHERE station_line_id &gt; 14</code>, so that's what you'll want to use on your <code>Order</code> column.</p>

<p>In your case, however, with an <code>IN</code> clause, you're only looking for equivalence. In that case, a B+ tree is going to have to lookup all m of your "[10 values]" separately, costing you m * log(n) time, which is apparently taking 5-30 seconds.</p>

<p>A hash index is used to lookup equivalent entries in a constant amount of time (very fast) which doesn't depend (theoretically) on the number of rows in your table -- it will always be very fast even on large tables. The downside of a hash index is that you can't use it to do queries like <code>&lt;</code> or <code>&gt;</code>, but it's the fastest at equivalence queries like the ones you're doing in your <code>IN</code> clause in <code>station_line_id</code>.</p>

<p><strong>Edit:</strong> For MySQL specifically, they unfortunately don't support HASH indexes on any of their popular database engines. If you're able to use the MEMORY or HEAP engine, then you could use a HASH index -- and having everything in memory will likely improve performance quite a bit anyways. Worth a shot.</p>

