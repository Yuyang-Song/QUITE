# Why why &#39;=&#39; does not work in this SQL query?
[Link to question](https://stackoverflow.com/questions/58156882/why-why-does-not-work-in-this-sql-query)
**Creation Date:** 1569772698
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have a query against the sakila database in MySQL 8(You can easily setup one from <a href="https://hub.docker.com/r/1maa/sakila" rel="nofollow noreferrer">https://hub.docker.com/r/1maa/sakila</a>).</p>

<pre><code>select * from store _0 where (
    select address_id from (
        select * from address _3 where (
            address_id = (
                select address_id from (
                    select * from store _1
                    where store_id=_0.store_id
                ) _2
            )
        )
    ) _4
);
</code></pre>

<p>This query returns an empty table.</p>

<p>However, when I rewrite the innermost</p>

<pre><code>                select address_id from (
                    select * from store _1
                    where store_id=_0.store_id
                ) _2
</code></pre>

<p>into:</p>

<pre><code>                select address_id from store _1
                where store_id=_0.store_id
</code></pre>

<p>, it returns all 2 rows from <code>store</code> table, which I expect.</p>

<p>Why is this? It seems I just simplified a 2-step select into 1.</p>

<p>I also noticed that if I use <code>in</code> instead of <code>=</code> in <code>address_id = ..</code> condition, I can get the expected result.</p>

<p>What's the theory behind this?</p>

<p>The query is over-complicated because it's generated. So thank you for your advice of simplified queries but I just want to know why it does not give the correct result.</p>

<p>And you must have MySQL 8.0.14 and above to reproduce it, because earlier versions does not allow alias beyond 1 level.</p>

## Answers
### Answer ID: 58204143
<p>I reported this to MySQL. This is confirmed to be an optimizer bug: <a href="https://bugs.mysql.com/bug.php?id=97063" rel="nofollow noreferrer">https://bugs.mysql.com/bug.php?id=97063</a>.</p>

### Answer ID: 58157704
<pre><code>            select address_id from (
                select * from store _1
                where store_id=_0.store_id
            ) _2
</code></pre>

<p>In the first code snippet, you are selecting the columns from store _1 that have the equivalent store_id entries as store _0. If the comparison statement returns true, the address_id is retrieved from these columns, but what if no address_id entries are stored in these columns?</p>

<pre><code>            select address_id from store _1
            where store_id=_0.store_id
</code></pre>

<p>In the second code snippet, you are selecting the address_id from store _1 where the comparison of store_ids of store _0 and _1 returns true. The scope for selecting the address_id in store _1 is broader than in the first code snippet, thus the address_id can be retrieved.</p>

<p>TL;DR The different results have everything to do with the scope of your searches and the structure of data in the relational database!</p>

### Answer ID: 58157098
<p>The reason you would need an in clause is because the sub select is returning multiple results.</p>

<p>Are you just trying to join the two tables? Why not use a join instead of the subselects?</p>

<pre><code>SELECT s.* 
  FROM store s
  JOIN address a
    ON a.address_id = s.address_id
</code></pre>

