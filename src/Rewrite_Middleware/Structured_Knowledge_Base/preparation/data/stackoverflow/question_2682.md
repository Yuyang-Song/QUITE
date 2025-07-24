# Replicate Multiple Database to Single Database AND conversely
[Link to question](https://stackoverflow.com/questions/47109888/replicate-multiple-database-to-single-database-and-conversely)
**Creation Date:** 1509792451
**Score:** 0
**Tags:** mysql, replication
## Question Body
<p>Here is my Master-Master Replication Scenario</p>

<pre><code>-------------------
| Master/Slave 1  |
| Database = MainDB |
-------------------
/\
|
|
|
\/
-------------------
| Master/Slave 2  |
| Database = DB1  |
| Database = DB2  |
| Database = DB3  |
-------------------
</code></pre>

<p>Here is my Master/Slave1 Configure:</p>

<pre><code>[mysqld]
binlog_format                   = MIXED
user                            = mysql
port                            = 3306
socket                          = /tmp/mysql.sock
#bind-address                    = 127.0.0.1
basedir                         = /usr/local
datadir                         = /var/db/mysql
tmpdir                          = /var/db/mysql_tmpdir
slave-load-tmpdir               = /var/db/mysql_tmpdir
secure-file-priv                = /var/db/mysql_secure
log-bin                         = MainDB.log
replicate-do-db                 = MainDB
replicate-rewrite-db            = "DB1-&gt;MainDB"
replicate-rewrite-db            = "DB2-&gt;MainDB"
replicate-rewrite-db            = "DB3-&gt;MainDB"
replicate-rewrite-db            = "DB4-&gt;MainDB"
log-output                      = TABLE
master-info-repository          = TABLE
relay-log-info-repository       = TABLE
relay-log-recovery              = 1
slow-query-log                  = 1
server-id                       = 1
</code></pre>

<p>and my Master/Slave2 Configure:</p>

<pre><code>[mysqld]
binlog_format                   = mixed
user                            = mysql
port                            = 3306
socket                          = /tmp/mysql.sock
#bind-address                    = 127.0.0.1
basedir                         = /usr/local
datadir                         = /var/db/mysql
tmpdir                          = /var/db/mysql_tmpdir
slave-load-tmpdir               = /var/db/mysql_tmpdir
secure-file-priv                = /var/db/mysql_secure
log-bin                         = mysql-bin
log-output                      = TABLE
master-info-repository          = TABLE
relay-log-info-repository       = TABLE
relay-log-recovery              = 1
slow-query-log                  = 1
server-id                       = 2
log_bin                         = cloud.log
binlog-do-db                    = DB1
binlog-do-db                    = DB2
binlog-do-db                    = DB3
binlog-do-db                    = DB4
</code></pre>

<p>With this configuration I can replicate from Master/slave2 to Master/slave1 but it can't replicate conversely. 
How cloud change my.cnf for both to be replicated together?</p>

## Answers
### Answer ID: 47111458
<p>yes we know it should be replicated with some DB in master/slave2 but we want to get back to that specific DB which had replicated to MainDB.</p>

### Answer ID: 47110570
<blockquote>
  <p>(1)If a master server does not write a statement to its binary log,
  the statement is not replicated. If the server does log the statement,
  the statement is sent to all slaves and each slave determines whether
  to execute it or ignore it.</p>
</blockquote>

<p><strong>Master/Slave1</strong> receive a binlog that has all <strong>DB%</strong> from <strong>Master/Slave2</strong> so he can handle to rewrite every DB into the <strong>MainDB</strong>. (using this <code>replicate-rewrite-db</code> even this option is a bit dangerous for me and you have to be carrful otherwise it will break see this <a href="https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-rewrite-db" rel="nofollow noreferrer">option_mysqld_replicate-rewrite-db</a> ).</p>

<p>First, In master master I think you should enable the option of loging in the slave <code>log_slave_updates</code> so the other slave "master" can store the statement in binary log (1). check this as well to undertand <a href="https://dev.mysql.com/doc/refman/5.7/en/replication-rules.html" rel="nofollow noreferrer">how Servers Evaluate Replication Filtering Rules</a></p>

<p>In the other hand <strong>Master/Slave2</strong> receive a binglog that has one database <strong>MainDB</strong>, and there is nothing you wrote than can help on taking a part to another Database. or rewrite everything in one.</p>

<blockquote>
  <p>On the master, you can control which databases to log changes for by
  using the <code>--binlog-do-db</code> and <code>--binlog-ignore-db</code> options to control
  binary logging.</p>
</blockquote>

<p>So you have to add this option in the <strong>Master/Slave1</strong> to tell him to log the changes of <strong>MainDB</strong>, then in <strong>Master/Slave2</strong> you specify which database you want to rewrite on it or which tables you want to  replicate in which database</p>

