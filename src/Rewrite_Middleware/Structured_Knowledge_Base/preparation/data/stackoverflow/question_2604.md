# How do I rewrite this Linq query to avoid using FirstOrDefault?
[Link to question](https://stackoverflow.com/questions/42353640/how-do-i-rewrite-this-linq-query-to-avoid-using-firstordefault)
**Creation Date:** 1487622472
**Score:** 3
**Tags:** c#, entity-framework, linq
## Question Body
<p>I have a Quotes table, which has an associated Revisions table. A basic business rule is that a quote must have at least one revision, but may have many. I have a query that starts like this...</p>

<pre><code>var revisions = ctx.Quotes
  .Select(q =&gt; q.Revisions.OrderByDescending(r =&gt; r.RevisionNumber).FirstOrDefault())
  // Do things with the revisions here...
</code></pre>

<p>The purpose is to get the latest revision of each quote, and then select some information from them.</p>

<p>This works fine, except that we had a rogue quote in the database that didn't have any revisions. Somewhere deep down in the code below what's shown above, I got an exception...</p>

<blockquote>
  <p>The cast to value type 'System.Int32' failed because the materialized
  value is null. Either the result type's generic parameter or the query
  must use a nullable type</p>
</blockquote>

<p>This took an age to debug, as we didn't realise it was caused by the rogue quote. Ideally, the second line of the query would have used First() instead of FirstOrDefault(), which would have thrown an exception right there, showing the source of the problem immediately. However, Entity Framework doesn't allow you to use First() or Single() mid-query, which is why we used FirstOrDefault().</p>

<p>Without rewriting the query completely, ie querying the Revisions table first and navigating back up to the Quote (which would be a pain for other reasons), is there a simple way to guard against this? In this case, I fixed it by changing the first line to...</p>

<pre><code>var revisions = ctx.Quotes.Where(q =&gt; q.Revisions.Any())
</code></pre>

<p>...but this is a specific fix for this case, and was only apparent after we eventually found the issue. Ideally, I would like a solution that would be generally applicable.</p>

## Answers
### Answer ID: 42353811
<p>To get an <em>inner join</em> semantics, IMO the general replacement of <code>Select</code> / <code>OrderBy</code> / <code>FirstOrDefault</code> is <code>SelectMany</code> / <code>OrderBy</code> / <code>Take(1)</code>:</p>

<pre><code>var revisions = ctx.Quotes
    .SelectMany(q =&gt; q.Revisions.OrderByDescending(r =&gt; r.RevisionNumber).Take(1))
    // Do things with the revisions here...
</code></pre>

