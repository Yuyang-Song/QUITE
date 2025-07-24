# How to use Linq or Lambda with IQueryable to GroupBy and get the first/last record on the collection in C#?
[Link to question](https://stackoverflow.com/questions/64834181/how-to-use-linq-or-lambda-with-iqueryable-to-groupby-and-get-the-first-last-reco)
**Creation Date:** 1605358971
**Score:** 1
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>I'm using Entity framework core 3.1 to connect to the database, what I'm trying is to get the Highest and lowest product details which grouped by its category id. based on answers shown on <a href="https://stackoverflow.com/questions/6963707/linq-query-group-by-and-selecting-first-items/7456167?noredirect=1#comment114606791_7456167">this question</a> and <a href="https://stackoverflow.com/questions/19012986/how-to-get-first-record-in-each-group-using-linq">this question</a> I tried to write the following code:</p>
<p>using Linq :</p>
<pre><code>//NOTE: 'Products' is an IQueryable for all the products in the database.
   var highPrice = from a in Products
                          group a by a.CategoryId
                               into prods
                          select prods.OrderByDescending(a =&gt; a.Price).First();
</code></pre>
<p>using Lambda:</p>
<pre><code> //NOTE: 'Products' is an IQueryable for all the products in the database.
     var highPrice = Products.GroupBy(a =&gt; a.CategoryId, (key, a) =&gt; a.OrderByDescending(a =&gt; a.Price).First()).ToList();
</code></pre>
<p>Both works fine only if I converted the <code>IQueryble</code> of <code>Products</code> to <code>IEnumerable</code> using for example <code>.ToList()</code> , but when running without converting it pops the following exception:</p>
<pre><code>System.InvalidOperationException
HResult=0x80131509
Message=The LINQ expression '(GroupByShaperExpression:
KeySelector: (a.CategoryId), 
ElementSelector:(EntityShaperExpression: 
EntityType: Product
ValueBufferExpression: 
(ProjectionBindingExpression: EmptyProjectionMember)
IsNullable: False))
.OrderByDescending(a =&gt; a.Price)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().
</code></pre>
<p>Is there any way to get the first/Last records of IQueryable collection without converting to IEnumerable ??</p>

## Answers
### Answer ID: 64837257
<p>Not all Linq methods can be translated to a SQL query (that's why your expression doesn't compile).</p>
<p>So, you can obtain the same result using the Take() method combined with order by clause.
Following your example:</p>
<pre><code>var mostExpensiveProductByCategory = dbContext.Products
                .GroupBy(x =&gt; x.CategoryId).Select(x =&gt; new
                {
                    CategoryId = x.Key,
                    Product = x.OrderByDescending(p =&gt; p.Price).Take(1)
                })
                .ToList();

var cheapestProductByCategory = dbContext.Products
                .GroupBy(x =&gt; x.CategoryId).Select(x =&gt; new
                {
                    CategoryId = x.Key,
                    Product = x.OrderBy(p =&gt; p.Price).Take(1)
                })
                .ToList();
</code></pre>
<p><strong>UPDATE:</strong></p>
<p>To achieve your requirement and avoid in-memory grouping, I would suggest you to work with navigation properties, see below:</p>
<pre><code>var mostExpensiveProductByCategory = dbContext.Categories.Select(x =&gt; new 
{ 
    x.CategoryId, 
    Products = x.Products.OrderByDescending(p =&gt; p.Price).Take(1) 
}).ToList();
</code></pre>
<p>This will produce the following query output:</p>
<pre><code>SELECT [c].[CategoryId], [t0].[ProductId], [t0].[CategoryId], [t0].[Price] 
FROM [Categories] AS [c] 
LEFT JOIN ( SELECT [t].[ProductId], [t].[CategoryId], [t].[Price] 
FROM ( SELECT [p].[ProductId], [p].[CategoryId], [p].[Price], ROW_NUMBER() OVER(PARTITION BY [p].[CategoryId] ORDER BY [p].[Price] DESC) AS [row] 
FROM [Products] AS [p] ) AS [t] WHERE [t].[row] &lt;= 1 ) AS [t0] ON [c].[CategoryId] = [t0].[CategoryId] 
ORDER BY [c].[CategoryId], [t0].[CategoryId], [t0].[Price] DESC, [t0].[ProductId]
</code></pre>

