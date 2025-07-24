# Long-running parallel Tasks with Entity Framework cause high CPU peak and memory usage
[Link to question](https://stackoverflow.com/questions/75632281/long-running-parallel-tasks-with-entity-framework-cause-high-cpu-peak-and-memory)
**Creation Date:** 1677881481
**Score:** 2
**Tags:** c#, entity-framework, task, parallel.for, asp.net-core-7.0
## Question Body
<p>I am shifting a C# ASP.NET Core 7 project from using  <code>SqlClient</code> with regular SQL queries to using Entity Framework instead. I have a particular place when the application runs multiple long-running tasks, it's kind of a simulation with a big for loop where the user can follow progress, and for that reason, each task writes into the database dozens of times in its own task. The old <code>SqlClient</code> solution worked smoothly with minimal CPU and memory usage, but with EF, once the threads are beginning to work, everything halts and freezes.</p>
<p>I know that <code>DbContext</code> is not thread-safe, therefore each task creates its own <code>DbContext</code>, and they create it, particularly where the database inserts occur, and I dispose them right away once they are not needed, and yet, in the for loop it completely freezes the computer and everything stops. The web application is not even responding anymore.</p>
<p>The simplified controller:</p>
<pre><code>    public SmContext db { get; set; }

    public SimulateRoundModel(SmContext db)
    {
        this.db = db;
    }

    public async Task&lt;IActionResult&gt; OnPost()
    {
        List&lt;Match&gt; matches = new CollectorClass(db).Collect();
        MyClass.Wrapper(matches);
        return Page();
    }
</code></pre>
<p>The simplified code:</p>
<pre><code>public static void Wrapper(List&lt;Match&gt; matches)
{
    Parallel.For(0, matches.Count,
           index =&gt;
           {
               matches[index].LongSim();
           });
}
</code></pre>
<p>Match class:</p>
<pre><code>
private SmContext db { get; set; }

public Match(db)
{
    this.db = db;
}

public void longSim()
{
    db.Dispose(); // disposing the main dbcontext that the constructor receives, we don't want to use that

    using (SmContext db = new SmContext())
    {
        // some initial query and insert
    }

    for (int i = 0; i &lt; 100; i++)
    {
        Thread.Sleep(5000);

        // some simulation

        db = new SmContext();

        SomeInsert(); // these are using the db for the insert
        SomeInsert();
        SomeInsert();

        db.Dispose();
    }
}
</code></pre>
<p>We are talking about 5-50 matches and <code>Parallel.For</code> optimized them very well with the old <code>SqlClient</code> solutions, I have seen running it with 200 matches without an issue before. These are not intensive tasks, only simple stuff, and some queries, but they are running long. Ideally, I would like to continue saving the progress to the database without a major rewrite.</p>
<p>The ultimate question is, is there a conceptual issue here, that I am too newbie to recognize, or this solution should work fine and there is something fuzzy going on in the black spots of the code?</p>

## Answers
### Answer ID: 75638484
<p>It would more in guess territory then something I can prove but from my experience multiple <code>SomeInsert</code>'s with the same context look a bit suspicious. EF Core performs insert/update operation relying on <a href="https://learn.microsoft.com/en-us/ef/core/change-tracking/" rel="nofollow noreferrer">tracking</a> and even if you use <code>AsNoTracking</code> new entries still will be handled by change tracker, so if you are actually inserting a lot of data (and note that EF always was not very suitable for batch inserts) you will end up with the change tracker having a lot of entities which can slow down EF performance considerably. I would suggest one of the following options:</p>
<ul>
<li>Call <a href="https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.changetracking.changetracker.clear?view=efcore-7.0" rel="nofollow noreferrer"><code>ChangeTracker.Clear</code></a> after inserting some considerable amount of entities<sup>*</sup> (this also can be used instead of recreating the context outside the loop)</li>
<li>Recreate the context after inserting some considerable amount of entities<sup>*</sup></li>
<li>Use another technology or extension library (<a href="https://github.com/borisdj/EFCore.BulkExtensions" rel="nofollow noreferrer"><code>EFCore.BulkExtensions</code></a> for example) supporting bulk inserts</li>
</ul>
<p><sup>*</sup> - you will need to determine the optimal size of inserted data to recreate/clear tracker and call <code>SaveChanges</code>, like was done for old iteration of EF in this <a href="https://stackoverflow.com/questions/5940225/fastest-way-of-inserting-in-entity-framework">answer</a>.</p>
<p>P.S.</p>
<blockquote>
<p><code>Parallel.For</code><br />
<code>public void longSim()</code><br />
<code>Thread.Sleep(5000);</code></p>
</blockquote>
<p>I would strongly advice to make <code>longSim</code> asynchronous by using <code>await Task.Delay(5000)</code> and switch to <a href="https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreachasync?view=net-7.0" rel="nofollow noreferrer"><code>Parallel.ForEachAsync</code></a> which supports async methods. This also will allow to use async versions of EF Core methods.</p>
<p>One more thing which can be worth taking into consideration is <a href="https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-threadpool-starvation" rel="nofollow noreferrer">thread pool starvation</a> which can sometimes have somewhat similar &quot;side&quot; effects but if the only change you made is the switch to EF Core instead <code>SQLClient</code> and it leads to the observed behaviour then thread pool starvation should not be the reason.</p>

