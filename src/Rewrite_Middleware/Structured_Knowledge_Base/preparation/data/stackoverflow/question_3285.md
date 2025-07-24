# Is it possible to guarantee the order row locks are obtained across multiple UPDATE CTEs in PostgreSQL 14?
[Link to question](https://stackoverflow.com/questions/75118549/is-it-possible-to-guarantee-the-order-row-locks-are-obtained-across-multiple-upd)
**Creation Date:** 1673705493
**Score:** 1
**Tags:** postgresql
## Question Body
<p>On PostgreSQL 14</p>
<p>To avoid deadlocks, the <a href="https://www.postgresql.org/docs/14/explicit-locking.html#LOCKING-DEADLOCKS" rel="nofollow noreferrer">documentation</a> provides the following guidance:</p>
<blockquote>
<p>The best defense against deadlocks is generally to avoid them by being certain that all applications using a database acquire locks on multiple objects in a consistent order.</p>
</blockquote>
<p>The <a href="https://www.postgresql.org/docs/14/queries-with.html#QUERIES-WITH-MODIFYING" rel="nofollow noreferrer">documentation</a> on CTEs states:</p>
<blockquote>
<p>The sub-statements in WITH are executed concurrently with each other and with the main query. Therefore, when using data-modifying statements in WITH, the order in which the specified updates actually happen is unpredictable.</p>
</blockquote>
<p>I assume this also means the order in which the locks are obtained for the specified updates is also unpredictable.</p>
<p>Does this apply even if there is a dependency between CTEs? I assumed so as I could not find any documentation that states otherwise. Perhaps because the query planer has the potential to rewrite the query in such a way that the dependency no longer exists?</p>
<p>I did some experimenting:</p>
<pre class="lang-sql prettyprint-override"><code>create table table_a (id int primary key, fu int);
create table table_b (id int primary key, bar int);
</code></pre>
<pre class="lang-sql prettyprint-override"><code>WITH update_a AS (
  UPDATE table_a
  SET fu = fu + 1
  WHERE id = 7
  RETURNING
    8 AS b_id,
    fu,
    pg_sleep(5)
),
update_b AS (
  UPDATE table_b
  SET bar = bar + 1
  FROM update_a
  WHERE id = b_id
  RETURNING
    bar,
    pg_sleep(3)
)
SELECT fu, bar FROM update_a, update_b;
</code></pre>
<p>I executed the above query and on another connection I executed:</p>
<pre class="lang-sql prettyprint-override"><code>update table_b set bar = 0; \timing on \watch 1
</code></pre>
<p>The results were:</p>
<pre><code>UPDATE 1 |    1.392 ms
UPDATE 1 |    1.123 ms
UPDATE 1 |    1.648 ms
UPDATE 1 |    1.419 ms
UPDATE 1 | 2903.621 ms
</code></pre>
<p>Which shows the second connection was able to repeatably obtain a lock and update <code>table_b</code> without waiting for the first 5 seconds, but then had to wait to obtain the lock for ~3 seconds afterwards. This aligns with the <code>pg_sleep(5)</code> and <code>pg_sleep(3)</code> which I assume means PSQL did not lock the <code>table_b</code> row until after the <code>update_a</code> CTE completed.</p>
<p>However, I also noticed the <code>pg_locks</code> table contains a <code>RowExclusiveLock</code> for both <code>table_a</code> and <code>table_b</code> immediately after executing the first query, and remained the same throughout the entire 8 seconds. Though I confess to not knowing how to really read this table:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>pid</th>
<th>virtualtransaction</th>
<th>transactionid</th>
<th>relname</th>
<th>locktype</th>
<th>mode</th>
<th>granted</th>
<th>waitstart</th>
</tr>
</thead>
<tbody>
<tr>
<td>2318</td>
<td>3/139</td>
<td>NULL</td>
<td>table_a</td>
<td>relation</td>
<td>RowExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
<tr>
<td>2318</td>
<td>3/139</td>
<td>NULL</td>
<td>table_a_pkey</td>
<td>relation</td>
<td>RowExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
<tr>
<td>2318</td>
<td>3/139</td>
<td>NULL</td>
<td>table_b</td>
<td>relation</td>
<td>RowExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
<tr>
<td>2318</td>
<td>3/139</td>
<td>NULL</td>
<td>table_b_pkey</td>
<td>relation</td>
<td>RowExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
<tr>
<td>2318</td>
<td>3/139</td>
<td>NULL</td>
<td>NULL</td>
<td>virtualxid</td>
<td>ExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
<tr>
<td>2318</td>
<td>3/139</td>
<td>13304</td>
<td>NULL</td>
<td>transactionid</td>
<td>ExclusiveLock</td>
<td>t</td>
<td>NULL</td>
</tr>
</tbody>
</table>
</div>
<p>If I rewrite the query to remove the dependency by omitting <code>FROM updated_b</code>, the behavior is inconsistent and seems to change based on table ordering in the <code>SELECT</code> statement or other factors.</p>
<p>Perhaps I got lucky? Again, I could not find this documented anywhere so I assume this behavior is not guaranteed.</p>
<p>If so, does this mean if one wanted to update two rows from <strong>different tables</strong> in a single query <strong>using CTEs</strong>, there is no way to guarantee the order the rows are locked, therefore allowing for the possibility of a deadlock?</p>
<p>(I realize I there are alternate solutions such using multiple queries, functions/<code>DO</code> statements, Repeatable Read isolation level, etc., but I am curious about the specific behavior of CTEs and locking order.)</p>

