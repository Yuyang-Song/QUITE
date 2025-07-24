# Why does mysql decide that this subquery is dependent?
[Link to question](https://stackoverflow.com/questions/10330856/why-does-mysql-decide-that-this-subquery-is-dependent)
**Creation Date:** 1335433187
**Score:** 2
**Tags:** mysql, performance, subquery
## Question Body
<p>On a MySQL 5.1.34 server, I have the following perplexing situation:</p>

<pre><code>mysql&gt; explain select * FROM master.ObjectValue WHERE id IN ( SELECT id FROM backup.ObjectValue ) AND timestamp &lt; '2008-04-26 11:21:59';
+----+--------------------+-------------+-----------------+-------------------------------------------------------------+------------------------------------+---------+------+--------+-------------+
| id | select_type        | table       | type            | possible_keys                                               | key                                | key_len | ref  | rows   | Extra       |
+----+--------------------+-------------+-----------------+-------------------------------------------------------------+------------------------------------+---------+------+--------+-------------+
|  1 | PRIMARY            | ObjectValue | range           | IX_ObjectValue_Timestamp,IX_ObjectValue_Timestamp_EventName | IX_ObjectValue_Timestamp_EventName | 9       | NULL | 541944 | Using where | 
|  2 | DEPENDENT SUBQUERY | ObjectValue | unique_subquery | PRIMARY                                                     | PRIMARY                            | 4       | func |      1 | Using index | 
+----+--------------------+-------------+-----------------+-------------------------------------------------------------+------------------------------------+---------+------+--------+-------------+
2 rows in set (0.00 sec)

mysql&gt; select * FROM master.ObjectValue WHERE id IN ( SELECT id FROM backup.ObjectValue ) AND timestamp &lt; '2008-04-26 11:21:59';
Empty set (2 min 48.79 sec)

mysql&gt; select count(*) FROM master.ObjectValue;
+----------+
| count(*) |
+----------+
| 35928440 |
+----------+
1 row in set (2 min 18.96 sec)
</code></pre>

<ul>
<li>How can it take 3 minutes to examine 500000 records when it only
takes 2 minutes to visit all records? </li>
<li>How can a subquery on a
separate database be classified dependent?</li>
<li>What can I do to speed up
this query?</li>
</ul>

<p>UPDATE:</p>

<p>The actual query that took a long time was a DELETE, but you can't do explain on those; DELETE is why I used subselect. I have now read the documentation and found out about the syntax "DELETE FROM t USING ..." Rewriting the query from:</p>

<pre><code>DELETE FROM master.ObjectValue 
WHERE timestamp &lt; '2008-06-26 11:21:59' 
AND id IN ( SELECT id FROM backup.ObjectValue ) ;
</code></pre>

<p>into:</p>

<pre><code>DELETE FROM m 
USING master.ObjectValue m INNER JOIN backup.ObjectValue b ON m.id = b.id 
WHERE m.timestamp &lt; '2008-04-26 11:21:59';
</code></pre>

<p>Reduced the time from minutes to .01 seconds for an empty backup.ObjectValue. </p>

<p>Thank you all for good advise.</p>

## Answers
### Answer ID: 10331134
<p>The dependent subquery slows you outer query down to a crawl (I suppose you know it means it's run once per row of found in the dataset being looked at).</p>

<p>You don't need the subquery there, and not using one will speedup your query quite significantly:</p>

<pre><code>SELECT m.*
FROM master.ObjectValue m
JOIN backup.ObjectValue USING (id)
WHERE m.timestamp &lt; '2008-06-26 11:21:59'
</code></pre>

<p>MySQL frequently treats subqueries as dependent even though they are not. I've never really understood the exact reasons for that - maybe it's simply because the query optimizer fails to recognize it as independent. I never bothered looking more in details because in these cases you can virtually always move it to the <code>FROM</code> clause, which fixes it.</p>

<p>For example:</p>

<pre><code>DELETE FROM m WHERE m.rid IN (SELECT id FROM r WHERE r.xid = 10)
// vs
DELETE m FROM m WHERE m.rid IN (SELECT id FROM r WHERE r.xid = 10)
</code></pre>

<p>The former will produce a dependent subquery and can be very slow. The latter will tell the optimizer to isolate the subquery, which avoids a table scan and makes the query run much faster.</p>

### Answer ID: 10331593
<p>Notice how it says there is only 1 row for the subquery? There is obviously more than 1 row. That is an indication that mysql is loading only 1 row at a time. What mysql is probably trying to do is "optimize" the subquery so that it only loads records in the subquery that also exist in the master query, a dependent subquery. This is how  a join works, but the way you phrased your query you have forced a reversal of the optimized logic of a join.</p>

<p>You've told mysql to load the backup table (subquery) then match it against the filtered result of the master table "timestamp &lt; '2008-04-26 11:21:59'". Mysql determined that loading the entire backup table is probably not a good idea. So mysql decided to use the filtered result of the master to filter the backup query, but the master query hasn't completed yet when trying to filter the subquery. So it needs to check as it loads each record from the master query. Thus your dependent subquery.</p>

<p>As others mentioned, use a join, it's the right way to go. Join the crowd.</p>

### Answer ID: 10331139
<blockquote>
  <p>How can it take 3 minutes to examine 500000 records when it only takes 2 minutes to visit all records?</p>
</blockquote>

<p><code>COUNT(*)</code> is always transformed to <code>COUNT(1)</code> in MySQL. So it doesn't even have to enter each record, and also, I would imagine that it uses in-memory indexes which speeds things up. And in the long-running query, you use range (<code>&lt;</code>) and <code>IN</code> operators, so for each record it visits, it has to do extra work, especially since it recognizes the subquery as dependent.</p>

<blockquote>
  <p>How can a subquery on a separate database be classified dependent?</p>
</blockquote>

<p>Well, it doesn't matter if it's in a separate database. A subquery is dependent if it depends on values from the outer query, which you could still do in your case... but you don't, so it is, indeed, strange that it's classified as a dependent subquery. Maybe it is just a bug in MySQL, and that's why it's taking so long - it executes the inner query for every record selected by the outer query.</p>

<blockquote>
  <p>What can I do to speed up this query?</p>
</blockquote>

<p>To start with, try using <code>JOIN</code> instead:</p>

<pre><code>SELECT master.*
FROM master.ObjectValue master
JOIN backup.ObjectValue backup
  ON master.id = backup.id
  AND master.timestamp &lt; '2008-04-26 11:21:59';
</code></pre>

