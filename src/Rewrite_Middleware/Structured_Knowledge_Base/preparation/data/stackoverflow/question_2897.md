# Different postgrese behavior in similar databases
[Link to question](https://stackoverflow.com/questions/57755978/different-postgrese-behavior-in-similar-databases)
**Creation Date:** 1567422862
**Score:** 0
**Tags:** postgresql, group-by, php-pgsql, sql-mode
## Question Body
<p>I use PHP 7.1 with Pgsql 9.2.24. Have two similar copy of project (production and development) and two similar databases with the same data on it. But queries work differently in GROUP BY case.</p>

<p>I tried to check all the sql settings with SHOW ALL query, but found no difference. I know, that rewriting query can solve my problem, but there is too many code with GROUP BY operator.
Full SQL version: PostgreSQL 9.2.24 on x86_64-redhat-linux-gnu, compiled by gcc (GCC) 4.8.5 20150623 (Red Hat 4.8.5-28), 64-bit.
Trying run sql-query:</p>

<p><code>SELECT  chr.*, usr.image, usr.first_name, usr.second_name, usr.last_activity, CASE WHEN MAX(chrm.created_at) IS NOT NUll THEN MAX(chrm.created_at) ELSE 0 END AS created_m, MAX(chrm.id) AS id_m FROM chat_rooms as chr  LEFT JOIN users usr ON chr.author_id = usr.id  LEFT JOIN chat_messages chrm ON chr.id = chrm.chat_id  LEFT JOIN chat_rooms_user chru ON chr.id = chru.chat_rooms_id  WHERE chru.user_id = 1104 AND chru.status = 1 AND ( chrm.status != 10 OR chrm.status IS NULL) AND chr.status =  1 GROUP BY chr.id, usr.id HAVING coalesce(COUNT(chrm.id),0) &gt; 0 ORDER BY created_m DESC LIMIT 10 OFFSET 0</code></p>

<p>And get error (server status 500):
Uncaught Exception: ERROR:  column &quot;chr.parent_id&quot; must appear in the GROUP BY clause or be used in an aggregate function</p>

<p>Other database returns me not errors but correct result with the data.</p>

