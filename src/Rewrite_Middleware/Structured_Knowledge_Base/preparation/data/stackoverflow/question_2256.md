# 1064 Error on replication slave in case statement query
[Link to question](https://stackoverflow.com/questions/26282256/1064-error-on-replication-slave-in-case-statement-query)
**Creation Date:** 1412868351
**Score:** 1
**Tags:** mysql, sql, percona
## Question Body
<p>I have mysql replication setup where the LOAD SQL runs without any error on master but on slave it fails with error 1064 and replication breaks</p>

<p>So 1064 is reserved word issue but in my case i don't have any reserved words to put "<code>"(back tick) here.
The issue is the case statement in SET command.
i want the case statement SET and i cant put "</code>" on "case" or "then" reserved words.
Also if i copy this SQL on slave as it is and run then works without complaint.</p>

<p>Is there way to rewrite this query so that slave server wont have any issue with the case statement.</p>

<p>Master Server : 5.5.28-29.1-log Percona Server
Slave Server : 5.6.20-68.0 Percona Server</p>

<pre><code>LOAD DATA INFILE 'myfile.csv' IGNORE INTO TABLE myTable FIELDS TERMINATED BY ',' IGNORE 1 LINES (
@Timeframe,
@reportdate
)
SET Timeframe = (
CASE
WHEN @timeframe LIKE '%(start time before request time)%' THEN
  'Immediate Requests'
WHEN @timeframe LIKE '%(start time less than 30 minutes after request time)%' THEN
  'Scheduled Requests'
WHEN @timeframe LIKE '%Start time more than 30 minutes after request time%' THEN
  'Delayed Scheduled Requests'
END
),
reportdate = date_sub(curdate(), INTERVAL 1 DAY);
</code></pre>

<p>Slave Error
Last_SQL_Error: Error 'You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ' <code>reportdate</code>=date_sub(curdate(),interval 1 day)' at line 3' on query. Default database:</p>

