# How to get average date difference in PostgreSQL using EF Core 3
[Link to question](https://stackoverflow.com/questions/62757853/how-to-get-average-date-difference-in-postgresql-using-ef-core-3)
**Creation Date:** 1594044509
**Score:** 0
**Tags:** c#, postgresql, linq, entity-framework-core, npgsql
## Question Body
<p>Using npgsql, EF Core 3 and a PostgreSQL database, I am trying to write the following SQL query in LINQ.</p>
<p>SQL:</p>
<pre><code>SELECT date(&quot;EndDate&quot;), avg(&quot;EndDate&quot;-&quot;StartDate&quot;) as avg_time
FROM trip
group by date(&quot;EndDate&quot;)
</code></pre>
<p>LINQ:</p>
<pre><code>var q = from trip in _context.Trips
        group trip by trip.EndDate.Date into tripGroup
        select new { date = tripGroup.Key, avg_time_mins = tripGroup.Average(tg =&gt; (tg.EndDate - tg.StartDate).TotalMinutes) };
</code></pre>
<p>I tried with <code>TotalMinutes</code>, because <code>.Average( )</code> does not seem to take a TimeSpan. All efforts ended up with a runtime exception stating that this construct is not supported and suggesting to rewrite the query.</p>

## Answers
### Answer ID: 62762123
<p>If u want to TimeSpan as average using Linq(that what I understand from question)
first u have to understand average will be done in memory.</p>
<pre><code>var groups = await _context.Trips.GroupBy(trip =&gt;trip.EndDate.Date).ToArrayAsync() // load Them in memory

var q = groups.Select(group=&gt; {
    var timeSpans = group.Select(trip=&gt;trip.EndDate - trip.StartDate);
    var avg = GetAverage(timeSpans)
    return new {group.key, avg }
}).ToArray()


TimeSpan GetAverage(IEnumerable&lt;TimeSpan&gt; timeSpans){
 var average= timeSpans.Average(x =&gt; x.TotalMilliseconds)
 return TimeSpan.FromMilliseconds(average);
} 
</code></pre>

