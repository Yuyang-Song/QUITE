# Checking if database column contains, starts with or ends with any of list items inside a where clause of an EF query doesn&#39;t work
[Link to question](https://stackoverflow.com/questions/75967996/checking-if-database-column-contains-starts-with-or-ends-with-any-of-list-items)
**Creation Date:** 1680993230
**Score:** 0
**Tags:** c#, sql-server, database, entity-framework, .net-core
## Question Body
<p>I'm trying to retrieve from database the list of products which names contains, starts with or ends with any of list elements that I pass as parameter to the method executing the query.</p>
<p>I've tried both Linq approaches (method and query syntax)</p>
<p>Here is the relevant code of Linq method query, names being List of names passed as argument to the method:</p>
<pre><code>var query =  _dbContext.Products
                       .Where(p =&gt; p.IdExternalProduct == null &amp;&amp; 
                                   names.Any(name =&gt; p.ProductName.Contains(name)))
                       .Select(item =&gt; new ProductEntity() { Uuid = item.Uuid, Code = item.Code});
</code></pre>
<p>or</p>
<pre><code>var query =  _dbContext.Products
                       .Where(p =&gt; p.IdExternalProduct == null &amp;&amp; 
                                   names.Any(name =&gt; p.ProductName.StartsWith(name)))
                       .Select(item =&gt; new ProductEntity() { Uuid = item.Uuid, Code = item.Code});
</code></pre>
<p>And here is the query syntax approach:</p>
<pre><code>IQueryable&lt;ProductEntity&gt; query = (
                        from p in _dbContext.Products
                        where 
                            p.IdExternalProduct == null &amp;&amp;
                            (names != null &amp;&amp; names.Count &gt; 0 ? names.Any(name =&gt; p.ProductName.Contains(name)) : true)
                        select new ProductEntity()
                        {
                          Uuid = p.Uuid,
                          Code = p.Code
                        }
</code></pre>
<p>The exact same query works when I try with <code>Equals</code> instead of <code>Contains</code>, <code>StartsWith</code> or <code>EndsWith</code>.</p>
<p>I searched a lot and found a lot of resources but no solution worked for me.</p>
<p>Here are two related Stack overflow's questions where Jon Skeet recommends the same implementation.</p>
<p><a href="https://stackoverflow.com/questions/9032655/check-if-a-string-within-a-list-contains-a-specific-string-with-linq">Check if a string within a list contains a specific string with Linq</a></p>
<p><a href="https://stackoverflow.com/questions/6359980/proper-linq-where-clauses">Proper LINQ where clauses</a></p>
<p>I'm using the version 6.0.10 of Entity Framework and SQL Server provider.</p>
<p>But it's seems that these formulas cannot be translated, throwing an exception with the following message:</p>
<blockquote>
<p>The LINQ expression 'name =&gt; EntityShaperExpression:<br />
Service.Product.Products<br />
ValueBufferExpression:<br />
ProjectionBindingExpression: EmptyProjectionMember<br />
IsNullable: False<br />
.ProductName.Contains(name)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>

## Answers
### Answer ID: 75972232
<p>The reason why Jon Skeet recommends this implementation in the other SO answers is because it refers to <code>IEnumerable</code> queries (linq-to-object) and not <code>IQueryable</code> queries (linq-to-entities). Linq-to-object executes on in-memory objects, and will actually execute the <code>string.Contains</code> method. Methods given to EF are not actually executed, they are <em>translated</em> into SQL statements, and efcore 6 does not know how to translate your statement, especially the <code>name</code> variable that comes from a linq-to-object lambda in the <code>IEnumerable.Any</code> call.</p>
<p>Most developper forget that <code>IQueryable&lt;T&gt;</code> is a cumulative type, and you can aggregate predicates on it. A simple solution would be to union queries from each name, and distinct all results:</p>
<pre class="lang-cs prettyprint-override"><code>var query = names.Select(name =&gt; _dbContext.Products
    .Where(product =&gt; product.IdExternalProduct == null)
    .Where(product =&gt; product.ProductName.Contains(name)))
  .Aggregate(Queryable.Union)
  .Distinct()
  .Select(product =&gt; new ProductEntity(...));
</code></pre>
<p>This query produces the following statement:</p>
<pre><code>DECLARE @__name_0 nvarchar(4000) = N'a';
DECLARE @__name_1 nvarchar(4000) = N'b';

SELECT DISTINCT [t].[Id], [t].[IdExternalProduct], [t].[ProductName]
FROM (
    SELECT [p].[Id], [p].[IdExternalProduct], [p].[ProductName]
    FROM [Products] AS [p]
    WHERE ([p].[IdExternalProduct] IS NULL) AND ((@__name_0 LIKE N'') OR CHARINDEX(@__name_0, [p].[ProductName]) &gt; 0)
    UNION
    SELECT [p0].[Id], [p0].[IdExternalProduct], [p0].[ProductName]
    FROM [Products] AS [p0]
    WHERE ([p0].[IdExternalProduct] IS NULL) AND ((@__name_1 LIKE N'') OR CHARINDEX(@__name_1, [p0].[ProductName]) &gt; 0)
) AS [t]
</code></pre>

