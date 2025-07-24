# H2 update with join
[Link to question](https://stackoverflow.com/questions/44409432/h2-update-with-join)
**Creation Date:** 1496829564
**Score:** 20
**Tags:** mysql, database, h2, liquibase
## Question Body
<p>As development DB I am using MySQL, and for tests I am using H2 database.
The following script works in MySQL very well, but it is fails on H2.</p>

<pre><code>UPDATE `table_a`
JOIN `table_b` ON `table_a`.id=`table_b`.a_id
SET `table_a`.b_id=`table_b`.id
</code></pre>

<p>In the internet I found that h2 doesn't support <code>UPDATE</code> clause with <code>JOIN</code>. Maybe there is a way to rewrite this script without <code>JOIN</code> clause?</p>

<p>By the way, I am using liquibase. Maybe I can write <code>UPDATE</code> clause with it's xml language?</p>

<p>I tried the following script</p>

<pre><code>UPDATE table_a, table_b
SET table_a.b_id = table_b.id
WHERE table_a.id = table_b.a_id
</code></pre>

<p>But I still getting errors. Seems, that H2 doesn't support updating multiple tables in one query. How can I rewrite this query in two different queries to collect ids and insert them?</p>

## Answers
### Answer ID: 69053888
<p>I've spend a lot of time for this kind of UPDATE. Please find out my comment, maybe somebody find it usefull:</p>
<ul>
<li>For every rows in WHERE condition executed UPDATE for SET</li>
<li>In inner SELECT you can use updated table columns</li>
<li>In case of error &quot;Scalar subquery contains more than one row&quot; - UPDATE for SET return more, than one row. Problem rows could be found with replace UPDATE by <code>SELECT COUNT(*)</code></li>
</ul>
<p>See also <a href="https://stackoverflow.com/questions/40565334/548473">Scalar subquery contains more than one row</a></p>
<p>Sample SELECT WITH UPDATE:</p>
<pre><code>UPDATE USER_DETAILS UD SET UD.GRADUATE_COMMENT=
(SELECT U.COMMENT FROM USERS U WHERE u.ID=UD.id) &lt;-- ref to outer updated table
WHERE UD.GRADUATE_COMMENT IS NULL;
</code></pre>

### Answer ID: 44845278
<p>Try something like this:</p>

<pre><code>update table_a a
set a.b_id = (select b.id from table_b b where b.a_id = a.id)
where exists
(select * from table_b b where b.a_id = a.id)
</code></pre>

