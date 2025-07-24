# MySQL Warning: #1287 Setting user variables within expressions is deprecated and will be removed in a future release
[Link to question](https://stackoverflow.com/questions/74254157/mysql-warning-1287-setting-user-variables-within-expressions-is-deprecated-and)
**Creation Date:** 1667142196
**Score:** 0
**Tags:** mysql, sql, sql-update, inner-join
## Question Body
<p>I use this query to rewrite the id number column by date, after a new row is added to the database.
Even if the query runs well I can't fix the error displayed at the end of the query. Any suggestion?</p>
<pre><code> SET @ROW = 0;
 UPDATE `mytable` SET `id` = @ROW := @ROW+1 ORDER BY `date` ASC;
</code></pre>
<p><code>Warning: #1287 Setting user variables within expressions is deprecated and will be removed in a future release. Consider alternatives: 'SET variable=expression, ...', or 'SELECT expression(s) INTO variables(s)'.</code></p>
<p>I tried to modify the query</p>
<pre><code> set id = &quot;0&quot;;
 UPDATE `mytable` SET := id+1 ORDER BY `data` ASC;
</code></pre>
<p>with no success.</p>

## Answers
### Answer ID: 74254910
<p>User variables are mostly superseded with window functions, available in MySQL 8.0.</p>
<p>You can what you ask for with <code>row_number()</code>  and the <code>update</code>/<code>join</code> syntax :</p>
<pre class="lang-sql prettyprint-override"><code>update mytable t
inner join (select id, row_number() over(order by date, id) new_id from mytable) t1
  on t.id = t1.id
set t.id = t1.new_id
</code></pre>
<p><a href="https://dbfiddle.uk/JWcasGDJ" rel="nofollow noreferrer">Demo on DB Fiddlde</a>.</p>
<p>This assumes that <code>id</code> is a unique key to start with.</p>
<p>I would still question why you would need to alter what looks like a surrogate primary key. You can compute the row number on the fly in your queries in that's what you want, or use a view :</p>
<pre class="lang-sql prettyprint-override"><code>create view myview as
select t.*, row_number() over(order by date, id) new_id from mytable t
</code></pre>
<p><a href="https://dbfiddle.uk/gLJz6e8H" rel="nofollow noreferrer">Demo on DB Fiddlde</a></p>

