# MySQL5.6 vs Percona 5.7 implicit conversion issue
[Link to question](https://stackoverflow.com/questions/36250847/mysql5-6-vs-percona-5-7-implicit-conversion-issue)
**Creation Date:** 1459102413
**Score:** 1
**Tags:** php, mysql, pdo, percona, tokudb
## Question Body
<p>We've recently begun testing an upgrade from mySQL5.6 to percona server 5.7 and the use of tokuDB tables.  The database is serving our PHP 5.5 application which use PDO library for parameterized querying.</p>

<p>Upon loading up percona with identical data into a tokudb table and comparing performance to the existing production we immediately noticed a huge drop in performance (10x slower).  For the queries below assume the table has 12 million rows</p>

<p>I've been able to narrow this issue down in the 5.7 database to the fact that when executing a query such as:</p>

<pre><code>SELECT * FROM TABLE WHERE id='12345'; -- exec time 10.5sec
vs.
SELECT * FROM TABLE WHERE id=12345; -- exec time 1.3sec
</code></pre>

<p>where id is of column type integer.  It was my impression and my research seems to confirm that mySQL should do implicit conversion of '12345' to 12345 when the column compared is a numeric type, however this doesn't seem to be happening in mySQL5.7/Percona.  It was happening in mySQL5.6x</p>

<p>The problem here is that with this behavior, you'd need to explicitly set the type using PDOStatement::bindParam  (ref <a href="http://php.net/manual/en/pdostatement.bindparam.php" rel="nofollow">http://php.net/manual/en/pdostatement.bindparam.php</a>) for each variable!  Doing this would cause a near global rewrite of all prepared statements which currently pass arrays of parameters to PDOStatement:execute() which doesn't support explicit type setting!</p>

<p>So - my question is this - has something changed in mySQL so implicit conversion isn't done in 5.7 or is it Percona or is it tokuDB table?  Is there a configuration parameter I can set to  turn this back on?</p>

## Answers
### Answer ID: 36265779
<p>It is not clear if you are trying to upgrade and compare 5.6 TokuDB performance to 5.7 TokuDB performance or 5.6 InnoDB to 5.7 TokuDB, can you please clarify and identify the specific 5.6 and 5.7 variants and versions?</p>

<p>If TokuDB all around, one possibility is incorrect index selection due to bad/old/NULL index statistics. There are also many SQL_MODE defaults changes in 5.7 some of which could also be influencing the behavior.</p>

<p>It might also be useful to see the results of 'SHOW CREATE TABLE' and 'SHOW INDEXES FROM' on both the 5.6 and 5.7 instances.</p>

