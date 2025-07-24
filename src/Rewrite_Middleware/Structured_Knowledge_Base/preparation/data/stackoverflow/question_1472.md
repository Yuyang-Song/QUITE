# Get Average of TimeSpans with EF Core
[Link to question](https://stackoverflow.com/questions/77553084/get-average-of-timespans-with-ef-core)
**Creation Date:** 1701025477
**Score:** -1
**Tags:** c#, linq, .net-core, entity-framework-core, ef-core-7.0
## Question Body
<p>I'm using EF Core 7 with Postgres. I need to calculate some stats:</p>
<pre class="lang-cs prettyprint-override"><code>public record Job(string Name, DateTime Started, DateTime Stopped);
public record Stats(TimeSpan Min, TimeSpan Mean, TimeSpan Max);

// 

var stats = await _context
  .Jobs
  .GroupBy(x =&gt; x.Name)
  .Select(x =&gt; new Stats(
    x.Min(y =&gt; y.Stopped - y.Started), 
    new TimeSpan((long)x.Select(y =&gt; y.Stopped - y.Started).Select(x =&gt; x.Ticks).Average()), 
    x.Max(y =&gt; y.Stopped - y.Started)
  ))
  .ToListAsync();
</code></pre>
<p>The average subquery is weird-looking but works as a non-EF query. But EF refuses with:</p>
<blockquote>
<p>InvalidOperationException: The LINQ expression 'RelationalGroupByShaperExpression:<br />
...<br />
.Average()' <strong>could not be translated</strong>. Either rewrite the query in a form that can be translated, or switch to client evaluation</p>
</blockquote>
<p>I think EF can't translate <code>Ticks</code>. I didn't find anything useful in <code>EF.Functions</code>.</p>
<p>I don't want to do this on the client, I want to do this on the database as the data set is large. Is that possible?</p>

## Answers
### Answer ID: 77554527
<p>Other than client-side eval, one could use a provider-specific function (I am using Postgres):</p>
<pre class="lang-cs prettyprint-override"><code>var stats = await _context
  .Jobs
  .GroupBy(x =&gt; x.Name)
  .Select(x =&gt; new Stats(
    x.Min(y =&gt; y.Stopped - y.Started), 
    EF.Functions.Average(x.Select(y =&gt; y.Stopped - y.Started)),  // &lt;---
    x.Max(y =&gt; y.Stopped - y.Started)
  ))
  .ToListAsync();
</code></pre>
<p>But then that property must be nullable:</p>
<pre class="lang-cs prettyprint-override"><code>public record Stats(TimeSpan Min, TimeSpan? Mean, TimeSpan Max);
</code></pre>
<p>The issue is <code>Ticks</code> is not (currently) supported. That was <a href="https://github.com/dotnet/efcore/issues/27103" rel="nofollow noreferrer">requested here</a>, please upvote it.</p>

### Answer ID: 77553781
<p>You are right, entity framework does not understand the concept of TimeSpan.Ticks.</p>
<p>However, class <a href="https://learn.microsoft.com/en-us/dotnet/api/system.data.entity.dbfunctions?view=entity-framework-6.2.0" rel="nofollow noreferrer">DbFunctions</a> has several methods to get the number of (nano)seconds / minutes / hours, etc between two DateTimes. Select the accuracy that you need, for example:</p>
<pre><code>var stats = await _context
    .Jobs
    .GroupBy(x =&gt; x.Name)
    .Select(x=&gt; new
        {
            Min = x.Select(y =&gt; y.Stopped - y.Started).Min(),
            AverageTimeSpanMilliSect = x.Select(y =&gt;
                    DbFunctions.DiffMilliSeconds(y.Stopped, y.Started)
                .Average(),
            Max = x.Select(y =&gt; y.Stopped - y.Started).Max(),
        })

    // Move the selected data to your local process and convert to Stats
    .AsEnumerable()
    .Select(x =&gt; new Stats(x.Min, 
                           TimeSpan.FromMilliSeconds(x.AverageTimeSpanMilliSec,
                           x.Max));
</code></pre>

