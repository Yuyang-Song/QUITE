# What is “E153 Updatable queries with subqueries” in the SQL standard?
[Link to question](https://stackoverflow.com/questions/2020189/what-is-e153-updatable-queries-with-subqueries-in-the-sql-standard)
**Creation Date:** 1262867043
**Score:** 2
**Tags:** sql, standards-compliance, semantics
## Question Body
<p>I don't have the (expensive) SQL standard at hand; what are updatable queries in SQL core/foundation?</p>

<p>I see that PostgreSQL doesn't support them, but some other databases do; can you point me to the documentation on how they work in those databases?</p>

<p>PostgreSQL has query rewriting and updatable views with the <a href="http://www.postgresql.org/docs/current/interactive/rules.html" rel="nofollow noreferrer">rule</a> <a href="http://www.postgresql.org/docs/current/interactive/sql-createrule.html" rel="nofollow noreferrer">system</a>; is this very different?</p>

## Answers
### Answer ID: 2020442
<p>I just found this Oracle example on Wikipedia that looks like a SELECT in the left-hand side of an update:</p>

<pre><code>UPDATE (
SELECT *
  FROM articles  
  JOIN classification c 
    ON a.articleID = c.articleID 
) AS a
SET a.[updated_column] = updatevalue
WHERE c.classID = 1
</code></pre>

<p>Whereas most databases need the query to be written as:</p>

<pre><code>UPDATE a
SET a.[updated_column] = updatevalue
FROM articles a 
JOIN classification c 
ON a.articleID = c.articleID 
WHERE c.classID = 1
</code></pre>

<p>Links: The oracle <a href="http://download.oracle.com/docs/cd/E11882_01/server.112/e10592/statements_10008.htm#SQLRF55455" rel="nofollow noreferrer">reference docs</a>, <a href="http://download.oracle.com/docs/cd/E11882_01/server.112/e10592/statements_10002.htm#i2071643" rel="nofollow noreferrer">examples</a>.</p>

<p>Do other databases support this? Where is it documented?</p>

<hr>

<p>Having now laid my grubby mittens on the standard, I'll just quote it.</p>

<p>E153 refers to:</p>

<blockquote>
  <p>Subclause 7.12, “&lt;query
  expression>”: A &lt;query expression> is
  updatable even though its &lt;where
  clause> contains a &lt;subquery></p>
</blockquote>

<p>Since a query expressions is also a table (not intuitive but it's in SQL99 4.16.3 Operations involving tables), it means the query expression is an “udpatable table”. Which according to 4.16 means I can INSERT into and DELETE from them.</p>

<p>Which means I can run the above, as well as:</p>

<pre><code>DELETE FROM (SELECT * FROM t1 JOIN t2 WHERE t1c1 = t2c3);
</code></pre>

<p>There are some more rules to determine what query expressions are updatable, contained in sql99-foundation 7.11 and 7.12; they are rather involved. PostgreSQL doesn't let query expressions that aren't table names be updatable. There is some work being done on updatable views. I'm not sure how useful the feature is outside of views, but the standard is definitely interesting, and weirder than expected.</p>

<p>[It's feeling lonely here. Picking my answer as best.]</p>

