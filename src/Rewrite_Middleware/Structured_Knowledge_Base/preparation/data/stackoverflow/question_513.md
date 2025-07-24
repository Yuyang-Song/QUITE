# Mysql replication not rewriting the database name
[Link to question](https://stackoverflow.com/questions/29407578/mysql-replication-not-rewriting-the-database-name)
**Creation Date:** 1427960543
**Score:** 0
**Tags:** mysql, replication, database-replication
## Question Body
<p>I'm replicating two database tables in two databases in the same MySql instant.</p>

<p>I have my.ini as:</p>

<pre><code>[mysqld]
server-id=1
log-bin 
report-host=master-is-slave-host
log-bin=D:/wamp/logs/log_bin.log
relay-log=D:/wamp/logs/relaylog.log

replicate-same-server-id=1

binlog-do-db=test
replicate-rewrite-db=test-&gt;test2
</code></pre>

<p>And when the errors are checked it says that:</p>

<p><code>Duplicate entry '18' for key 'PRIMARY'' on query. Default database: 'test2'. Query: 'INSERT INTO</code>test<code>.</code>c<code>(</code>id<code>,</code>a<code>,</code>b<code>,</code>c<code>) VALUES (NULL, 'fff', '', '')', Error_code: 1062</code></p>

<p>It seems that the rewrite has not worked.</p>

<p>Any one who has done this before?</p>

<p><strong>UPDATE</strong></p>

<p>I empty the table test.c (master) and restarted the slave. That table got repopulated with data. Where the slave table test2.c must be the one to get populated.</p>

## Answers
### Answer ID: 29407649
<p>The error doesn't look it relates to replication. You're attempting to insert values where you're adding in "18" where "18" already exists. As that column is the primary key, you can only have one "18". </p>

<p>I doubt that query would even run on the primary, let alone make its way to the slave and work. </p>

