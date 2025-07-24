# Add Day to DateTime in EF Core 3 when Select executed
[Link to question](https://stackoverflow.com/questions/60188266/add-day-to-datetime-in-ef-core-3-when-select-executed)
**Creation Date:** 1581510187
**Score:** 1
**Tags:** linq, entity-framework-core, linq-to-entities
## Question Body
<p>I am trying to query the database using EF Core 3, group DateTime field by Date and Hours and add Hour part to Date on Select. So far all my Linqs fail.</p>

<p>Fail case 1. Add hours to Date using AddHours.</p>

<pre><code>Logs.GroupBy(g =&gt; new
{
    g.DateStamp.Date,
    g.DateStamp.Hour,
    g.Result
}).Select(s =&gt; new
{
    Date = s.Key.Date.AddHours(s.Key.Hour),
    s.Key.Result,
    Conversions = s.Count(),
    Cost = s.Sum(sum =&gt; sum.ConversionCost)
}).OrderBy(o =&gt; o.Date)
</code></pre>

<p>Error: </p>

<blockquote>
  <p>The datepart hour is not supported by date function dateadd for data
  type date.</p>
</blockquote>

<p>Not sure exactly where is the problem, AddHours is not supported by Linq to Entity provider or s.Key.Date fields can't contain hours anymore because it becomes Date only field.</p>

<p>Fail case 2. Create new DateTime object and pass variables.</p>

<pre><code>Logs.GroupBy(g =&gt; new
{
    g.DateStamp.Date,
    g.DateStamp.Hour,
    g.Result
}).Select(s =&gt; new
{
    Date =new DateTime(s.Key.Date.Year, s.Key.Date.Month, s.Key.Date.Day,  s.Key.Hour, 0, 0),   
    s.Key.Result,
    Conversions = s.Count(),
    Cost = s.Sum(sum =&gt; sum.ConversionCost)
}).OrderBy(o =&gt; o.Date)
</code></pre>

<p>Error:</p>

<blockquote>
  <p>InvalidOperationException: The LINQ expression
  'OrderBy&lt;&lt;>f__AnonymousType1, DateTime>(
      source: Selectf__AnonymousType0, Log>, &lt;>f__AnonymousType1>(
          source: GroupByf__AnonymousType0, Log>(
              source: DbSet, 
              keySelector: (l) => new { 
                  Date = l.DateStamp.Date, 
                  Hour = l.DateStamp.Hour, 
                  Result = l.Result
               }, 
              elementSelector: (l) => l), 
          selector: (e) => new { 
              Date = new DateTime(
                  e.Key.Date.Year, 
                  e.Key.Date.Month, 
                  e.Key.Date.Day, 
                  e.Key.Hour, 
                  0, 
                  0
              ), 
              Result = e.Key.Result, 
              Conversions = Count(e), 
              Cost = Sum(
                  source: e, 
                  selector: (sum) => sum.ConversionCost)
           }), 
      keySelector: (e0) => e0.Date)' could not be translated. Either rewrite the query in a form that can be translated, or switch to
  client evaluation explicitly by inserting a call to either
  AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See
  <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>

<p>The <code>OrderBy(o =&gt; o.Date)</code> stops working and gives an exception, why? I have no idea either. </p>

<p>So the final question would be, how to group DateTime field from SQL Database using EF Core by Date+Hour and move it to Select into one field and also perform OrderBy by new Date field at the end.</p>

## Answers
### Answer ID: 73653202
<p>I had the same issue when using EFCore 6, I was getting an error doing a Date.AddHours because it looks like it cast to date instead of datetime. In order to get it to work I had to cast to object and then cast to DATETIME, then I was able to add my hours.</p>
<pre><code>Logs.GroupBy(g =&gt; new
{
    g.DateStamp.Date,
    g.DateStamp.Hour,
    g.Result
}).Select(s =&gt; new
{
    Date = ((DateTime)(object)s.Key.Date).AddHours(s.Key.Hour),
    s.Key.Result,
    Conversions = s.Count(),
    Cost = s.Sum(sum =&gt; sum.ConversionCost)
}).OrderBy(o =&gt; o.Date)
</code></pre>

### Answer ID: 67094434
<p>I'm able to comment on the fail case 1 as I've also encountered the same issue.</p>
<ol>
<li><code>x.Date</code> is converted to sql as <code>CONVERT(date, x)</code></li>
<li><code>x.AddHours(y)</code> is converted to sql as <code>DATEADD(hour, x, y)</code></li>
<li>We have both, so it's <code>DATEADD(hour, CONVERT(date, x), y)</code> and it's not possible, as you can't add hours to data of type <code>date</code> hence the error message.</li>
</ol>
<p>On the sql level it's usually fixed by adding additional cast to <code>datetime2</code>, sth like</p>
<pre><code>CAST(CONVERT(date, x) AS datetime2)
</code></pre>
<p>So you deal on <code>datetime2</code> level again and able to add hours to the resulting value.</p>
<p>Having said that I dunno how to force EF to generate additional cast (both <code>(DateTime)</code> or <code>Convert.ToDateTime</code> were of no help), so here is a workaround I came up with (can't say whether it could fail with overflow once)</p>
<pre><code>   x.AddMilliseconds(-EF.Functions.DateDiffMillisecond(TimeSpan.Zero, x.TimeOfDay))
    .AddHours(y)
</code></pre>
<p>Tested it with EF Core 3.1.12 and it works for me as expected. This is the output</p>
<pre><code>(DATEADD(
    hour, 
    CAST(y AS int), 
    DATEADD(
        millisecond, 
        CAST(
            CAST(
                -DATEDIFF(MILLISECOND, '00:00:00', CAST(x AS time)) AS float) AS int
            ), 
        x
    )
)
</code></pre>
<p>Would guess that case 2 fails, as EF is not able to translate <code>new DateTime</code> expression, but it's just error being cryptic.</p>

