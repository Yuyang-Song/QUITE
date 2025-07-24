# Difficult Linq expression throws translation error
[Link to question](https://stackoverflow.com/questions/70001648/difficult-linq-expression-throws-translation-error)
**Creation Date:** 1637140561
**Score:** 0
**Tags:** .net, linq
## Question Body
<p>im actually dont know how i should fix my following problem. Before i show you my code, i will explain the situation. So there comes a list of strings from my frontend, which needs to be compared with items of my database. The goal is to filter with my frontend list, so there are only results on my Website with the selected elements. I created already multiple expressions but none of these could be translated.</p>
<p>Here is the problem:</p>
<pre class="lang-cs prettyprint-override"><code>.Where(p =&gt; user.personenTypFilter.Any(i =&gt; 
    p.Personentypzuordnungens.ToList().Any(u =&gt; u.Personentyp.Bezeichnung == i)))
</code></pre>
<p>So personenTypFilter is my List from my Frontend. Personentypzuordnungens is a table of my Database which collect the strings of the persontyp through a Foreign key(u.personentyp.bezeichnung). My Idea is going through the personenTypFilter with Any and compare with another Any in the Database.</p>
<p>I get no results and only a translation error:</p>
<pre><code>&quot;System.InvalidOperationException: The LINQ expression 'DbSet&lt;Personen&gt;()
    .Where(p =&gt; p.Vorname.ToLower().Contains(__user_vorname_0))
    .Where(p =&gt; p.Nachname.ToLower().Contains(__user_nachname_1))
    .Where(p =&gt; p.Anrede.ToLower().Contains(__user_anrede_2))
    .Where(p =&gt; p.Ort.ToLower().Contains(__user_adresse_3) || p.Plz.Contains(__user_adresse_3) || p.Land.Contains(__user_adresse_3) || p.Bundesland.Contains(__user_adresse_3) || p.Straße.Contains(__user_adresse_3))
    .Where(p =&gt; p.Firmenbezeichnung.ToLower().Contains(__user_firmenbezeichnung_4))
    .Where(p =&gt; __user_personenTypFilter_5
        .Any(i =&gt; DbSet&lt;Personentypzuordnungen&gt;()
            .Where(p0 =&gt; EF.Property&lt;Nullable&lt;Guid&gt;&gt;(p, &quot;PersonId&quot;) != null &amp;&amp; object.Equals(
                objA: (object)EF.Property&lt;Nullable&lt;Guid&gt;&gt;(p, &quot;PersonId&quot;), 
                objB: (object)EF.Property&lt;Nullable&lt;Guid&gt;&gt;(p0, &quot;PersonId&quot;)))
            .Join(
                inner: DbSet&lt;Personentypen&gt;(), 
                outerKeySelector: p0 =&gt; EF.Property&lt;Nullable&lt;Guid&gt;&gt;(p0, &quot;PersonentypId&quot;), 
                innerKeySelector: p1 =&gt; EF.Property&lt;Nullable&lt;Guid&gt;&gt;(p1, &quot;PersonentypId&quot;), 
                resultSelector: (o, i) =&gt; new TransparentIdentifier&lt;Personentypzuordnungen, Personentypen&gt;(
                    Outer = o, 
                    Inner = i
                ))
            .Any(p0 =&gt; p0.Inner.Bezeichnung == i)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|15_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass15_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
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
   at DadaAPI.Controllers.PersonensController.Filter(Filter user) in C:\Users\Dada\source\repos\DadaAPI\DadaAPI\Controllers\Personen\PersonensController.cs:line 125
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
   at Swashbuckle.AspNetCore.SwaggerUI.SwaggerUIMiddleware.Invoke(HttpContext httpContext)
   at Swashbuckle.AspNetCore.Swagger.SwaggerMiddleware.Invoke(HttpContext httpContext, ISwaggerProvider swaggerProvider)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)

HEADERS
=======
Cache-Control: no-cache
Connection: keep-alive
Pragma: no-cache
Content-Type: application/json
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhM2YzZDA3NS0xODQ1LTQwNzEtYTU4ZS1mMGM5Yzc4MTJhNTAifQ.NaPhXxgCCy7r9mUFZ54DC4DIMwe21GNnO3-8GFdtPWQ
Host: localhost:5000
Referer: http://localhost:4200/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36
Origin: http://localhost:4200
Content-Length: 576
sec-ch-ua: &quot;Google Chrome&quot;;v=&quot;95&quot;, &quot;Chromium&quot;;v=&quot;95&quot;, &quot;;Not A Brand&quot;;v=&quot;99&quot;
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: &quot;Windows&quot;
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
&quot;
</code></pre>
<p>Full Query:</p>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IActionResult&gt; Filter([FromBody] Filter user)
{
    //Variable für Personentypen als Liste machen
    return Ok(await _context
        .Personens
        //Obere Felder (nicht erweitert)
        .Where(p =&gt; p.Vorname.ToLower().Contains(user.vorname))
        .Where(p =&gt; p.Nachname.ToLower().Contains(user.nachname))
        .Where(p =&gt; p.Anrede.ToLower().Contains(user.anrede))
        .Where(p =&gt; p.Ort.ToLower().Contains(user.adresse) || p.Plz.Contains(user.adresse) || p.Land.Contains(user.adresse) || p.Bundesland.Contains(user.adresse) || p.Straße.Contains(user.adresse))
        .Where(p =&gt; p.Firmenbezeichnung.ToLower().Contains(user.firmenbezeichnung))
        .Where(p =&gt; user.personenTypFilter.Any(i =&gt; p.Personentypzuordnungens.ToList().Any(u =&gt; u.Personentyp.Bezeichnung == i)))
        .Where(p =&gt; p.ArbeitgeberPersonIdTNavigation.Ort.ToLower().Contains(user.arbeitgeberOrt) || p.ArbeitgeberPersonIdTNavigation.Plz.ToLower().Contains(user.arbeitgeberOrt)
                    || p.ArbeitgeberPersonIdTNavigation.Straße.ToLower().Contains(user.arbeitgeberOrt) || p.ArbeitgeberPersonIdTNavigation.Land.ToLower().Contains(user.arbeitgeberOrt) || p.ArbeitgeberPersonIdTNavigation.Bundesland.ToLower().Contains(user.arbeitgeberOrt))
        .Select(p =&gt; new
        {
            personId = p.PersonId,
            nachname = p.Nachname,
            vorname = p.Vorname,
            plz = p.Plz,
            firmBez = p.Firmenbezeichnung,
            ort = p.Ort,
            personentyp = p.Personentypzuordnungens.Select(i =&gt; new
            {
                personentypId = i.PersonentypId,
            }),
            aktuellePosition = p.AktuellePosition,
            taetigkeit = p.Tätigkeit,
            kernkompetenzen = p.Kernkompetenzen,
            datenReviewedZeitpunkt = p.DatenReviewedZeitpunkt,
        }).ToListAsync());
}
</code></pre>

