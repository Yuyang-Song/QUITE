# SQL conditional join challenge
[Link to question](https://stackoverflow.com/questions/11478287/sql-conditional-join-challenge)
**Creation Date:** 1342213167
**Score:** 0
**Tags:** mysql, sql, join, conditional-statements
## Question Body
<p>I have 2 tables stores and shares in a mysql database. I am trying to avoid an IN clause. Please see below for more details</p>

<pre><code>select id, user_id from stores where user_id =7;
+----+---------+
| id | user_id |
+----+---------+
| 36 |       7 |
| 37 |       7 |


select stores_id,share_id from shares where share_id=7;
+-----------+----------+
| stores_id | share_id |
+-----------+----------+
|        15 |        7 |
|        38 |        7 |
</code></pre>

<p>Now I run this </p>

<pre><code>SELECT stores.id
FROM   stores
WHERE  user_id = 7
UNION
(SELECT stores.id
 FROM   stores
 WHERE  id IN (SELECT stores_id
               FROM   shares
               WHERE  share_id = 7)); 
</code></pre>

<p>To get the below result:</p>

<pre><code>+----+
| id |
+----+
| 36 |
| 37 |
| 15 |
| 38 |
+----+
</code></pre>

<p><b>QUESTION</b>
How can I rewrite the query so that I don't use the <b>  IN </b> key word.?</p>

## Answers
### Answer ID: 11478399
<p>A left join should accomplish what you are looking for:</p>

<pre><code>select distinct stores.id 
from stores 
left join shares on stores.id = shares.stores_id
where stores.user_id = 7 
or shares.share_id = 7
</code></pre>

### Answer ID: 11478394
<p>If all you need is the ID, this will do just fine...</p>

<pre><code>SELECT stores.id
FROM   stores
WHERE  user_id = 7

UNION

SELECT stores_id as id
FROM   shares
WHERE  share_id = 7
</code></pre>

<p>But if you need some data from the other columns in the stores table, INNER JOIN or EXISTS will be your best bet.</p>

### Answer ID: 11478327
<p>This can help to you:</p>

<pre><code>select stores.id from stores where user_id = 7  
UNION  
select s1.id from stores s1 
       inner join shares s2 
       on s2.share_id = 7 
       and s1.id = s2.stores_id;
</code></pre>

### Answer ID: 11478343
<p>You can use either <code>EXISTS</code>:</p>

<pre><code>WHERE EXISTS
       ( SELECT 1
           FROM shares
          WHERE share_id = 7
            AND stores_id = stores.id
       )
</code></pre>

<p>or <code>JOIN</code>:</p>

<pre><code>JOIN shares
  ON shares.stores_id = stores.id
 AND shares.share_id = 7
</code></pre>

<p>(Note that the <code>JOIN</code> potentially returns multiple copies of some stores, but because <code>UNION</code> implies <code>SELECT DISTINCT</code>, that won't actually affect your final result-set.)</p>

