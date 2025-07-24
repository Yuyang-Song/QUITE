# MySQL: SELECT conditional statement with grouping based off of per record parameters possible?
[Link to question](https://stackoverflow.com/questions/10239290/mysql-select-conditional-statement-with-grouping-based-off-of-per-record-parame)
**Creation Date:** 1334887498
**Score:** 2
**Tags:** php, mysql, sql, database
## Question Body
<p>I have a report I'm rewriting for an application using MySQL as the database. Currently, the report is using a lot of grunt work coming from php, which creates arrays, re-stores them into a temp database then generates results from that temp DB.</p>

<p>One of the main goals from rewriting a bulk of all this code is to simplify and clean a lot of my old code and am wondering whether the below process can be simplified, or even better done solely on MySQL to let php just handle the dstribution of the data to the client.</p>

<p>I will use a made up scenario to describe what I am attempting to do:</p>

<p>Let's assume the following table (please note in real app, this table's information is actually pulled from several tables, but this should get the point across for clarity):</p>

<pre><code>+----+-----------+--------------+--------------+
| id | location  | date_visited | time_visited |
+----+-----------+--------------+--------------+
| 1  | place 1   | 2012-04-20   | 11:00:00     |
+----+-----------+--------------+--------------+
| 2  | place 2   | 2012-04-20   | 11:06:00     |
+----+-----------+--------------+--------------+
| 3  | place 1   | 2012-04-20   | 11:06:00     |
+----+-----------+--------------+--------------+
| 4  | place 3   | 2012-04-20   | 11:20:00     |
+----+-----------+--------------+--------------+
| 5  | place 2   | 2012-04-20   | 11:21:00     |
+----+-----------+--------------+--------------+
| 6  | place 1   | 2012-04-20   | 11:22:00     |
+----+-----------+--------------+--------------+
| 7  | place 3   | 2012-04-20   | 11:23:00     |
+----+-----------+--------------+--------------+
</code></pre>

<p>The report I need requires me to first list each location and then the number of visits made to that place. However, the caveat and what makes the query difficult for me is that there needs to be a time interval met for the visit to count whithin this report.</p>

<p>For example: Let's say the interval between visits to any given place is 10 minutes.</p>

<p>The first entry is locked in automatically because there are no previous entries, and so is the second since there are no other entries for 'place 2' yet. However on the third entry, place 1 is checked for the last time it was visited, which was less than the interval defined (10 minutes), therefore the report would ignore this entry and move along to the next one.</p>

<p>In essence, we are checking on a case by case scenario where the time interval is not from the last entry, but from the last entry from the same location.</p>

<p>The results from the report should look something like this in the end:</p>

<pre><code>+----+-----------+--------+
| id | location  | visits |
+----+-----------+--------+
| 1  | place 1   | 2      |
+----+-----------+--------+
| 2  | place 2   | 2      |
+----+-----------+--------+
| 3  | place 3   | 1      |
+----+-----------+--------+
</code></pre>

<p>My current implementation on a basic level goes through the following steps to acquire the above result set:</p>

<ol>
<li>MySQL query creates one temp table with a list of all the required locations and their ID.</li>
<li>MySQL query selects all the visit data whithin the specified time frame and passes it to PHP.</li>
<li>PHP &amp; MySQL populate the temporary table with the visits data, PHP does the grunt work here.</li>
<li>MySQL selects data from temporary table and returns it to client for display.</li>
</ol>

<p>My question is. Is there a way to do most of this with MySQL alone? What I've been trying to find is a way to write a MySQL query which can parse through the select statement and select only the visits which meet the above criteria and then finally groups it by location and provides me with a COUNT(*) of each group.</p>

<p>I really don't know if it's possible and am in hopes that one of the database gurus out there might be able to shed some light on how to do this.</p>

## Answers
### Answer ID: 10240805
<p>Suppose you have a table (probably temporary) of a slightly different structure:</p>

<pre><code>CREATE TABLE  `visits` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `location` varchar(45) NOT NULL,
  `visited` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `loc_vis` (`location`,`visited`)
) ENGINE=InnoDB;

INSERT INTO visits (location, visited) VALUES
('place 1', '2012-04-20 11:00:00'),
('place 2', '2012-04-20 11:06:00'),
('place 1', '2012-04-20 11:06:00'),
('place 3', '2012-04-20 11:20:00'),
('place 2', '2012-04-20 11:21:00'),
('place 1', '2012-04-20 11:22:00'),
('place 1', '2012-04-20 11:23:00');
</code></pre>

<p>which, as you see, has an index on (<code>location</code>,<code>visited</code>). Then the following query will use the index, that is read data in the order of the index, and return the results you expected:</p>

<pre><code>SELECT
  location,
  COUNT(IF(@loc &lt;&gt; @loc:=location,
           @vis:=visited,
           IF(@vis + INTERVAL 10 MINUTE &lt; @vis:=visited,
              visited,
              NULL))) as visit_count
FROM visits,
     (SELECT @loc:='', @vis:=FROM_UNIXTIME(0)) as init
GROUP BY location;
</code></pre>

<p>Result:</p>

<pre><code>+----------+-------------+
| location | visit_count |
+----------+-------------+
| place 1  |           2 |
| place 2  |           2 |
| place 3  |           1 |
+----------+-------------+
3 rows in set (0.00 sec)
</code></pre>

<p><strong>Some explanation</strong>:</p>

<p>The key of the solution is that it fades out the functional nature of SQL, and uses MySQL implementation specifics (they say it is bad, never do it again!!!).</p>

<ol>
<li><p>If a table has an index (an ordered representation of column values) and the index is used in a query, that means that the data from the table is read in the order of the index.</p></li>
<li><p>GROUP BY operation will benefit from an index (since the data is already grouped there) and will choose it if it is applicable.</p></li>
<li><p>All aggregating functions in SQL (except for <code>COUNT(*)</code> which has a special meaning) check each row, and use the value only if it is not NULL (the expression within COUNT above returns NULL for wrong conditions)</p></li>
<li><p>The rest is just a hacky representation of procedural iteration over a list of rows (which is read in the order of the index, that is ordered by <code>location asc, visisted asc</code>): I initialize some variables, if location differs from the previous row - I count it, if not - I check the interval and return NULL if it is wrong.</p></li>
</ol>

### Answer ID: 10239394
<p>You can populate the temporary table using a INSERT / SELECT statement.</p>

<p>See manual. <a href="http://dev.mysql.com/doc/refman/5.0/en/insert-select.html" rel="nofollow">http://dev.mysql.com/doc/refman/5.0/en/insert-select.html</a></p>

<p>I'd use the GROUP BY in the SELECT statement to narrow down the places.</p>

<p>For the visits column that can be populated as a COUNT operation, and I think it might be possible to perform that as also part of the INSERT / SELECT.</p>

<p>See manual. <a href="http://dev.mysql.com/doc/refman/5.1/en/counting-rows.html" rel="nofollow">http://dev.mysql.com/doc/refman/5.1/en/counting-rows.html</a></p>

<p>So your SQL might look something like this.</p>

<pre><code>INSERT INTO temp 
    SELECT * FROM (
        SELECT *,COUNT('visits') 
             FROM source AS table1 
             GROUP BY location
             WHERE date_visited &gt; xxxx AND date_visited &lt; xxxx
        )
       AS table2
</code></pre>

<p>Seriously, that is off the top of my head but it should give you some ideas on how SQL can be structured. But you likely can do the report using just one good query.</p>

