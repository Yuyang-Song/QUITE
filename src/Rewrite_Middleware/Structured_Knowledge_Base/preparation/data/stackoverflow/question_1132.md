# EF Core 3.1 throws an exception for Contains
[Link to question](https://stackoverflow.com/questions/60412799/ef-core-3-1-throws-an-exception-for-contains)
**Creation Date:** 1582716162
**Score:** 1
**Tags:** c#, asp.net-core, linq-to-sql, asp.net-core-webapi, ef-core-3.0
## Question Body
<p>I recently updated the project code into .NET Core 3.1 and EF Core 3.1, now most of my linq queries brake, EX.</p>

<pre><code>public override ICollection&lt;ContactDetailModel&gt; GetAll(ICollection&lt;int&gt; ids)
{
            return _context
                .Set&lt;TEntity&gt;()
                .IgnoreDeletedEntities()                
                .Where(x =&gt; ids.Distinct().Contains(x.ContactId))                
                .Select(EntityToDTOMapper)
                .ToList();
}
</code></pre>

<p>This code throws an error where I use Contains, I saw in some other posts this issues has been fixed as a bug, but yet it fails.</p>

<p>Error I get is "could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()."</p>

<pre><code>System.InvalidOperationException
  HResult=0x80131509
  Message=The LINQ expression 'DbSet&lt;SupplierContactDetails&gt;
    .Where(s =&gt; !(s.DeletedOn.HasValue) &amp;&amp; !(s.DeletedBy.HasValue))
    .Where(s =&gt; __Distinct_0
        .Contains(s.ContactId))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
  Source=Microsoft.EntityFrameworkCore
  StackTrace:
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at BlueTag.DAL.Repositories.ContactRepository`1.GetAll(ICollection`1 ids) in D:\Projects\BlueTag Version 2\.net-core-server\DAL\Repositories\ContactRepository.cs:line 95
   at BlueTag.DAL.Repositories.SupplierRepository.ToDomain(IEnumerable`1 supplier) in D:\Projects\BlueTag Version 2\.net-core-server\DAL\Repositories\SupplierRepository.cs:line 216
   at BlueTag.DAL.Repositories.SupplierRepository.GetFilteredSuppliers(RequestPagingOptionsModel`1 options) in D:\Projects\BlueTag Version 2\.net-core-server\DAL\Repositories\SupplierRepository.cs:line 129
   at BlueTag.Supplier.Services.SupplierService.GetFilteredSupplierDetails(RequestPagingOptionsModel`1 options) in D:\Projects\BlueTag Version 2\.net-core-server\Supplier\Serrvices\SupplierService.cs:line 49
   at BlueTag.Supplier.Controllers.SupplierController.GetFilteredSuppliers(RequestPagingOptionsModel`1 options) in D:\Projects\BlueTag Version 2\.net-core-server\Supplier\Controllers\SupplierController.cs:line 54
   at Microsoft.Extensions.Internal.ObjectMethodExecutor.Execute(Object target, Object[] parameters)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.SyncObjectResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeActionMethodAsync()
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeNextActionFilterAsync()

</code></pre>

## Answers
### Answer ID: 60413294
<p>Entity Framework cannot translate every query, and as such it sometimes has to load all the data and perform the LINQ expression in-memory, this is called Client Side Evaluation and is not desired, as it is more resource intensive and takes longer. For your specific problem, there are 2 solutions, both of which are outlined in the error message.</p>

<p>1) Rewrite your LINQ queries to include explicit calls to client side evaluation versus implicit calls</p>

<p>or </p>

<p>2) Rewrite your LINQ queries to not need client side evaluation</p>

<p>You could do number 1 like so:</p>

<pre class="lang-cs prettyprint-override"><code>public override ICollection&lt;ContactDetailModel&gt; GetAll(ICollection&lt;int&gt; ids)
{
    return _context
        .Set&lt;TEntity&gt;()
        .IgnoreDeletedEntities()
        .ToList()                
        .Where(x =&gt; ids.Distinct().Contains(x.ContactId))                
        .Select(EntityToDTOMapper)
        .ToList();
}
</code></pre>

<p>Notice the explicit call to <code>ToList</code> after <code>IgnoreDeletedEntities</code>, this needs to be done to explicitly switch to client side evaluation so your <code>Where</code> statement will properly execute and not throw any errors. This is because <code>x =&gt; ids.Distinct().Contains(x.ContactId)</code> cannot be translated to SQL (or whatever) by your version of EF.</p>

<p>Number 2 could be solved like so:</p>

<pre class="lang-cs prettyprint-override"><code>public override ICollection&lt;ContactDetailModel&gt; GetAll(ICollection&lt;int&gt; ids)
{
    ids = ids.Distinct();
    return _context
        .Set&lt;TEntity&gt;()
        .IgnoreDeletedEntities()
        .Where(x =&gt; ids.Contains(x.ContactId))
        .Select(EntityToDTOMapper)
        .ToList();
}
</code></pre>

<p>Notice how I moved the use of <code>ids.Distinct()</code> from the <code>Where</code> to the top, as that was the part EF couldn't translate</p>

