# Odata filtering in expanded property does not work
[Link to question](https://stackoverflow.com/questions/66257708/odata-filtering-in-expanded-property-does-not-work)
**Creation Date:** 1613642795
**Score:** 1
**Tags:** c#, linq, asp.net-core, entity-framework-core, odata
## Question Body
<p>We have created a .NET Core API which uses Odata to filter, select, and expand the data. The data is stored in a Microsoft SQL Server database and retrieved through EntityFramework Core (code first). We use Linq projection so the Odata filter is applied directly to the query, but this gives an error in the following situation:</p>
<p>When retrieving a list of results, e.g. authors expanded with books, everything works fine. It gives an error when filtering inside the expanded books e.g.: https://localhost:44316/odata/authors?$expand=Books($filter=Id eq 1)</p>
<pre><code>    System.InvalidOperationException: The LINQ expression 'DbSet&lt;Book&gt;()
    .Where(b0 =&gt; EF.Property&lt;Nullable&lt;int&gt;&gt;(EntityShaperExpression: 
        EntityType: Author
        ValueBufferExpression: 
            ProjectionBindingExpression: EmptyProjectionMember
        IsNullable: False
    , &quot;Id&quot;) != null &amp;&amp; object.Equals(
        objA: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(EntityShaperExpression: 
            EntityType: Author
            ValueBufferExpression: 
                ProjectionBindingExpression: EmptyProjectionMember
            IsNullable: False
        , &quot;Id&quot;), 
        objB: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(b0, &quot;AuthorId&quot;)))
    .Where(b0 =&gt; b0
        .ToDto().Id == __TypedProperty_1)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|15_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass15_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.TranslateSubquery(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
   at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
   at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)
   at Microsoft.AspNetCore.Mvc.Infrastructure.AsyncEnumerableReader.ReadInternal[T](Object value)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ObjectResultExecutor.ExecuteAsyncEnumerable(ActionContext context, ObjectResult result, Object asyncEnumerable, Func`2 reader)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextResultFilterAsync&gt;g__Awaited|29_0[TFilter,TFilterAsync](ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResultExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.ResultNext[TFilter,TFilterAsync](State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.InvokeResultFilters()
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)
</code></pre>
<p>I already created an <a href="https://github.com/OData/AspNetCoreOData/issues/79" rel="nofollow noreferrer">issue</a> on the odata github page, but it only partially solved our problem and we got no reaction on the second comment.</p>
<p>This is the code that we use to map from database model to DTO.</p>
<pre><code>public static IQueryable&lt;AuthorDTO&gt; ProjectTo(IQueryable&lt;Author&gt; source)
{
    return source?.Select(ProjectToAuthorDto());
}

private static Expression&lt;Func&lt;Author, AuthorDTO&gt;&gt; ProjectToAuthorDto()
{
    return author =&gt; new AuthorDTO
    {
        Firstname = author.Firstname,
        Lastname = author.Lastname,
        Id = author.Id,
        Books = author.Books.Select(book =&gt; book.ToDto())
    };
}

public static BookDTO ToDto(this Book book)
{
    return ProjectToBookDto().Compile().Invoke(book);
}

private static Expression&lt;Func&lt;Book, BookDTO&gt;&gt; ProjectToBookDto()
{
    return book =&gt; new BookDTO
    {
        AuthorId = book.AuthorId,
        Author = book.Author.ToDto(),
        Id = book.Id,
        ISBN = book.ISBN,
        Title = book.Title
    };
}
</code></pre>
<p>When I perform the mapping inline, everything works fine (see image below), but this is not a solution as the mappings need to be reusable.
<a href="https://i.sstatic.net/ikPad.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/ikPad.png" alt="enter image description here" /></a></p>
<p>This problem only occurs with Odata in combination with Linq projection. When we remove the Odata packages, everything is returned as expected. Furthermore, when we execute the query before returning the result (by adding .ToList()), we do get the expected result, however, the odata filter is not applied to the query. We have this problem in .NET Core 3.1 as well as in .NET 5.
I created an extremely simplified minimal version of our problem in <a href="https://github.com/NielsDWG/TheBookStoreTestProject" rel="nofollow noreferrer">this repo</a>.</p>
<p>We ran out of ideas and do not know what to try next. I hope that anyone got an idea to get the filter to work.</p>
<p>Thanks in advance!</p>
<p><strong>Edit</strong></p>
<p>I reworked the helper as Svyatoslav Danyliv suggested.</p>
<pre><code>public static IQueryable&lt;AuthorDTO&gt; ProjectTo(IQueryable&lt;Author&gt; source)
{
    return source?.Select(item =&gt; item.ToDto());
}

[Computed]
public static AuthorDTO ToDto(this Author author)
{
    return new AuthorDTO
    {
        Firstname = author.Firstname,
        Lastname = author.Lastname,
        Id = author.Id,
        Books = author.Books.Select(book =&gt; book.ToDto())
    };
}
[Computed]
public static BookDTO ToDto(this Book book)
{
    return new BookDTO
    {
        AuthorId = book.AuthorId,
        //Author = book.Author.ToDto(),
        Id = book.Id,
        ISBN = book.ISBN,
        Title = book.Title
    };
}
</code></pre>
<p>And call it via:</p>
<pre><code>// Convert to DTO
IQueryable&lt;AuthorDTO&gt; result = CustomMapper.ProjectTo(authors);

return Ok(result.Decompile());
</code></pre>
<p>The error is gone, but now the result is truncated:</p>
<p><a href="https://i.sstatic.net/R3297.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/R3297.png" alt="Truncated response" /></a></p>
<p>I also see in SQL Server Profiler that the query is not executed anymore when I apply the $filter.</p>
<p>when I use <code>.DecompileAsync()</code> I get the following error:</p>
<pre><code>System.InvalidOperationException: The LINQ expression '$it' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
   at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at System.Linq.Expressions.ExpressionVisitor.VisitLambda[T](Expression`1 node)
   at System.Linq.Expressions.Expression`1.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitConditional(ConditionalExpression conditionalExpression)
   at System.Linq.Expressions.ConditionalExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
   at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
   at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
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
   at DelegateDecompiler.EntityFrameworkCore.AsyncDecompiledQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)
   at Microsoft.AspNetCore.Mvc.Infrastructure.AsyncEnumerableReader.ReadInternal[T](Object value)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ObjectResultExecutor.ExecuteAsyncEnumerable(ActionContext context, ObjectResult result, Object asyncEnumerable, Func`2 reader)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeNextResultFilterAsync&gt;g__Awaited|29_0[TFilter,TFilterAsync](ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResultExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.ResultNext[TFilter,TFilterAsync](State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.InvokeResultFilters()
--- End of stack trace from previous location ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)

</code></pre>
<p>Any ideas? Thanks again!</p>
<p><strong>Edit 2</strong></p>
<p>Svyatoslav Danyliv suggested to use the code below and that fixed the error above!</p>
<pre><code>[EnableQuery(HandleNullPropagation = HandleNullPropagationOption.False]
</code></pre>
<p>Thank you for your effort!</p>
<p><a href="https://i.sstatic.net/B7cB0.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/B7cB0.png" alt="enter image description here" /></a></p>
<p>Final (working) code:</p>
<pre><code>public static IQueryable&lt;AuthorDTO&gt; ProjectTo(IQueryable&lt;Author&gt; source)
{
    return source?.Select(item =&gt; item.ToDto());
}

[Computed]
public static AuthorDTO ToDto(this Author author)
{
    return new AuthorDTO
    {
        Firstname = author.Firstname,
        Lastname = author.Lastname,
        Id = author.Id,
        Books = author.Books.Select(book =&gt; book.ToDto())
    };
}      

[Computed]
public static BookDTO ToDto(this Book book)
{
    return new BookDTO
    {
        AuthorId = book.AuthorId,
        //Author = book.Author.ToDto(),
        Id = book.Id,
        ISBN = book.ISBN,
        Title = book.Title
    };
}
</code></pre>
<p>And call it with:</p>
<pre><code>IQueryable&lt;AuthorDTO&gt; result = CustomMapper.ProjectTo(authors);

return Ok(result.DecompileAsync());
</code></pre>

## Answers
### Answer ID: 66258628
<p>Well, it is common mistake when working with Expresion Tree. You cannot use <code>ToDto</code> in that way. LINQ translator has to see Expression Tree but not compiled lambda.</p>
<p>There are two libraries, that I know, and which can help you to achieve this result:</p>
<p><a href="https://github.com/hazzik/DelegateDecompiler" rel="nofollow noreferrer">https://github.com/hazzik/DelegateDecompiler</a></p>
<p><a href="https://github.com/axelheer/nein-linq" rel="nofollow noreferrer">https://github.com/axelheer/nein-linq</a></p>
<p>Then you have to rewrite your helper methods (using DelegateDecompiler):</p>
<pre class="lang-cs prettyprint-override"><code>[Computed]
public static BookDTO ToDto(this Book book)
{
    return new BookDTO
    {
        AuthorId = book.AuthorId,
        Author = book.Author.ToDto(),
        Id = book.Id,
        ISBN = book.ISBN,
        Title = book.Title
    };
}

[Computed]
public static AuthorDTO ToDto(this Author author)
{
   ...
}
</code></pre>
<p>And use <code>.Decompile()</code> or <code>.DecompileAsync()</code> as specified in documentation</p>
<p><strong>Note for performance and query translation</strong></p>
<p><code>EnableQuery</code> attribute should be initialised with:</p>
<pre class="lang-cs prettyprint-override"><code>[EnableQuery(HandleNullPropagation = HandleNullPropagationOption.False, 
   HandleReferenceNavigationPropertyExpandFilter = false)]
</code></pre>
<p>Also, during to bug in OData, query will select expanded item two times: with filter and without filer. And it is a limitation of current OData library. Probably issue for that should be created in their repository.</p>

