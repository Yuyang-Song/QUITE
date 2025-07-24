# How to solve StringComparison.OrdinalIgnoreCase and LINQ issue?
[Link to question](https://stackoverflow.com/questions/66781983/how-to-solve-stringcomparison-ordinalignorecase-and-linq-issue)
**Creation Date:** 1616592171
**Score:** 1
**Tags:** c#, linq-to-entities, string-comparison, postman-testcase, ignore-case
## Question Body
<p>Here's the code:
<strong>controller:</strong></p>
<pre><code>
        //POST api/substances
        [HttpPost]
        [ServiceFilter(typeof(ValidateNameExistsAttribute&lt;Substance&gt;))]
        public ActionResult&lt;SubstanceReadDto&gt; CreateSubstance([FromBody]SubstanceSaveDto dto)
        {
            var substanceModel = _mapper.Map&lt;Substance&gt;(dto);
            _repository.CreateSubstance(substanceModel);
            _repository.SaveChanges();

            var substanceReadDto = _mapper.Map&lt;SubstanceReadDto&gt;(substanceModel);

            return CreatedAtRoute(nameof(GetSubstanceById), new {substanceReadDto.Id}, substanceReadDto);
        }
</code></pre>
<p><strong>Filter</strong></p>
<pre><code>using System.Linq;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using Pharmacy.Data;
using Pharmacy.Models;

namespace Pharmacy.Filters
{
    public class ValidateNameExistsAttribute&lt;T&gt; : IActionFilter where T : class, INameEntity
    {
        private readonly PharmacyContext _context;

        public ValidateNameExistsAttribute(PharmacyContext context)
        {
            _context = context;
        }

        public void OnActionExecuted(ActionExecutedContext context)
        {
        }

        public void OnActionExecuting(ActionExecutingContext context)
        {
            if (context.ActionArguments.ContainsKey(&quot;dto&quot;))
            {
                var entity = new object();

                var dto = context.ActionArguments[&quot;dto&quot;] as INameDto;
                if (dto == null)
                {
                    context.Result = new BadRequestObjectResult(&quot;Invalid request body&quot;);
                    return;
                }

                if (context.ActionArguments.ContainsKey(&quot;id&quot;))
                {
                    var id = (int) context.ActionArguments[&quot;id&quot;];
                    entity = _context.Set&lt;T&gt;().SingleOrDefault(it =&gt; String.Equals(it.Name, dto.Name, StringComparison.OrdinalIgnoreCase) &amp;&amp; it.Id != id);
                }
                else
                {
                    entity = _context.Set&lt;T&gt;().SingleOrDefault(it =&gt; String.Equals(it.Name, dto.Name, StringComparison.OrdinalIgnoreCase));
                }

                if (entity != null)
                {
                    var problemDetails = new ProblemDetails
                    {
                        Title = &quot;Duplicate resource&quot;,
                        Detail = $&quot;A record with provided name {dto.Name} already exists&quot;,
                        Instance = context.HttpContext.Request.Path
                    };

                    context.Result = new ObjectResult(problemDetails)
                    {
                        StatusCode = 409
                    };
                }
            }
        }
    }
}
</code></pre>
<p>and here's the error message: What's wrong with code?</p>
<blockquote>
<p>{
&quot;type&quot;: &quot;https://tools.ietf.org/html/rfc7231#section-6.6.1&quot;,
&quot;title&quot;: &quot;The LINQ expression 'DbSet\r\n    .Where(s =&gt; string.Equals(\r\n        a: s.Name, \r\n        b: __dto_Name_0, \r\n        comparisonType: OrdinalIgnoreCase))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;,
&quot;status&quot;: 500,
&quot;detail&quot;: &quot;   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)\r\n   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)\r\n   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0<code>1.&lt;Execute&gt;b__0()\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func</code>1 compiler)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func<code>1 compiler)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)\r\n   at System.Linq.Queryable.SingleOrDefault[TSource](IQueryable</code>1 source, Expression<code>1 predicate)\r\n   at Pharmacy.Filters.ValidateNameExistsAttribute</code>1.OnActionExecuting(ActionExecutingContext context) in D:\.Pharmac Project\pharmac\Filters\ValidateNameExistsAttribute.cs:line 43\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeNextActionFilterAsync()\r\n--- End of stack trace from previous location where exception was thrown ---\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()\r\n--- End of stack trace from previous location where exception was thrown ---\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)\r\n   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)\r\n   at Microsoft.AspNetCore.Routing.EndpointMiddleware.g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)\r\n   at Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext httpContext)\r\n   at Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext httpContext, ISwaggerProvider swaggerProvider)\r\n   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)\r\n   at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext context)\r\n   at Serilog.AspNetCore.RequestLoggingMiddleware.Invoke(HttpContext httpContext)\r\n   at Microsoft.AspNetCore.Diagnostics.ExceptionHandlerMiddleware.g__Awaited|6_0(ExceptionHandlerMiddleware middleware, HttpContext context, Task task)&quot;,
&quot;traceId&quot;: &quot;|9542c43b-43548354a97cc054.&quot;
}</p>
</blockquote>

