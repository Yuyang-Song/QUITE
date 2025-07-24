# ASP.NET MVC Query with both CASE statement and SUM function
[Link to question](https://stackoverflow.com/questions/69814343/asp-net-mvc-query-with-both-case-statement-and-sum-function)
**Creation Date:** 1635872687
**Score:** 1
**Tags:** c#, sql, asp.net, asp.net-mvc-3, entity-framework-core
## Question Body
<p>I've found some solutions for this problem, but i don't know why it is not working...
I am using ASP.NET MVC</p>
<p>My database has 2 tables: <code>HealthRegister</code> &amp; <code>Member</code>.</p>
<p>Each HealthRegister has one Member and each Member has many Member.</p>
<pre class="lang-cs prettyprint-override"><code>public class HealthRegistration
    {
        [Key]
        public int HealthRegistrationID { get; set; }
        [ForeignKey(&quot;Member&quot;)]
        public string MemberRegistrationNumber { get; set; }
        [Display(Name = &quot;Data e hora do registro&quot;)]
        public DateTime RegisterDateTime { get; set; }
        [Display(Name = &quot;Está de sentindo bem?&quot;)]
        public bool HowRUFeeling { get; set; }
        [Display(Name = &quot;Falta de ar&quot;)]
        public bool FaltaDeAr { get; set; }
        [Display(Name = &quot;Cansaço&quot;)]
        public bool Cansaco { get; set; }
        [Display(Name = &quot;Febre&quot;)]
        public bool Febre { get; set; }
        [Display(Name = &quot;Calafrios&quot;)]
        public bool Calafrios { get; set; }
        [Display(Name = &quot;Tosse&quot;)]
        public bool Tosse { get; set; }
        [Display(Name = &quot;Dor de garganta&quot;)]
        public bool DorDeGarganta { get; set; }
        [Display(Name = &quot;Dor de cabeça&quot;)]
        public bool DorDeCabeca { get; set; }
        [Display(Name = &quot;Dor no peito&quot;)]
        public bool DorNoPeito { get; set; }
        [Display(Name = &quot;Perda de olfato&quot;)]
        public bool PerdaDeOlfato { get; set; }
        [Display(Name = &quot;Perda de paladar&quot;)]
        public bool PerdaPaladar { get; set; }
        [Display(Name = &quot;Diarreia&quot;)]
        public bool Diarreia { get; set; }
        [Display(Name = &quot;Coriza&quot;)]
        public bool Coriza { get; set; }
        [Display(Name = &quot;Espirros&quot;)]
        public bool Espirros { get; set; }
        public virtual Member Member { get; set; }
    }

public class Member
    {
        public enum Sectors
        {
            Administrador,
            Aluno,
            Professor,
            Funcionario            
        }

        [Key]
        [Display(Name = &quot;Número de matrícula&quot;)]
        public string MemberRegistrationNumber { get; set; }
        [Display(Name = &quot;Nome&quot;)]
        public string Name { get; set; }
        [Display(Name = &quot;Setor&quot;)]
        public Sectors Sector { get; set; }
        [Display(Name = &quot;Senha&quot;)]
        public string Password { get; set; }
        [Column(TypeName = &quot;Date&quot;)]
        [Display(Name = &quot;Data de nascimento&quot;)]
        [DisplayFormat(ApplyFormatInEditMode = true, DataFormatString = &quot;{0:d}&quot;)]
        [DataType(DataType.Date)]
        public DateTime BirthDate { get; set; }
        [Display(Name = &quot;Cidade&quot;)]
        public string City { get; set; }
        [Display(Name = &quot;Estado&quot;)]
        public string State { get; set; }
        [Display(Name = &quot;Administrador&quot;)]
        public bool Admin { get; set; }
        [Display(Name = &quot;Registros de saúde&quot;)]
        public virtual ICollection&lt;HealthRegistration&gt; HealthRegistrations { get; set; }
    }
</code></pre>
<p>I want to make the following SQL query in ASP.NET MVC:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT
    CONVERT(DATE, RegisterDateTime),
    SUM(CASE WHEN Sector = 0 THEN 1 ELSE 0 END),
    SUM(CASE WHEN Sector = 1 THEN 1 ELSE 0 END),
    SUM(CASE WHEN Sector = 2 THEN 1 ELSE 0 END),
    SUM(CASE WHEN Sector = 3 THEN 1 ELSE 0 END)
FROM
    [dbo].[HealthRegistration]
    INNER JOIN
    [dbo].[Member]
    ON [dbo].[Member].MemberRegistrationNumber = [dbo].[HealthRegistration].MemberRegistrationNumber
GROUP BY CONVERT(DATE, RegisterDateTime);
</code></pre>
<p>I have tried this solution with an error message:</p>
<pre class="lang-cs prettyprint-override"><code>var registerBySectorByDate = await _context.HealthRegistration
                .Include(m =&gt; m.Member)
                .Where(m =&gt; DateTime.Compare(m.RegisterDateTime, fromDate) &gt;= 0 &amp;&amp; DateTime.Compare(m.RegisterDateTime, toDate) &lt;= 0)
                .GroupBy(m =&gt; m.RegisterDateTime.Date)
                .Select(m =&gt; new
                {
                    Key = m.Key,
                    x = m.Sum(n =&gt; n.Member.Sector == Member.Sectors.Administrador ? 1 : 0)
}).ToListAsync();

</code></pre>
<p>Error message:</p>
<pre><code>fail: Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware[1]
      An unhandled exception has occurred while executing the request.
      System.InvalidOperationException: The LINQ expression 'GroupByShaperExpression:
      KeySelector: CONVERT(date, h.RegisterDateTime),
      ElementSelector:EntityShaperExpression:
          EntityType: HealthRegistration
          ValueBufferExpression:
              ProjectionBindingExpression: EmptyProjectionMember
          IsNullable: False

          .Sum(n =&gt; (int)n.Member.Sector == 0 ? 1 : 0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
         at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
         at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
         at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
         at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateInternal(Expression expression)
         at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.Translate(Expression expression)
         at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
         at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitNew(NewExpression newExpression)
         at System.Linq.Expressions.NewExpression.Accept(ExpressionVisitor visitor)
         at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
         at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
         at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
         at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
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
         at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)
         at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1.GetAsyncEnumerator()
         at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
         at ManagerCovid19.Controllers.HealthController.Filter(DateTime fromDate, DateTime toDate) in C:\Users\fekel\source\repos\ManagerCovid19\ManagerCovid19\Controllers\HealthController.cs:line 59
         at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Awaited|12_0(ControllerActionInvoker invoker, ValueTask`1 actionResultValueTask)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeNextActionFilterAsync&gt;g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
      --- End of stack trace from previous location ---
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextResourceFilter&gt;g__Awaited|24_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResourceExecutedContextSealed context)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.InvokeFilterPipelineAsync()
      --- End of stack trace from previous location ---
         at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
         at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
         at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
         at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext context)
         at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)
</code></pre>
<p>What am i doing wrong??</p>

## Answers
### Answer ID: 69814515
<p>I think this is related to the change in EF Core 3.x and above -&gt; <a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client</a></p>
<p>It cant translate the x = m.Sum(n =&gt; n.Member.Sector == Member.Sectors.Administrador ? 1 : 0) expression into SQL so its throwing an exception(as its expected too)</p>
<p>The documentation says to call AsEnumberable() or ToList() first, so that it can be called on the client side.</p>

