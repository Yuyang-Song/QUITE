# Why jit can destroy performance on Linux server?
[Link to question](https://stackoverflow.com/questions/74948680/why-jit-can-destroy-performance-on-linux-server)
**Creation Date:** 1672301503
**Score:** 1
**Tags:** performance, indexing, postgresql-14
## Question Body
<p>We have a Postgresql development server on Windows and a production server on Ubuntu Linux. The Postgresql release versions are slightly different, the newer in on linux (Postgresql 14.5).</p>
<p>One database was exported from development and imported in production, so they are the same. We noticed that some queries are <strong>100 times slower</strong> on Ubuntu server. Too much to blame a different hardware. The critical queries are like the following:</p>
<pre><code>SELECT a.field1,
...
a.field_n,
CASE (EXISTS ( 
SELECT b.&quot;waterBodyCode&quot;
  FROM &quot;GAP_ecologico_SWB_1&quot; b
  WHERE a.field1 = b.field1_b AND ...))
  WHEN true 
    THEN 'Yes'
        ELSE 'No'
  END AS &quot;attributableQE&quot;
FROM &quot;SWB_ecological_quality_elements&quot; a
ORDER BY a.field1, ...;  
</code></pre>
<p>I know we can rewrite the query in a better and more efficient way but before doing that we would like to understand the root cause of the poor performance on Ubuntu.</p>
<p><strong>SWB_ecological_quality_elements</strong> and <strong>swaterBodyCode</strong> are views. What we suspect is that on Windows server the inner query is executed using indexing or caching while on Ubuntu  a full scan is done. The <strong>postgresql.conf</strong> files are quite similar, what can we check ?</p>
<p><strong>UPDATE 1</strong></p>
<p>I tuned the memory as suggested by PgTune but it was useless, same poor performance. I executed the query with Analyze, the timing result looks weird but I'm not an expert.</p>
<pre><code>&quot;  Functions: 1499&quot;
&quot;  Options: Inlining true, Optimization true, Expressions true,         Deforming true&quot;
&quot;  Timing: Generation 101.424 ms, Inlining 103.476 ms, Optimization 10402.780 ms, Emission 6866.288 ms, Total 17473.968 ms&quot;
&quot;Execution Time: 18005.457 ms&quot;
</code></pre>
<p><strong>UPDATE 2</strong></p>
<p>Setting jit to false cause an incredible performance boost on the query execute on the Linux server. Don't know anything about jit and cannot figure out why it behaves so differently on Windows (Postgresql 14.4) and on Linux (Postgresql 14.5), but others noticed its weird effects as can be read here: <a href="https://dba.stackexchange.com/questions/264955/handling-performance-problems-with-jit-in-postgres-12">Handling performance problems with jit in postgres 12</a>.
Any explanation ?</p>

