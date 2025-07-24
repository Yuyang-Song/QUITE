# Querying using subqueries on a SQLite database approx 10x slower using newer versions of System.Data.SQLite/sqlite3.dll
[Link to question](https://stackoverflow.com/questions/14812712/querying-using-subqueries-on-a-sqlite-database-approx-10x-slower-using-newer-ver)
**Creation Date:** 1360588329
**Score:** 0
**Tags:** .net, performance, sqlite, subquery, linqpad
## Question Body
<p><strong>(See update below)</strong></p>

<p>I am having an issue of slow query performance when querying a very simplistic Sqlite datatable of about 500,000 rows from within a C#.Net application (~5sec).</p>

<p>I have tried the exact same query on exactly the same database using LinqPad, as well as 2 database browsers (both based on QtSql), and it runs 10x faster (~0.5secs). Same query, same db, different apps, only mine doesn't run fast.</p>

<p>It makes negligible difference whether I'm returning values or just a Count(*).</p>

<p>I've tried:</p>

<ul>
<li>building for each of .Net 3.5/4/4.5</li>
<li>building for each of of AnyCPU/x86/x64</li>
<li>using each of System.Data.Sqlite, sqlite-net, as well as directly accessing a sqlite3 dll via COM</li>
<li>building for each of WPF/WinForms</li>
<li>different variations of the queries</li>
</ul>

<p>None of these make any noticible difference to the query time.</p>

<p>I know that rewriting the query using JOINs may help, but what I can't figure out is why the same query works fine in LinqPad/Sql browers but not from any app I try to create. I must be missing something pretty fundamental.</p>

<p>Example Table:</p>

<pre><code>"CREATE TABLE items(id INTEGER PRIMARY KEY, id1 INTEGER, id2 INTEGER, value INTEGER)"
</code></pre>

<p>Example Query String (though basically any query using a subquery takes a long time):</p>

<pre><code>SELECT count(*) 
FROM items WHERE 
id2 IN 
(
    SELECT DISTINCT id2 FROM items WHERE id1 IN 
    (
        SELECT DISTINCT id1 FROM items WHERE id2 = 100000 AND value = 10
    )
    AND value = 10
) 
AND value = 10 
GROUP BY id2
</code></pre>

<p>I know this could probably be re-written using JOINS and indexing to speed it up, but the fact remains that this query works significantly faster from other apps. What am I missing here as to why the same query runs so much slower no matter what I try?</p>

<p><strong>UPDATE:</strong> It seems the version of sqlite has something to do with the issue. Using the legacy System.Data.Sqlite v1.0.66.0 the query runs just like the other apps, however using a more recent version it is slow. I haven't pinpointed what at what version exactly this changed, but am pretty sure it's to do with the underlying sqlite3 version not System.Data.Sqlite specifically. If anyone knows what could have changed that would cause subqueries to slow down so much in this situation, or if there are settings or something that can make subqueries run faster in new versions of sqlite please let me know!</p>

<p>Again, the query is an example and is not ideal and partially redundant... the question is more about why it works in one and not the other.</p>

<p>Thanks in advance for any additional input!</p>

<p><strong>UPDATE:</strong> SOLVED</p>

<p>See my answer below.</p>

## Answers
### Answer ID: 14828449
<p>Ok turns out it was to do with Automatic Indexing, which was introduced with SQLite 1.7.0. In my situation using subqueries on this kind of table without indexes meant that the time it took SQLite to create the automatic indexes was causing the additional overhead that the queries were experiencing.</p>

<p>The solution was to use:</p>

<pre><code>PRAGMA automatic_index=OFF;
</code></pre>

<p>at the start of any query that uses the "IN" clause.</p>

<p>Creating indexes on the columns may also solve this (untested), however in this particular situation the additional size/disk usage necessary to create the indexes is not worth it.</p>

<p>This would also suggest that the LinqPad SQLite plugin and the database viewers I was using are based on old sqlite versions.</p>

<p>More information can be found at:</p>

<p><a href="http://www.sqlite.org/src/info/8011086c85c6c4040" rel="nofollow">http://www.sqlite.org/src/info/8011086c85c6c4040</a></p>

<p><a href="http://www.sqlite.org/optoverview.html#autoindex" rel="nofollow">http://www.sqlite.org/optoverview.html#autoindex</a></p>

<p>Thanks to everyone that responded.</p>

### Answer ID: 14814773
<p>Some suggestions:</p>

<p>You say you don't want to rework your queries nor add indexes. That is the obvious thing to do here. Without any indexes sqlite has to scan your 500,000 row table at least one time (or more likely multiple times).</p>

<p>Based on your query above I would add indexes to columns <code>id1</code> and <code>id2</code>.</p>

<p><strike>
One other thing is that your query above seems a little redundant. Maybe you have your reasons, but I cannot see why the query should be so complicated. Simplified query:</p>

<pre><code>select count(*)
from items
where id2 = 100000 and value = 10
</code></pre>

<p></strike></p>

### Answer ID: 14817191
<p>try </p>

<pre><code>SELECT ID1.id2, count(*) 
FROM items ID2
JOIN items ID1
  on ID2.id2 = ID1.id1
 and ID1.id2 = 100000 
 and ID1.value = 10 
 and ID2.valu3 = 10
group by ID1.id2
</code></pre>

