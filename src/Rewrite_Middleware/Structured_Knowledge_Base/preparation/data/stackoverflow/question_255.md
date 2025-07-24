# MySQL Replication: struggling with replicate-rewrite-db to change the database name
[Link to question](https://stackoverflow.com/questions/18241462/mysql-replication-struggling-with-replicate-rewrite-db-to-change-the-database-n)
**Creation Date:** 1376511453
**Score:** 3
**Tags:** mysql, database-replication
## Question Body
<p>I have my master database with the one table in it, products (will have more later, this is just dev).</p>

<p>OS: CentOS 6.4</p>

<p>I have set it up as the master for replication using this:</p>

<p>In /etc/my.cnf:</p>

<pre><code>server-id = 1
binlog-do-db=product_database
relay-log = /var/lib/mysql/mysql-relay-bin
relay-log-index = /var/lib/mysql/mysql-relay-bin.index
log-error = /var/lib/mysql/mysql.err
master-info-file = /var/lib/mysql/mysql-master.info
relay-log-info-file = /var/lib/mysql/mysql-relay-log.info
log-bin = /var/lib/mysql/mysql-bin
</code></pre>

<p>On the master I created the user with this command:</p>

<pre><code>GRANT REPLICATION SLAVE ON *.* TO 'hcp_slave'@'%' IDENTIFIED BY 'password_here';
</code></pre>

<p>Then on the slave:</p>

<pre><code>server-id = 2
master-host=HOST_IP_ADDRESS
master-connect-retry=60
master-user=hcp_slave
master-password=PASSWORD
replicate-do-db=product_database
#The below line is what causes issues
replicate-rewrite-db=product_database-&gt;product_database2
relay-log = /var/lib/mysql/mysql-relay-bin
relay-log-index = /var/lib/mysql/mysql-relay-bin.index
log-error = /var/lib/mysql/mysql.err
master-info-file = /var/lib/mysql/mysql-master.info
relay-log-info-file = /var/lib/mysql/mysql-relay-log.info
log-bin = /var/lib/mysql/mysql-bin
</code></pre>

<p>Before I added the "replicate-rewrite-db" line (and with it removed) the replication works perfectly between the servers with the same database name. However, I need it to go into a database with a different name, for testing purposes, "product_database2."</p>

<p>From everything I have read in the mysql manual and on a few random forums (plus stackoverflow) I think I am using the replicate command properly, but clearly, I am not, so I would greatly appreciate a little help in figuring out where my issue lies, or if I am trying to go about this the entirely wrong way!</p>

<p>For those curious, what I am actually trying to do, in case I have an XY problem going on here:</p>

<p>I am trying to create a master database to feed products to a handful of websites instead of having to update them all manually. I figured the best way to do this would be to create 1 master database and have all the sites configured as slaves to automatically pull products from it.</p>

<p>Edit:</p>

<p>I tried commenting out the line 'replicate-do-db' in the slave configuration file, and at least now it is giving some indication of knowing that product_database2 exists, but it is in the form of an error:</p>

<pre><code>Last_Error: Error 'Error on rename of './product_database/asdf.frm' to     './product_database2/asdf.frm' (Errcode: 2)' on query. Default database: 'product_database2'. Query: 'RENAME TABLE `product_database`.`asdf`
</code></pre>

## Answers
### Answer ID: 54651900
<p>I faced the same problem regarding database naming. My solution:</p>

<p>In the my.cnf file:</p>

<pre><code>replicate-rewrite-db="product_database-&gt;product_database2"
replicate-do-db="product_database2"
</code></pre>

### Answer ID: 28039439
<p>On the slave side you need to set </p>

<pre><code>replicate-do-db=product_database2
</code></pre>

<p>because you have rewritten db name like <code>product_database-&gt;product_database2</code>.</p>

### Answer ID: 23136840
<p>From <a href="http://dev.mysql.com/doc/refman/5.0/en/replication-options-slave.html#option_mysqld_replicate-rewrite-db" rel="nofollow">refman</a>:</p>

<blockquote>
  <p>Only statements involving tables are affected (not statements such as
  CREATE DATABASE, DROP DATABASE, and ALTER DATABASE), <strong>and only if
  <em>from_name</em> is the default database on the master</strong>.</p>
</blockquote>

<p>So try this. Use the config you have above, but try adding a USE right before the query you run on master.</p>

<pre><code>USE product_database;
INSERT INTO product_database (c1,c2) VALUES (1,2);
</code></pre>

