# Rewrite SQL for best performance (oracle)
[Link to question](https://stackoverflow.com/questions/57050169/rewrite-sql-for-best-performance-oracle)
**Creation Date:** 1563252110
**Score:** -3
**Tags:** sql, oracle-database, performance, query-optimization, oracle12c
## Question Body
<p>We are wondering what the best way is to rewrite the following SQL so it can perform better in Oracle database. </p>

<p>As you see, the query was to filter from two tables (Period and Account) based on the data based on the keys. I believe this can be tweaked very well, may be replacing <code>&lt;&gt;</code> with <code>!=</code> would give any benefits etc. </p>

<pre><code>SELECT 
    p.key, p.period 
FROM 
    Period p 
WHERE
    p.version = 0 
    AND p.balance &lt;&gt; 0 
    AND EXISTS (SELECT 1 
                FROM Period p2 
                WHERE p2.jointKey &lt;&gt; 0 
                  AND p.key = p2.jointKey 
                  AND p.period = p2.period 
                  AND EXISTS (SELECT 1 FROM Account a 
                              WHERE a.customerKey = :B1 AND a.key = p.jointKey) );
</code></pre>

## Answers
### Answer ID: 57050265
<p>Please verify index of the tables and query decide to part.</p>

<pre><code>(SELECT 1 FROM Account a WHERE a.customerKey = :B1 AND a.key = p.jointKey)

(SELECT 1 FROM Period p2 WHERE p2.jointKey &lt;&gt; 0 AND p.key = p2.jointKey AND p.period = p2.period AND EXISTS  );


SELECT p.key, p.period FROM Period p WHERE p.version = 0 AND p.balance &lt;&gt; 0 AND EXISTS 
</code></pre>

### Answer ID: 57050225
<p>One of the rewrites will be like following</p>

<pre><code>SELECT p1.key, p1.period 
FROM Period p1 
join Period p2 on p1.key = p2.jointKey AND p1.period = p2.period and p2.jointKey &lt;&gt; 0
join Account a on a.key = p.jointKey
WHERE p.version = 0
and a.customerKey = :B1
</code></pre>

