# Query logging scenarios in query-heavy website
[Link to question](https://stackoverflow.com/questions/11263337/query-logging-scenarios-in-query-heavy-website)
**Creation Date:** 1340978931
**Score:** 1
**Tags:** php, mysql, logging, lamp
## Question Body
<p>I'm facing with the problem of logging the database activity of a LAMP (Debian/PHP/MySQL) site.</p>

<p>This is complicated by the fact that I'd wish every query logged also with the user's context in which they were launched, to know, let's say, "who did what". I admit to be not too well informed about MySQL's logging capabilities but I have problems in finding info about my specific scenario.</p>

<p>Now we have implemented a <code>mysql_query()</code> replacement <em>(I know, I know, code rewriting with PDO and prepared statements is on its way!)</em> that executes the query and logs it with <code>INSERT DELAYED</code> in a log table.</p>

<p>Problem is, the log table, as one can easily predict, reaches millions of rows, of which the oldest ones are quite useless. Other problem is, for every query needed, two are executed. A partial solution has been NOT to log the <code>SELECT</code>s.</p>

<p>Another solution would be logging on text file with fancy log rotation and gzipping and stuff. But how about knowing the user context in which the queries were run?</p>

<p>Has someone implemented a successful query logger that logs also the logged user and is performance-aware?</p>

## Answers
### Answer ID: 11263656
<p>Well its a trade off. If you want to log user activity it will take up lots of space, and use more processing.</p>

<p>I personally log all HTTP requests for PHP files (including GET, POST, COOKIE, etc), instead of SQL queries. But that still leads to millions of rows. I also keep them forever as HDD space is generally cheap. When I need to do audits, it can be slow, but I don't need to audit often.</p>

<p>Writing to a file would just make it harder to analyse, and you will still be processing extra IO every request. </p>

<p>If space is an issue, you could just run a cron job to remove all rows older the X amount of time. </p>

