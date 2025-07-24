# Issue when building lambda expression progressively
[Link to question](https://stackoverflow.com/questions/71720878/issue-when-building-lambda-expression-progressively)
**Creation Date:** 1648930545
**Score:** 0
**Tags:** c#, asp.net-mvc, asp.net-core
## Question Body
<p>I am trying to build a lambda expression progressively in this manner:</p>
<pre><code>public class PropertySearchFilter
{
    public virtual Expression&lt;Func&lt;T,bool&gt;&gt; GetSearchFilter&lt;T&gt;(SearchFilterModel filterModelModel) where T: Property
    {
        Expression&lt;Func&lt;T, bool&gt;&gt; combinedFilter = null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? countryFilter = filterModelModel.CountryId.HasValue ? x =&gt; x.CountryId == filterModelModel.CountryId.GetValueOrDefault() : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? cityFilter = filterModelModel.CityId.HasValue ? x =&gt; x.CityId == filterModelModel.CityId.GetValueOrDefault() : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? categoryFilter = filterModelModel.CategoryId.HasValue ? x =&gt; x.CategoryId == filterModelModel.CategoryId.GetValueOrDefault() : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? transactionTypeFilter = filterModelModel.TransactionTypeId.HasValue
            ? x =&gt; x.TransactionTypeId == filterModelModel.TransactionTypeId.GetValueOrDefault()
            : null;

        Expression&lt;Func&lt;T, bool&gt;&gt;? publicFilter = filterModelModel.IsPublic.HasValue ? x =&gt; x.IsPublic == filterModelModel.IsPublic.GetValueOrDefault() : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? createdByFilter = !string.IsNullOrEmpty(filterModelModel.CreatedBy) ? x =&gt; x.CreatedBy == filterModelModel.CreatedBy : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? minimumPriceFilter =
            filterModelModel.MinimumPrice.HasValue ? x =&gt; x.Price &gt;= filterModelModel.MinimumPrice.GetValueOrDefault() : null;
        Expression&lt;Func&lt;T, bool&gt;&gt;? maximumPriceFilter = filterModelModel.MaximumPrice.HasValue ? x =&gt; x.Price &lt;= filterModelModel.MaximumPrice.GetValueOrDefault() : null;

        if (countryFilter != null)
            combinedFilter = countryFilter;
        if (cityFilter != null)
        {
            combinedFilter = combinedFilter.And(cityFilter);
        }

        if (categoryFilter != null)
        {
            combinedFilter = combinedFilter.And(categoryFilter);
        }

        if (transactionTypeFilter != null)
        {
            combinedFilter = combinedFilter.And(transactionTypeFilter);
        }

        if (publicFilter != null)
        {
            combinedFilter = combinedFilter.And(publicFilter);
        }

        if (createdByFilter != null)
        {
            combinedFilter = combinedFilter.And(createdByFilter);
        }

        if (minimumPriceFilter != null)
        {
            combinedFilter = combinedFilter.And(minimumPriceFilter);
        }

        if (maximumPriceFilter != null)
        {
            combinedFilter = combinedFilter.And(maximumPriceFilter);
        }

        return combinedFilter;
    }
}
</code></pre>
<p>Here's the extensionMethods:</p>
<pre><code>public static class ExpressionExtensionsMethods
{
    public static Expression&lt;Func&lt;T, bool&gt;&gt; And&lt;T&gt;(this Expression&lt;Func&lt;T, bool&gt;&gt; left, Expression&lt;Func&lt;T, bool&gt;&gt; right)
    {
        if (left == null) return right;
        var and = Expression.AndAlso(left.Body, right.Body);
        return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(and, left.Parameters.Single());
    }

    public static Expression&lt;Func&lt;T, bool&gt;&gt; Or&lt;T&gt;(this Expression&lt;Func&lt;T, bool&gt;&gt; left, Expression&lt;Func&lt;T, bool&gt;&gt; right)
    {
        if (left == null) return right;
        var and = Expression.OrElse(left.Body, right.Body);
        return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(and, left.Parameters.Single());
    }
}
</code></pre>
<p>And I am getting the following error:</p>
<pre class="lang-none prettyprint-override"><code>System.InvalidOperationException: The LINQ expression 'x' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitParameter(ParameterExpression parameterExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMember(MemberExpression memberExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitBinary(BinaryExpression binaryExpression)
   at Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerSqlTranslatingExpressionVisitor.VisitBinary(BinaryExpression binaryExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitBinary(BinaryExpression binaryExpression)
   at Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerSqlTranslatingExpressionVisitor.VisitBinary(BinaryExpression binaryExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateInternal(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.Translate(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateExpression(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateLambdaExpression(ShapedQueryExpression shapedQueryExpression, LambdaExpression lambdaExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateWhere(ShapedQueryExpression source, LambdaExpression predicate)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)
   at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1.GetAsyncEnumerator()
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
   at Meerkat.Application.Persistence.GenericRepository`1.GetPageAsync(Int32 pageNumber, Int32 pageSize, Expression`1 filter, Func`2 orderBy, String includeProperties) in C:\Azure DevOps\Meerkat Back-end\Meerkat.Service\Meerkat.Application\Persistence\GenericRepository.cs:line 100
   at Meerkat.Application.Facades.RealEstateFacade.GetPropertiesAsync(Int32 pageNumber, Int32 pageSize, SearchFilterModel filterModel, String includeProperties) in C:\Azure DevOps\Meerkat Back-end\Meerkat.Service\Meerkat.Application\Facades\RealEstateFacade.cs:line 126
   at Meerkat.Application.Facades.RealEstateFacade.GetPropertiesAsync(SearchFilterModel filterModel, String includeProperties, Int32 pageNumber, Int32 propertiesPerPage) in C:\Azure DevOps\Meerkat Back-end\Meerkat.Service\Meerkat.Application\Facades\RealEstateFacade.cs:line 41
   at Meerkat.WebService.Controllers.RealEstateController.GetProperties(String filter) in C:\Azure DevOps\Meerkat Back-end\Meerkat.Service\Meerkat.WebService\Controllers\RealEstateController.cs:line 34
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Logged|12_1(ControllerActionInvoker invoker)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeNextActionFilterAsync&gt;g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeInnerFilterAsync&gt;g__Awaited|13_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextResourceFilter&gt;g__Awaited|25_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResourceExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|20_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Logged|17_1(ResourceInvoker invoker)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Logged|17_1(ResourceInvoker invoker)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Localization.RequestLocalizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)
</code></pre>
<p>What I am missing?</p>
<p>Thanks for any help.</p>

## Answers
### Answer ID: 71721612
<p>LINQ <code>Expression</code>s are trees of objects, not collections of text to be compiled. While the parameters from the source function expressions may look the same on the outside they are in fact different objects that just happen to have the same properties. So when you combine two function expressions and throw out the parameter(s) from one of them you're left with an <code>Expression</code> that doesn't have all the information.</p>
<p>To make this more obvious, imagine you're adding <code>a =&gt; a.Name == &quot;test&quot;</code> to <code>b =&gt; b.Age &gt; 0</code>. Your code will produce a LINQ expression equivalent to <code>a =&gt; a.Name == &quot;test&quot; &amp;&amp; b.Age &gt; 0</code>... which leaves an unknown object <code>b</code> in the mix. Even if you changed the name in the source expression it would still be an unknown object.</p>
<p>Fortunately we can use an <code>ExpressionVisitor</code> to fix this up for us. Here's one I've used in similar situations:</p>
<pre><code>class ExpressionReplacer : ExpressionVisitor
{
    private readonly Expression From;
    private readonly Expression To;
    
    private ExpressionReplacer(Expression from, Expression to)
    {
        From = from;
        To = to;
    }
    
    public override Expression Visit(Expression node)
    {
        if (ReferenceEquals(node, From))
            return To;
        return base.Visit(node);
    }
    
    public static T Replace&lt;T&gt;(T target, Expression from, Expression to)
        where T : Expression
    {
        var replacer = new ExpressionReplacer(from, to);
        return (T)replacer.Visit(target);
    }
}
</code></pre>
<p>You can use that in your extension methods to change the body of one of the functions being combined to use the correct parameter instance like this:</p>
<pre><code>public static Expression&lt;Func&lt;T, bool&gt;&gt; And&lt;T&gt;(this Expression&lt;Func&lt;T, bool&gt;&gt; left, Expression&lt;Func&lt;T, bool&gt;&gt; right)
{
    if (left == null) return right;
    var right_body = ExpressionReplacer.Replace(right.Body, right.Parameters[0], left.Parameters[0]);
    var and = Expression.AndAlso(left.Body, right_body);
    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(and, left.Parameters[0]);
}
</code></pre>
<p>LINQ expressions are fun and interesting and you can do some very useful things with them, and expression visitors are all part of the fun.</p>

