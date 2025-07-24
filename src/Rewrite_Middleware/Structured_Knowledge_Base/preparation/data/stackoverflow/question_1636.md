# Performance bottleneck - Linq to SQL or the database - how do I tell?
[Link to question](https://stackoverflow.com/questions/2257507/performance-bottleneck-linq-to-sql-or-the-database-how-do-i-tell)
**Creation Date:** 1266064721
**Score:** 3
**Tags:** sql, performance, linq-to-sql, sql-server-2008
## Question Body
<p>I am currently trying to ring more performance out of my reporting website which uses linq to sql and an sql server express 2008 database. 
I am finding that as I now approach a million rows in on of my more 'ugly' tables that performance is becoming a real issue, with one report in particular taking 3 minutes to generate.</p>

<p>Essentially, I have a loop that, for each user, hits the database and grabs a collection of data on them. This data is then queried in various ways (and more rows loaded as needed) until I have a nice little summary object that I can fire off to a set of silverlight charts. Lazy loading comes is used and the reporting pulls into data from around 8 linked tables.</p>

<p>The problem is I don't know where the bottleneck now is and how to improve performance. Due to  certain constraints I was forced to use uniqueidentifiers for a number of primary keys in the tables involved - could this be an issue? </p>

<p>Basically, I need to put time into increasing performance but don't have enough to do that with both the database or the linq to sql. Is there anyway I can see where the bottlenecks are? </p>

<p>As im running express I don't have access to the profiler. I am considering rewriting my queries into compiled linq to sql but fear the database may be the culprit.</p>

<p>I understand this question is a bit open ended and its hard to answer without knowing much more about my setup (database schema etc) but any advice on how to find out where the bottlenecks are is more appreciated!</p>

<p>Thanks</p>

<p>UPDATE:
Thanks for all the great advice guys, and some links to some great tools.</p>

<p>UPDATE for those interested
I have been unable to make my queries any quicker through tweaking the linq. the problem seems to be that the majority of my database access code takes place in a loop. I can't see a way around it. Basically I am building up a report by looking through a number of users data - hence the loop. Pulling all the records up front seems a bit crazy - 800,000 + rows. My gut feeling is that there is a much better way, but its a technological leap too far for me!</p>

<p>However, adding another index to one of the foreign keys in one of the tables boosted performance so now the report takes 20 seconds to generate as opposed to 3 minutes!</p>

## Answers
### Answer ID: 2257534
<p>There are 2 tools I use for this, LinqPad and the Visual Studio Debugger.  First, <a href="http://www.linqpad.net/" rel="nofollow noreferrer"><strong>check out LinqPad</strong></a>, even the free version is very powerful, showing you execution time, the SQL generated and you can use it to run any code snippet...<strong>it's tremendously useful</strong>.</p>

<p>Second, you can use the Visual studio debugger, this is something we use on our DataContext <em>(note: only use this in debug, it's a performance hit and completely unnecessary outside of debugging)</em></p>

<pre><code>#if DEBUG
  private readonly Stopwatch Watch = new Stopwatch();

  private static void Connection_StateChange(object sender, StateChangeEventArgs e)
  {
    if (e.OriginalState == ConnectionState.Closed &amp;&amp; e.CurrentState == ConnectionState.Open) 
    {
      Current.Watch.Start();
    }
    else if (e.OriginalState == ConnectionState.Open &amp;&amp; e.CurrentState == ConnectionState.Closed)
    {
      Current.Watch.Stop();

      string msg = string.Format("SQL took {0}ms", Current.Watch.ElapsedMilliseconds);
      Trace.WriteLine(msg);
    }
  }
#endif

private static DataContext New
{
  get
  {
    var dc = new DataContext(ConnectionString);
#if DEBUG
    if (Debugger.IsAttached)
    {
      dc.Connection.StateChange += Connection_StateChange;
      dc.Log = new DebugWriter();
    }
#endif
    return dc;
  }
}
</code></pre>

<p>In a debug build, as an operation completes with each context, we see the timestamp in the debug window and the SQL it ran.  <a href="http://www.u2u.info/Blogs/Kris/Lists/Posts/Post.aspx?ID=11" rel="nofollow noreferrer">The DebugWriter class you see can be found here</a> <em>(Credit: Kris Vandermotten)</em>.  We can quickly see if a query's taking a while.  To use it we just initiate a DataContext by:</p>

<pre><code>var DB = DataContext.New;
</code></pre>

<p><em>(The profiler is not an option for me since we don't use SQL server, this answer is simply to give you some alternatives that have been very useful for me)</em></p>

### Answer ID: 2257591
<p>As you're using SQL Express which doesn't have Profiler, there is a free third party profiler you can download <a href="http://sqlprofiler.googlepages.com/" rel="nofollow noreferrer">here</a>. I've used it when running SQL Express. That will allow you to trace what's going on in the database.</p>

<p>Also, you can query the Dynamic Management Views to see what the costly queries are:
e.g. TOP 10 queries that have taken the most time</p>

<pre><code>SELECT TOP 10 t.text, q.*, p.query_plan
FROM sys.dm_exec_query_stats q
    CROSS APPLY sys.dm_exec_sql_text(q.sql_handle) t
    CROSS APPLY sys.dm_exec_query_plan (q.plan_handle) AS p
ORDER BY q.total_worker_time DESC
</code></pre>

### Answer ID: 2257555
<p>I used this excelent tool: <a href="http://dotnetslackers.com/articles/csharp/LINQ-to-SQL-Profiler.aspx" rel="nofollow noreferrer">Linq2Sql profiler</a>. It works on the application side, so there is no need for database server profiling functionality. </p>

<p>You have to add one line of initialization code to your application and then in separate desktop application profiler shows you SQL query for each LINQ query with exact line of code where it was executed (cs or aspx), database time and application time of executions and it even detects some common performance problems like n+1 queries (query executed for iteration) or unbounded datasets. You have to pay for it, but the trial version is also available. </p>

