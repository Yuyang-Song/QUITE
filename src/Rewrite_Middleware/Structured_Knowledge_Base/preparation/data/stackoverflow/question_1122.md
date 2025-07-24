# Extending DbFunctions in Entity Framework Core?
[Link to question](https://stackoverflow.com/questions/60049369/extending-dbfunctions-in-entity-framework-core)
**Creation Date:** 1580779738
**Score:** 0
**Tags:** c#, .net, linq, asp.net-core, entity-framework-core
## Question Body
<p>With .NET Core 3.1.1 and Entity Framework Core 3.1.1, I have:</p>

<pre class="lang-cs prettyprint-override"><code>var query = from user in context.Users
            join userRole in userRoleView on user.Id equals userRole.UserId into gj
            from p in gj.DefaultIfEmpty()
            select new
                   {
                        user.Id,
                        user.UserName,
                        RoleName = p.Rolename,
                        user.CreatedUtc,
                        user.ModifiedUtc,
                  };

if (!String.IsNullOrWhiteSpace(conditions.Keyword))
{
    query = query.Where(d =&gt; EF.Functions.Like(d.UserName, "%" + conditions.Keyword + "%"));
}
</code></pre>

<p>This is working well, and then I would like to have <code>EF.Functions.Contains(d.UserName, conditions.Keyword)</code>, so I wrote an extension:</p>

<pre class="lang-cs prettyprint-override"><code>public static class DbFunctionsExtensions
{
    public static bool Contains(this DbFunctions _, string matchExpression, string keyword)
    {
        return _.Like(matchExpression, "%" + keyword + "%");
    }
}
</code></pre>

<p>However, when running </p>

<pre><code>query.Where(d =&gt; EF.Functions.Contains(d.UserName, conditions.Keyword))
</code></pre>

<p>I get this exception:</p>

<blockquote>
  <p>System.InvalidOperationException
  ... could not be translated. </p>
  
  <p>Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either <code>AsEnumerable()</code>, <code>AsAsyncEnumerable()</code>, <code>ToList()</code>, or <code>ToListAsync()</code>. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
  
  <p>Source=Microsoft.EntityFrameworkCore  </p>
  
  <p>StackTrace:
  at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;>c__DisplayClass8_0&amp; )<br>
  at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)<br>
  at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)<br>
  at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)<br>
  at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)<br>
  at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)<br>
  at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
     at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
     at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
     at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
     at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
     at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
     at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
     at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;>c__DisplayClass9_0<code>1.&lt;Execute&gt;b__0()
     at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func</code>1 compiler)
     at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func<code>1 compiler)
     at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
     at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
     at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable</code>1.GetEnumerator()
     at System.Collections.Generic.LargeArrayBuilder<code>1.AddRange(IEnumerable</code>1 items)
     at System.Collections.Generic.EnumerableHelpers.ToArray[T](IEnumerable<code>1 source)
     at System.Linq.Enumerable.ToArray[TSource](IEnumerable</code>1 source)
     at APS.WebPos.DAL.SearchOperations.GetActivePeopleByKeyword(String keyword) in C:\VSProjects\ApsCloudTrunk\APS.WebPos.DALCore\SearchOperations.cs:line 96
     at APS.WebPos.WebApi.Controllers.SearchController.GetActivePeopleByKeyword(String keyword) in C:\VSProjects\ApsCloudTrunk\APS.WebPos.WebApiCore\Controllers\SearchController.cs:line 25
     at Microsoft.Extensions.Internal.ObjectMethodExecutor.Execute(Object target, Object[] parameters)
     at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.SyncObjectResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
     at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeActionMethodAsync()
     at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
     at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeNextActionFilterAsync()</p>
</blockquote>

<p>Is it possible to extend DbFunctions in application with Entity Framework Core, and use it in LINQ? How?</p>

<p>Remarks:</p>

<p><code>String.Contains()</code> is case sensitive in EF Core query, though it is case insensitive in EF being translated into LIKE in SQL.</p>

## Answers
### Answer ID: 60096651
<p>The parameter of the <code>Where</code> method is an <code>Expression</code> and its body is irrelevant when the query is being translated into SQL. That is why you are getting an exception.</p>

<p>To make it work you need to construct an Expression dynamically.</p>

<pre class="lang-cs prettyprint-override"><code>public static Expression&lt;Func&lt;T, bool&gt;&gt; Like&lt;T&gt;(Expression&lt;Func&lt;T, string&gt;&gt; prop, string keyword)
{
    var concatMethod = typeof(string).GetMethod(nameof(string.Concat), new[] { typeof(string), typeof(string) });
    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(
        Expression.Call(
            typeof(DbFunctionsExtensions),
            nameof(DbFunctionsExtensions.Like),
            null,
            Expression.Constant(EF.Functions),
            prop.Body,
            Expression.Add(
                Expression.Add(
                    Expression.Constant("%"),
                    Expression.Constant(keyword),
                    concatMethod),
                Expression.Constant("%"),
                concatMethod)),
        prop.Parameters);
}
</code></pre>

<p>And then use it in your query</p>

<pre class="lang-cs prettyprint-override"><code>if (!String.IsNullOrWhiteSpace(conditions.Keyword))
{
    query = query.Where(Like&lt;User&gt;(d =&gt; d.UserName, conditions.Keyword));
}
</code></pre>

<p>P.S. The way the question is titled looks close to what <a href="http://anthonygiretti.com/2018/01/11/entity-framework-core-2-scalar-function-mapping/" rel="nofollow noreferrer">Scalar function mapping</a> is, but its not applicable in the case of LIKE clause.</p>

### Answer ID: 60049555
<p>You can use simple one -> context.Users.Where(x => (conditions.Keyword == null || x.UserName.Contains(conditions.Keyword))). If conditions.Keyword is null, it skips filter.</p>

<pre><code>var query = from user in context.Users.Where(x =&gt; (conditions.Keyword == null || x.UserName.Contains(conditions.Keyword)))
                        join userRole in userRoleView
                        on user.Id equals userRole.UserId into gj
                        from p in gj.DefaultIfEmpty()
                        select new
                        {
                            user.Id,
                            user.UserName,
                            RoleName = p.Rolename,
                            user.CreatedUtc,
                            user.ModifiedUtc,
                        };
</code></pre>

