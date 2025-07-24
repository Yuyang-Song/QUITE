# The LINQ expression DbSet&lt;&gt;.Any could not be translated
[Link to question](https://stackoverflow.com/questions/62304205/the-linq-expression-dbset-any-could-not-be-translated)
**Creation Date:** 1591793966
**Score:** 2
**Tags:** c#, asp.net-core, entity-framework-core, azure-cosmosdb
## Question Body
<p>I'm using ConsmoDB and Entity Framework Core 3.1.
Need to check if entity exists</p>

<pre><code>bool callExists = await _context.Calls
    .AsNoTracking()
    .AnyAsync(x =&gt; x.Number == request.Number &amp;&amp; x.CustomerId == request.CustomerId, cancellationToken);

if (callExists)
{
    throw new ConflictException($"Call already exists");
}
</code></pre>

<p>after run, got the following exception</p>

<blockquote>
  <p>System.InvalidOperationException: The LINQ expression 'DbSet
          .Any(c => c.Number == __request_Number_0 &amp;&amp; c.CustomerId  == __request_CustomerId_1)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation
  explicitly by inserting a call to either AsEnumerable(),
  AsAsyncEnumerable(), ToList(), or ToListAsync(). See
  <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.
         at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.g__CheckTranslated|8_0(ShapedQueryExpression
  translated, &lt;>c__DisplayClass8_0&amp; )
         at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression
  methodCallExpression)
         at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor
  visitor)
         at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
         at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression
  query)
         at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression
  query, Boolean async)
         at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase
  database, Expression query, IModel model, Boolean async)
         at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;>c__DisplayClass12_0<code>1.&lt;ExecuteAsync&gt;b__0()
         at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object
  cacheKey, Func</code>1 compiler)
         at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object
  cacheKey, Func<code>1 compiler)
         at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression
  query, CancellationToken cancellationToken)
         at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression
  expression, CancellationToken cancellationToken)
         at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo
  operatorMethodInfo, IQueryable</code>1 source, Expression expression,
  CancellationToken cancellationToken)
         at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo
  operatorMethodInfo, IQueryable<code>1 source, LambdaExpression expression,
  CancellationToken cancellationToken)
         at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.AnyAsync[TSource](IQueryable</code>1
  source, Expression<code>1 predicate, CancellationToken cancellationToken)
         at Call.Api.Handlers.CreateCallCommandHandler.Handle(CreateCallMappingCommand
  request, CancellationToken cancellationToken) in
  D:\Call.Api\Handlers\CreateCallCommandHandler.cs:line 40
         at MediatR.Pipeline.RequestExceptionProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at MediatR.Pipeline.RequestExceptionProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at MediatR.Pipeline.RequestExceptionActionProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at MediatR.Pipeline.RequestExceptionActionProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at MediatR.Pipeline.RequestPostProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at MediatR.Pipeline.RequestPreProcessorBehavior</code>2.Handle(TRequest
  request, CancellationToken cancellationToken, RequestHandlerDelegate<code>1
  next)
         at Call.Api.Controllers.CallsController.Create(CreateCallMappingCommand
  createCallMappingCommand) in
  D:\Call.Api\Controllers\CallsController.cs:line 52
         at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper
  mapper, ObjectMethodExecutor executor, Object controller, Object[]
  arguments)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Awaited|12_0(ControllerActionInvoker
  invoker, ValueTask</code>1 actionResultValueTask)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.g__Awaited|10_0(ControllerActionInvoker
  invoker, Task lastTask, State next, Scope scope, Object state, Boolean
  isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed
  context)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp;
  next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
      --- End of stack trace from previous location where exception was thrown ---
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|19_0(ResourceInvoker
  invoker, Task lastTask, State next, Scope scope, Object state, Boolean
  isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|17_0(ResourceInvoker
  invoker, Task task, IDisposable scope)
         at Microsoft.AspNetCore.Routing.EndpointMiddleware.g__AwaitRequestTask|6_0(Endpoint
  endpoint, Task requestTask, ILogger logger)
         at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext
  context)
         at Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext
  httpContext)
         at Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext
  httpContext, ISwaggerProvider swaggerProvider)
         at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext
  context)</p>
</blockquote>

<p>Model Call
public class Call</p>

<pre><code>{
    public Guid CallId { get; set; }

    public string Number { get; set; }

    public int CustomerId { get; set; }

    public Type Type { get; set; }
}
</code></pre>

<p>Request is the same (only without CallId)</p>

## Answers
### Answer ID: 67498754
<p><code>.AnyAsync</code> is not supported.  As an alternative you can use <code>.CountAsync()</code> and check for <code>count &gt; 0</code>;</p>
<p>It boggles the mind that the team would implement <code>.CountAsync</code> and not <code>.AnyAsync</code>.</p>

