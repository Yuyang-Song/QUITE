# Possible Indexing Question? - How do I increase query speed?
[Link to question](https://stackoverflow.com/questions/53891813/possible-indexing-question-how-do-i-increase-query-speed)
**Creation Date:** 1545434521
**Score:** 0
**Tags:** postgresql, indexing
## Question Body
<p>I have a table with several million rows, and the query I'm running is starting to bog down (more data goes into it everyday). I'm just a lowly web dev, so I kinda muddle along when it comes to database-related tasks. I suspect that a couple of indexes will correct this, or potentially some query rewrites, but was hoping someone would point me in the right direction. Here's the query:</p>

<pre><code>   SELECT 
       impressionreport.sitecode AS site, impressionreport.advertisername AS advertiser, impressionreport.mediafilename AS filename,
       SUM(impressionreport.mediafileplays) AS totalplays, SUM(impressionreport.views) AS totalviewers, SUM(impressionreport.impressions) AS totalimpressions, 
       SUM(CASE WHEN impressionreport.gender LIKE 'male' THEN impressionreport.views ELSE 0 END) AS totalmale, 
       SUM(CASE WHEN impressionreport.gender LIKE 'female' THEN impressionreport.views ELSE 0 END) AS totalfemale, 
       SUM(CASE WHEN impressionreport.gender LIKE 'female' AND agegroup.name LIKE 'young' THEN impressionreport.views ELSE 0 END) AS femaleyoung, 
       SUM(CASE WHEN impressionreport.gender LIKE 'female' AND agegroup.name LIKE 'young adult' THEN impressionreport.views ELSE 0 END) AS femaleyoungadult, 
       SUM(CASE WHEN impressionreport.gender LIKE 'female' AND agegroup.name LIKE 'adult' THEN impressionreport.views ELSE 0 END) AS femaleadult, 
       SUM(CASE WHEN impressionreport.gender LIKE 'female' AND agegroup.name LIKE 'senior' THEN impressionreport.views ELSE 0 END) AS femalesenior, 
       SUM(CASE WHEN impressionreport.gender LIKE 'male' AND agegroup.name LIKE 'young' THEN impressionreport.views ELSE 0 END) AS maleyoung, 
       SUM(CASE WHEN impressionreport.gender LIKE 'male' AND agegroup.name LIKE 'young adult' THEN impressionreport.views ELSE 0 END) AS maleyoungadult, 
       SUM(CASE WHEN impressionreport.gender LIKE 'male' AND agegroup.name LIKE 'adult' THEN impressionreport.views ELSE 0 END) AS maleadult, 
       SUM(CASE WHEN impressionreport.gender LIKE 'male' AND agegroup.name LIKE 'senior' THEN impressionreport.views ELSE 0 END) AS malesenior 
   FROM impressionreport 
   LEFT JOIN agegroup ON impressionreport.age &gt;= agegroup.min AND impressionreport.age &lt;= agegroup.max 
   WHERE 
       impressionreport.datelocal &gt;= '5-1-2018' AND
       impressionreport.datelocal &lt; '5-15-2018' AND
       impressionreport.network LIKE '%' AND
       impressionreport.sitecode LIKE '%' AND
       impressionreport.devicename LIKE '%' AND
       impressionreport.advertisername LIKE '%' AND
       impressionreport.mediafilename LIKE '%'
   GROUP BY impressionreport.sitecode, impressionreport.advertisername, impressionreport.mediafilename
   ORDER BY impressionreport.sitecode, impressionreport.advertisername, impressionreport.mediafilename
</code></pre>

<p>There are indexes on datelocal, devicename, sitecode, advertisername, mediafilename, gender, age, network (all btree).</p>

<p>EDIT:</p>

<blockquote>
  <p>GroupAggregate  (cost=197785.58..223336.77 rows=533798 width=161)
  (actual time=3789.770..5819.410 rows=4577 loops=1)   Group Key:
  impressionreport.sitecode, impressionreport.advertisername,
  impressionreport.mediafilename   ->  Sort  (cost=197785.58..198469.86
  rows=1368560 width=103) (actual time=3789.651..4450.374 rows=1384106
  loops=1)
          Sort Key: impressionreport.sitecode, impressionreport.advertisername, impressionreport.mediafilename
          Sort Method: external merge  Disk: 119504kB
          ->  Nested Loop Left Join  (cost=0.09..116428.54 rows=1368560 width=103) (actual time=0.029..1485.883 rows=1384106 loops=1)
                Join Filter: ((impressionreport.age >= agegroup.min) AND (impressionreport.age &lt;= agegroup.max))
                Rows Removed by Join Filter: 4885607
                ->  Index Scan using impressionreport_datelocal_index on impressionreport  (cost=0.09..91793.44 rows=1368560 width=75) (actual
  time=0.020..443.316 rows=1384106 loops=1)
                      Index Cond: ((datelocal >= '2018-05-01 00:00:00'::timestamp without time zone) AND (datelocal &lt; '2018-05-15
  00:00:00'::timestamp without time zone))
                ->  Materialize  (cost=0.00..1.02 rows=4 width=40) (actual time=0.000..0.000 rows=4 loops=1384106)
                      ->  Seq Scan on agegroup  (cost=0.00..1.01 rows=4 width=40) (actual time=0.004..0.005 rows=4 loops=1) Planning time:
  0.270 ms Execution time: 5838.433 ms</p>
</blockquote>

## Answers
### Answer ID: 53953793
<p>-> Sort (cost=197785.58..198469.86 rows=1368560 width=103) (<strong>actual time=3789.651..4450.374</strong> rows=1384106 loops=1)
Sort Key: impressionreport.sitecode, impressionreport.advertisername, impressionreport.mediafilename <strong>Sort Method: external merge Disk: 119504kB</strong> </p>

<p>3789.651..4450.374 means that it took 3789 ms for the first row and 4450 ms for all rows to complete that part of the query. </p>

<p>So the slowest part is the sorting and it's slow because it decided to do the sorting on disk. This is probably because it has to little work_mem</p>

<p>Try tuning postgresql.conf with the help of <a href="https://pgtune.leopard.in.ua" rel="nofollow noreferrer">https://pgtune.leopard.in.ua</a> just enter how much ram you have and hit generate</p>

### Answer ID: 53891918
<p>Try an index on <code>impressionreport (datelocal, sitecode, advertisername, mediafilename)</code> (compound, i.e. one index for the complete list of columns, not one for each column).</p>

<p>Check the execution plan, to see if the index gets picked up.</p>

<hr>

<p>Edit:</p>

<p>I was wrong about the <code>LIKE</code>s. I missed that it could filter for <code>datelocal</code> before checking for the <code>LIKE</code>s even if they don't get optimized away.</p>

