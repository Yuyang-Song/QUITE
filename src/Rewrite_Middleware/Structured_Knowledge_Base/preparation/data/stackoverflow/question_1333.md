# EF Core can&#39;t translate an expression to compare two collections which EF 6 could
[Link to question](https://stackoverflow.com/questions/70753699/ef-core-cant-translate-an-expression-to-compare-two-collections-which-ef-6-coul)
**Creation Date:** 1642500341
**Score:** 1
**Tags:** entity-framework, linq, entity-framework-core
## Question Body
<p>I have the following query in the old Entity Framework (.NET Framework):</p>
<pre><code>db.ProductVariations
    .Where(pv =&gt; pv.Product.Categories
        .Any(cat =&gt; categorySearchStrings
            .Any(categorySearchString =&gt; cat.SearchTree.StartsWith(categorySearchString))));
</code></pre>
<p><em>I realize this isn't pretty, but I'm refactoring a legacy app and we have to choose our battles.</em></p>
<p>So what happens is that you can pass a list of search string (the <code>categorySearchStrings</code>), e.g.:</p>
<pre><code>&quot;38.54.&quot;, &quot;45.&quot;
</code></pre>
<p>This is basically an implementation of a <a href="https://en.wikipedia.org/wiki/Search_tree" rel="nofollow noreferrer">search tree</a> where each category in our database has a <code>SearchTree</code> property. So a category with search tree <code>38.54.99</code> would match, but <code>38.</code> would not.</p>
<p>A product can have multiple categories and we can pass in multiple search tree strings to the query. So we're comparing two collections.</p>
<p>This gets translated to</p>
<pre><code>SELECT 
    [GroupBy1].[A1] AS [C1]
    FROM ( SELECT 
        COUNT(1) AS [A1]
        FROM [dbo].[ProductVariation] AS [Extent1]
        WHERE  EXISTS (SELECT 
            1 AS [C1]
            FROM ( SELECT 
                [Extent3].[SearchTree] AS [SearchTree]
                FROM  [dbo].[ProductCategory] AS [Extent2]
                INNER JOIN [dbo].[Category] AS [Extent3] ON [Extent2].[CategoryId] = [Extent3].[Id]
                WHERE [Extent1].[ProductId] = [Extent2].[ProductId]
            )  AS [Project1]
            WHERE  EXISTS (SELECT 
                1 AS [C1]
                FROM  ( SELECT 1 AS X ) AS [SingleRowTable1]
                WHERE ( CAST(CHARINDEX(N'38.', [Project1].[SearchTree]) AS int)) = 1
            )
        )
    )  AS [GroupBy1]
</code></pre>
<p>I'm trying to migrate to Entity Framework Core (6, running on .NET 6) but this now gives me the following error:</p>
<pre><code>System.InvalidOperationException : The LINQ expression 'categorySearchString =&gt; categorySearchString == &quot;&quot; || EntityShaperExpression: 
        Company.Data.Models.Category
        ValueBufferExpression: 
            ProjectionBindingExpression: Inner
        IsNullable: False
    .SearchTree != null &amp;&amp; categorySearchString != null &amp;&amp; EntityShaperExpression: 
        Company.Data.Models.Category
        ValueBufferExpression: 
            ProjectionBindingExpression: Inner
        IsNullable: False
    .SearchTree.StartsWith(categorySearchString)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>
<p>Switching to client evaluation isn't really an option I believe, because there's too many data that will be retrieved. Plus, there's more going on than just this Where clause. I simplified it.</p>
<p>I also tried rewriting it as this:</p>
<pre><code>.Where(pv =&gt; pv.Product.Categories.Select(c =&gt; c.SearchTree).Any(st =&gt; categorySearchStrings.Any(ss =&gt; st.StartsWith(ss))));
</code></pre>
<p>But I just get the same error.</p>
<p>Is it possible to do this with EF Core?</p>

## Answers
### Answer ID: 70753903
<p>I'd be inclined to build a dynamic <a href="https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/expression-trees/" rel="nofollow noreferrer">expression tree</a> to represent the filter:</p>
<pre class="lang-c# prettyprint-override"><code>var cat = Expression.Parameter(typeof(Category), &quot;cat&quot;);
var parts = new List&lt;Expression&gt;(categorySearchStrings.Count);
var startsWithMethod = typeof(string).GetMethod(nameof(string.StartsWith), new[] { typeof(string) });

foreach (string categorySearchString in categorySearchStrings)
{
    var searchTree = Expression.Property(cat, nameof(Category.SearchTree));
    var value = Expression.Constant(categorySearchString);
    var startsWith = Expression.Call(searchTree, startsWithMethod, value);
    parts.Add(startsWith);
}

var body = parts.Aggregate(Expression.OrElse);
var categoryFilter = Expression.Lambda&lt;Func&lt;Category, bool&gt;&gt;(body, cat);

var pv = Expression.Parameter(typeof(ProductVariation), &quot;pv&quot;);
var product = Expression.Property(pv, nameof(ProductVariation.Product));
var categories = Expression.Property(product, nameof(Product.Categories));
var any = Expression.Call(typeof(Enumerable), nameof(Enumerable.Any), new[] { typeof(Category) }, categories, categoryFilter);
var finalFilter = Expression.Lambda&lt;Func&lt;ProductVariation, bool&gt;&gt;(any, pv);

db.ProductVariations
    .Where(finalFilter)
    ...
</code></pre>
<p>You should also report this as <a href="https://github.com/dotnet/efcore/issues" rel="nofollow noreferrer">an issue on the efcore repository</a>, to see if it can be fixed in a future version.</p>
<p>Update: the issue was <a href="https://github.com/dotnet/efcore/issues/27205" rel="nofollow noreferrer">created</a> but was a duplicate of an <a href="https://github.com/dotnet/efcore/issues/19070" rel="nofollow noreferrer">existing issue</a>.</p>

