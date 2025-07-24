# OData filter flags enum &#39;has&#39; operator translated to .HasFlag(value) but not in a form EF Core accepts
[Link to question](https://stackoverflow.com/questions/78433664/odata-filter-flags-enum-has-operator-translated-to-hasflagvalue-but-not-in)
**Creation Date:** 1714940818
**Score:** 0
**Tags:** entity-framework-core, odata, automapper, ef-core-8.0, automapper-13
## Question Body
<p>The <code>AutoMapper.Extensions.OData</code> github repo instructs to go here first, so I hope this finds the right people. I'm not exactly sure if this is related to <code>AutoMapper.AspNetCore.OData.EFCore</code>, <code>AutoMapper.Extensions.ExpressionMapping</code>, neither, or both!</p>
<p>I have a sample repo <a href="https://github.com/engenb/AutoMapper.OData.EFCore.Issue" rel="nofollow noreferrer">here</a> that reproduces the problem. Steps to get set up and run the project can be found in the README.</p>
<p><strong>Summary</strong></p>
<p>I have an entity and a DTO each named <code>Foo</code> that each have a flags enum such as:</p>
<pre class="lang-cs prettyprint-override"><code>namespace Domain.Enumerations;
[Flags]
public enum FooType
{
    One =   0b0001,
    Two =   0b0010,
    Three = 0b0100,
    Four =  0b1000
}

namespace Domain.Components.Foos;

public class Foo
{
    public Guid Id { get; set; }
    public FooType Type { get; set; }
}

namespace ApiModel;

[Flags]
public enum FooType
{
    One =   0b0001,
    Two =   0b0010,
    Three = 0b0100,
    Four =  0b1000
}

public class Foo
{
    public Guid Id { get; set; }
    public FooType Type { get; set; }
}
</code></pre>
<p>The domain entity <code>Foo</code> is bound to the database via EF Core and the model/dto <code>Foo</code> is used to build the OData EDM.  I'm using AutoMapper's OData/EFCore/ExpressionMapping extensions to translate between entity <code>Foo</code> and model <code>Foo</code>.</p>
<p>If I query my API with <code>$filter=type eq 'Four'</code> everything works great.  If I query my API with <code>$filter=type has 'Four'</code> the application throws an exception:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet().Where(f =&gt; f.Type.HasFlag((Enum)Four))' could not be translated.<br />
Additional information: Translation of method 'System.Enum.HasFlag' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
<p>at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)<br />
at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)<br />
at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)<br />
at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)<br />
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)<br />
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0<code>1.&lt;ExecuteAsync&gt;b__0()   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func</code>1 compiler)<br />
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)<br />
at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)<br />
at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable<code>1.GetAsyncEnumerator(CancellationToken cancellationToken)   at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable</code>1.GetAsyncEnumerator()<br />
at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsync[TSource](IQueryable<code>1 source, CancellationToken cancellationToken)   at AutoMapper.AspNet.OData.QueryableExtensions.GetAsync[TModel,TData](IQueryable</code>1 query, IMapper mapper, Expression<code>1 filter, Expression</code>1 queryFunc, ICollection<code>1 includeProperties, AsyncSettings asyncSettings)   at AutoMapper.AspNet.OData.QueryableExtensions.GetAsync[TModel,TData](IQueryable</code>1 query, IMapper mapper, ODataQueryOptions`1 options, QuerySettings querySettings)<br />
at Domain.Components.Foos.Queries.GetFoosODataQueryHandler.Handle(GetFoosODataQuery query, CancellationToken ct) in C:\Projects\AutoMapper.OData.EFCore.Issue\Domain\Components\Foos\Queries\GetFoosOData.cs:line 29</p>
</blockquote>
<p>In some of our older projects, we've been able to use a flags enum <code>has</code> such as this but only when the <code>DbSet&lt;Foo&gt;</code> is returned directly from the controller as an <code>IQueryable</code> - this becomes problematic with a versioned API as the versioned API contracts won't be 1-to-1 with the database schema.</p>
<p>I've considered introducing database views that perform this translation layer and then exposing view pocos as the OData EDM but exposing the data layer in this way wouldn't be ideal from an architecture / design perspective.</p>
<p><strong>Expression Mapping Debug</strong></p>
<p>I've added some unit tests that attempt to illustrate and compare the differences between</p>
<pre class="lang-cs prettyprint-override"><code>Expression&lt;Func&lt;Foo, bool&gt;&gt; filter = x =&gt; x.Type.HasFlag(FooType.Three);
</code></pre>
<p>and</p>
<pre class="lang-cs prettyprint-override"><code>Expression&lt;Func&lt;ApiModel.Foo, bool&gt;&gt; modelFilter = x =&gt; x.Type.HasFlag(ApiModel.FooType.Three);
var filter = _mapper.MapExpression&lt;Expression&lt;Func&lt;Foo, bool&gt;&gt;&gt;(modelFilter);
</code></pre>
<p>I, so far, am unable to find a difference between the two <code>filter</code>s, but the former works and the latter does not.</p>
<p>Has anyone run into something similar who knows a solution? I'm hoping I can continue using AutoMapper to perform mapping between layers vs moving this responsibility into the database.</p>
<p>At any rate, thanks for taking a look!</p>

