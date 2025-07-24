# Join in subquery failing on MySQL 5.7
[Link to question](https://stackoverflow.com/questions/76460736/join-in-subquery-failing-on-mysql-5-7)
**Creation Date:** 1686609838
**Score:** 0
**Tags:** sql, mysql
## Question Body
<p>I'm writing a data migration in SQL for an app that has to support multiple possible databases, including MySQL 5.7. Here is the code that I currently have:</p>
<pre><code>UPDATE sandboxes s
SET permission_id = (
  SELECT p.id
  FROM permissions p
  JOIN tables t ON t.id = s.table_id
  WHERE
    p.object LIKE CONCAT('/db/', t.db_id, '/schema/', t.schema, '/table/', s.table_id, '/query/segmented/')
    AND p.group_id = s.group_id
  LIMIT 1
)
WHERE permission_id IS NULL;
</code></pre>
<p>This fails on MySQL 5.7 with the error <code>Unknown column 's.table_id' in 'on clause'</code>. I'm assuming the <code>ON</code> clause is more strict in 5.7 than in later versions since it works in other versions of MySQL as well as in Postgres. Is there any way to get around this limitation? Or a way I can rewrite the query? I'm not great with SQL so any help is appreciated.</p>

## Answers
### Answer ID: 76460888
<p>It's not clear why you're getting the error, but you can solve it by using a <code>JOIN</code> in the <code>UPDATE</code> query rather than a subquery.</p>
<pre><code>UPDATE sandboxes s
JOIN permissions AS p on p.group_id = s.group_id
JOIN tables AS t ON t.table_id = s.table_id AND p.object = CONCAT('/db/', t.db_id, '/schema/', t.schema, '/table/', s.table_id, '/query/segmented/')
SET s.permission_id = p.id
</code></pre>

