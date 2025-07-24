# Can you use &quot;?&quot; for parameters in postgres SQL?
[Link to question](https://stackoverflow.com/questions/15916003/can-you-use-for-parameters-in-postgres-sql)
**Creation Date:** 1365561633
**Score:** 1
**Tags:** sql, postgresql
## Question Body
<p>This should be stupidly simple to answer, but for the life of me I cannot find a definitive answer on this.</p>

<p>Can you use "?" in postgres, like you can in other database engines?</p>

<p>For example:</p>

<pre><code>SELECT * FROM MyTable WHERE MyField = ?
</code></pre>

<p>I know I can use the $n syntax for this, for example from psql this works:</p>

<pre><code>CREATE TABLE dummy (id SERIAL PRIMARY KEY, value INT);
PREPARE bar(int) AS INSERT INTO dummy (value) VALUES ($1);
EXECUTE bar(10);
SELECT * FROM DUMMY;
</code></pre>

<p>But if I try to prepare a statement using "?", eg.</p>

<pre><code>PREPARE bar(int) AS INSERT INTO dummy (value) VALUES (?);
</code></pre>

<p>I get:</p>

<blockquote>
  <p>ERROR:  syntax error at or near ")"
  LINE 1: PREPARE bar(int) AS INSERT INTO dummy (value) VALUES (?);</p>
</blockquote>

<p>...and yet, in various places I read that "postgres supports the ? syntax".</p>

<p>What's going on here? <em>Does</em> postgres support using ? instead of $1, $2, etc. 
If so, how do you use it?</p>

<p>Specifically, this is making my life a pain porting a bunch of existing sql server queries to postgres, and if I can avoid having to rewrite all the where conditions an <em>all of the sql statements</em> that would be very, very nice.</p>

## Answers
### Answer ID: 15916222
<p>SQL-level <code>PREPARE</code> in PostgreSQL does not support the <code>?</code> placeholder, it uses the <code>$1</code> ... <code>$n</code> style.</p>

<p>Most client libraries  support the standard placeholders used by that language in parameterized queries, eg PgJDBC uses <code>?</code> placeholders.</p>

<p>If you're sending your queries via a client library like nPgSQL, psqlODBC, PgJDBC, psycopg2, etc then you should be able to use the usual placeholders for that language and client.</p>

