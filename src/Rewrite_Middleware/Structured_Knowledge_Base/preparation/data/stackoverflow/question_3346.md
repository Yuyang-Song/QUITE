# PostgreSQL - Subquery gives different results inside and outside function
[Link to question](https://stackoverflow.com/questions/76944420/postgresql-subquery-gives-different-results-inside-and-outside-function)
**Creation Date:** 1692613680
**Score:** 1
**Tags:** postgresql, function, subquery
## Question Body
<p>I have 2 identical queries except for one being inside a function and the other outside a function and they produce different results.</p>
<p>Originally I wrote the query outside a function substituting input with a CTE as this was easier to experiment with. Once done I placed it inside a function with minor tweaks to it.</p>
<p>I tracked the issue down to a subquery and then wrote a simplified version of what I was doing to post here.</p>
<h3>PostgreSQL versions</h3>
<p>The database I'm using is:</p>
<p>Docker image:</p>
<pre><code>timescale/timescaledb-ha:pg14.6-ts2.9.2-p0
</code></pre>
<p>SELECT VERSION():</p>
<pre><code>PostgreSQL 14.6 (Ubuntu 14.6-1.pgdg22.04+1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, 64-bit
</code></pre>
<p>As it is a bit older and not official one I also tried newest version as of this post:</p>
<p>Docker image:</p>
<pre><code>postgres:15.4-bookworm
</code></pre>
<p>SELECT VERSION():</p>
<pre><code>PostgreSQL 15.4 (Debian 15.4-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
</code></pre>
<h3>SQL</h3>
<p>There are 3 tables, table_a, table_b and table_join (for many-many relation between a and b) and the function.</p>
<p>A few drops for convenience:</p>
<pre><code>DROP FUNCTION IF EXISTS testfunc;  
DROP TABLE IF EXISTS table_join;  
DROP TABLE IF EXISTS table_a;  
DROP TABLE IF EXISTS table_b;
</code></pre>
<p>Tables:</p>
<pre><code>CREATE TABLE table_a  
(  
    id INT PRIMARY KEY,  
    name TEXT NOT NULL  
);  
  
CREATE TABLE table_b  
(  
    id INT PRIMARY KEY,  
    state TEXT NOT NULL  
);  
  
CREATE TABLE table_join  
(  
    table_a_id INT NOT NULL  
        CONSTRAINT &quot;FK_table_a&quot;  
            REFERENCES table_a,  
    table_b_id INT NOT NULL  
        CONSTRAINT &quot;FK_table_b&quot;  
            REFERENCES table_b  
);
</code></pre>
<p>Some test data for table_a, table_b:</p>
<pre><code>INSERT INTO table_a  
VALUES  
    (1, 'has_include')  
    ,(2, 'has_exclude')  
    ,(3, 'has_include_exclude')  
    ,(4, 'has_optional')  
;  
  
INSERT INTO table_b  
VALUES  
    (1, 'include'),  
    (2, 'exclude'),  
    (3, 'optional')  
;
</code></pre>
<p>The test data for table_join is hardcoded into the 2 queries below. Note that the issue can be reproduced without table_join and some of the records but this gives slightly more context to what I was doing. The function in its original state also inserts into table_join. The logic is as follows: Get table_a records with at least 1 include and no exclude in table_b</p>
<p>Query without function:</p>
<pre><code>WITH args (table_a_id, table_b_id) AS (  
    VALUES  
    -- table_a record 1 + include (table_b)  
    (1, 1),  
    -- table_a record 2 + exclude (table_b)  
    (2, 2),  
    -- table_a record 3 + include &amp; exclude (table_b)  
    (3, 1),  
    (3, 2),  
    -- table_a record 4 + optional (table_b)  
    (4, 3)  
), with_join AS (  
    SELECT x.table_a_id, b.state FROM args x  
    JOIN table_b b ON b.id = x.table_b_id  
), with_include AS (  
    SELECT * FROM with_join x  
    WHERE x.state = 'include'  
    -- AND x.state &lt;&gt; 'exclude'  
    AND x.table_a_id NOT IN (  
        SELECT y.table_a_id FROM with_join y  
        WHERE y.state = 'exclude'  
        )  
)  
SELECT * FROM with_include;
</code></pre>
<p>Query with function and call:</p>
<pre><code>CREATE FUNCTION testfunc(table_join)  
RETURNS TABLE(table_a_id INT, table_b_id TEXT)  
AS $$  
  
    WITH args (table_a_id, table_b_id) AS (  
        SELECT $1.*  
    ), with_join AS (  
        SELECT x.table_a_id, b.state FROM args x  
        JOIN table_b b ON b.id = x.table_b_id  
    ), with_include AS (  
        SELECT * FROM with_join x  
        WHERE x.state = 'include'  
        AND x.table_a_id NOT IN (  
            SELECT y.table_a_id FROM with_join y  
            WHERE y.state = 'exclude'  
            )  
    )  
    SELECT * FROM with_include;  
  
$$ LANGUAGE SQL;  
  
WITH args AS (  
VALUES  
    -- table_a record 1 + include (table_b)  
    (1, 1),  
    -- table_a record 2 + exclude (table_b)  
    (2, 2),  
    -- table_a record 3 + include &amp; exclude (table_b)  
    (3, 1),  
    (3, 2),  
    -- table_a record 4 + optional (table_b)  
    (4, 3)  
)  
SELECT f.* FROM args a, testfunc(a) AS f;
</code></pre>
<h3>Results</h3>
<p>When calling without function the result is:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>table_a_id</th>
<th>state</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>include</td>
</tr>
</tbody>
</table>
</div>
<p>When  calling with function the result is:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>table_a_id</th>
<th>state</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>include</td>
</tr>
<tr>
<td>3</td>
<td>include</td>
</tr>
</tbody>
</table>
</div>
<p>Interestingly enough if you swap the subquery for the commented out AND clause in the query without function it produces the same result as the function. I do not know what happens underneath but it is possible that inside the function the subquery gets replaced by a simpler not equals check. This could also just be a coincidence.</p>
<h3>Questions</h3>
<ol>
<li><p>This looks like a bug to me and wondering if anybody can confirm and/or knows that is going on?</p>
</li>
<li><p>Since it is not working I assume I would have to rewrite it to using joins instead of subquery. Can this be done with a single join or require 2?</p>
</li>
<li><p>As an aside. In the original I have 3 joins inside the CTE called with_joins in this example. It also has a WHERE clause that checks on some values that only requires the first join. Question then is will all 3 joins be performed first and then the where executed after or is the query optimization smart enough to do check after first join and then only join matched elements with the next joins? Should I instead replace WHERE clause with AND on the ON or move the other 2 joins into separate CTE?</p>
</li>
<li><p>Another aside. For posts like this is it better to have explanations in between code sections for the sql above or make it easier to copy past all at once without text in between?</p>
</li>
</ol>

