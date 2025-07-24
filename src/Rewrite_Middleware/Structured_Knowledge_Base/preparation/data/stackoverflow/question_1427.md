# Postgresql: How to insert or update a record
[Link to question](https://stackoverflow.com/questions/75826376/postgresql-how-to-insert-or-update-a-record)
**Creation Date:** 1679593437
**Score:** 1
**Tags:** sql, postgresql
## Question Body
<p>I need to update the data, and if they are not in the database, then insert and return the key. Unfortunately, I can't use merge, on conflict and procedural blocks. Now I'm using the following query,</p>
<pre><code>WITH _a AS (
  UPDATE mytable1 SET name=expr1, last_name = expr2
  WHERE empId = expr3
  RETURNING empId 
), _b AS (
  INSERT INTO mytable1 (empId, name, last_name)
  SELECT(expr3, expr1, expr2)
  WHERE NOT EXISTS (SELECT * FROM _a)
  RETURNING empId 
</code></pre>
<p>but unfortunately, if the query inserts data, it returns the key, and if it updates, it doesn't.</p>
<p>Is it possible to somehow rewrite the request so that it always returns the key?</p>

## Answers
### Answer ID: 75826479
<blockquote>
<p>Is it possible to somehow rewrite the request so that it always
returns the key?</p>
</blockquote>
<p>You are almost there.</p>
<p>Just use <code>union all</code> to combine results of <code>insert</code> and <code>update</code> statements.</p>
<pre><code>WITH _a AS (
  UPDATE mytable1 SET name = expr1, last_name = expr2
  WHERE empId = expr3
  RETURNING empId 
), _b AS (
  INSERT INTO mytable1 (empId, name, last_name)
  SELECT expr3, expr1, expr2
  WHERE NOT EXISTS (SELECT * FROM _a)
  RETURNING empId 
)
SELECT empId FROM _a
UNION ALL
SELECT empId FROM _b;
</code></pre>

