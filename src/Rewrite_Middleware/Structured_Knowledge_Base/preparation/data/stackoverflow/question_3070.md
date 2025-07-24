# EF Core throw exception when using EF.Functions.Like on array type
[Link to question](https://stackoverflow.com/questions/65061446/ef-core-throw-exception-when-using-ef-functions-like-on-array-type)
**Creation Date:** 1606661646
**Score:** 1
**Tags:** postgresql, asp.net-core, entity-framework-core
## Question Body
<p>By following the document from <a href="https://www.npgsql.org/efcore/mapping/array.html" rel="nofollow noreferrer">Array Type Mapping</a>, I should able to search the string inside the array but that's not happen. Here my code snippet</p>
<pre class="lang-cs prettyprint-override"><code>getFiles = await _context.Files.Include(r =&gt; r.Box)
                        .Where(r =&gt; r.Box.AccountId == accountId &amp;&amp; r.SealCodes.Any(s =&gt; EF.Functions.Like(searchFile, s)))
                        .OrderByDescending(c =&gt; c.CreatedOn)
                        .ToListAsync();
</code></pre>
<p>Here the exception message which I not really clear what happen</p>
<pre><code>Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware
An unhandled exception has occurred while executing the request.
System.InvalidOperationException: The LINQ expression 'DbSet&lt;FileBox&gt;
    .Where(f =&gt; f.SealCodes
        .Any(s =&gt; __Functions_0
            .Like(
                _: __searchFile_1,
                matchExpression: s)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at Subalipack.Fms.V2.WebAdmin.Controllers.FileController.LoadTable(FileParametersDto dtParameters, String From, String To) in C:\Users\user\Documents\Project\Subalipack\FMS\Source Code\Subalipack.Fms.V2.WebAdmin\Controllers\FileController.cs:line 101
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Awaited|12_0(ControllerActionInvoker invoker, ValueTask`1 actionResultValueTask)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeNextActionFilterAsync&gt;g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeInnerFilterAsync&gt;g__Awaited|13_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextResourceFilter&gt;g__Awaited|24_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResourceExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)
</code></pre>
<p>Using asp.net core 3.1 and <code>Npgsql.EntityFrameworkCore.PostgreSQL</code> version 3.1.4</p>
<p>Any idea?</p>

## Answers
### Answer ID: 65078319
<p>This exception happens because in .NetCore 3.1 you can't call LINQ that is unable to be converted to SQL unless you have called ToList() before that part of your LINQ expression. So you could do something like:</p>
<pre><code>getFiles = await _context.Files.Include(r =&gt; r.Box)
                        .ToListAsync()
                        .Where(r =&gt; r.Box.AccountId == accountId &amp;&amp; r.SealCodes.Any(s =&gt; EF.Functions.Like(searchFile, s)))
                        .OrderByDescending(c =&gt; c.CreatedOn)
                        .ToListAsync();

</code></pre>
<p>Now everything will be evaluated in memory which is slower especialy on large data sets, so If you perhaps explained what do you want to acomplish somebody will give you more optimized solution. Also I would urge you to keep List and not change it to string[] since string[] doesn't have many features that List has.</p>

### Answer ID: 65061900
<p>I just change from <code>List&lt;string&gt;</code> to <code>string[]</code> on data model then problem gone.</p>

