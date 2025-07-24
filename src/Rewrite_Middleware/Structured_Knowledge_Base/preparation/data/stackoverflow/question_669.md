# HY000/2003 error using mysqli to connect on localhost or 127.0.0.1
[Link to question](https://stackoverflow.com/questions/36585469/hy000-2003-error-using-mysqli-to-connect-on-localhost-or-127-0-0-1)
**Creation Date:** 1460501340
**Score:** 0
**Tags:** php, mysql, mysqli, wamp
## Question Body
<p>I am writing a php page that connects to a database on WAMP.</p>

<p>I have the following code:</p>

<pre><code>$servername = "127.0.0.1";
$username = "root";
$password = "";

// connect to database
$conn = new mysqli($servername, $username, $password); //error line (1)
$sql = "USE xdbl0zz14_biodiversity"; 
$conn-&gt;query($sql); //error line (2)
</code></pre>

<p>The error line (1) gives the following error:</p>

<pre><code>Warning: mysqli::mysqli(): (HY000/2003): Can't connect to MySQL server on '127.0.0.1' (111)
</code></pre>

<p>The error line (2) gives the following error:</p>

<pre><code>Warning: mysqli::query(): Couldn't fetch mysqli
</code></pre>

<p>but I assume that is a direct result of the error before.</p>

<p>I have looked at services.msc and the wampmysqld64 service is started.</p>

<p>Thank you in advance.</p>

<p><strong><em>EDIT</em></strong></p>

<p>The mysql logs show:</p>

<pre><code>2016-04-05T12:05:50.193100Z 0 [Warning] InnoDB: Resizing redo log from      2*3072 to 2*320 pages, LSN=2471251
2016-04-05T12:05:50.380111Z 0 [Warning] InnoDB: Starting to delete and rewrite log files.
2016-04-05T12:05:51.310164Z 0 [Warning] InnoDB: New log files created, LSN=2471251
2016-04-12T11:10:57.423304Z 0 [Warning] wampmysqld64: Forcing close of thread 2  user: 'root'

2016-04-12T22:34:23.288955Z 0 [Warning] wampmysqld64: Forcing close of thread 2  user: 'root'
</code></pre>

## Answers
### Answer ID: 36585938
<p>Given the information my best guess would be that mysqld fails to start up due to some internal error, possibly due to some InnoDB data file corruption. If the data is valuable (e.g.there is no backup, or it takes too long to load), I would try to figure out what <code>mysqld</code> process is doing with the help of <code>strace</code> and <code>gdb</code> and then go from there.</p>

<p>Otherwise, I would shut down mysqld process (<code>kill -9</code> if stubborn), wipe out all InnoDB files in the MySQL data directory (usually <code>/var/lib/mysql</code>) plus all <code>.frm</code> files of existing InnoDB tables, and try restarting MySQL service normally, then load the database from backup. </p>

