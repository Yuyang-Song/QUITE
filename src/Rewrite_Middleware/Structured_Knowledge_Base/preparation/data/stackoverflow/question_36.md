# Possible multiple enumeration of IEnumerable when counting and skipping
[Link to question](https://stackoverflow.com/questions/10678334/possible-multiple-enumeration-of-ienumerable-when-counting-and-skipping)
**Creation Date:** 1337559598
**Score:** 1
**Tags:** linq-to-sql, c#-4.0, count, ienumerable, skip-take
## Question Body
<p>I'm preparing data for a datatable in Linq2Sql</p>

<p>This code highlights as a 'Possible multiple enumeration of IEnumerable' (in Resharper)</p>

<pre><code>// filtered is an IEnumerable or an IQueryable

var total = filtered.Count();

var displayed = filtered
                .Skip(param.iDisplayStart)
                .Take(param.iDisplayLength).ToList(); 
</code></pre>

<p>And I am 100% sure Resharper is right.</p>

<p>How do I rewrite this to avoid the warning</p>

<p>To clarify, I get that I can put a ToList on the end of filtered to only do one query to the Database eg.</p>

<pre><code> var filteredAndRun = filtered.ToList();

 var total = filteredAndRun.Count();

 var displayed = filteredAndRun
                .Skip(param.iDisplayStart)
                .Take(param.iDisplayLength).ToList(); 
</code></pre>

<p>but this brings back a ton more data than I want to transport over the network.</p>

<p>I'm expecting that I can't have my cake and eat it too. :(</p>

## Answers
### Answer ID: 13845340
<p>You could also do something like</p>

<pre><code>count = 0;
displayed = new List();
iDisplayStop = param.iDisplayStart + param.iDisplayLength;
foreach (element in filteredAndRun) {
    ++count;
    if ((count &lt; param.iDisplayStart) || (count &gt; iDisplayStop))
          continue;
    displayed.Add(element);
}
</code></pre>

<p>That's pseudocode, obviously, and I might be off-by-one in the edge conditions, but that algorithm gets you the count with only a single iteration and you have the list of displayed items only at the end.</p>

### Answer ID: 10678371
<p>It sounds like you're more concerned with multiple enumeration of <code>IQueryable&lt;T&gt;</code> rather than <code>IEnumerable&lt;T&gt;</code>.</p>

<p>However, in your case, it doesn't matter.</p>

<p>The <code>Count</code> call should translate to a simple and very fast SQL count query. It's only the second query that actually brings back any records.</p>

<p>If it is an <code>IEnumerable&lt;T&gt;</code> then the data is in memory and it'll be super fast in any case.</p>

<p>I'd keep your code exactly the same as it is and only worry about performance tuning when you discover you have a significant performance issue. :-)</p>

