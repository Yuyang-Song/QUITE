# Postgres faster order by of calculated field
[Link to question](https://stackoverflow.com/questions/63888816/postgres-faster-order-by-of-calculated-field)
**Creation Date:** 1600102981
**Score:** 0
**Tags:** postgresql, performance, search
## Question Body
<p>I'm solving the problem of finding similar vectors in the database.</p>
<p>So I have created a function  which calculates the cosine distance (all vectors in database are normalized)</p>
<pre><code>CREATE OR REPLACE FUNCTION dot_product(IN vector1 float[], IN vector2 float[])
    RETURNS double precision
AS $BODY$
BEGIN
    RETURN (
        SELECT sum(mul) FROM (SELECT v1 * v2 as mul FROM unnest(vector1, vector2) AS t(v1, v2)) as denominator
        );
END;
$BODY$ LANGUAGE 'plpgsql';
</code></pre>
<pre><code>
CREATE OR REPLACE FUNCTION cosine_similarity(IN vector1 float[], IN vector2 float[])
    RETURNS double precision
AS $BODY$
BEGIN
    RETURN (select dot_product(vector1, vector2)  AS similarity_value);
END;
$BODY$ LANGUAGE 'plpgsql';
</code></pre>
<p>And I'm searching with this query</p>
<pre><code>explain
select *, cosine_similarity(vector, (select vector from image where id = 2852)) as sim
from image
order by sim desc;


Sort  (cost=11091.29..11144.30 rows=21204 width=212)
&quot;  Sort Key: (cosine_similarity((image.vector)::double precision[], ($0)::double precision[])) DESC&quot;
  InitPlan 1 (returns $0)
    -&gt;  Index Scan using image_pkey on image image_1  (cost=0.29..8.30 rows=1 width=18)
          Index Cond: (id = 2852)
  -&gt;  Seq Scan on image  (cost=0.00..7382.26 rows=21204 width=212)

</code></pre>
<p>although if i don't call order by I get:</p>
<pre><code>explain
select *, cosine_similarity(vector, (select vector from image where id = 2852)) as sim
from image;


Seq Scan on image  (cost=8.30..7390.57 rows=21204 width=212)
  InitPlan 1 (returns $0)
    -&gt;  Index Scan using image_pkey on image image_1  (cost=0.29..8.30 rows=1 width=18)
          Index Cond: (id = 2852)

</code></pre>
<p>Therefore, I conclude that my function works fast enough, and 'order by ' is very heavy
Please tell me if anyone has any ideas about this.</p>
<p><strong>UPDATE</strong>:</p>
<p>I have rewrite my function as @Jeremy and Laurenz Albe advised, but my query still takes a very long time</p>
<pre><code>CREATE OR REPLACE FUNCTION cosine_similarity_sql(vector1 float[], vector2 float[]) RETURNS double precision
    AS ' SELECT sum(mul) FROM (SELECT v1 * v2 as mul FROM unnest(vector1, vector2) AS t(v1, v2)) as denominator;'
    LANGUAGE SQL
IMMUTABLE
PARALLEL SAFE;
</code></pre>
<pre><code>explain analyse
select name, cosine_similarity_sql(vector, (select vector from image where id = 2852)) as sim
from image
order by sim desc;

Sort  (cost=8914.29..8967.30 rows=21204 width=26) (actual time=7692.156..7694.807 rows=20580 loops=1)
&quot;  Sort Key: (cosine_similarity_sql((image.vector)::double precision[], ($0)::double precision[])) DESC&quot;
  Sort Method: quicksort  Memory: 2376kB
  InitPlan 1 (returns $0)
    -&gt;  Index Scan using image_pkey on image image_1  (cost=0.29..8.30 rows=1 width=18) (actual time=0.011..0.011 rows=1 loops=1)
          Index Cond: (id = 2852)
  -&gt;  Seq Scan on image  (cost=0.00..7382.26 rows=21204 width=26) (actual time=0.635..7662.591 rows=20580 loops=1)
Planning Time: 0.242 ms
Execution Time: 7696.030 ms

</code></pre>

## Answers
### Answer ID: 63889633
<p>The sort is no problem, unless the estimate of 10000 rows is way off.</p>
<p>You will gain most by declaring the functions <code>IMMUTABLE</code> like they should be. Moreover, the second function does nothing, get rid of it. Finally, using <code>LANGUAGE sql</code> functions may save a little bit, but I don't know if that is measurable.</p>

