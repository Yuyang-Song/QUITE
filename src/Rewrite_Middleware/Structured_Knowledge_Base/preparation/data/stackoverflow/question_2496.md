# Postgresql doesn&#39;t use index
[Link to question](https://stackoverflow.com/questions/37138386/postgresql-doesnt-use-index)
**Creation Date:** 1462882806
**Score:** 1
**Tags:** json, postgresql, postgresql-9.4
## Question Body
<p>I have large table crumbs (about 100M+ rows, 100GB). It's just collection of json stored as text. It has index on column run_id that has about 10K unique values. So each run is small (1K - 1M rows).</p>

<p>For simple query:</p>

<pre><code>explain analyze verbose select * from crumbs c 
where c.run_id='2016-04-26T19_02_01_015Z' limit 10
</code></pre>

<p>Plan is good:</p>

<pre><code>Limit  (cost=0.56..36.89 rows=10 width=2262) (actual time=1.978..2.016 rows=10 loops=1)
  Output: id, robot_id, run_id, content, created_at, updated_at, table_id, fork_id, log, err
  -&gt;  Index Scan using index_crumbs_on_run_id on public.crumbs c  (cost=0.56..5533685.73 rows=1523397 width=2262) (actual time=1.975..1.996 rows=10 loops=1)
        Output: id, robot_id, run_id, content, created_at, updated_at, table_id, fork_id, log, err
        Index Cond: ((c.run_id)::text = '2016-04-26T19_02_01_015Z'::text)
Planning time: 0.117 ms
Execution time: 2.048 ms
</code></pre>

<p>But if I try to look inside json stored in one of the columns it then wants to do full scan:</p>

<pre><code>explain verbose select x from crumbs c, 
lateral json_array_elements(c.content::json) x
where c.run_id='2016-04-26T19_02_01_015Z' 
limit 10
</code></pre>

<p>Plan:</p>

<pre><code>Limit  (cost=0.01..0.69 rows=10 width=32)
  Output: x.value
  -&gt;  Nested Loop  (cost=0.01..10332878.67 rows=152343800 width=32)
        Output: x.value
        -&gt;  Seq Scan on public.crumbs c  (cost=0.00..7286002.66 rows=1523438 width=895)
              Output: c.id, c.robot_id, c.run_id, c.content, c.created_at, c.updated_at, c.table_id, c.fork_id, c.log, c.err
              Filter: ((c.run_id)::text = '2016-04-26T19_02_01_015Z'::text)
        -&gt;  Function Scan on pg_catalog.json_array_elements x  (cost=0.01..1.01 rows=100 width=32)
              Output: x.value
              Function Call: json_array_elements((c.content)::json)
</code></pre>

<p>Tried:</p>

<pre><code>analyze crumbs
</code></pre>

<p>But made no difference.  </p>

<p><strong>Update 1</strong> 
Disabling sequential scanning for whole database works, but this is not an option in our application.  In many other places seq scan should stay:</p>

<pre><code>set enable_seqscan=false;
</code></pre>

<p>Plan: </p>

<pre><code>Limit  (cost=0.57..1.14 rows=10 width=32) (actual time=0.120..0.294 rows=10 loops=1)
  Output: x.value
  -&gt;  Nested Loop  (cost=0.57..8580698.45 rows=152343400 width=32) (actual time=0.118..0.273 rows=10 loops=1)
        Output: x.value
        -&gt;  Index Scan using index_crumbs_on_run_id on public.crumbs c  (cost=0.56..5533830.45 rows=1523434 width=895) (actual time=0.087..0.107 rows=10 loops=1)
              Output: c.id, c.robot_id, c.run_id, c.content, c.created_at, c.updated_at, c.table_id, c.fork_id, c.log, c.err
              Index Cond: ((c.run_id)::text = '2016-04-26T19_02_01_015Z'::text)
        -&gt;  Function Scan on pg_catalog.json_array_elements x  (cost=0.01..1.01 rows=100 width=32) (actual time=0.011..0.011 rows=1 loops=10)
              Output: x.value
              Function Call: json_array_elements((c.content)::json)
Planning time: 0.124 ms
Execution time: 0.337 ms
</code></pre>

<p><strong>Update 2</strong>:</p>

<p>Schema is:</p>

<pre><code>CREATE TABLE crumbs
(
  id serial NOT NULL,
  run_id character varying(255),
  content text,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT crumbs_pkey PRIMARY KEY (id)
);

CREATE INDEX index_crumbs_on_run_id
  ON crumbs
  USING btree
  (run_id COLLATE pg_catalog."default");
</code></pre>

<p><strong>Update 3</strong></p>

<p>Rewriting query like so:</p>

<pre><code>select json_array_elements(c.content::json) x
from crumbs c
where c.run_id='2016-04-26T19_02_01_015Z' 
limit 10
</code></pre>

<p>Gets correct plan.  Still unclear why wrong plan is chosen for second query.</p>

## Answers
### Answer ID: 37140619
<p>Data modelling suggestions:</p>

<pre><code>        -- Suggest replacing the column run_id (low cardinality, and rather fat)
        -- by a reference to a domain table, like:
        -- ------------------------------------------------------------------
CREATE TABLE runs
        ( run_seq serial NOT NULL PRIMARY KEY
        , run_id character varying UNIQUE
        );

        -- Grab all the distinct values occuring in crumbs.run_id
        -- -------------------------------------------------------
INSERT INTO runs (run_id)
SELECT DISTINCT run_id FROM crumbs;

        -- Add an FK column
        -- -----------------
ALTER TABLE crumbs
        ADD COLUMN run_seq integer REFERENCES runs(run_seq)
        ;

UPDATE crumbs c
SET run_seq = r.run_seq
FROM runs r
WHERE r.run_id = c.run_id
        ;
VACUUM ANALYZE runs;

        -- Drop old column and set new column to not nullable
        -- ---------------------------------------------------
ALTER TABLE crumbs
        DROP COLUMN run_id
        ;
ALTER TABLE crumbs
        ALTER COLUMN run_seq SET NOT NULL
        ;

        -- Recreate the supporting index for the FK
        -- adding id to support index-only lookups
        -- (and enforce uniqueness)
        -- -------------------------------------
CREATE UNIQUE INDEX index_crumbs_run_seq_id ON crumbs (run_seq,id)
        ;

        -- Refresh statistics
        -- ------------------
VACUUM ANALYZE crumbs; -- this may take some time ...

-- and then: join the runs table to your original crumbs table
-- -----------------------------------------------------------
-- explain analyze 
SELECT x FROM crumbs c
JOIN runs r ON r.run_seq = c.run_seq
        , lateral json_array_elements(c.content::json) x
WHERE r.run_id='2016-04-26T19_02_01_015Z'
LIMIT 10
        ;
</code></pre>

<p>Or: use the other answerers's suggestion with a similar join.</p>

<hr>

<p>But possibly even better: replace the ugly <code>run_id</code> text string by an actual timestamp.</p>

### Answer ID: 37139700
<p>Rewriting the query so that the limit is applied <em>first</em> and <em>then</em> the cross join against the function should make Postgres use the index: </p>

<p>Using a derived table:</p>

<pre><code>select x 
from (
    select *
    from crumbs 
    where run_id='2016-04-26T19_02_01_015Z' 
    limit 10
) c 
  cross join lateral json_array_elements(c.content::json) x
</code></pre>

<p>Alternatively using a CTE: </p>

<pre><code>with c as (
  select *
  from crumbs 
  where run_id='2016-04-26T19_02_01_015Z' 
  limit 10
)
select x
from c 
  cross join lateral json_array_elements(c.content::json) x
</code></pre>

<p>Or use <code>json_array_elements()</code> directly in the select list:</p>

<pre><code>select json_array_elements(c.content::json) 
from crumbs c
where c.run_id='2016-04-26T19_02_01_015Z' 
limit 10
</code></pre>

<p>However this is something different then the other two queries because it applies the limit <em>after</em> "unnesting" the json array, not on the number of rows returned from the <code>crumbs</code> table (which is what your first query is doing).</p>

### Answer ID: 37139692
<p>You've got three different problems going on. First, the <code>limit 10</code> in the first query is tipping the planner in favor of the index scan, which would otherwise be pretty expensive to get all rows matching that <code>run_id</code>. For the sake of comparison you might want to see what the first (un-joined) query plan looks like if you remove the limit. My guess is the planner switches to a table scan.</p>

<p>Second, that lateral join is unnecessary and throwing off the planner. You can expand the elements of the content array in your select clause like so:</p>

<pre><code>select json_array_elements(content::json)
from crumbs
where run_id = '2016-04-26T19_02_01_015Z'
;
</code></pre>

<p>This is more likely to use the index scan to pick off rows for that <code>run_id</code>, then "unnest" the array elements for you.</p>

<p>But the third hidden problem is what you're actually trying to get. If you run this last query as is then you're in the same boat as the first (un-joined) query without a limit, which means you'll likely not get an index scan (not that that's inherently bad if you're reading such a large chunk of the table).</p>

<p>Do you want just the first few arbitrary array elements from all content arrays in that run? If so then tacking on a limit clause here should be the end of the story. If you want all array elements for this particular run then you may just have to accept a table scan, although without the lateral join you're potentially in a much better situation than the original query.</p>

