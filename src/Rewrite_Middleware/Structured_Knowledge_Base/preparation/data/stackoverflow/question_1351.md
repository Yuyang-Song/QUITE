# LINQ query throws client side evaluation error
[Link to question](https://stackoverflow.com/questions/71977774/linq-query-throws-client-side-evaluation-error)
**Creation Date:** 1650699670
**Score:** 2
**Tags:** c#, linq, entity-framework-core, ef-core-6.0
## Question Body
<p>Been recently delving into EF Core 6 and I'm getting a client side evalutation error which I'm wondering if there's any way to rewrite this in a more efficient way.</p>
<p>I need to query some <code>Photos</code> based on a list of <code>TagIds</code>. For example when filtering by the tags [Portugal,Beach], need to get all photos that include <strong>all those tags</strong>. So the photo X with [Portugal, Beach, Food] will be included but the photo Y [Portugal] will be out.</p>
<p>I believe I need to achieve something like this but that throws the client side evaluation exception:</p>
<pre class="lang-cs prettyprint-override"><code>_context.Photo
    .Include(i =&gt; i.PhotoTags)
       .ThenInclude(j =&gt; j.Tag)
    .Where(i =&gt; filter.tagIds.All(j =&gt; i.PhotoTags.Exists(k =&gt; k.TagId == j)))
</code></pre>
<p>With the following classes:</p>
<pre><code>public class Photo
{
    public Guid Id { get; set; }
        
    public string Description { get; set; }

    public DateTime Date { get; set; }

    public bool IsCover { get; set; }
        
    public virtual List&lt;PhotoTag&gt; PhotoTags { get; set; }
        
}

public class PhotoTag : Base
{
    public Guid Id { get; set; }

    public Tag Tag { get; set; }
    
    public Guid TagId { get; set; }
    
    public Photo Photo { get; set; }
    
    public Guid PhotoId { get; set; }
}
</code></pre>
<p><strong>Edit</strong></p>
<p>This is the error I'm getting:</p>
<pre><code>System.InvalidOperationException: The LINQ expression 'j =&gt; MaterializeCollectionNavigation(
    Navigation: Photo.PhotoTags,
    subquery: DbSet&lt;PhotoTag&gt;()
        .Where(p0 =&gt; EF.Property&lt;Guid?&gt;(EntityShaperExpression: 
            rvc.Models.Photo
            ValueBufferExpression: 
                ProjectionBindingExpression: EmptyProjectionMember
            IsNullable: False
        , &quot;Id&quot;) != null &amp;&amp; object.Equals(
            objA: (object)EF.Property&lt;Guid?&gt;(EntityShaperExpression: 
                rvc.Models.Photo
                ValueBufferExpression: 
                    ProjectionBindingExpression: EmptyProjectionMember
                IsNullable: False
            , &quot;Id&quot;), 
            objB: (object)EF.Property&lt;Guid?&gt;(p0, &quot;PhotoId&quot;)))).Exists(k =&gt; k.TagId == j)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitLambda[T](Expression`1 lambdaExpression)
   at System.Linq.Expressions.Expression`1.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateInternal(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.Translate(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateExpression(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateLambdaExpression(ShapedQueryExpression shapedQueryExpression, LambdaExpression lambdaExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateWhere(ShapedQueryExpression source, LambdaExpression predicate)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at rvc.Services.PhotoService.GetAll(FilterParameters filter) in C:\Users\jjtfs\Work\rvc\server\Services\PhotoService.cs:line 145
</code></pre>

## Answers
### Answer ID: 71978087
<p>This can be rewritten in a translatable form by counting the tags that are in the filter. This count should equal the number of items in the filter:</p>
<pre class="lang-cs prettyprint-override"><code>var count = filter.tagIds.Count();

var result = _context.Photo
.Include(p =&gt; p.PhotoTags)
    .ThenInclude(pt =&gt; pt.Tag)
.Where(p =&gt; p.PhotoTags.Count(pt =&gt; filter.tagIds.Contains(pt.TagId)) == count);
</code></pre>

