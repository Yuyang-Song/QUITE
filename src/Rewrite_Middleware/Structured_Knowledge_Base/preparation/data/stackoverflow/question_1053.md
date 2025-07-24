# Is there a way to force Oracle to evaluate the Filter after the Join Access?
[Link to question](https://stackoverflow.com/questions/56777528/is-there-a-way-to-force-oracle-to-evaluate-the-filter-after-the-join-access)
**Creation Date:** 1561567277
**Score:** 2
**Tags:** sql, oracle-database, oracle11g, oracle18c
## Question Body
<p>I want to filter on the result of a join, using a cast. The problem is that part of the original field cannot be cast to an Integer. It would not be a problem if the filter was applied after the join. This is why I wonder if there's a way (perhaps an Optimizer Hint or something) to push the filter evaluation after the join operation.</p>

<p>This is a query that I built for the example. I would expect it to work, but fails with an 'ORA-01722 invalid number' :</p>

<pre><code>WITH "literal" AS (
    SELECT 1 AS "literal_id", 'abc' AS "literal"
    FROM "DUAL"
    UNION
    SELECT 2 AS "literal_id", '7' AS "literal"
    FROM "DUAL"
),
     "scalar" AS (
         SELECT 3 AS "scalar_id", 2 AS "literal_id"
         FROM "DUAL"
         CONNECT BY ROWNUM &lt;= 10000
     )
SELECT *
FROM "scalar"
         JOIN "literal" USING ("literal_id")
WHERE TO_NUMBER("literal") &gt; 6;
</code></pre>

<p>The ORA-01722 is thrown because it's applied on the "literal" CTE, hence crashes because 'abc' is obviously not a number. 
We can see this in the execution plan :</p>

<p><a href="https://i.sstatic.net/ocoWL.png" rel="nofollow noreferrer">Query execution plan</a></p>

<p>To reduce the possibilities around the cause of my problem, I executed that query:</p>

<pre><code>CREATE TABLE "literal" AS (
    SELECT 1 AS "literal_id", 'abc' AS "literal"
    FROM "DUAL"
    UNION
    SELECT 2 AS "literal_id", '7' AS "literal"
    FROM "DUAL"
);
CREATE TABLE "scalar" AS (
    SELECT 3 AS "scalar_id", 2 AS "literal_id"
    FROM "DUAL"
    CONNECT BY ROWNUM &lt;= 10000
);
CREATE TABLE "joined" AS (
    SELECT *
    FROM "scalar"
             JOIN "literal" USING ("literal_id")
);
SELECT *
FROM "joined"
WHERE TO_NUMBER("literal") &gt; 6;
</code></pre>

<p>Which works perfectly fine.</p>

<p>So, is there a way to rewrite this query (I still need this to be a single query though) so it will not try to convert the 'abc' ?</p>

<p>For reference, I tried this on Oracle Database 18c Standard Edition 2 Release 18.0.0.0.0 as well as Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 </p>

<p>Thanks a lot.</p>

## Answers
### Answer ID: 56778173
<p>The old school trick is to structure the query such that the predicate can't be pushed into the join.  If you put the join into an inline view and add a <code>rownum</code>, that'll prevent the optimizer from evaluating the predicate until the join is complete</p>

<pre><code>WITH "literal" AS (
    SELECT 1 AS "literal_id", 'abc' AS "literal"
    FROM "DUAL"
    UNION
    SELECT 2 AS "literal_id", '7' AS "literal"
    FROM "DUAL"
),
     "scalar" AS (
         SELECT 3 AS "scalar_id", 2 AS "literal_id"
         FROM "DUAL"
         CONNECT BY ROWNUM &lt;= 10000
     )
select *
  from (
SELECT "scalar_id",  "literal_id", "literal", rownum
FROM "scalar"
         JOIN "literal" USING ("literal_id")
)
WHERE TO_NUMBER("literal") &gt; 6;
</code></pre>

<p>If you're on 12.2 or later, you have the ability to take advantage of enhancements to the <code>to_number</code> function to return a NULL if there is a conversion error.</p>

<pre><code>WITH "literal" AS (
    SELECT 1 AS "literal_id", 'abc' AS "literal"
    FROM "DUAL"
    UNION
    SELECT 2 AS "literal_id", '7' AS "literal"
    FROM "DUAL"
),
     "scalar" AS (
         SELECT 3 AS "scalar_id", 2 AS "literal_id"
         FROM "DUAL"
         CONNECT BY ROWNUM &lt;= 10000
     )
SELECT "scalar_id",  "literal_id", "literal"
FROM "scalar"
         JOIN "literal" USING ("literal_id")
WHERE to_number("literal" default null on conversion error) &gt; 6;
</code></pre>

### Answer ID: 56777607
<p>For the <code>where</code>, use a conditional conversion.  For example:</p>

<pre><code>SELECT *
FROM "scalar" s JOIN
     "literal" l
      USING ("literal_id")
WHERE (CASE WHEN REGEXP_LIKE(l.literal, '[^[0-9]+$')
            THEN TO_NUMBER(l.literal)
       END) &gt; 6;
</code></pre>

<p>As for your question, I don't think so.  Oracle has a pretty sophisticated optimizer, so it will rearrange operations to optimize performance.  You <em>could</em> use a CTE and a compiler hint to materialize the CTE, but that seems like overkill.</p>

