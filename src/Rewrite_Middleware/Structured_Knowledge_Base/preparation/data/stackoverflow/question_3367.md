# &quot;The LINQ expression could not be translated&quot; when accessing the value of the property of an entity dynamically
[Link to question](https://stackoverflow.com/questions/77601031/the-linq-expression-could-not-be-translated-when-accessing-the-value-of-the-pr)
**Creation Date:** 1701707193
**Score:** 0
**Tags:** c#, entity-framework-core
## Question Body
<p>I am writing a class to access an Entity framework DbSet.</p>
<p>I am having troubles with a FetchMany method.</p>
<p>I am using inheritance and I need to get the value of the Identifier of the table by using a method, as each class has a different Identifier name and need to access in a generic way.</p>
<p>I have read several threads about this error message, but I haven't been able to find any with something similar to this issue, having to access a property of the entity dynamically.</p>
<p>Here is a simplified version of my code:</p>
<pre><code>public class Test {
    public DbSet&lt;MyClass&gt; DbSet =&gt; GetDbSet(Context);

    protected Expression&lt;Func&lt;MyClass, string&gt;&gt; GetIdExpression() =&gt;
        return entity =&gt; entity.Id;
        
    protected Expression&lt;Func&lt;MyClass, bool&gt;&gt; CheckIds(List&lt;string&gt; ids) {
        var idExpression = GetIdExpression();
        return entity =&gt; ids.Contains(idExpression.Compile()(entity));
    }

    public IEnumerable&lt;MyClass&gt; FetchMany(List&lt;string&gt; ids) {
        var query = DbSet.Where(CheckIds(ids));
        return query.AsEnumerable();
    }
}
</code></pre>
<p>Then I call it like this:</p>
<pre><code>List&lt;MyClass&gt; entities = Test.FetchMany(ids).ToList();
</code></pre>
<p>I get this exception:</p>
<pre><code>System.InvalidOperationException: The LINQ expression  could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|15_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass15_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at TestApi.Test.FetchMany(List`1 ids)
   at TestApi.Controllers.MyController.FetchManyTest(List`1 ids)
   at lambda_method143(Closure , Object , Object[] )
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.SyncObjectResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeActionMethodAsync()
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeNextActionFilterAsync()
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextExceptionFilterAsync&gt;g__Awaited|25_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
</code></pre>
<p>What am I doing wrong? I thought that using a method returning an expresion like the <code>GetIdExpression()</code> method in the example would fix the problem.</p>
<p>Maybe it is related to my Entity framework version?
I am using Entity framework core 5.0.7</p>
<p>Thank you for your time.</p>
<p><strong>EDIT</strong>:
Thank you all for your help.</p>
<p>Finally I have managed to achieve it by modifying the <code>CheckIds()</code> method using code from the link suggested as duplicate:
<a href="https://stackoverflow.com/questions/19433316/combine-two-linq-lambda-expressions">Combine two Linq lambda expressions</a></p>
<p>The code of the method now is:</p>
<pre><code>protected Expression&lt;Func&lt;MyClass, bool&gt;&gt; CheckIds(List&lt;string&gt; ids) {
    Expression&lt;Func&lt;string, bool&gt;&gt; mainExpression = id =&gt; ids.Contains(id);
    Expression&lt;Func&lt;MyClass, string&gt;&gt; idExpression = GetIdExpression();

    ParameterExpression param = Expression.Parameter(typeof(MyClass), &quot;param&quot;);
    InvocationExpression body = Expression.Invoke(mainExpression, Expression.Invoke(idExpression, param));

    return Expression.Lambda&lt;Func&lt;MyClass, bool&gt;&gt;(body, param);
}
</code></pre>

