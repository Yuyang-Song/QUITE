# Why does this SQLite query not use an index for the correlated subquery?
[Link to question](https://stackoverflow.com/questions/51906826/why-does-this-sqlite-query-not-use-an-index-for-the-correlated-subquery)
**Creation Date:** 1534581574
**Score:** 1
**Tags:** sqlite
## Question Body
<p>Consider a SQLite database for things with parts, containing the following tables</p>

<pre><code>CREATE TABLE thing (id integer PRIMARY KEY, name text, total_cost real);
CREATE TABLE part (id integer PRIMARY KEY, cost real);
CREATE TABLE thing_part (thing_id REFERENCES thing(id), part_id REFERENCES part(id));
</code></pre>

<p>I have an index to find the parts of a thing</p>

<pre><code>CREATE INDEX thing_part_idx ON thing_part (thing_id);
</code></pre>

<p>To illustrate the problem, I'm using the following queries to fill the tables with random data</p>

<pre><code>INSERT INTO thing(name)
    WITH RECURSIVE
        cte(x) AS (
            SELECT 1
            UNION ALL
            SELECT 1 FROM cte LIMIT 10000
        )
SELECT hex(randomblob(4)) FROM cte;
INSERT INTO part(cost)
    WITH RECURSIVE
        cte(x) AS (
            SELECT 1
            UNION ALL
            SELECT 1 FROM cte LIMIT 10000
        )
SELECT abs(random()) % 100 FROM cte;
INSERT INTO thing_part (thing_id, part_id)
SELECT thing.id, abs(random()) % 10000 FROM thing, (SELECT 1 UNION ALL SELECT 1), (SELECT 1 UNION ALL SELECT 1);
</code></pre>

<p>So each thing is associated with a small number of parts (4 in this example).</p>

<p>At this point, I have not yet set the total cost of the things. I thought I could use the following query</p>

<pre><code>UPDATE thing SET total_cost = (
    SELECT sum(part.cost)
    FROM thing_part, part
    WHERE thing_part.thing_id = thing.id
    AND thing_part.part_id = part.id);
</code></pre>

<p>but it is extremely slow (I did not have the patience to wait for it to complete).</p>

<p><code>EXPLAIN QUERY PLAN</code> shows that both <code>thing</code> and <code>thing_part</code> are being scanned over, only the lookup in <code>part</code> is done using the rowid:</p>

<pre><code>SCAN TABLE thing
EXECUTE CORRELATED SCALAR SUBQUERY 0
SCAN TABLE thing_part
SEARCH TABLE part USING INTEGER PRIMARY KEY (rowid=?)
</code></pre>

<p>If I look at the query plan for the inner query with a fixed <code>thing_id</code>, i.e.</p>

<pre><code>SELECT sum(part.cost)
FROM thing_part, part
WHERE thing_part.thing_id = 1000
AND thing_part.part_id = part.id;
</code></pre>

<p>it does use the <code>thing_part_idx</code>:</p>

<pre><code>SEARCH TABLE thing_part USING INDEX thing_part_idx (thing_id=?)
SEARCH TABLE part USING INTEGER PRIMARY KEY (rowid=?)
</code></pre>

<p>I would expect the first query to be equivalent to iterating over all rows of <code>thing</code> and executing the inner query each time, but obviously that's not the case. Why? Should I use a different index or rewrite my query or maybe do the iteration in the client to generate multiple queries instead?</p>

<p>In case it matters, I'm using SQLite version 3.22.0</p>

## Answers
### Answer ID: 51907505
<p>SQLite might use dynamic typing, but column types still matter for <a href="https://www.sqlite.org/datatype3.html#affinity" rel="nofollow noreferrer">affinity</a>, and indexes can be used only when the database can prove that index lookups behave the same as comparisons with the actual table values, which often requires the affinities to be compatible.</p>

<p>So when you tell the database that the <code>thing_part</code> values are integers:</p>

<pre><code>CREATE TABLE thing_part (
  thing_id integer REFERENCES thing(id),
  part_id  integer REFERENCES part(id)
);
</code></pre>

<p>then the index on that will have the correct affinity, and will be used:</p>

<pre>
QUERY PLAN
|--SCAN TABLE thing
`--CORRELATED SCALAR SUBQUERY
   |--SEARCH TABLE thing_part USING INDEX thing_part_idx (thing_id=?)
   `--SEARCH TABLE part USING INTEGER PRIMARY KEY (rowid=?)
</pre>

### Answer ID: 51906866
<p>I would rewrite your query as:</p>

<pre><code>-- calculating sum for each thing_id at once
WITH cte AS (
   SELECT thing_part.thing_id, sum(part.cost) AS s
    FROM thing_part 
    JOIN part
      ON thing_part.part_id = part.id
    GROUP BY thing_part.thing_id
)
UPDATE thing 
SET total_cost = (SELECT s FROM cte WHERE thing.id = cte.thing_id);
</code></pre>

