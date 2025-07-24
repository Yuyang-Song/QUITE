# Group by hour in IQueryable
[Link to question](https://stackoverflow.com/questions/57038298/group-by-hour-in-iqueryable)
**Creation Date:** 1563188234
**Score:** 3
**Tags:** c#, datetime, entity-framework-core, linq-to-entities, iqueryable
## Question Body
<p>In my project I receive some data from an SPS all x seconds. Every y minutes I archive the current Data in a database so I'm able to show statistics.  </p>

<p>The data I receive gets put in a model. Something like this but much more complex:</p>

<pre><code>public class Data
{
    public DateTime ArchiveTime { get; set; }
    public float TempC { get; set; }
    public float CO2Percent { get; set; }
}
</code></pre>

<p>I have a repository for the database that returns all entries in a certain time span. See this code:</p>

<pre><code>// Context is my DbContext for a SQLite db and Data is the DbSet&lt;Data&gt; on that
IQueryable&lt;Data&gt; GetDataBetween(DateTime from, DateTime to) =&gt; Context.Data.Where(d =&gt; (d.ArchiveTime &gt;= from &amp;&amp; d.ArchiveTime &lt;= to));
</code></pre>

<p>As you can see this returns an <code>IQueryable</code> so I want to make use of the linq to entities functionality.<br>
<em>I believe it's called linq to entities but in case it isn't, I mean the functionality that converts expression trees to sql or whatever instead of just executing it in C#.</em>  </p>

<p>Since there is an indeterminable amount of entries per hour in the database I want to <strong>only get one entry per hour (the first one)</strong> so I can display it in a graph.  </p>

<p>Here's an example of some datetimes that maybe show my intent a bit better:<br>
<strong>NOTE:</strong> these are only the datetimes contained in the object, I want the whole object - not just the times.</p>

<pre><code>// say this is all the data I get between two times
2019-07-06 10:30:01 // I want
2019-07-06 10:40:09
2019-07-06 10:50:10
2019-07-06 11:00:13 // I want
2019-07-06 11:10:20
2019-07-06 11:20:22
2019-07-06 11:30:24
2019-07-06 11:40:32
2019-07-06 11:50:33
2019-07-06 12:00:35 // I want
2019-07-06 12:10:43
2019-07-06 12:20:45
2019-07-06 12:40:54
2019-07-06 12:50:56
2019-07-06 13:00:58 // I want
2019-07-06 13:11:06
2019-07-06 13:21:08
2019-07-06 13:31:09
</code></pre>

<p>The current way I do this is via a <code>IEnumerable</code> and <code>GroupBy</code>. See this code: </p>

<pre><code>var now = DateTime.Now;
IQueryable&lt;Data&gt; dataLastWeek = repos.GetDataBetween(now.AddDays(-7), now);

IEnumerable&lt;Data&gt; onePerHour = dataLastWeek.AsEnumerable()
    .GroupBy(d =&gt; new DateTime(d.ArchiveTime.Year, d.ArchiveTime.Month, d.ArchiveTime.Day, d.ArchiveTime.Hour, 0, 0))
    .Select(g =&gt; g.First());
</code></pre>

<p>This works fine but since it uses <code>IEnumerable</code> and creates objects, I don't get the advantages of linq to entities and I think it must a lot slower this way.   </p>

<p>Is there any way to rewrite this query to work with <code>IQueryable</code> on a SQLite database?  </p>

<p>EDIT: I'm working with the .net core 3 preview6 (newest preview) version of EF Core. Maybe there is a new feature that allowes for what I want :)</p>

## Answers
### Answer ID: 57039296
<p>The key part of the <code>GroupBy</code> can easily be made translatable by avoiding <code>new DateTime(...)</code> and using either anonymous type</p>

<pre><code>.GroupBy(d =&gt; new { d.ArchiveTime.Date, d.ArchiveTime.Hour })
</code></pre>

<p>or <code>Date</code> property + <code>AddHours</code>:</p>

<pre><code>.GroupBy(d =&gt; d.ArchiveTime.Date.AddHours(d.ArchiveTime.Hour))
</code></pre>

<p>Unfortunately currently (EF Core 2.2) does not translate nested <code>First</code> / <code>FirstOrDefault</code> / <code>Take(1)</code> to SQL and uses client evaluation. For <code>First()</code> it is forced in order to emulate the LINQ to Objects throwing behavior, but for the other two patterns it's caused by the lack of proper translation.</p>

<p>The only server side solution I see for your concrete query is to not use <code>GroupBy</code> at all, but correlated self antijoin, something like this:</p>

<pre><code>var onePerHour = dataLastWeek.Where(d =&gt; !dataLastWeek.Any(d2 =&gt;
    d2.ArchiveTime.Date == d.ArchiveTime.Date &amp;&amp;
    d2.ArchiveTime.Hour == d.ArchiveTime.Hour &amp;&amp;
    d2.ArchiveTime &lt; d.ArchiveTime));
</code></pre>

