# Microsoft Entity Framework Core Sum items in nested table
[Link to question](https://stackoverflow.com/questions/61503199/microsoft-entity-framework-core-sum-items-in-nested-table)
**Creation Date:** 1588167707
**Score:** 0
**Tags:** c#, .net-core, entity-framework-core
## Question Body
<p>I am using Microsoft Entity Framework Core 5.0.0-preview.2.20120.8 and I want to calculate amount of posts in each Category. Version of .NET Core 3.1. </p>

<pre><code>var result = dataRepository.Categories
        .Include(forum =&gt; forum.Forums)
        .ThenInclude(topic =&gt; topic.Topics)
        .ThenInclude(post =&gt; post.Posts)
        .GroupBy(x =&gt; x.Name)
        .Select(category =&gt; new
        {
            Category = category.Key,
            Count = category.Sum(forum =&gt; forum.Forums.Sum(topic =&gt; topic.Topics.Sum(post =&gt; post.Posts.Count())))
        });
</code></pre>

<p>But in result I have exception</p>

<pre><code>The LINQ expression '(EntityShaperExpression: 
    EntityType: Category
    ValueBufferExpression: 
        (ProjectionBindingExpression: EmptyProjectionMember)
    IsNullable: False
).Forums
    .Sum(topic =&gt; topic.Topics
        .Sum(post =&gt; post.Posts
            .Count()))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>

<p>How to calculate number of posts in each category? How to fix this?</p>

<p><strong>Stack Trace</strong></p>

<pre><code> at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateSum(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.Translate(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitNew(NewExpression newExpression)
   at System.Linq.Expressions.NewExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at System.Collections.Generic.LargeArrayBuilder`1.AddRange(IEnumerable`1 items)
   at System.Collections.Generic.EnumerableHelpers.ToArray[T](IEnumerable`1 source)
   at System.Linq.Enumerable.ToArray[TSource](IEnumerable`1 source)
   at System.Linq.SystemCore_EnumerableDebugView`1.get_Items()
</code></pre>

