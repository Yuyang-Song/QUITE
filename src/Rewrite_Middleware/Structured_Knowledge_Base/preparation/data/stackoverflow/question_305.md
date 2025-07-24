# Select full outer join from many-to-many relationships
[Link to question](https://stackoverflow.com/questions/20083559/select-full-outer-join-from-many-to-many-relationships)
**Creation Date:** 1384900532
**Score:** 3
**Tags:** sql, sql-server-2008
## Question Body
<p>I am trying to do something in MSSQL which I suppose is a fairly simple and common thing in any database with many-to-many relationships. However I seem to always end up with a quite complicated select query, I seem to be repeating the same conditions several times to get the desired output.</p>

<p>The scenario is like this. I have 2 tables (table A and B) and a cross table with foreign keys to the ID columns of A and B. There can only be one unique pair of As and Bs in the crosstable (I guess the 2 foreign keys make up a primary key in the cross table ?!?). Data in the three tables could look like this:</p>

<pre><code>TABLE A          TABLE B            TABLE AB
ID     Type      ID     Type        AID    BID
--------------------------------------------------
R      Up         1      IN         R      3
S      DOWN       2      IN         T      3
T      UP         3      OUT        T      5
X      UP         4      OUT        Z      6
Y      DOWN       5      IN
Z      UP         6      OUT
</code></pre>

<p>Now let's say I select all rows in A of type UP and all rows in B of type OUT:</p>

<pre><code>SELECT ID FROM A AS A1
WHERE Type = 'UP'
(Result: R, T, X, Z)

SELECT ID FROM B AS B1
WHERE Type = 'OUT'
(Result: 3, 4, 6)
</code></pre>

<p>What I want now is to fully outer join these 2 sub queries based on the relations listed in AB. Hence I want all IDs in A1 and B1 to be listed at least once:</p>

<pre><code>A.ID    B.ID
R       3
T       3
null    4
X       null
Z       6
</code></pre>

<p>From this results set I want to be able to see:
- Which rows in A1 does not relate to any rows in B1
- Which rows in B1 does not relate to any rows in A1
- Relations between rows in A1 and B1</p>

<p>I have tried a couple of things such as:</p>

<pre><code>SELECT A1.ID, B1.ID
FROM (
    SELECT * FROM A
    WHERE Type = 'UP') AS A1

FULL OUTER JOIN AB ON
A1.ID = AB.AID

FULL OUTER JOIN (
    SELECT * FROM B
    WHERE Type = 'OUT') AS B1
ON AB.BID = B1.ID 
</code></pre>

<p>This doesn't work, since some of the relations listed in AB are between rows in A1 and rows NOT IN B1 OR between rows in B1 but NOT IN A1.</p>

<p>In other words - I seem to be forced to create a subquery for the AB table also:</p>

<pre><code>SELECT A1.ID, B1.ID
FROM (
    SELECT * FROM A
    WHERE Type = 'UP') AS A1

FULL OUTER JOIN (
    SELECT * FROM AB AS AB1
    WHERE
      AID IN (SELECT ID FROM A WHERE type = 'UP') AND
      BID IN (SELECT ID FROM B WHERE type = 'OUT')
) AS AB1 ON
A1.ID = AB1.AID

FULL OUTER JOIN (
    SELECT * FROM B
    WHERE Type = 'OUT') AS B1
ON AB1.BID = B1.ID
</code></pre>

<p>That just seems like a rather complicated solution for a seemingly simply problem. Especially when you consider that for A1 and B1 subqueries with more (complex) conditions - possible involving joins to other tables (one-to-many) would require the same temporary joins and conditions to be repeated in the AB1 subquery.</p>

<p>I am thinking that there must be an obvious way to rewrite the above select statements in order to avoid having to repeat the same conditions several times. The solution is probably right there in front me, but I just can't see it.</p>

<p>Any help would be appreciated.</p>

## Answers
### Answer ID: 20085045
<p>I think you could employ a CTE in this case, like this:</p>

<pre><code>;WITH cte AS (
  SELECT A.ID AS AID, A.Type AS AType, B.ID AS BID, B.Type AS BType
  FROM A FULL OUTER JOIN AB ON A.ID = AB.AID
  FULL OUTER JOIN B ON B.ID = AB.BID)
SELECT AID, BID FROM CTE WHERE AType = 'UP' OR BType = 'OUT'
</code></pre>

<p>The advantage of using a CTE is that it will be compiled once. Then you can add additional criteria to the WHERE clause outside the CTE</p>

<p>Check this <a href="http://sqlfiddle.com/#!3/247bc6/6" rel="nofollow">SQL Fiddle</a></p>

