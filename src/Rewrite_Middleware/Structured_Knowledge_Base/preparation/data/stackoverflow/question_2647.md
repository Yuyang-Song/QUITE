# MySQL InnoDB Locking statistics
[Link to question](https://stackoverflow.com/questions/44508443/mysql-innodb-locking-statistics)
**Creation Date:** 1497300324
**Score:** 0
**Tags:** mysql, optimization, locking, innodb
## Question Body
<p>We are planning to rewrite legacy system that is using MySQL InnoDB database and trying to analyse main bottlenecks that should be avoided in next version. </p>

<p>System has many services/jobs that runs over night that generates data - inserts/updates, that mainly should be optimized. Jobs runs avg. 2-3 hours now.
We already gathered long running queries that must be optimized. </p>

<p>But I am wondering if it is possible to gather information and statistics about long running transactions. </p>

<p>Very helpful will be information which tables is locked by transaction the most - average locking time, lock type, periods.</p>

<p>Could somebody advice any tool or script that can gather such information? 
Or maybe someone can share own experience in database analyse and optimization?</p>

## Answers
### Answer ID: 44508565
<p>MySQL has built in capability for capturing "slow" query statistics (but to get an accurate picture you need to set the slow threshold as 0). You can turn the log into useful information with mysqldumpslow (bundled with mysql). I like the percona toolkit, but there are lots of other tools available.</p>

