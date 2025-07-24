# MySql Replication not working properly with replicate-wild-do-table
[Link to question](https://stackoverflow.com/questions/41350895/mysql-replication-not-working-properly-with-replicate-wild-do-table)
**Creation Date:** 1482866028
**Score:** 0
**Tags:** mysql
## Question Body
<p>I am creating the MySQL master-slave replication on CentOS 7 below are the configuration files details of both the server:</p>

<h2>Master server's my.cnf</h2>

<pre><code>[mysqld]
server-id=1
log-bin=mysql-bin

datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

symbolic-links=0


sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
</code></pre>

<h2><strong>Slave Server's my.cnf</strong></h2>

<pre><code>[mysqld]
server-id=2
replicate-wild-do-table=db1%.%

datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock


symbolic-links=0

sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

[mysqld_safe]
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
</code></pre>

<p><strong>Database details given below:</strong></p>

<h2><strong>Master Server</strong></h2>

<pre><code>create database db1;
create table db1.dbtb1(name varchar(100));
</code></pre>

<h2><strong>Slave Server</strong></h2>

<pre><code>create database db1slave;
create table db1slave.dbtb1(name varchar(100));
</code></pre>

<p>AS you can see the Database name on both the sever are different for that I have use the below statement into the slave server for replication.</p>

<pre><code>replicate-wild-do-table=db1%.%
</code></pre>

<p>But when I try to insert data into the Master Data base server I got the below error or slave server status: </p>

<pre><code>Error 'Table 'db1.dbtb1' doesn't exist' on query. Default database: ''. Query: 'insert into db1.dbtb1 values ('Punu')'
</code></pre>

<p>Slave server Status: </p>

<pre><code>Slave_IO_State: Waiting for master to send event
Master_Host: IP address
              Master_User: repl
              Master_Port: 3306
            Connect_Retry: 60
          Master_Log_File: mysql-bin.000003
      Read_Master_Log_Pos: 971
           Relay_Log_File: mysqld-relay-bin.000002
            Relay_Log_Pos: 283
    Relay_Master_Log_File: mysql-bin.000003
         Slave_IO_Running: Yes
        Slave_SQL_Running: No
          Replicate_Do_DB:
      Replicate_Ignore_DB:
       Replicate_Do_Table:
   Replicate_Ignore_Table:
  Replicate_Wild_Do_Table: db1%.%
Replicate_Wild_Ignore_Table:
               Last_Errno: 1146
               Last_Error: Error 'Table 'db1.dbtb1' doesn't exist' on query. Default database: ''. Query: 'insert into db1.dbtb1 values ('Punu')'
             Skip_Counter: 0
      Exec_Master_Log_Pos: 760
          Relay_Log_Space: 668
          Until_Condition: None
           Until_Log_File:
            Until_Log_Pos: 0
       Master_SSL_Allowed: No
       Master_SSL_CA_File:
       Master_SSL_CA_Path:
          Master_SSL_Cert:
        Master_SSL_Cipher:
           Master_SSL_Key:
    Seconds_Behind_Master: NULL
    Master_SSL_Verify_Server_Cert: No
            Last_IO_Errno: 0
            Last_IO_Error:
           Last_SQL_Errno: 1146
           Last_SQL_Error: Error 'Table 'db1.dbtb1' doesn't exist' on   query. Default database: ''. Query: 'insert into db1.dbtb1 values ('Punu')'
 Replicate_Ignore_Server_Ids:
         Master_Server_Id: 1
              Master_UUID: 2fc2ef76-c87a-11e6-ae22-000d3aa2da57
         Master_Info_File: /var/lib/mysql/master.info
                SQL_Delay: 0
      SQL_Remaining_Delay: NULL
  Slave_SQL_Running_State:
       Master_Retry_Count: 86400
              Master_Bind:
  Last_IO_Error_Timestamp:
 Last_SQL_Error_Timestamp: 161227 18:40:36
           Master_SSL_Crl:
       Master_SSL_Crlpath:
       Retrieved_Gtid_Set:
        Executed_Gtid_Set:
            Auto_Position: 0
</code></pre>

<p>If I will take the same database name it will work fine. But as per my requirement I can't put the database name same on both the server.  </p>

<p>Simply I want that when the table "dbtb1" updated in Master server database then it will be replicated to the slave database table.</p>

<p>I have also try the below options in the slave my.cnf file:</p>

<p>1</p>

<pre><code>   replicate-wild-do-table=db1%.dbtb1
</code></pre>

<p>2</p>

<pre><code>   replicate-rewrite-db="db1-&gt;db1slave"
</code></pre>

<p>Above option will work fine if I insert record but it will not reflect when I delete or update record.</p>

<p>3</p>

<pre><code> replicate-wild-do-table=%.dbtb1
</code></pre>

## Answers
### Answer ID: 41351049
<p>your option <strong>replicate-wild-do-table=db1%.%</strong> will replicate all table in all schemas starts with <strong>db1%</strong> ans also replicate all tables start with <strong>%</strong>. so  it will replicate all tables. thats a wrong config.</p>

<p>use the <strong>replicate-rewrite-db</strong> option to config this. read this below. </p>

<p><a href="https://mariadb.com/resources/blog/multisource-replication-how-resolve-schema-name-conflicts" rel="nofollow noreferrer">https://mariadb.com/resources/blog/multisource-replication-how-resolve-schema-name-conflicts</a></p>

