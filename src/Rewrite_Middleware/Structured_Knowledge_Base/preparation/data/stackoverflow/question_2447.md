# MySQL query index &amp; performance improvements
[Link to question](https://stackoverflow.com/questions/34657561/mysql-query-index-performance-improvements)
**Creation Date:** 1452176721
**Score:** 0
**Tags:** mysql, sql, performance
## Question Body
<p>I have created an application to track progress in <strong>League of Legends</strong> for me and my friends. For this purpose, I collect information about the current rank several times a day into my MySQL database. To fetch the results and show the to them in the graph, I use the following query / queries:</p>

<pre><code>SELECT 
    lol_summoner.name as name, grid.series + ? as timestamp, 
    AVG(NULLIF(lol.points, 0)) as points
FROM 
    series_tmp grid
JOIN 
    lol ON lol.timestamp &gt;= grid.series AND lol.timestamp &lt; grid.series + ?
JOIN 
    lol_summoner ON lol.summoner = lol_summoner.id
GROUP BY
    lol_summoner.name, grid.series
ORDER BY
    name, timestamp ASC

SELECT 
    lol_summoner.name as name, grid.series + ? as timestamp, 
    AVG(NULLIF(lol.points, 0)) as points
FROM 
    series_tmp grid
JOIN 
    lol ON lol.timestamp &gt;= grid.series AND lol.timestamp &lt; grid.series + ?
JOIN 
    lol_summoner ON lol.summoner = lol_summoner.id
WHERE 
    lol_summoner.name IN (". str_repeat('?, ', count($names) - 1) ."?)
GROUP BY
    lol_summoner.name, grid.series
ORDER BY
    name, timestamp ASC
</code></pre>

<p>The first query is used in case I want to retrieve all players which are saved in the database. The grid table is a temporary table which generated timestamps in a specific interval to retrive information in chunks of this interval. The two variable in this query are the interval. The second query is used if I want to retrieve information for specific players only.</p>

<p>The grid table is produces by the following stored procedure which is called with three parameters (n_first - first timestamp, n_last - last timestamp, n_increments - increments between two timestamps):</p>

<pre><code>BEGIN
    -- Create tmp table
    DROP TEMPORARY TABLE IF EXISTS series_tmp;
    CREATE TEMPORARY TABLE series_tmp (
        series bigint
    ) engine = memory;

    WHILE n_first &lt;= n_last DO
        -- Insert in tmp table
        INSERT INTO series_tmp (series) VALUES (n_first);

        -- Increment value by one
        SET n_first = n_first + n_increment; 
    END WHILE;
END
</code></pre>

<p>The query works and finishes in reasonable time (~10 seconds) but I am thankful for any help to improve the query by either rewriting it or adding additional indexes to the database.</p>

<p>/Edit:</p>

<p>After review of @Rick James answer, I modified the queries as follows:</p>

<pre><code>SELECT lol_summoner.name as name, (lol.timestamp div :range) * :range + :half_range as timestamp, AVG(NULLIF(lol.points, 0)) as points
  FROM lol
    JOIN lol_summoner ON lol.summoner = lol_summoner.id
  GROUP by lol_summoner.name, lol.timestamp div :range
  ORDER by name, timestamp ASC

SELECT lol_summoner.name as name, (lol.timestamp div :range) * :range + :half_range as timestamp, AVG(NULLIF(lol.points, 0)) as points
  FROM lol
    JOIN lol_summoner ON lol.summoner = lol_summoner.id
  WHERE lol_summoner.name IN (&lt;NAMES&gt;)
  GROUP by lol_summoner.name, lol.timestamp div " . $steps . "
  ORDER by name, timestamp ASC
</code></pre>

<p>This improves the query execution time by a really good margin (finished way under 1s).</p>

## Answers
### Answer ID: 34661722
<p><strong>Problem 1 and Solution</strong></p>

<p>You need a series of integers between two values?  And they differ by 1?  Or by some larger value?</p>

<p>First, create a <em>permanent</em> table of the numbers from 0 to some large enough value:</p>

<pre><code>CREATE TABLE Num10 ( n INT );
INSERT INTO Num10 VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);
CREATE TABLE Nums ( n INT, PRIMARY KEY(n))
    SELECT a.n*1000 + b.n*100 + c.n*10 + d.n
        FROM Num10 AS a
        JOIN Num10 AS b  -- note "cross join"
        JOIN Num10 AS c
        JOIN Num10 AS d;
</code></pre>

<p>Now <code>Nums</code> has 0..9999.  (Make it bigger if you might need more.)</p>

<p>To get a sequence of consecutive numbers from 123 through 234:</p>

<pre><code> SELECT 123 + n FROM Nums WHERE n &lt; 234-123+1;
</code></pre>

<p>To get a sequence of consecutive numbers from 12345 through 23456, in steps of 15:</p>

<pre><code> SELECT 12345 + 15*n FROM Nums WHERE n &lt; (23456-12345+1)/15;
</code></pre>

<p><code>JOIN</code> to a <code>SELECT</code> like one of those instead of to <code>series_tmp</code>.</p>

<p>Barring other issue, that should significantly speed things up.</p>

<p><strong>Problem 2</strong></p>

<p>You are <code>GROUPing BY</code> <code>series</code>, but <code>ORDERing</code> by <code>timestamp</code>.  They are related, so you might get the 'right' answer.  But think about it.</p>

<p><strong>Problem 3</strong></p>

<p>You seem to be building "buckets" (called "series"?) from "timestamps".  Is this correct?  If so, let's work backwards -- Turn a "timestamp" into a "bucket" number:</p>

<pre><code>bucket_number = (timestamp - start) / bucket_size
</code></pre>

<p>By doing that throughout, you can avoid 'Problem 1' and eliminate my solution to it.  That is, reformulate the entire queries in terms of buckets.</p>

