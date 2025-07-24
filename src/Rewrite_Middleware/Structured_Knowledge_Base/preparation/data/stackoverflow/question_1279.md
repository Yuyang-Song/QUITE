# .Net Core API Microsoft.AspNet.Identity.Core
[Link to question](https://stackoverflow.com/questions/68004804/net-core-api-microsoft-aspnet-identity-core)
**Creation Date:** 1623854085
**Score:** 1
**Tags:** c#, asp.net, api, asp.net-core
## Question Body
<p><strong>My question.</strong></p>
<p>So my question is how do I connect a .Net Core API using Microsoft.AspNetCore.Identity  to an identity (AspNetUser) table created using .Net 4.5 and Microsoft.AspNet.Identity.Core</p>
<p><strong>The Details.</strong></p>
<p>I have a MVC web application that allows user to register an login, and view certain information based on there credentials. This was written in .Net4.5. and I'm assuming using Microsoft.AspNet.Identity.Core. (Which I think is the non .NET core version. ITs not the best naming convention) This project cant be changed.</p>
<p>I'm trying to extend some of the features such as login and register to use an API. I'm trying to build the API in .Net Core and Microsoft.AspNetCore.Identity;</p>
<p>I have created a simple test login controller.</p>
<pre><code>    [ApiController]
    public class AuthController : ControllerBase
    {

        private readonly UserManager&lt;IdentityUser&gt; _userManager;
        private readonly SignInManager&lt;IdentityUser&gt; _signInManager;
        private readonly IConfiguration _config;
        public AuthController(UserManager&lt;IdentityUser&gt; userManager,
                              SignInManager&lt;IdentityUser&gt; signInManager,
                                 IConfiguration config)
        {
            _userManager = userManager;
            _signInManager = signInManager;
            _config = config; ;
        }

 

      
        [HttpPost]
        [AllowAnonymous]
        public async Task&lt;IActionResult&gt; Login(LoginDto user)
        {
            if (ModelState.IsValid)
            {
                var testResult = await _signInManager.PasswordSignInAsync(user.Username, user.Password, false, false);
                return Ok(testResult);
            }
            return BadRequest();
        }
    }
</code></pre>
<p>Originally I was getting invalid column errors, as it seems that the AspNetUsers table is now created with additional fields compared with the AspNetUsers table created by the .NET4.5 system.</p>
<p>I got round this issue by ignoring them in the ModelBuilderof the dbcontext class</p>
<pre><code>    {

        public AuthConext(DbContextOptions&lt;AuthConext&gt; options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);


            modelBuilder.Entity&lt;IdentityUser&gt;().Ignore(c =&gt; c.PhoneNumberConfirmed)
                                             .Ignore(c =&gt; c.TwoFactorEnabled)
                                             .Ignore(c =&gt; c.SecurityStamp)
                                             .Ignore(c =&gt; c.LockoutEnabled)
                                             .Ignore(c =&gt; c.NormalizedEmail)
                                             .Ignore(c =&gt; c.NormalizedUserName)
                                             .Ignore(c =&gt; c.ConcurrencyStamp)
                                             .Ignore(c =&gt; c.LockoutEnd);
        }
    }
</code></pre>
<p>However I'm not getting errors regarding the LINQ query.</p>
<pre><code>    .Where(i =&gt; i.NormalizedUserName == __normalizedUserName_0)' could not be translated. Additional information: Translation of member 'NormalizedUserName' on entity type 'IdentityUser' failed. This commonly occurs when the specified member is unmapped. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|15_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass15_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, LambdaExpression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.FirstOrDefaultAsync[TSource](IQueryable`1 source, Expression`1 predicate, CancellationToken cancellationToken)
   at Microsoft.AspNetCore.Identity.EntityFrameworkCore.UserStore`9.FindByNameAsync(String normalizedUserName, CancellationToken cancellationToken)
   at Microsoft.AspNetCore.Identity.UserManager`1.FindByNameAsync(String userName)
   at MyFirstChoice_Api_CORE.Controllers.AuthController.Login(LoginDto user) in C:\Repos\MyFirstChoice_Api_CORE\MyFirstChoice_Api_CORE\Controllers\AuthController.cs:line 43
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Awaited|12_0(ControllerActionInvoker invoker, ValueTask`1 actionResultValueTask)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeNextActionFilterAsync&gt;g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext httpContext)
   at Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext httpContext, ISwaggerProvider swaggerProvider)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)
</code></pre>
<p>While it does suggest a solution. I'm not sure where to make that change as I'm not creating a query myself just simply calling _signInManager.PasswordSignInAsync.</p>
<p>So my question is how to I connect and .Net Core API using Microsoft.AspNetCore.Identity  to and identity table created using .net 4.5 and Microsoft.AspNet.Identity.Core</p>

## Answers
### Answer ID: 68014339
<p>Microsoft.AspNetCore.Identity and Microsoft.AspNet.Identity.Core seem to not have a lot in common</p>
<p><a href="https://stackoverflow.com/questions/41140952/what-is-the-difference-between-microsoft-aspnet-identity-core-and-microsoft-aspn/41141049">What is the difference between Microsoft.AspNet.Identity.Core and Microsoft.AspNetCore.Identity?</a></p>
<p>However Microsoft.AspNetCore.Identity is a .net standard library so it should be compatible with .net core / 5 apps</p>
<p>So you should just try to use it in your web api</p>
<p><a href="https://www.c-sharpcorner.com/article/authentication-and-authorization-in-asp-net-core-web-api-with-json-web-tokens/" rel="nofollow noreferrer">https://www.c-sharpcorner.com/article/authentication-and-authorization-in-asp-net-core-web-api-with-json-web-tokens/</a></p>

