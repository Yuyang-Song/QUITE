# Why Postgres EXPLAIN ANALYSE report huge performance difference compare to real query execution
[Link to question](https://stackoverflow.com/questions/66488886/why-postgres-explain-analyse-report-huge-performance-difference-compare-to-real)
**Creation Date:** 1614931652
**Score:** 0
**Tags:** sql, postgresql, sql-execution-plan
## Question Body
<p>I have been tasked with rewriting some low performance sql in our system for which I have this query</p>
<pre><code>select
    &quot;aggtable&quot;.id as t_id,
    count(joined.packages)::integer as t_package_count,
    sum(coalesce((joined.packages -&gt;&gt; 'weight'::text)::double precision, 0::double precision)) as t_total_weight
from
    &quot;aggtable&quot;
join (
    select
        &quot;unnested&quot;.myid, json_array_elements(&quot;jsontable&quot;.jsondata) as packages
    from
        (
        select
            distinct unnest(&quot;tounnest&quot;.arrayofid) as myid
        from
            &quot;aggtable&quot; &quot;tounnest&quot;) &quot;unnested&quot;
    join &quot;jsontable&quot; on
        &quot;jsontable&quot;.id = &quot;unnested&quot;.myid) joined on
    joined.myid = any(&quot;aggtable&quot;.arrayofid)
group by
    &quot;aggtable&quot;.id
</code></pre>
<p>The EXPLAN ANALYSE result is</p>
<pre><code>        Sort Method: quicksort  Memory: 611kB
        -&gt;  Nested Loop  (cost=30917.16..31333627.69 rows=27270 width=69) (actual time=4.028..2054.470 rows=3658 loops=1)
              Join Filter: ((unnest(tounnest.arrayofid)) = ANY (aggtable.arrayofid))
              Rows Removed by Join Filter: 9055436
              -&gt;  ProjectSet  (cost=30917.16..36645.61 rows=459000 width=48) (actual time=3.258..13.846 rows=3322 loops=1)
                    -&gt;  Hash Join  (cost=30917.16..34316.18 rows=4590 width=55) (actual time=3.246..7.079 rows=1661 loops=1)
                          Hash Cond: ((unnest(tounnest.arrayofid)) = jsontable.id)
                          -&gt;  Unique  (cost=30726.88..32090.38 rows=144700 width=16) (actual time=1.901..3.720 rows=1664 loops=1)
                                -&gt;  Sort  (cost=30726.88..31408.63 rows=272700 width=16) (actual time=1.900..2.711 rows=1845 loops=1)
                                      Sort Key: (unnest(tounnest.arrayofid))
                                      Sort Method: quicksort  Memory: 135kB
                                      -&gt;  ProjectSet  (cost=0.00..1444.22 rows=272700 width=16) (actual time=0.011..1.110 rows=1845 loops=1)
                                            -&gt;  Seq Scan on aggtable tounnest  (cost=0.00..60.27 rows=2727 width=30) (actual time=0.007..0.311 rows=2727 loops=1)
                          -&gt;  Hash  (cost=132.90..132.90 rows=4590 width=55) (actual time=1.328..1.329 rows=4590 loops=1)
                                Buckets: 8192  Batches: 1  Memory Usage: 454kB
                                -&gt;  Seq Scan on jsontable  (cost=0.00..132.90 rows=4590 width=55) (actual time=0.006..0.497 rows=4590 loops=1)
              -&gt;  Materialize  (cost=0.00..73.91 rows=2727 width=67) (actual time=0.000..0.189 rows=2727 loops=3322)
                    -&gt;  Seq Scan on aggtable  (cost=0.00..60.27 rows=2727 width=67) (actual time=0.012..0.317 rows=2727 loops=1)
Planning Time: 0.160 ms
Execution Time: 2065.268 ms
</code></pre>
<p>I tried to rewrite this query from scratch to profile performance and to understand the original intention</p>
<pre><code>select 
    joined.joinid,
    count(joined.packages)::integer as t_package_count,
    sum(coalesce((joined.packages -&gt;&gt; 'weight'::text)::double precision, 0::double precision)) as t_total_weight
from 
(
select
    joinid ,
    json_array_elements(jsondata) as packages
from
    ( (
    select
        distinct unnest(at2.arrayofid) as joinid, at2.id as rootid
    from
        aggtable at2) unnested
join jsontable jt on
    jt.id = unnested.joinid)) joined
    group by joined.joinid
</code></pre>
<p>For which the EXPLAIN ANALYSE return</p>
<pre><code>HashAggregate  (cost=873570.28..873572.78 rows=200 width=28) (actual time=18.379..18.741 rows=1661 loops=1)
  Group Key: (unnest(at2.arrayofid))
  -&gt;  ProjectSet  (cost=44903.16..191820.28 rows=27270000 width=48) (actual time=3.019..14.684 rows=3658 loops=1)
        -&gt;  Hash Join  (cost=44903.16..53425.03 rows=272700 width=55) (actual time=3.010..4.999 rows=1829 loops=1)
              Hash Cond: ((unnest(at2.arrayofid)) = jt.id)
              -&gt;  Unique  (cost=44712.88..46758.13 rows=272700 width=53) (actual time=1.825..2.781 rows=1845 loops=1)
                    -&gt;  Sort  (cost=44712.88..45394.63 rows=272700 width=53) (actual time=1.824..2.135 rows=1845 loops=1)
                          Sort Key: (unnest(at2.arrayofid)), at2.id
                          Sort Method: quicksort  Memory: 308kB
                          -&gt;  ProjectSet  (cost=0.00..1444.22 rows=272700 width=53) (actual time=0.009..1.164 rows=1845 loops=1)
                                -&gt;  Seq Scan on aggtable at2  (cost=0.00..60.27 rows=2727 width=67) (actual time=0.005..0.311 rows=2727 loops=1)
              -&gt;  Hash  (cost=132.90..132.90 rows=4590 width=55) (actual time=1.169..1.169 rows=4590 loops=1)
                    Buckets: 8192  Batches: 1  Memory Usage: 454kB
                    -&gt;  Seq Scan on jsontable jt  (cost=0.00..132.90 rows=4590 width=55) (actual time=0.007..0.462 rows=4590 loops=1)
Planning Time: 0.144 ms
Execution Time: 18.889 ms
</code></pre>
<p>I see a huge difference in the query performance (20ms to 2000ms), as evaluated by postgres. Howver, the real query performance is no where near that difference <strong>( the fast one is about 500ms and the slow one is about 1s )</strong></p>
<p>My question</p>
<p>1/ Is that normal that EXPLAIN produce drastic difference in performance but not so much in real life?</p>
<p>2/ Is the second - optimized query correct? what did the first query do wrong?</p>
<p>I suppy also the credential to a sample database so that everyone can try the queries out</p>
<p>postgres://birylwwg:X6EM3Al9Jhqzz0w6EaSSx79pa4aXRBZq@arjuna.db.elephantsql.com:5432/birylwwg</p>
<p>PW is</p>
<p>X6EM3Al9Jhqzz0w6EaSSx79pa4aXRBZq</p>

