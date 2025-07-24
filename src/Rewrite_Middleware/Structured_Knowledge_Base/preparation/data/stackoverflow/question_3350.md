# SQLite, select greatest nearest value from same table
[Link to question](https://stackoverflow.com/questions/77003431/sqlite-select-greatest-nearest-value-from-same-table)
**Creation Date:** 1693340618
**Score:** 0
**Tags:** sql, sqlite
## Question Body
<p>I have a such database schema:</p>
<pre><code>CREATE TABLE callchain(
  seq_no INT,
  entry_oid INT,
  leave_oid,
  tid INT,
  pid INT,
  depth
);
CREATE UNIQUE INDEX callchain_idx on callchain(seq_no);
</code></pre>
<p>And for each row in this table I want to select nearest corresponding following row where <code>tid</code>, <code>pid</code> is the same, <code>leave_oid</code> is not null and <code>entry_oid</code> is null, and <code>seq_no</code> is larger than current <code>seq_no</code> (seq_no is unique for a table), and where depth is less by 1 from current one.</p>
<p>I have written a query for this:</p>
<pre><code>select *, (select min(seq_no) from callchain where seq_no &gt; cc.seq_no and cc.pid = pid and cc.tid = tid and leave_oid not null and depth = cc.depth -1) from callchain as cc;
</code></pre>
<p>Unfortunately, this query tooks too long time (almost endless) on 1000000 records (and I need something like 100000000 records...)</p>
<p>Basically, this is a trace record from running program. Where <code>entry_oid</code> is not null on function entry, and <code>leave_oid</code> is not null on function exit. And I want to find function exit record for each function entry record. For example, there is a piece of the table:</p>
<pre><code>seq_no    entry_oid  leave_oid  tid  pid  depth
--------  ---------  ---------  ---  ---  -----
2         117544                24   21   1    
3         117545                24   21   2    
4                    117556     24   21   1    
5                    117557     24   21   0    
6                    117558     24   21   -1   
7         117546                24   21   0    
8         117547                24   21   1    
9                    117559     24   21   0    
10        117548                24   21   1    
11        117549                24   21   2    
12                   117560     24   21   1    
13                   117561     24   21   0    
14                   117562     24   21   -1   
15                   117563     24   21   -2   
</code></pre>
<p>For row #7 (entry point) corresponding exit point will be row #14.</p>
<p>I have tried to write JOIN query for the same, like the following:</p>
<pre><code>select A.seq_no, min(B.seq_no), B.leave_oid from callchain as A inner join callchain as B on A.seq_no &lt; B.seq_no AND A.tid=B.tid AND A.pid=B.pid AND B.leave_oid NOT NULL AND B.depth = A.depth - 1  GROUP BY A.seq_no   ORDER BY A.seq_no;
</code></pre>
<p>But I had no big succes with this query. It takes too large time too. :-(</p>
<p>With correlated subquery, as I understood data first is divided by <code>seq_no</code> and then by <code>pid/tid/depth</code> (or vice versa). And single index is not sufficient for both cases (index by <code>seq_no</code> or index by <code>pid/tid/depth</code>). And after data is divided previously build index becomes not valid, so SQLite engine builds temporary B-tree and all becomes too slow...</p>
<p>Why join query is slow I not understood, looks there is no any temporary indices build, just by algorithmic complexity is too large.</p>
<p>I want to ask, how can I rewrite my query and/or redesign a database to perform a query I want quickly (in a few seconds) ?</p>
<p>I am using SQlite engine as embedded database for C++ program. I want to avoid switching to full featured DBMS.</p>

## Answers
### Answer ID: 77005155
<p><strong>Add a covering index</strong></p>
<p>Since your query filters and joins on <code>tid</code>, <code>pid</code>, <code>seq_no</code>, <code>depth</code> and <code>leave_oid</code>, adding a covering index on these columns will allow the query to be satisfied purely from the index without hitting the main table:</p>
<pre><code>CREATE INDEX callchain_cover_idx ON callchain (tid, pid, seq_no, depth, leave_oid);
</code></pre>
<p><strong>Use a CTE to filter first</strong></p>
<p>Apply the conditions on leave_oid and depth first in a CTE to reduce the dataset before joining:</p>
<pre><code>WITH filtered AS (
  SELECT * FROM callchain
  WHERE leave_oid IS NOT NULL AND depth &gt;= 0
)

SELECT 
  c1.seq_no, 
  MIN(c2.seq_no) as exit_seq_no,
  c2.leave_oid
FROM callchain c1
JOIN filtered c2
ON c1.tid = c2.tid AND 
   c1.pid = c2.pid AND
   c2.depth = c1.depth - 1 AND
   c2.seq_no &gt; c1.seq_no
GROUP BY c1.seq_no
ORDER BY c1.seq_no;
</code></pre>
<p><strong>Use an IN subquery instead of a join</strong></p>
<p>This may perform better by doing direct index lookups:</p>
<pre><code>SELECT
  c1.seq_no,
  (
    SELECT MIN(c2.seq_no) 
    FROM filtered c2
    WHERE 
      c2.tid = c1.tid AND
      c2.pid = c1.pid AND  
      c2.depth = c1.depth - 1 AND
      c2.seq_no &gt; c1.seq_no
  ) AS exit_seq_no,
  c1.leave_oid
FROM callchain c1
</code></pre>

