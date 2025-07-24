# DBI database handle with AutoCommit set to 0 not returning proper data with SELECT?
[Link to question](https://stackoverflow.com/questions/3952242/dbi-database-handle-with-autocommit-set-to-0-not-returning-proper-data-with-sele)
**Creation Date:** 1287296532
**Score:** 11
**Tags:** mysql, perl, select, dbi, autocommit
## Question Body
<p>This is a tricky one to explain (and very weird), so bear with me. I will explain the problem, and the fix for it, but I would like to see if anyone can explain why it works the way it works :)</p>

<p>I have a web application that uses mod_perl. It uses MySQL database, and I am writing data to a database on regular basis. It is modular, so it also has its own 'database' type of a module, where I handle connection, updates, etc. database::db_connect() subroutine is used to connect to database, and <code>AutoCommit</code> is set to 0.</p>

<p>I made another Perl application (standalone daemon), that periodically fetches data from the database, and performs various tasks depending on what data is returned. I am including database.pm module in it, so I don't have to rewrite/duplicate everything.</p>

<p>Problem I am experiencing is:</p>

<p>Application connects to the database on startup, and then loops forever, fetching data from database every X seconds. However, if data in the database is updated, my application is still being returned 'old' data, that I got on the initial connection/query to the database.</p>

<p>For example - I have 3 rows, and column "Name" has values 'a', 'b' and 'c' - for each record. If I update one of the rows (using mysql client from command line, for example) and change Name from 'c' to 'x', my standalone daemon will not get that data - it will still get a/b/c returned from MySQL. I captured the db traffic with tcpdump, and I could definitely see that MySQL was really returning that data. I have tried using SQL_NO_CACHE with SELECT as well (since I wasn't sure what was going on), but that didn't help either.</p>

<p>Then, I have modified the DB connection string in my standalone daemon, and set <code>AutoCommit</code> to 1. Suddenly, application started getting proper data.</p>

<p>I am puzzled, because I thought AutoCommit only affects INSERT/UPDATE types of statements, and had no affect on SELECT statement. But it seemingly does, and I don't understand why.</p>

<p>Does anyone know why SELECT statement will not return 'updated' rows from the database when <code>AutoCommit</code> is set to 0, and why it will return updated rows when <code>AutoCommit</code> is set to 1?</p>

<p>Here is a simplified (taken out error checking, etc) code that I am using in standalone daemon, and that doesn't return updated rows.</p>

<pre><code>#!/usr/bin/perl

use strict;
use warnings;
use DBI;
use Data::Dumper;
$|=1;

my $dsn = "dbi:mysql:database=mp;mysql_read_default_file=/etc/mysql/database.cnf";
my $dbh = DBI-&gt;connect($dsn, undef, undef, {RaiseError =&gt; 0, AutoCommit =&gt; 0});
$dbh-&gt;{mysql_enable_utf8} = 1;

while(1)
{
    my $sql = "SELECT * FROM queue";
    my $stb = $dbh-&gt;prepare($sql);
    my $ret_hashref = $dbh-&gt;selectall_hashref($sql, "ID");
    print Dumper($ret_hashref);
    sleep(30);
}

exit;
</code></pre>

<p>Changing <code>AutoCommit</code> to 1 fixes this. Why?</p>

<p>Thanks :)</p>

<p>P.S: Not sure if it anyone cares, but DBI version is 1.613, DBD::mysql is 4.017, perl is 5.10.1 (on Ubuntu 10.04).</p>

## Answers
### Answer ID: 3952529
<p>I suppose you are using InnoDB tables and not MyISAM ones. As described in the InnoDB <a href="http://dev.mysql.com/doc/refman/5.0/en/innodb-transaction-model.html" rel="noreferrer">transaction model</a>, <em>all</em> your queries (including SELECT) are taking place inside a transaction. </p>

<p>When <code>AutoCommit</code> is on, a transaction is started for each query and if it is successful, it is implicitly committed (if it fails, the behavior may vary, but the transaction is guaranteed to end). You can see the implicit commits in MySQL's binlog. By setting <code>AutoCommit</code> to false, you are required to manage the transactions on your own. </p>

<p>The default transaction isolation level is <a href="http://dev.mysql.com/doc/refman/5.0/en/set-transaction.html#isolevel_repeatable-read" rel="noreferrer">REPEATABLE READ</a>, which means that all <code>SELECT</code> queries will read the same snapshot (the one established when the transaction started).</p>

<p>In addition to the solution given in the other answer (<code>ROLLBACK</code> before starting to read) here are a couple of solutions:</p>

<p>You can choose another transaction isolation level, like <a href="http://dev.mysql.com/doc/refman/5.0/en/set-transaction.html#isolevel_read-committed" rel="noreferrer">READ COMMITTED</a>, which makes your <code>SELECT</code> queries read a fresh snapshot every time. </p>

<p>You could also leave <code>AutoCommit</code> to true (the default setting) and start your own transactions by issuing <code>BEGIN WORK</code>. This will temporarily disable the <code>AutoCommit</code> behavior until you issue a <code>COMMIT</code> or <code>ROLLBACK</code> statement after which each query gets its own transaction again (or you start another with <code>BEGIN WORK</code>).</p>

<p>I, personally, would choose the latter method, as it seems more elegant.</p>

### Answer ID: 3952347
<p>I think that when you turn autocommit off, you also start a transaction.  And, when you start a transaction, you may be protected from other people's changes until you commit it, or roll it back.  So, if my semi-informed guess is correct, and since you're only querying the data, add a rollback before the sleep operation (no point in holding locks that you aren't using, etc):</p>

<pre><code>$dbh-&gt;rollback;
</code></pre>

