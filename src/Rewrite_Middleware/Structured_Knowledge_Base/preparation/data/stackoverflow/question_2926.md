# Using MS Sequel server with PHP on Mac returns returns a different query result then on a Windows machine
[Link to question](https://stackoverflow.com/questions/58835379/using-ms-sequel-server-with-php-on-mac-returns-returns-a-different-query-result)
**Creation Date:** 1573641926
**Score:** 0
**Tags:** php, sql-server, windows, macos, sqlsrv
## Question Body
<p><strong>Context</strong></p>

<p>We are using a Microsoft Sequel database and our application runs php (7.3 version) and everybody is using Windows to do their development. Recently I started using a Mac as a working station, installed apache and php (7.3) on it. To be able to use the MS Sequel database I installed the recommended drivers following this Microsoft tutorial: <a href="https://learn.microsoft.com/en-us/sql/connect/php/installation-tutorial-linux-mac?view=sql-server-ver15" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/sql/connect/php/installation-tutorial-linux-mac?view=sql-server-ver15</a>. </p>

<p><strong>Problem</strong></p>

<p>All of this is working well, except some queries return a empty result where the same query on Windows returns the expected (not empty) result. We suspect that the PHP drivers for MS Sequel are not working the same between the 2 OS’s. We use PDO_SQLSRV (5.6.1 version) extension in PHP.</p>

<p>We pinpointed it to the fact that a declare statement with assignment is returned as the first result set, where on Windows the result set of the actual select query is returned. </p>

<p>The query we use is: </p>

<pre><code>$sql1 = "
declare @test bigint = 1
select top 3 name from sys.databases
";
$illuminate_connection-&gt;select($sql1)
</code></pre>

<p>Does anybody have experience with this? And would there be a fix/workaround without having to rewrite the code? </p>

