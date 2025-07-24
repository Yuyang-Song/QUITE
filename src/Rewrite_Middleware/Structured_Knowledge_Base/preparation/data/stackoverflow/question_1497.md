# How to replace a where condition by another in Hot Chocolate?
[Link to question](https://stackoverflow.com/questions/78976369/how-to-replace-a-where-condition-by-another-in-hot-chocolate)
**Creation Date:** 1726111816
**Score:** -1
**Tags:** c#, hotchocolate
## Question Body
<p>I'm using <a href="https://chillicream.com/docs/hotchocolate/v13" rel="nofollow noreferrer">Hot Chocolate</a> to query peoples:</p>
<pre class="lang-cs prettyprint-override"><code>using Microsoft.EntityFrameworkCore;

namespace SageApi.Model.Sage;

public partial class People
{
    public string Id { get; set; } = null!;

    public int? Age { get; set; }

    public string? Name { get; set; }


    public static void ConfigureModelBuilder(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity&lt;People&gt;(entity =&gt;
        {
            entity.HasIndex(e =&gt; e.Id, &quot;UKA_PEOPLE_Id&quot;).IsUnique();
            entity.Property(e =&gt; e.Age).HasColumnName(&quot;Age&quot;);
            entity.Property(e =&gt; e.Name).HasColumnName(&quot;Name&quot;);
        });
    }
}
</code></pre>
<h3>What I want to do ?</h3>
<p>I want the people who use my API to be able to query the peoples who are over 21 years old without having to specify the age 21 (this is a simplify example of what I want to do, to keep it simple).</p>
<p>Something like:</p>
<pre><code>{
    peoples(where: { aboveAge: { eq: true } }) {
        items {
            id
            age
            name
        }
    }
}
</code></pre>
<h3>What I tried</h3>
<p>So I added a field <code>AboveAge</code> in <code>People</code> like so (this way I can query this field even if this field doesn't exists in the bdd):</p>
<pre><code>using System.ComponentModel.DataAnnotations.Schema;
    // ...
    public string? Name { get; set; }
    
    [IsProjected(false)] [NotMapped] public virtual bool? AboveAge { get; set; }

    public static void ConfigureModelBuilder(ModelBuilder modelBuilder)
    // ...
</code></pre>
<p>In my <code>Query.cs</code>, I use <a href="https://chillicream.com/docs/hotchocolate/v13/fetching-data/pagination#definition-1" rel="nofollow noreferrer"><code>UseOffsetPaging</code></a>, <a href="https://chillicream.com/docs/hotchocolate/v13/fetching-data/projections" rel="nofollow noreferrer"><code>UseProjection</code></a>, <a href="https://chillicream.com/docs/hotchocolate/v13/fetching-data/filtering" rel="nofollow noreferrer"><code>UseFiltering</code></a>, <a href="https://chillicream.com/docs/hotchocolate/v13/fetching-data/sorting" rel="nofollow noreferrer"><code>UseSorting</code></a> and my custom <code>UseAboveAgeFilter</code> to modify the query before <a href="https://chillicream.com/docs/hotchocolate/v13/fetching-data/filtering" rel="nofollow noreferrer"><code>UseFiltering</code></a> is called</p>
<pre class="lang-cs prettyprint-override"><code>public class Query
{
    [UseOffsetPaging(MaxPageSize = 100, IncludeTotalCount = true, DefaultPageSize = 20)]
    [UseProjection]
    [UseFiltering]
    [UseSorting]
    [UseAboveAgeFilter]
    public IEnumerable&lt;People&gt; GetPeoples([Service] AppDbContext context) =&gt;
        context.Peoples;
}
</code></pre>
<p>In my <code>UseAboveAgeFilter.cs</code>:</p>
<pre class="lang-cs prettyprint-override"><code>using System.Reflection;
using System.Runtime.CompilerServices;
using HotChocolate.Types.Descriptors;
using SageApi.Model.Sage;

namespace SageApi.Services.GraphQl.Middleware;

public class UseAboveAgeFilterAttribute : ObjectFieldDescriptorAttribute
{
    public UseAboveAgeFilterAttribute([CallerLineNumber] int order = 0)
    {
        Order = order;
    }

    protected override void OnConfigure(
        IDescriptorContext context,
        IObjectFieldDescriptor descriptor,
        MemberInfo member
    )
    {
        descriptor.Use(next =&gt; async middlewareContext =&gt;
        {
            // can I modify the middlewareContext in a way that I remove aboveAge param and replace it
            // with age &gt;= 21, this way the UseFiltering Middleware will work as intended when it will
            // be called after ?
            await next(middlewareContext);
            object? result = middlewareContext.Result;
            if (result is InternalDbSet&lt;People&gt; dbSet)
            {
                // or can I do it here ?
            }
        });
    }
}
</code></pre>
<p>I want to modify the middlewareContext by removing the <code>aboveAge = true</code> condition and replace it with <code>age &gt;= 21</code> condition but I can't find a way to it. If I can do that in my Middleware <code>UseAboveAgeFilter</code> which is call before all the Hot Chocolate Middleware it should work.</p>
<p>When I try to query I got error (which is normal, as I didn't modify the middlewareContext to remove <code>aboveAge = true</code> condition and replace it with <code>age &gt;= 21</code>):</p>
<pre><code>{
    &quot;errors&quot;: [
        {
            &quot;message&quot;: &quot;Unexpected Execution Error&quot;,
            &quot;locations&quot;: [
                {
                    &quot;line&quot;: 2,
                    &quot;column&quot;: 5
                }
            ],
            &quot;path&quot;: [
                &quot;peoples&quot;
            ],
            &quot;extensions&quot;: {
                &quot;message&quot;: &quot;The LINQ expression 'DbSet&lt;People&gt;()\r\n    .Where(f =&gt; f.AboveAge == __p_0)' could not be translated. Additional information: Translation of member 'AboveAge' on entity type 'People' failed. This commonly occurs when the specified member is unmapped. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.&quot;,
                &quot;stackTrace&quot;: &quot;   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)\r\n   at System.Linq.Queryable.Count[TSource](IQueryable`1 source)\r\n   at HotChocolate.Types.Pagination.QueryableOffsetPagingHandler`1.&lt;&gt;c__DisplayClass3_0.&lt;ResolveAsync&gt;b__0()\r\n   at System.Threading.Tasks.Task`1.InnerInvoke()\r\n   at System.Threading.Tasks.Task.&lt;&gt;c.&lt;.cctor&gt;b__281_0(Object obj)\r\n   at System.Threading.ExecutionContext.RunFromThreadPoolDispatchLoop(Thread threadPoolThread, ExecutionContext executionContext, ContextCallback callback, Object state)\r\n--- End of stack trace from previous location ---\r\n   at System.Threading.ExecutionContext.RunFromThreadPoolDispatchLoop(Thread threadPoolThread, ExecutionContext executionContext, ContextCallback callback, Object state)\r\n   at System.Threading.Tasks.Task.ExecuteWithThreadLocal(Task&amp; currentTaskSlot, Thread threadPoolThread)\r\n--- End of stack trace from previous location ---\r\n   at HotChocolate.Types.Pagination.QueryableOffsetPagingHandler`1.ResolveAsync(IResolverContext context, IQueryable`1 source, OffsetPagingArguments arguments, CancellationToken cancellationToken)\r\n   at HotChocolate.Types.Pagination.OffsetPagingHandler.HotChocolate.Types.Pagination.IPagingHandler.SliceAsync(IResolverContext context, Object source)\r\n   at HotChocolate.Types.Pagination.PagingMiddleware.InvokeAsync(IMiddlewareContext context)\r\n   at HotChocolate.Utilities.MiddlewareCompiler`1.ExpressionHelper.AwaitTaskHelper(Task task)\r\n   at SageApi.Services.GraphQl.Middleware.UseFDocenteteMappingAttribute.&lt;&gt;c__DisplayClass1_0.&lt;&lt;OnConfigure&gt;b__1&gt;d.MoveNext() in C:\\Users\\sagealexandrehome\\Documents\\SageApi\\SageApi\\Services\\GraphQl\\Middleware\\UseFDocenteteMappingAttribute.cs:line 26\r\n--- End of stack trace from previous location ---\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.ExecuteResolverPipelineAsync(CancellationToken cancellationToken)\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.TryExecuteAsync(CancellationToken cancellationToken)&quot;
            }
        }
    ],
    &quot;data&quot;: {
        &quot;peoples&quot;: null
    }
}
</code></pre>
<h2>Question</h2>
<p>Am I on the right path to solve this problem ?</p>
<p>If yes, how can I continue ?</p>
<p>If no, what can I try ?</p>

## Answers
### Answer ID: 78982173
<p>You need to go through the <code>middlewareContext.Selection.Arguments</code> and replace the argument you need by another:</p>
<pre class="lang-cs prettyprint-override"><code>using System.Reflection;
using System.Runtime.CompilerServices;
using HotChocolate.Language;
using HotChocolate.Resolvers;
using HotChocolate.Types.Descriptors;

namespace SageApi.Services.GraphQl.Middleware;

public class UseAboveAgeFilterAttribute : ObjectFieldDescriptorAttribute
{
    public UseAboveAgeFilterAttribute([CallerLineNumber] int order = 0)
    {
        Order = order;
    }

    protected override void OnConfigure(
        IDescriptorContext context,
        IObjectFieldDescriptor descriptor,
        MemberInfo member
    )
    {
        descriptor.Use(next =&gt; async middlewareContext =&gt;
        {
            await next(middlewareContext);
            var arguments = middlewareContext.Selection.Arguments;
            foreach (var argument in arguments)
            {
                if (argument.Name == &quot;where&quot;)
                {
                    var objectFieldNodes = (List&lt;ObjectFieldNode&gt;)argument.ValueLiteral?.Value;
                    foreach (var objectFieldNode in objectFieldNodes.ToList())
                    {
                        if (objectFieldNode.Name.Value == &quot;aboveAge&quot;)
                        {
                            objectFieldNodes.Remove(objectFieldNode);// remove above age
                            
                            // add age &gt;= 21
                            var newObjectFieldNode = new ObjectFieldNode(
                                &quot;age&quot;,
                                new ObjectValueNode(new List&lt;ObjectFieldNode&gt;
                                {
                                    new(&quot;gte&quot;, new IntValueNode(21))
                                })
                            );
                            objectFieldNodes.Add(newObjectFieldNode);
                        }
                    }

                    middlewareContext.ReplaceArgument(&quot;where&quot;, new ArgumentValue(
                        argument,
                        argument.Kind ?? ValueKind.Object,
                        argument.IsFullyCoerced,
                        argument.IsDefaultValue,
                        argument.Value,
                        new ObjectValueNode(objectFieldNodes)
                    ));
                }
            }
        });
    }
}
```
</code></pre>

