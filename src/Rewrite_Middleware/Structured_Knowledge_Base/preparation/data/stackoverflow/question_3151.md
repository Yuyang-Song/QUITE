# Is it possible to improve the performance of query with distinct and multiple joins?
[Link to question](https://stackoverflow.com/questions/68907020/is-it-possible-to-improve-the-performance-of-query-with-distinct-and-multiple-jo)
**Creation Date:** 1629805669
**Score:** 0
**Tags:** sql, join, left-join, query-optimization, key-value
## Question Body
<p>There is following query:</p>
<pre><code>SELECT DISTINCT ID, ACCOUNT,
   CASE
       WHEN p.GeneralLevel = '1' THEN '1'
       WHEN p.Level3 IS NULL THEN '2'
       WHEN p.Level4 IS NULL THEN '3'
       WHEN p.Level5 IS NULL THEN '4'
       WHEN p.Level6 IS NULL THEN '5'
       WHEN p.Level7 IS NULL THEN '6'
       WHEN p.Level8 IS NULL THEN '7'
       ELSE '8'
   END AS LEVEL,
   CASE
       WHEN c.codeValueDescription IS NULL THEN p.Level2
       ELSE c.codeValueDescription
   END AS L2_CODE,
   CASE
       WHEN d.codeValueDescription IS NULL THEN p.Level3
       ELSE d.codeValueDescription
   END AS L3_CODE,
   CASE
       WHEN j.codeValueDescription IS NULL THEN p.Level4
       ELSE j.codeValueDescription
   END AS L4_CODE,
   CASE
       WHEN f.codeValueDescription IS NULL THEN p.Level5
       ELSE f.codeValueDescription
   END AS L5_CODE,
   CASE
       WHEN g.codeValueDescription IS NULL THEN p.Level6
       ELSE g.codeValueDescription
   END AS L6_CODE,
   CASE
       WHEN h.codeValueDescription IS NULL THEN p.Level7
       ELSE h.codeValueDescription
   END AS L7_CODE,
   p.Level8
   FROM generic p
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '2') c ON p.Level2 = c.codeValue
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '3') d ON p.Level3 = d.codeValue
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '4') j ON p.Level4 = j.codeValue
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '5') f ON p.Level5 = f.codeValue
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '3') g ON p.Level6 = g.codeValue //yes, code is 3 again
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '3') h ON p.Level7 = h.codeValue //and yes, again code 3 here
</code></pre>
<p>Some columns of the table 'generic' (excluded dates and other non-important columns for us):</p>
<pre><code>ID INTEGER NOT NULL,
ACCOUNT VARCHAR(50) NOT NULL,
GeneralLevel1 VARCHAR(50),
Level2 VARCHAR(50),
Level3 VARCHAR(50),
Level4 VARCHAR(50),
Level5 VARCHAR(50),
Level6 VARCHAR(50),
Level7 VARCHAR(50),
Level8 VARCHAR(50)
</code></pre>
<p>Simple data:</p>
<pre><code>ID,ACCOUNT_ID,LEVEL_1,LEVEL_2,...LEVEL_8
id1,ACCOUNT_ID1,GENERAL,null,...null
id1,ACCOUNT_ID2,GENERAL,A,...null
id1,ACCOUNT_ID2,GENERAL,B,...null
id2,ACCOUNT_ID1,GENERAL,null,...null
id2,ACCOUNT_ID2,GENERAL,A,...null
id2,ACCOUNT_ID3,GENERAL,B,...H
</code></pre>
<p>Current query is running more than 1s, usually it returns between 100 and 1000 records, I want to improve the performance of this query. The idea is to get rid of these LEFT JOINS and somehow rewrite this query to improve performance.</p>
<p>Maybe there are ways to improve this query to fetch data a bit faster? I hope I've provided enough information here. Database is custom, NO_SQL giant under the hood but syntax of our database bridge is very similar to MySQL. Unfortunately, I cannot provide the EXECUTION PLAN of this query because it is processing on the server side and then generate some SQL for which I cannot have an access.</p>

## Answers
### Answer ID: 68911125
<p>You're doing key/value lookups from your <code>codes</code> tables.  Your query contains several of these LEFT JOIN patterns.</p>
<pre class="lang-sql prettyprint-override"><code>   FROM generic p
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '2') c ON p.Level2 = c.codeValue
   LEFT JOIN
     (SELECT codeValue, codeValueDescription
      FROM codes
      WHERE code = '3') d ON p.Level3 = d.codeValue
</code></pre>
<p>These LEFT JOINs can be refactored to eliminate the subqueries. This refactoring may signal your intent to your SQL system more clearly. The result looks like this.</p>
<pre class="lang-sql prettyprint-override"><code>   FROM generic p
   LEFT JOIN codes c ON  p.Level2 = c.codeValue AND c.code = '2'
   LEFT JOIN codes d ON  p.Level3 = d.codeValue AND d.code = '3'
</code></pre>
<p>If your SQL system allows indexes, a covering index like this on your <code>codes</code> table will help speed up your key/value lookup.</p>
<pre><code>ALTER TABLE codes ADD INDEX (codeValue, code, codeValueDescription)
</code></pre>
<p>Your SELECT clause contains a lot of this sort of thing:</p>
<pre class="lang-sql prettyprint-override"><code>   CASE
       WHEN c.codeValueDescription IS NULL THEN p.Level2
       ELSE c.codeValueDescription
   END AS L2_CODE,
   CASE
       WHEN d.codeValueDescription IS NULL THEN p.Level3
       ELSE d.codeValueDescription
   END AS L3_CODE
</code></pre>
<p>It probably doesn't help much, but this can be simplified by rewriting it as</p>
<pre class="lang-sql prettyprint-override"><code>   COALESCE(c.codeValueDescription, p.Level2) AS L2_CODE,
   COALESCE(d.codeValueDescription, p.Level3) AS L3_CODE
</code></pre>
<p>What happens if you eliminate your <code>DISTINCT</code> qualifier? It probably takes some processing time. If your <code>generic.ID</code> column is the primary key, <code>DISTINCT</code> does you no good at all: those column values don't repeat.  (Most modern SQL query planners detect that case and skip the deduplication step, but we don't know how modern your query planner is.)</p>
<p>Your query contains no overall <code>WHERE</code> clause so it necessarily must handle every row in your <code>generic</code> table. And, if that table is large your result set will be large. As I'm sure you know, scanning entire large tables takes time and resources.</p>
<p>All that being said, a millisecond per row for a query like this through a SQL bridge isn't smoking-gun-horrible performance. You may have to live with it.  The alternative might be to apply the codes to your data in your application program:  slurp the entire <code>codes</code> table then write some application logic to do your CASE / WHEN / THEN or COALESCE work. In other words, move the LEFT JOIN operations to your app. If your SQL bridge is fast at handling dirt-simple <code>SELECT * FROM generic</code> single table queries this will help a lot.</p>

