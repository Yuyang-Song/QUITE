# How to index a calender query with different timezones in PostgreSQL?
[Link to question](https://stackoverflow.com/questions/42250827/how-to-index-a-calender-query-with-different-timezones-in-postgresql)
**Creation Date:** 1487165536
**Score:** 1
**Tags:** postgresql, date, timezone
## Question Body
<p>In our PostgreSQL 9.6 application, we're currently rewriting one of the most performance-critical parts: A calendar showing some posts. </p>

<pre><code>SELECT
  assigned_user_id,
  channel_id,
  id,
  row_number()
  OVER (
    PARTITION BY DATE(publication_at AT TIME ZONE 'Europe/Vienna')
    ORDER BY publication_at ASC, id ASC )                            AS "row_number",
  TO_CHAR(publication_at AT TIME ZONE 'Europe/Vienna', 'YYYY-MM-DD') AS "day",
  COUNT(*)
  OVER (
    PARTITION BY DATE(publication_at AT TIME ZONE 'Europe/Vienna') ) AS "count_per_day"
FROM posts
WHERE client_id = 159 AND publication_at BETWEEN '2016-12-25 23:00:00' AND '2017-02-05 22:59:59'
ORDER BY publication_at AT TIME ZONE 'Europe/Vienna', id ASC
</code></pre>

<p>Based on a specific month (in this case: January 2017), we select all posts with a specific <code>publication_at</code> (note: the passed values in the <code>WHERE</code> clause are already converted to local time). for some other reason (not relevant to this case here) we select row number and how many posts per local day we have in the database.</p>

<p>At the moment, our index (posts_client_id_publication_at_assigned_user_id_id) is only partially used because the <code>AT TIME ZONE …</code> does not work against the index (it's simply not <a href="https://en.wikipedia.org/wiki/Sargable" rel="nofollow noreferrer">sargable</a>). </p>

<p>Here's the <code>EXPLAIN ANALYSE</code> output from my development machine - production table has almost 10 mio rows:</p>

<pre><code>Sort  (cost=268.52..268.74 rows=87 width=92) (actual time=2.464..2.517 rows=524 loops=1)
  Sort Key: (timezone('Europe/Vienna'::text, publication_at)), id
  Sort Method: quicksort  Memory: 98kB
  Buffers: shared hit=246 read=6
  -&gt;  WindowAgg  (cost=260.93..265.72 rows=87 width=92) (actual time=0.920..2.306 rows=524 loops=1)
        Buffers: shared hit=246 read=6
        -&gt;  WindowAgg  (cost=260.93..263.32 rows=87 width=44) (actual time=0.899..1.173 rows=524 loops=1)
              Buffers: shared hit=246 read=6
              -&gt;  Sort  (cost=260.93..261.15 rows=87 width=36) (actual time=0.895..0.952 rows=524 loops=1)
                    Sort Key: (date(timezone('Europe/Vienna'::text, publication_at))), publication_at, id
                    Sort Method: quicksort  Memory: 65kB
                    Buffers: shared hit=246 read=6
                    -&gt;  Index Scan using posts_client_id_publication_at_assigned_user_id_id on posts  (cost=0.41..258.13 rows=87 width=36) (actual time=0.050..0.774 rows=524 loops=1)
                          Index Cond: ((client_id = 159) AND (publication_at &gt;= '2016-12-25 23:00:00+01'::timestamp with time zone) AND (publication_at &lt;= '2017-02-05 22:59:59+01'::timestamp with time zone))
                          Buffers: shared hit=246 read=6
Planning time: 0.343 ms
Execution time: 2.641 ms
</code></pre>

<p>I'm aware that we should move the time zone part from the column to the right part, so that we still can use <code>publication_at</code> inside the index. But I'm simply not sure how we can do this with the given query here. </p>

<p>Hint: Our users can select different timezones, so we can't simply put one specific time zone value inside the index.</p>

