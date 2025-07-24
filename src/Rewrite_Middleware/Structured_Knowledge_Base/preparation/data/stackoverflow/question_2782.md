# How to optimize OR clauses in ON condition in PostgreSQL?
[Link to question](https://stackoverflow.com/questions/52115155/how-to-optimize-or-clauses-in-on-condition-in-postgresql)
**Creation Date:** 1535717212
**Score:** 0
**Tags:** sql, postgresql, sql-optimization
## Question Body
<p>I have a query like this:</p>

<pre><code>SELECT a.*
FROM a
LEFT JOIN b
  ON b.a_id = a.id
LEFT JOIN c
  ON c.a_id = a.id
LEFT JOIN (/* some complex subquery */) AS q
  ON q.id = a.id OR q.id = b.id OR q.id = c.id
</code></pre>

<p>Obviously it's not optimal because using ORs in the ON condition makes the planner unable to use indexes.</p>

<p>I tried to rewrite it like this:</p>

<pre><code>WITH (/* some complex subquery */) AS q
SELECT a.*
FROM a
LEFT JOIN q AS qa
  ON qa.id = a.id
LEFT JOIN b
  ON b.a_id = a.id
LEFT JOIN q AS qb
  ON qb.id = b.id
LEFT JOIN c
  ON c.a_id = a.id
LEFT JOIN q AS qc
  ON qc.id = c.id
WHERE COALESCE(qa.id, qb.id, qc.id) IS NOT NULL
</code></pre>

<p>but it didn't get much faster because the database still needs to evaluate  the WHERE clause.</p>

<p>Is there any technique to optimize such a kind of joins? If not, then how can I redesign the schema?</p>

