# Core 3.x LINQ -&gt; DateTime and string comparison error
[Link to question](https://stackoverflow.com/questions/67415029/core-3-x-linq-datetime-and-string-comparison-error)
**Creation Date:** 1620291958
**Score:** 0
**Tags:** c#, linq
## Question Body
<p>I wrote the code as below.</p>
<pre><code>purchaseList = (from tp in context.TbPurchasebill
                            where
                              tp.CompanyNo == companyNo &amp;&amp;
                              tp.BillDate.ToString(&quot;yyyy-MM&quot;).Contains(billDate) &amp;&amp;
                              tp.DeleteTf == false
                            orderby
                              tp.BusinessName
                            select new PurchaseList
                            {
                                BillNo = tp.BillNo,
                                BillDate = tp.BillDate,
                                BusinessName = tp.BusinessName,
                                GoodsName = tp.GoodsName
                            }).ToList();
</code></pre>
<p>tp.BillDate.ToString(&quot;yyyy-MM&quot;).In Contents (billDate), BillDate is in DateTime format and billDate is a string of values &quot;2021-05&quot;.</p>
<p>Executing the code will cause the following error:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression
'DbSet
.Where(t =&gt; t.CompanyNo == __companyNo_0 &amp;&amp; (Nullable)t.BillDate != null &amp;&amp;
t.BillDate.ToString(&quot;yyyy-MM&quot;).Contains(__billDate_1) &amp;&amp; t.DeleteTf ==
(Nullable)False)' could not be translated. Either rewrite the
query in a form that can be translated, or switch to client evaluation
explicitly by inserting a call to either AsEnumerable(),
AsAsyncEnumerable(), ToList(), or ToListAsync(). See
<a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.
at
Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.g__CheckTranslated|8_0(ShapedQueryExpression
translated, &lt;&gt;c__DisplayClass8_0&amp; )    at
Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor
visitor)    at
System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at
Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor
visitor)    at
System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at
Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
methodCallExpression)    at
System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor
visitor)    at
System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at
Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression
query)    at
Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression
query, Boolean async)    at
Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase
database, Expression query, IModel model, Boolean async)    at
Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0<code>1.&lt;Execute&gt;b__0() at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func</code>1 compiler)    at
Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object
cacheKey, Func<code>1 compiler)    at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)    at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)    at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable</code>1.GetEnumerator()
at System.Collections.Generic.List<code>1..ctor(IEnumerable</code>1 collection)<br />
at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)    at
AccountManagerData.Repository.GetPurchaseList(Int32 companyNo, String
billDate) in
C:\Users\Administrator\source\repos\AccountManager\AccountManagerData\Repository.cs:line
3573    at
AccountManager.Controllers.Bill.PurchaseController.GetPurchaseList(PurchaseForListFind
purchase) in
C:\Users\Administrator\source\repos\AccountManager\AccountManager\Controllers\Bill\PurchaseController.cs:line
30    at lambda_method(Closure , Object , Object[] )    at
Microsoft.Extensions.Internal.ObjectMethodExecutor.Execute(Object
target, Object[] parameters)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.SyncActionResultExecutor.Execute(IActionResultTypeMapper
mapper, ObjectMethodExecutor executor, Object controller, Object[]
arguments)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeActionMethodAsync()
at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp;
next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeNextActionFilterAsync()
--- End of stack trace from previous location where exception was thrown ---    at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed
context)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp;
next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
--- End of stack trace from previous location where exception was thrown ---    at
Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|19_0(ResourceInvoker
invoker, Task lastTask, State next, Scope scope, Object state, Boolean
isCompleted)    at
Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|17_0(ResourceInvoker
invoker, Task task, IDisposable scope)    at
Microsoft.AspNetCore.Routing.EndpointMiddleware.g__AwaitRequestTask|6_0(Endpoint
endpoint, Task requestTask, ILogger logger)    at
Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext
context)    at
Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext
context)    at
Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext
httpContext)    at
Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext
httpContext, ISwaggerProvider swaggerProvider)    at
Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext
context)</p>
<hr />
<p>To fix the error, you can run 'AsEnumerable()' at the end and call
'Where' one more time.</p>
</blockquote>
<p>Is there any other way but to do this?</p>

## Answers
### Answer ID: 67427773
<p>I don't think there's much to solve.</p>
<p>I just decided to do the following.</p>
<p>int year = billDate.split('-')[0];
int month = billDate.split('-')[1];</p>
<p>tp.BillDate.Year == year &amp;&amp; tp.BillDate.Month == month;</p>

### Answer ID: 67417791
<p>I think you have to replace</p>
<pre><code>tp.BillDate.ToString(&quot;yyyy-MM&quot;).Contains(billDate) &amp;&amp;
</code></pre>
<p>with</p>
<pre><code>tp.BillDate.ToString(&quot;yyyy-MM&quot;) == billDate &amp;&amp;
</code></pre>

