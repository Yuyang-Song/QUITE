# How to refactor PHP to help improve SQL Server speed?
[Link to question](https://stackoverflow.com/questions/12318738/how-to-refactor-php-to-help-improve-sql-server-speed)
**Creation Date:** 1347023226
**Score:** 0
**Tags:** php, sql-server
## Question Body
<p>I've been tasked with finding a solution to some performance issues we've been having with our PHP web application (basically, we're reaching a "failure" point when combining high-volume users with peak traffic/load hours). What I've found so far is that the bottleneck is occurring when trying to access the MS SQL Server database. Our sysadmin suggested that it's probably due to SQL Server having to do too much context switching, because of the amount that the code queries the database. </p>

<p>Upon looking more into context switching and how to reduce it, though, I've only been able to find vague mentions of how to actually do so at the application code level, mostly along the lines of "refactor your code so it doesn't make so many calls," or .Net-specific tips. </p>

<p>We're dealing with a large, complex codebase, so we can't do things like completely rewrite the system, and we also have pretty well optimized (as best we could) the individual queries that we can, so what other refactoring opportunities can we look for to help make our code not bring our database server to its knees?</p>

<p>I don't currently know the full stats on our database server, but it's beefy enough to run MS SQL Server 2008 and was doing well until recently.</p>

<p>ETA: I'm simply a developer and don't have any authoritative power, so I can't do things like hire consultants. While I'm willing to make the suggestion to my superiors, I'm primarily looking for things that we can do in-house to further work toward solving the underlying issue. </p>

<p>As I explained in a comment, I understand that the context switching is more a symptom of something else, which is then causing the issues we're actually seeing (slow responses from the database; just like in an OS, doing a lot of swapping results in slow response from an application, but is itself a symptom of other things taking up too much RAM). What is causing the context switching? A lot of database access from the application code. The problem is, the individual queries are already as good as we can get them right now, as indicated by our monitoring software, so what else can we do to help this problem?</p>

<p>My admin's use of context switching has since been clarified. It seems that the issue, given his clarification, is that there are a lot of relatively small calls being made, which would require the database server to enqueue them as it handles each one in turn, driving up the response time as the scripts wait for their requested data. Are there any strategies, then, for combining these database calls, or otherwise adjusting how an MVC-structured PHP application makes calls to the database so that the scripts aren't constantly waiting on the database?</p>

## Answers
### Answer ID: 12319017
<p>You have a SQL Server performance problem, approach it as a SQL Server performance troubleshooting. There are some well known methodologies like <a href="http://technet.microsoft.com/en-us/library/cc966413.aspx" rel="nofollow">Waits and Queues</a>. The SQL Server <a href="http://sqlcat.com/sqlcat/b/presentations/archive/2008/04/18/troubleshooting-sql-server-2005-2008-performance-and-scalability-flowchart.aspx" rel="nofollow">Performance Troubleshooting Flowchart</a> is a great syntheses of the various articles, tools, methodologies and metrics at your disposal to identify the bottleneck.</p>

<p>Saying that the problem is 'context switching' is non-informative, unhelpful and unactionable.  For the record, there is not even such concept as 'context switching' in SQL Server troubleshooting because of the very specific way <a href="http://msdn.microsoft.com/en-us/library/ms189267%28v=sql.105%29.aspx" rel="nofollow">SQL Server scheduling architecture</a> works. This is not how SQL Server performance troubleshooting is done, it is not even close to true root cause analysis. You need to identify the problem before you can attempt a solution. If your admin cannot help you, seek specialized help from qualified consultants.</p>

<p>And yes, if you can cache anything in the client and avoid querying the server is always, by definition, good. If the client and proxies can cache the page and avoid even hitting your HTTP server, is even better. These are true with any technology stack.</p>

<blockquote>
  <p>there are a lot of relatively small calls being made, which would
  require the database server to enqueue them as it handles each one in
  turn, driving up the response time as the scripts wait for their
  requested data. Are there any strategies, then, for combining these
  database calls</p>
</blockquote>

<p>There is no silver bullet. Consider though that a well tuned database can drive <strong>a lot</strong> of small requests per second (many thousands per second) w/o problems. Did you measure metrics in:</p>

<ul>
<li><a href="http://msdn.microsoft.com/en-us/library/ms189883%28v=sql.105%29.aspx" rel="nofollow">SQL Server, Databases Object</a></li>
<li><a href="http://msdn.microsoft.com/en-us/library/ms189038%28v=sql.105%29" rel="nofollow">SQL Server, Transactions Object</a></li>
<li><a href="http://msdn.microsoft.com/en-us/library/ms190732%28v=sql.105%29" rel="nofollow">SQL Server, Wait Statistics Object</a></li>
<li><a href="http://msdn.microsoft.com/en-us/library/ms190697%28v=sql.105%29" rel="nofollow">SQL Server, General Statistics Object</a></li>
<li><a href="http://msdn.microsoft.com/en-us/library/ms177426%28v=sql.105%29" rel="nofollow">SQL Server, Access Methods Object</a></li>
<li><a href="http://msdn.microsoft.com/en-us/library/ms189628%28v=sql.105%29" rel="nofollow">SQL Server, Buffer Manager Object</a></li>
</ul>

<p><em>These</em> are interesting metrics that can tell a lot where you should focus your effort.</p>

