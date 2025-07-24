# Trouble with Linq Select Query
[Link to question](https://stackoverflow.com/questions/71622002/trouble-with-linq-select-query)
**Creation Date:** 1648235369
**Score:** 0
**Tags:** c#, linq
## Question Body
<p>I am trying to query my Database for a single record ins three steps and I am having problems getting the result that I am looking for.  These are the steps that I created:</p>
<pre><code>client = client
    .Where(s =&gt; s.CompanyName.Contains(name));

var res = client.Select(x =&gt; x.ID);

Tracker = Tracker
    .Where(s =&gt; s.ClientId.Equals(client.Select(x =&gt; x.ID)));
</code></pre>
<p>Debugging the code indicated that steps one and two worked correctly and generated the data that I needed to run my third query, which should provide the whole record, utilizing the result of the second step.</p>
<p>The third and last steps generated the following error:</p>
<blockquote>
<p>&quot;The LINQ expression <code>DbSet&lt;TimeTrackerViewModel&gt;().Where(t =&gt; t.ClientId.Equals(DbSet&lt;ClientsViewModel&gt;().Where(c =&gt; c.CompanyName.Contains(__name_0)).Select(c =&gt; c.ID)))</code> could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;</p>
</blockquote>
<p>How do I query my database, utilizing the query result from the second step?</p>

## Answers
### Answer ID: 71650556
<p>You should try this:</p>
<pre><code>var trakers = (from c in client.Where(s =&gt; s.CompanyName.Contains(name))
              join t in tracker
                  on c.ID
                  equals t.ClientId
              select t).ToList();
</code></pre>
<p>So you do only a query on db.</p>

### Answer ID: 71623196
<p>After reading several related posts, I was able to combine thier ideas into a single working solution as posted below:</p>
<pre><code>                var client = _context.ClientsViewModel
                    .Where(s =&gt; s.CompanyName.Contains(name))
                    .Select(x =&gt; x.ID).ToList();

                Tracker = Tracker
                    .Where(s =&gt; s.ClientId == client[0])
                    .OrderByDescending(x =&gt; x.Id);
</code></pre>

### Answer ID: 71623057
<p>If you want to use the <code>ID</code>s in <code>res</code> to filter <code>Tracker</code> then you can use <a href="https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable.any?view=net-6.0" rel="nofollow noreferrer"><code>Any()</code></a>:</p>
<pre><code>var res = client.Select(x =&gt; x.ID);
trackers = Tracker.Where(s =&gt; res.Any(r =&gt; r == s.ClientId));
</code></pre>
<p>The above query will return a collection.</p>
<blockquote>
<p>I am trying to query my Database for a single record</p>
</blockquote>
<p>If you want to return a single record then you could to use <a href="https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable.firstordefault?view=net-6.0" rel="nofollow noreferrer"><code>FirstOrDefault()</code></a>, either in place of the <code>Where</code> clause (using the same predicate), or after the <code>Where</code> (you could consider <a href="https://learn.microsoft.com/en-us/dotnet/api/system.linq.enumerable.single?view=net-6.0" rel="nofollow noreferrer"><code>Single()</code></a> if you know there's exactly 1 matching record). But you should also consider what you expect to happen if multiple records match the <code>name</code> parameter in your first query and how you would handle that.</p>

