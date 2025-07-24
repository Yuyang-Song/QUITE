# Query where multiple columns have to match a value set simultaneously in EF Core
[Link to question](https://stackoverflow.com/questions/70744232/query-where-multiple-columns-have-to-match-a-value-set-simultaneously-in-ef-core)
**Creation Date:** 1642435455
**Score:** 6
**Tags:** c#, entity-framework, entity-framework-core
## Question Body
<p><strong>The problem</strong></p>
<p>I have a client application which loads a local data file. This data file specifies for each item the <code>Type</code> and <code>Version</code>.</p>
<p>From this file, I compile a list of <code>Type</code> and <code>Version</code> pairs.</p>
<pre><code>var typeVersionSets = datafile.Select(item =&gt; new { Type = item.TypeId, Version = item.VersionId }).Distinct();
</code></pre>
<p><em>Note</em>: there are more than these two fields, but for the sake of simplicity I just denote these two.</p>
<p>I also have a SQL Server which runs in the cloud. I need to get all records from a table which meet the value pairs (so the column values must match <em>simultaneously</em>).</p>
<p>I wrote this simple query which cannot be run by EF Core:</p>
<pre><code>List&lt;MyTableRow&gt; MyResult = await dbContext.MyTable
    .Where(dbItem =&gt; typeVersionSets.Contains(new { Type = dbItem.TypeId, Version = dbItem.VersionId }))
    .ToListAsync();
</code></pre>
<p>I get the following runtime error:</p>
<blockquote>
<p>One or more errors occurred. (The LINQ expression 'DbSet().Where(p =&gt; __MyTableRowTypeVersions_2.Contains(new { Type = p.TypeId, Version = p.VersionId }))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.)</p>
</blockquote>
<p><strong>TLDR some details</strong></p>
<p>The <code>MyTable</code> is huge and I cannot afford to download it every time and evaluate the LINQ expression on the client.</p>
<p>The number of <code>typeVersionSets</code> is reasonably small (let's say 10 sets).</p>
<p>Of course, I can loop over <code>typeVersionSets</code> like:</p>
<pre><code>List&lt;MyTableRow&gt; MyResult = new List&lt;MyTableRow&gt;();

foreach (var set in typeVersionSets)
{
    MyResult.AddRange(
            await dbContext.MyTable
                .Where(pp =&gt; pp.TypeId == set.Type &amp;&amp; pp.VersionId == set.Version)
                .ToListAsync()
            );
}
    
</code></pre>
<p>However, this would require 10 database calls.</p>
<p>This code will be executed many times per user and by many users.</p>
<p>Is there a more efficient solution which would result in 1 database call per event without transferring a lot of unnecessary data to the client (or the server).</p>
<p><strong>Some additional notes</strong></p>
<p>I use:</p>
<ul>
<li>.NET (core) 5.0</li>
<li>Entity Framework Core version 5.0.9.</li>
</ul>
<p>In case it matters, I cannot migrate to EF Core 6 since this required a migration to .NET (core) 6.0 which raises a lot of issues which are out of my scope.</p>

## Answers
### Answer ID: 78732959
<p>From <a href="https://github.com/dotnet/efcore/issues/32092#issuecomment-2221633692" rel="nofollow noreferrer">https://github.com/dotnet/efcore/issues/32092#issuecomment-2221633692</a></p>
<pre class="lang-cs prettyprint-override"><code>/// &lt;see&gt;https://github.com/dotnet/efcore/issues/32092#issuecomment-2221633692&lt;/see&gt;
/// &lt;see&gt;https://stackoverflow.com/questions/70744232/query-where-multiple-columns-have-to-match-a-value-set-simultaneously-in-ef-core/78732959#78732959&lt;/see&gt;
public static IQueryable&lt;TEntity&gt; WhereOrContainsValues&lt;TEntity, TToCompare&gt;(
    this IQueryable&lt;TEntity&gt; queryable,
    IEnumerable&lt;TToCompare&gt; valuesToCompare,
    IEnumerable&lt;Func&lt;TToCompare, Expression&lt;Func&lt;TEntity, bool&gt;&gt;&gt;&gt; comparatorExpressionFactories) =&gt;
    queryable.Where(valuesToCompare.Aggregate(
        LinqKit.PredicateBuilder.New&lt;TEntity&gt;(),
        (outerPredicate, valueToCompare) =&gt; outerPredicate.Or(
            comparatorExpressionFactories.Aggregate(
                LinqKit.PredicateBuilder.New&lt;TEntity&gt;(),
                (innerPredicate, expressionFactory) =&gt;
                    innerPredicate.And(expressionFactory(valueToCompare))))));
</code></pre>
<p>Taking the example from <a href="https://github.com/dotnet/efcore/issues/32092#issue-1951139044" rel="nofollow noreferrer">https://github.com/dotnet/efcore/issues/32092#issue-1951139044</a></p>
<pre class="lang-cs prettyprint-override"><code>public class Order
{
     [Key]
     public long TenantId {get;set;}

    [Key]
     public long Id {get;set;}

    //other properties...
}

(long tenantId, long orderId)[] orderIds = //array of (long, long) tuples of the composite ids of the orders that need to be fetched
var orders = await ctx.Orders.Where(o =&gt; orderIds.Contains((o.TenantId, o.Id)).ToArrayAsync(); //this doesn't work
</code></pre>
<p>it now would be:</p>
<pre class="lang-cs prettyprint-override"><code>var orders = await ctx.Orders.WhereOrContainsValues(orderIds,
[
    orderId =&gt; order =&gt; orderId.tenantId == order.TenantId,
    orderId =&gt; order =&gt; orderId.orderId == order.Id 
]).ToArrayAsync();
</code></pre>
<p>and translated to SQL like:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT fields FROM Orders
WHERE (TenantId = $1 AND Id = $2)
   OR (TenantId = $3 AND Id = $4)
-- keep go on for each item in orderIds
</code></pre>

### Answer ID: 70744821
<p>You can use this <a href="https://stackoverflow.com/a/67666993/10646316">extension</a>:</p>
<pre class="lang-cs prettyprint-override"><code>dbContext.MyTable
    .FilterByItems(typeVersionSets, (pp, set) =&gt; pp.TypeId == set.Type &amp;&amp; pp.VersionId == set.Version, true)
    .ToListAsync();
</code></pre>

### Answer ID: 70744370
<p>I'd be inclined to build a dynamic <code>Expression&lt;Func&lt;MyTableRow, bool&gt;&gt;</code> to represent the filter.</p>
<pre><code>var p = Expression.Parameter(typeof(MyTableRow), &quot;dbItem&quot;);

var parts = new List&lt;Expression&gt;();
foreach (var set in typeVersionSets)
{
    var typeIdValue = Expression.Property(p, nameof(MyTableRow.TypeId));
    var typeIdTarget = Expression.Constant(set.Type);
    var typeIdTest = Expression.Equal(typeIdValue, typeIdTarget);
    
    var versionIdValue = Expression.Property(p, nameof(MyTableRow.VersionId));
    var versionIdTarget = Expression.Constant(set.Version);
    var versionIdTest = Expression.Equal(versionIdValue, versionIdTarget);
    
    var part = Expression.AndAlso(typeIdTest, versionIdTest);
    parts.Add(part);
}

var body = parts.Aggregate(Expression.OrElse);
var filter = Expression.Lambda&lt;Func&lt;MyTableRow, bool&gt;&gt;(body, p);

List&lt;MyTableRow&gt; MyResult = await dbContext.MyTable
    .Where(filter)
    .ToListAsync()
</code></pre>
<p><a href="https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/expression-trees/" rel="nofollow noreferrer">Expression Trees (C#) | Microsoft Docs</a></p>

