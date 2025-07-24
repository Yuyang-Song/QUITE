# Rewrite sql to support joins
[Link to question](https://stackoverflow.com/questions/15509810/rewrite-sql-to-support-joins)
**Creation Date:** 1363725016
**Score:** 0
**Tags:** mysql, sql, wordpress
## Question Body
<p>I have the following query which in oracle databases should work but current wordpress instalation uses a mysql database. Could you please help me out to rewrite the next query so it will work on mysql ?</p>

<pre><code>$wpdb-&gt;get_results("SELECT a.ID, a.post_title, DAYOFMONTH(b.meta_value) as dom "
."FROM $wpdb-&gt;posts a, $wpdb-&gt;postmeta b "
."WHERE b.meta_value &gt;= '{$thisyear}-{$thismonth}-01 00:00:00' "
."AND b.meta_value &lt;= '{$thisyear}-{$thismonth}-{$last_day} 23:59:59' "
."AND a.post_type = 'post' AND a.post_status = 'publish' AND a.ID = b.postid AND   b.meta_key='Event Date'"
);
</code></pre>

## Answers
### Answer ID: 15510568
<p>You may have a problem with the date format of the constant.  I would suggest converting the date into the same format using <code>to_char()</code>.  I'm thinking something along the lines of:</p>

<pre><code>SELECT a.ID, a.post_title, to_char(b.meta_value, 'DD') as dom "
."FROM $wpdb-&gt;posts a, $wpdb-&gt;postmeta b "
."WHERE to_char(b.meta_value, 'YYYY-MM-DD HH:MI:SS') &gt;= '{$thisyear}-{$thismonth}-01 00:00:00' "
."AND to_char(b.meta_value, 'YYYY-MM-DD HH:MI:SS') &lt;= '{$thisyear}-{$thismonth}-{$last_day} 23:59:59' "
."AND a.post_type = 'post' AND a.post_status = 'publish' AND a.ID = b.postid AND   b.meta_key='Event Date'
</code></pre>

<p>Or, more simply:</p>

<pre><code>SELECT a.ID, a.post_title, to_char(b.meta_value, 'DD') as dom "
."FROM $wpdb-&gt;posts a, $wpdb-&gt;postmeta b "
."WHERE to_char(b.meta_value, 'YYYY-MM') = '{$thisyear}-{$thismonth}' "
."AND a.post_type = 'post' AND a.post_status = 'publish' AND a.ID = b.postid AND   b.meta_key='Event Date'
</code></pre>

<p>This assumes that <code>meta-value</code> is stored as a date.  If not, you have to deal with conversion of values into dates.  I'm making this assumption because you are using a function <code>DAYOFMONTH</code>.</p>

### Answer ID: 15509966
<p>There isn't an issue with your query in MySQL from what I can tell.  Both of the following statements produce the same results (although I prefer to use the <code>JOIN</code>).  Here is a simplified version:</p>

<pre><code>SELECT  *
FROM table1 t 
    JOIN table2 t2 on t.id = t2.id
WHERE t.dt &gt;= '2011-01-02 00:00:00';

SELECT  *
FROM table1 t, table2 t2
WHERE t.dt &gt;= '2011-01-02 00:00:00' 
   AND t.id = t2.id;
</code></pre>

<p><a href="http://sqlfiddle.com/#!2/a5aba6/3" rel="nofollow">SQL Fiddle Demo</a></p>

