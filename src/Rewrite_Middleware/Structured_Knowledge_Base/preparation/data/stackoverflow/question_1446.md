# Linq list any as conditional variables inside linq query
[Link to question](https://stackoverflow.com/questions/76695332/linq-list-any-as-conditional-variables-inside-linq-query)
**Creation Date:** 1689447477
**Score:** 0
**Tags:** c#, asp.net, .net, linq
## Question Body
<pre><code>var log = db.ViewLogs.Where(d =&gt; 
    time_ranges.Any(t =&gt; (d.FinishedWatchingAt &gt; t.start) &amp;&amp; (d.StartedWatchingAt &lt; t.end))).ToList();
</code></pre>
<p>here time_ranges(which is a a helper class, not connected to database) is a list of objects from below class</p>
<pre><code>public class TimeRange
{
    public DateTime start { get; set; }
    public DateTime end { get; set; }
}
</code></pre>
<p>the error I am getting:</p>
<blockquote>
<p>The LINQ expression 't =&gt; EntityShaperExpression:
Bscl.Models.ViewLog
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.FinishedWatchingAt &gt; t.start &amp;&amp; EntityShaperExpression:
Bscl.Models.ViewLog
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.StartedWatchingAt &lt; t.end &amp;&amp; __userIds_1.Contains(EntityShaperExpression:
Bscl.Models.ViewLog
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.UserId)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>But I can't establish it. please forgive me if its a dumb mistake and help me.</p>

## Answers
### Answer ID: 76697841
<p>The issue you are facing is due to Entity Framework's inability to translate some LINQ operations into SQL queries. Specifically, your problem lies in the usage of the Any operator with a list of complex objects (time_ranges), which is not directly convertible to SQL. The database provider doesn't know how to execute this part of the query on the database server.</p>
<p>One way to solve this problem is by rewriting your query to be understandable by Entity Framework, or performing part of the operations in memory (client-side) by loading the data into memory first. Note that this could be inefficient for large datasets.</p>
<p>Try this instead :</p>
<pre><code>var log = new List&lt;ViewLog&gt;();

foreach (var range in time_ranges)
{
    var temp = db.ViewLogs
                 .Where(d =&gt; d.FinishedWatchingAt &gt; range.start &amp;&amp; d.StartedWatchingAt &lt; range.end)
                 .ToList();

    log.AddRange(temp);
}
</code></pre>

