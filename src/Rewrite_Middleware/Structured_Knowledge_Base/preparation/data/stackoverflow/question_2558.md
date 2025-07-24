# Rewriting a query that has two sub queries using no sub queries
[Link to question](https://stackoverflow.com/questions/40139254/rewriting-a-query-that-has-two-sub-queries-using-no-sub-queries)
**Creation Date:** 1476902677
**Score:** -1
**Tags:** mysql, sql
## Question Body
<p>Given the database schema:</p>

<pre><code>Part( PID, PName, Producer, Year, Price)
Customer( CID, CName, Province)
Supply(SID, PID, CID, Quantity, Amount, Date)
</code></pre>

<p>And the query:</p>

<pre><code>Select cname, Province
From Customer c
Where exists (
    Select * 
    from Supply s
    join Part p on p.pId = s.pId 
    Where CId = c.CId 
    and p.Producer = 'Apple'
)
and Not exists (
    Select * 
    from Supply n
    join Part nap on nap.pId = n.pId 
    Where CId = c.CId 
    and nap.Producer != 'Apple'
)
</code></pre>

<p>How would I go about rewriting this query without the two sub queries? </p>

## Answers
### Answer ID: 40139515
<p>You can use the <code>LEFT JOIN/NULL</code> pattern to find customers who haven't bought any non-Apple products. Then you can do this all with just joins. You'll have to join with <code>Supply</code> and <code>Parts</code> twice, once for finding Apple products, then again for excluding non-Apple products.</p>

<pre><code>SELECT distinct c.name, c.province
FROM Customer AS c
JOIN Supply AS s1 ON s1.cid = c.cid
JOIN Parts AS p1 ON p1.pid = s1.pid
LEFT JOIN Supply AS s2 ON s2.cid = c.cid
LEFT JOIN Parts AS p2 ON p2.pid = s2.pid AND p2.producer != 'Apple'
WHERE p1.producer = 'Apple' AND p2.pid IS NULL
</code></pre>

<p>Notice that in the <code>LEFT JOIN</code> you put restrictions of the second table in the <code>ON</code> clause, not the <code>WHERE</code> clause. See <a href="https://stackoverflow.com/questions/21633115/return-row-only-if-value-doesnt-exist?lq=1">Return row only if value doesn&#39;t exist</a> for more about this part of the query.</p>

### Answer ID: 40139366
<p>You want customer who only bought Apple products?</p>

<p>One possible solution is based on conditional aggregation:</p>

<pre><code>Select c.cname, c.Province
From Customer c
join
 ( -- this is not a Subquery, it's a Derived Table
   Select s.CId -- assuming there's a CId in Supply
   from Supply s
   join Part p
     on p.pId = s.pId
   group by s.CId 
   -- when there's any other supplier this will return 1
   having max(case when p.Producer = 'Apple' then 0 else 1 end) = 0
 ) as p
on p.CId = c.CId 
</code></pre>

