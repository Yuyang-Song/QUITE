# ASP.NET LINQ query DbSet.Join() does not work
[Link to question](https://stackoverflow.com/questions/75282645/asp-net-linq-query-dbset-join-does-not-work)
**Creation Date:** 1675072190
**Score:** 0
**Tags:** c#, linq, entity-framework-core, ef-core-7.0
## Question Body
<p>I try to run this code here, in ASP.NET Entity Framework 7. The target is to have the most efficient solution here which should be a JOIN if the database.</p>
<pre><code>public async Task&lt;List&lt;Building&gt;&gt; GetAllAsync(string commaSeparatedBuildingIDs)
    {
        var buildingRefIDs = commaSeparatedBuildingIDs.Split(&quot;,&quot;).ToList();

            return await semiSoftDbContext.Buildings
            .Join(buildingRefIDs, building =&gt; building.ReferenceId, refID =&gt; refID, (building, id) =&gt; building)
            .ToListAsync();

    }
</code></pre>
<p>I get the following error:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet()
.Join(
inner: __p_0,
outerKeySelector: building =&gt; building.ReferenceId,
innerKeySelector: refID =&gt; refID,
resultSelector: (building, id) =&gt; building)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.`</p>
</blockquote>
<p>I already have tried several variations of join and read through the internet, but it says that ASP.Net should work with Join().</p>

## Answers
### Answer ID: 75282767
<p>You should not join here (assuming you are using Entity Framework - AFAIK it does not handle quite a lot of operations with local collections, like joins), use <code>Where</code> with <code>Contains</code>:</p>
<pre class="lang-cs prettyprint-override"><code>return await semiSoftDbContext.Buildings
   .Where(b =&gt; buildingRefIDs.Contains(b.ReferenceId))
   .ToListAsync();
</code></pre>

