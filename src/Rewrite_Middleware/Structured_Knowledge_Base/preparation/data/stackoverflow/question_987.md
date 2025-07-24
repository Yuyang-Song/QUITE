# search mysql text field on plain equivalents chars
[Link to question](https://stackoverflow.com/questions/53590482/search-mysql-text-field-on-plain-equivalents-chars)
**Creation Date:** 1543828118
**Score:** -1
**Tags:** mysql
## Question Body
<p>I need to search a text field on a database avoiding mismatch for special chars but for the same phrase.</p>

<p>For example, if my search term in DB field is saved as "I lòve mysql ánd query" I would like to match the search for "I love mysql ánd query","I love mysql and query","I löve mysql ánd query",etc.</p>

<p>I was thinking to convert the phrases with a PHP function that I use for url rewrites flattening them out always to "I love mysql and query" but I'm not sure I can flatten them out in the query?</p>

## Answers
### Answer ID: 53591481
<p>Since your data is already written to the DB with accents, can you try using DB collation to map directly between accented characters:</p>

<pre><code>$connection-&gt;query("SET NAMES utf8 COLLATE utf8_general_ci");
</code></pre>

<p>You can read more about it <a href="https://dev.mysql.com/doc/refman/8.0/en/charset-collation-implementations.html" rel="nofollow noreferrer">here</a></p>

<p>The page above explaints clearly what this collation will do for you:</p>

<pre><code>mysql&gt; SET NAMES 'utf8' COLLATE 'utf8_general_ci';
Query OK, 0 rows affected (0.00 sec)

mysql&gt; CREATE TABLE t1
       (c1 CHAR(1) CHARACTER SET UTF8 COLLATE utf8_general_ci);
Query OK, 0 rows affected (0.01 sec)

mysql&gt; INSERT INTO t1 VALUES ('a'),('A'),('À'),('á');
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql&gt; SELECT c1, HEX(c1), HEX(WEIGHT_STRING(c1)) FROM t1;
+------+---------+------------------------+
| c1   | HEX(c1) | HEX(WEIGHT_STRING(c1)) |
+------+---------+------------------------+
| a    | 61      | 0041                   |
| A    | 41      | 0041                   |
| À    | C380    | 0041                   |
| á    | C3A1    | 0041                   |
+------+---------+------------------------+
4 rows in set (0.00 sec)
</code></pre>

<p>You can also test it for youself directly in the DB (test taken from <a href="https://stackoverflow.com/questions/4234010/how-do-i-convert-a-column-to-ascii-on-the-fly-without-saving-to-check-for-matche">here</a>):</p>

<pre><code>mysql&gt; SET NAMES 'utf8' COLLATE 'utf8_general_ci';
Query OK, 0 rows affected (0.00 sec)

mysql&gt; SELECT 'a' = 'A', 'a' = 'À', 'a' = 'á';
+-----------+-----------+-----------+
| 'a' = 'A' | 'a' = 'À' | 'a' = 'á' |
+-----------+-----------+-----------+
|         1 |         1 |         1 |
+-----------+-----------+-----------+
1 row in set (0.06 sec)
</code></pre>

