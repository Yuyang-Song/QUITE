# Postgres chooses wrong query plan
[Link to question](https://stackoverflow.com/questions/29120658/postgres-chooses-wrong-query-plan)
**Creation Date:** 1426677595
**Score:** 1
**Tags:** postgresql, indexing, amazon-rds, sql-execution-plan
## Question Body
<p>I have problems with a query that uses a wrong query plan. Because of the non-optimal query plan the query takes almost 20s.</p>

<p>The problem occurs only for a small number of owner_ids. The distribution of the owner_ids is not uniform. The owner_id in the example has 7948 routes. The total number of routes is 2903096.</p>

<p>The database is hosted on Amazon RDS on a server with 34.2 GiB memory, 4vCPU and provisioned IOPS (instance type db.m2.2xlarge). The Postgres version is 9.3.5.</p>

<pre><code>EXPLAIN ANALYZE SELECT
    route.id, route_meta.name
FROM
    route
INNER JOIN
    route_meta
USING (id)
WHERE
    route.owner_id = 128905
ORDER BY
    route_meta.name
LIMIT
    61

Query plan:    
"Limit  (cost=0.86..58637.88 rows=61 width=24) (actual time=49.731..18828.052 rows=61 loops=1)"
"  -&gt;  Nested Loop  (cost=0.86..7934263.10 rows=8254 width=24) (actual time=49.728..18827.887 rows=61 loops=1)"
"        -&gt;  Index Scan using route_meta_i_name on route_meta  (cost=0.43..289911.22 rows=2902910 width=24) (actual time=0.016..2825.932 rows=1411126 loops=1)"
"        -&gt;  Index Scan using route_pkey on route  (cost=0.43..2.62 rows=1 width=4) (actual time=0.009..0.009 rows=0 loops=1411126)"
"              Index Cond: (id = route_meta.id)"
"              Filter: (owner_id = 128905)"
"              Rows Removed by Filter: 1"
"Total runtime: 18828.214 ms"
</code></pre>

<p>If I increase the limit to 100, a better query plan is used. It takes now less then 100ms.</p>

<pre><code>EXPLAIN ANALYZE SELECT
    route.id, route_meta.name
FROM
    route
INNER JOIN
    route_meta
USING (id)
WHERE
    route.owner_id = 128905
ORDER BY
    route_meta.name
LIMIT
    100

Query plan:
"Limit  (cost=79964.98..79965.23 rows=100 width=24) (actual time=93.037..93.294 rows=100 loops=1)"
"  -&gt;  Sort  (cost=79964.98..79985.61 rows=8254 width=24) (actual time=93.033..93.120 rows=100 loops=1)"
"        Sort Key: route_meta.name"
"        Sort Method: top-N heapsort  Memory: 31kB"
"        -&gt;  Nested Loop  (cost=0.86..79649.52 rows=8254 width=24) (actual time=0.039..77.955 rows=7948 loops=1)"
"              -&gt;  Index Scan using route_i_owner_id on route  (cost=0.43..22765.84 rows=8408 width=4) (actual time=0.023..13.839 rows=7948 loops=1)"
"                    Index Cond: (owner_id = 128905)"
"              -&gt;  Index Scan using route_meta_pkey on route_meta  (cost=0.43..6.76 rows=1 width=24) (actual time=0.003..0.004 rows=1 loops=7948)"
"                    Index Cond: (id = route.id)"
"Total runtime: 93.444 ms"
</code></pre>

<p>I already tried following things:</p>

<ul>
<li><p>increasing statistics for owner_id (The owner_id in the example is included in the pg_stats)</p>

<p>ALTER TABLE route ALTER COLUMN owner_id SET STATISTICS 1000;</p></li>
<li><p>reindex owner_id and name</p></li>
<li><p>vacuum analyse</p></li>
<li><p>increased work_mem from 1MB to 16MB</p></li>
<li><p>when I rewrite the query to <code>row_number() OVER (ORDER BY xxx) AS rn
... WHERE rn &lt;= yyy</code> in a subquery, the specific case is solved. However it
introduces performance problems with other ownerids.</p></li>
</ul>

<p>A similar problem was solved with a combined index, but that seems impossible here because of the different tables.
<a href="https://stackoverflow.com/questions/28740639/postgres-uses-wrong-index-in-query-plan">Postgres uses wrong index in query plan</a></p>

