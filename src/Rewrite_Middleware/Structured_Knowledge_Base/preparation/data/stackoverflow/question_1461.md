# PostgreSQL Index Not Utilized for JSONB Field Filtering on Non-Equality: What Am I Missing?
[Link to question](https://stackoverflow.com/questions/77068694/postgresql-index-not-utilized-for-jsonb-field-filtering-on-non-equality-what-am)
**Creation Date:** 1694192330
**Score:** 1
**Tags:** postgresql, sql-execution-plan, postgresql-12, query-planner, partial-index
## Question Body
<p>I have a table in my database called &quot;mytable,&quot; which contains a &quot;date&quot; field with JSONB data like this:</p>
<pre><code>{
  ...
  &quot;myfield&quot;: &quot;value1&quot;
}
</code></pre>
<p>The &quot;myfield&quot; field can currently have values &quot;value1,&quot; &quot;value2,&quot; and &quot;value3.&quot; Additionally, &quot;myfield&quot; can be null, or it might not exist at all.</p>
<p>In my queries, I need to find rows where &quot;myfield&quot; is not equal to &quot;value1.&quot;</p>
<pre class="lang-sql prettyprint-override"><code>select * from mytable where data-&gt;&gt;'myfield' &lt;&gt; 'value1'
</code></pre>
<p>I've created a partial index on the &quot;mytable&quot; table to speed up the query:</p>
<pre class="lang-sql prettyprint-override"><code>CREATE INDEX &quot;idx_mytable_myfield&quot; ON &quot;mytable&quot; USING btree (
  ((data-&gt;&gt;'myfield'::text) COLLATE &quot;pg_catalog&quot;.&quot;default&quot; &quot;pg_catalog&quot;.&quot;text_ops&quot; ASC NULLS LAST
) WHERE 
  (data-&gt;&gt;'myfield'::text)::text &lt;&gt; 'value1'::text
)
</code></pre>
<p>However, the query is not using this index. At the same time, the selectivity of the query is high, and a sequential scan is significantly slower.</p>
<p>If I rewrite the query and index to use &quot;in&quot; instead of &quot;&lt;&gt;&quot;, the index is used in the query. But this means I'll have to rewrite both the query and the index when adding new values in the future:</p>
<pre class="lang-sql prettyprint-override"><code>select * from mytable where (data-&gt;&gt;'myfield'::text)::text in ('value2'::text,'value3'::text)
</code></pre>
<p>Can you please help me understand what I'm doing wrong? Is there a way to rewrite the query and/or the index?</p>
<hr />
<p>To address possible questions in advance:</p>
<ol>
<li>I've run <code>ANALYZE mytable</code> after each index change.</li>
<li>The query has high selectivity.</li>
<li>ChatGPT asked about this and suggested exactly what I'm trying to do.</li>
<li>My PostgreSQL version is 12.14.</li>
<li>I don't want to build not partial index on data-&gt;&gt;'myfield' or GIN index on all data field because of perfomance and index size</li>
</ol>
<p>P.S.
I've tried adding additional conditions to both the index and the query, but it didn't help:</p>
<pre class="lang-sql prettyprint-override"><code>...
and data is not null
and data-&gt;'myfield'::text is not null
</code></pre>
<pre class="lang-sql prettyprint-override"><code>CREATE INDEX &quot;mytable_myfield_idx&quot; ON &quot;set10&quot;.&quot;mytable&quot; USING btree (
  (&quot;data&quot; -&gt;&gt; 'myfield'::text)  COLLATE &quot;pg_catalog&quot;.&quot;default&quot; &quot;pg_catalog&quot;.&quot;text_ops&quot; ASC NULLS LAST
)
WHERE (&quot;data&quot; -&gt;&gt; 'myfield'::text &lt;&gt; 'нет');
</code></pre>
<pre class="lang-sql prettyprint-override"><code>EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS)
SELECT  
    *
FROM
    mytable
WHERE
    &quot;data&quot; -&gt;&gt; 'myfield'::text &lt;&gt; 'нет'
</code></pre>
<pre><code>Seq Scan on set10.mytable  (cost=0.00..2041.22 rows=86911 width=35) (actual time=19.098..35.258 rows=74 loops=1)
  Output: &quot;jiraKey&quot;, data, created
  Filter: ((mytable.data -&gt;&gt; 'myfield'::text) &lt;&gt; 'нет'::text)
  Rows Removed by Filter: 87274
  Buffers: shared hit=731
Planning Time: 0.051 ms
Execution Time: 35.278 ms
</code></pre>
<p>And my experiments show that the problem is in &quot;&lt;&gt;&quot;, the optimizer won't use the index in this case.</p>
<p><strong>upd</strong></p>
<p>if I force to disable seqscan - the optimizer uses my index properly. For the some reason, it thinks that it is better to use seqscan, but it wrong</p>
<pre class="lang-sql prettyprint-override"><code>SET enable_seqscan = false;
EXPLAIN (ANALYZE,BUFFERS, COSTS, VERBOSE)
select 
    *
FROM    
    mytable
WHERE
    &quot;data&quot;-&gt;&gt;'myfield' &lt;&gt; 'нет' 
</code></pre>
<pre><code>Bitmap Heap Scan on set10.mytable  (cost=30.20..2064.86 rows=86911 width=35) (actual time=0.024..0.098 rows=74 loops=1)
  Output: &quot;jiraKey&quot;, data, created
  Recheck Cond: ((mytable.data -&gt;&gt; 'myfield'::text) &lt;&gt; 'нет'::text)
  Heap Blocks: exact=52
  Buffers: shared hit=53
  -&gt;  Bitmap Index Scan on mytable_myfield_idx  (cost=0.00..8.47 rows=86911 width=0) (actual time=0.013..0.014 rows=74 loops=1)
        Buffers: shared hit=1
Planning Time: 0.059 ms
Execution Time: 0.128 ms
</code></pre>

## Answers
### Answer ID: 77069610
<p>In order to let it get an accurate estimate of the row counts, you need an expression index like this:</p>
<pre><code>create index on mytable ((data-&gt;&gt;'myfield'));
</code></pre>
<p>And then do an ANALYZE after it is created.  You already have that expression index in a partial form, but partial indexes are not used by the planner to derive rows counts.</p>
<p>If you were using a modern version of the software, you could instead create extended statistics on the expression:</p>
<pre><code>create statistics asldfj on (data-&gt;&gt;'myfield') from mytable;
</code></pre>
<p>This will generate the same statistics as the index does, but doesn't have the same storage or maintenance needs as the index.  But it requires v14 or above.</p>

