# MariaDB/MySQL str_to_date format with timezone offset
[Link to question](https://stackoverflow.com/questions/70340209/mariadb-mysql-str-to-date-format-with-timezone-offset)
**Creation Date:** 1639425136
**Score:** 3
**Tags:** php, mysql, date, datetime, mariadb
## Question Body
<h2>Edit: TL;DR</h2>
<pre class="lang-sql prettyprint-override"><code># This query ---------------------------------------

SELECT STR_TO_DATE('2020-10-20T14:43:49+00:00', '%Y-%m-%dT%H:%i:%s') AS date;

# Results in----------------------------------------

+---------------------+
| date                |
+---------------------+
| 2020-10-20 14:43:49 |
+---------------------+

# But throws----------------------------------------

+---------+------+-----------------------------------------------------------------+
| Level   | Code | Message                                                         |
+---------+------+-----------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect datetime value: '2020-10-20T14:43:49+00:00' |
+---------+------+-----------------------------------------------------------------+
</code></pre>
<p>Why?</p>
<h2>Detailed description</h2>
<p>I have read through a lot of questions regarding similar issues, but could not find a definitive answer to this problem.</p>
<p>I'm running Doctrine migrations in a Symfony 5.2.x project on a MariaDB 10.2 database. I am trying to extract a date string from a JSON data column into its own column on the same table, but running into error messages when the original date string has a certain format.</p>
<pre class="lang-sql prettyprint-override"><code>ALTER TABLE form 
  ADD updated_at DATETIME DEFAULT NULL;

UPDATE form AS f 
  SET updated_at = STR_TO_DATE(
    TRIM(BOTH '&quot;' FROM (
      SELECT JSON_EXTRACT(f.data, '$.updatedAt')
    )), 
    '%Y-%m-%dT%H:%i:%s+00:00'
  );
</code></pre>
<p>This works for any date string with a timezone offset of 0, like <code>2020-12-04T11:14:07+00:00</code>. For obvious reasons, it fails for a non-zero offset like <code>2020-12-04T11:14:07+01:00</code>, because</p>
<blockquote>
<p>Literal characters in <em>format</em> must match literally in <em>str</em>.</p>
<p>-- <a href="https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_str-to-date" rel="nofollow noreferrer">https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_str-to-date</a></p>
</blockquote>
<p>and results in an error</p>
<pre><code>Warning | 1411 | Incorrect datetime value: '2020-12-04T11:14:07+01:00' for function str_to_date
</code></pre>
<p><strong>However</strong>, if I understand the documentation correctly, I shouldn't even have to include the timezone offset in the format string:</p>
<blockquote>
<p>Extra characters at the end of <em>str</em> are ignored.</p>
</blockquote>
<p>But when I change the format string from <code>'%Y-%m-%dT%H:%i:%s+00:00'</code> to <code>'%Y-%m-%dT%H:%i:%s'</code>, the update operation fails for <em><strong>all</strong></em> items, even though the dates are parsed correctly (or, at least, <em>look</em> correct):</p>
<pre class="lang-sql prettyprint-override"><code>MariaDB [db]&gt; select STR_TO_DATE('2020-10-20T14:43:49+00:00', '%Y-%m-%dT%H:%i:%s') as date;
+---------------------+
| date                |
+---------------------+
| 2020-10-20 14:43:49 |
+---------------------+
1 row in set, 1 warning (0.00 sec)


MariaDB [db]&gt; show warnings;
+---------+------+-----------------------------------------------------------------+
| Level   | Code | Message                                                         |
+---------+------+-----------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect datetime value: '2020-10-20T14:43:49+00:00' |
+---------+------+-----------------------------------------------------------------+
1 row in set (0.00 sec)

</code></pre>
<h2>The Question</h2>
<p>Apart from the historic bug in the application that would in some cases result in a non-UTC <code>updated_at</code> date, <strong>what am I doing wrong</strong>? As I understand it, anything in the string after the bit matching <code>%s</code> should be ignored by <code>STR_TO_DATE()</code> and irrelevant to the query. Why are my migrations failing when the DB clearly manages to parse the strings to something that looks like the <code>datetime</code> type it understands? How can I make sure it parses every item's date irrespective of its TZ offset (I wouldn't even mind if the result was updated_at times for some items with an hour's difference to the actual datetime)?</p>
<h2>Edit</h2>
<p>Because I don't fully understand what it does or what the implications are, I've tried changing <code>sql_mode</code> before executing my queries, but got the same results:</p>
<pre class="lang-sql prettyprint-override"><code>SET @@SQL_MODE = REPLACE(@@SQL_MODE, 'NO_ZERO_IN_DATE', '');
SET @@SQL_MODE = REPLACE(@@SQL_MODE, 'NO_ZERO_DATE', '');
</code></pre>
<h2>Edit II</h2>
<p>I ended up rewriting the migration and manually looping over each entry in PHP, re-setting the timezone and writing the corrected (UTC) value back to the DB.
This is obviously way more verbose and much slower than the SQL one-liner. The lack of answers (or even comments) here suggests I might have stumbled upon either a Maria/MySQL bug or faulty documentation.</p>

