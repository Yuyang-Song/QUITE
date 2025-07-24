# SelectMany after Select to get 2 int columns into single distinct List in EF Core 7
[Link to question](https://stackoverflow.com/questions/75072959/selectmany-after-select-to-get-2-int-columns-into-single-distinct-list-in-ef-cor)
**Creation Date:** 1673367837
**Score:** 0
**Tags:** c#, .net, postgresql, entity-framework-core
## Question Body
<p>I have a table containing columns UserId1 and UserId2 and my goal is to load some rows based on different criterias into single distinct list. In other words I'm trying to get the List of user Ids.</p>
<pre class="lang-cs prettyprint-override"><code>await _dbContext.MyTable.Where(p =&gt; ...)
                .Select(p =&gt; new[] { p.UserId1, p.UserId2 })
                .SelectMany(id =&gt; id).Distinct().ToListAsync();
</code></pre>
<p>Executing the code throws an Exception</p>
<blockquote>
<p>'The LINQ expression 'id =&gt; id' could not be translated. Either
rewrite the query in a form that can be translated, or switch to
client evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I know that I can load the sets into memory and execute SelectMany() on the loaded data but still, is there an efficient way to retrieve the distinct list of ints from 2 columns directly from the database into the single list?</p>

## Answers
### Answer ID: 75073017
<p>You can't run such query via EF Core, but you can emulate:</p>
<pre class="lang-cs prettyprint-override"><code>var filtered = _dbContext.MyTable.Where(p =&gt; ...);

var result = await filtered
    .Select(p =&gt; p.UserId1)
    .Union(filtered.Select(p =&gt; p.UserId2))
    .ToListAsync();
</code></pre>
<p><code>Distinct</code> is not needed, <code>Union</code> filters out duplicates.</p>
<p>Also compare performance with partial client-side calculation:</p>
<pre class="lang-cs prettyprint-override"><code>var result = (await filtered
    .Select(p =&gt; new[] { p.UserId1, p.UserId2 })
    .ToListAsync())
    .SelectMany(id =&gt; id)
    .Distinct()
    .ToList();
</code></pre>

