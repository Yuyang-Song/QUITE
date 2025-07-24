# using linq query with include/then_include vs using sql query with joins and gettng db server error
[Link to question](https://stackoverflow.com/questions/62182817/using-linq-query-with-include-then-include-vs-using-sql-query-with-joins-and-get)
**Creation Date:** 1591218844
**Score:** 0
**Tags:** c#, sql, sql-server, linq, asp.net-core
## Question Body
<p>I have an application I am working on where I need to be able to search and display records; with paging. </p>

<p>I have a method that will pull all records and display them properly with the paging. It is the search that appears to be throwing a wrench into the works on the SQL database side.</p>

<p>I have var listQuery using sql, and var listQuery2 using linq.  I would rather use the linq, but it also is giving me troubles getting all the same fields populated as the sql query. </p>

<p>What I am trying to achieve is when I do the sort, the `if (!string.IsNullOrEmpty(partParams.SearchString))' looks at the list of items, gets the ones that match and passes the list to the return from the PagedList method.  </p>

<p>I am pulling from 3 tables (part, brand, supplier) and two key tables (partBrand, partSupplier) use primary key fields.  when the records are pulled from the db, I add them to a new entity that is used for displaying specific fields (MaterialPart).  Var listQuery works find when NOT using the search.  All records come back, properly paged. Var listQuery2 is not complete as I would like to set up the merged entity, but am having trouble relating the data.</p>

<p>If needed, I can add the class entities to assist with clarity.</p>

<pre><code>        public async Task&lt;PagedList&lt;MaterialPart&gt;&gt; GetMaterialParts(PartParams partParams)
        {
            var listQuery = from p in _dbcontext.Parts
                            join ps in _dbcontext.PartsSuppliers on p.Id equals ps.PartId
                            join s in _dbcontext.Suppliers on ps.SupplierId equals s.Id
                            join pb in _dbcontext.PartsBrands on p.Id equals pb.PartId
                            join b in _dbcontext.Brands on pb.BrandId equals b.Id
                            select (new MaterialPart
                            {
                                PartId = p.Id,
                                PartNumber = p.PartNumber,
                                Description = p.Description,
                                SupplierId = s.Id,
                                SupplierName = s.SupplierName,
                                BrandId = b.Id,
                                BrandName = b.BrandName,
                                Cost = ps.Cost
                            });

            var listQuery2 = _dbcontext.Parts
                    .Include(x =&gt; x.PartBrands)
                        .ThenInclude(x =&gt; x.Brand)
                    .Include(x =&gt; x.PartSuppliers)
                        .ThenInclude(x =&gt; x.Supplier)
                    .Select(t =&gt; new MaterialPart
                    {
                        PartId = t.Id,
                        PartNumber = t.PartNumber,
                        Description = t.Description
                    });

            if (!string.IsNullOrEmpty(partParams.SearchString))
            {
                listQuery = listQuery
                    .AsQueryable()
                    .Where(x =&gt; x.PartNumber
                        .Contains(partParams.SearchString, StringComparison.OrdinalIgnoreCase)
                    || x.Description
                        .Contains(partParams.SearchString, StringComparison.OrdinalIgnoreCase));
            }

            return await PagedList&lt;MaterialPart&gt;.CreateAsync(listQuery,
                partParams.PageNumber,
                partParams.PageSize);

        }
</code></pre>

<p>My api URL in Postman looks like the following: </p>

<pre><code>http://localhost:5001/api/materials?pageNumber=1&amp;pageSize=5&amp;searchString=100-
</code></pre>

<p>Sql Server error</p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Part&gt;
    .Join(
        outer: DbSet&lt;PartSupplier&gt;, 
        inner: p =&gt; p.Id, 
        outerKeySelector: p0 =&gt; p0.PartId, 
        innerKeySelector: (p, p0) =&gt; new TransparentIdentifier&lt;Part, PartSupplier&gt;(
            Outer = p, 
            Inner = p0
        ))
    .Join(
        outer: DbSet&lt;Supplier&gt;, 
        inner: ti =&gt; ti.Inner.SupplierId, 
        outerKeySelector: s =&gt; s.Id, 
        innerKeySelector: (ti, s) =&gt; new TransparentIdentifier&lt;TransparentIdentifier&lt;Part, PartSupplier&gt;, Supplier&gt;(
            Outer = ti, 
            Inner = s
        ))
    .Join(
        outer: DbSet&lt;PartBrand&gt;, 
        inner: ti0 =&gt; ti0.Outer.Outer.Id, 
        outerKeySelector: p1 =&gt; p1.PartId, 
        innerKeySelector: (ti0, p1) =&gt; new TransparentIdentifier&lt;TransparentIdentifier&lt;TransparentIdentifier&lt;Part, PartSupplier&gt;, Supplier&gt;, PartBrand&gt;(
            Outer = ti0, 
            Inner = p1
        ))
    .Join(
        outer: DbSet&lt;Brand&gt;, 
        inner: ti1 =&gt; ti1.Inner.BrandId, 
        outerKeySelector: b =&gt; b.Id, 
        innerKeySelector: (ti1, b) =&gt; new TransparentIdentifier&lt;TransparentIdentifier&lt;TransparentIdentifier&lt;TransparentIdentifier&lt;Part, PartSupplier&gt;, Supplier&gt;, PartBrand&gt;, Brand&gt;(
            Outer = ti1, 
            Inner = b
        ))
    .Where(ti2 =&gt; ti2.Outer.Outer.Outer.Outer.PartNumber.Contains(
        value: __partParams_SearchString_0, 
        comparisonType: OrdinalIgnoreCase) || ti2.Outer.Outer.Outer.Outer.Description.Contains(
        value: __partParams_SearchString_0, 
        comparisonType: OrdinalIgnoreCase))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.CountAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
   at pMinder4.API.Helpers.PagedList`1.CreateAsync(IQueryable`1 source, Int32 pageNumber, Int32 pageSize) in C:\Users\lsieting\Documents\Source\repos\pMinder4\pMinder4.API\Helpers\PagedList.cs:line 27
   at pMinder4.API.Data.MaterialRepository.GetMaterialParts(PartParams partParams) in C:\Users\lsieting\Documents\Source\repos\pMinder4\pMinder4.API\Data\MaterialRepository.cs:line 95
   at pMinder4.API.Controllers.MaterialsController.GetMaterialParts(PartParams partParams) in C:\Users\lsieting\Documents\Source\repos\pMinder4\pMinder4.API\Controllers\MaterialsController.cs:line 30
   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor.TaskOfIActionResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeActionMethodAsync&gt;g__Awaited|12_0(ControllerActionInvoker invoker, ValueTask`1 actionResultValueTask)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.&lt;InvokeNextActionFilterAsync&gt;g__Awaited|10_0(ControllerActionInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow(ActionExecutedContextSealed context)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next(State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.InvokeInnerFilterAsync()
--- End of stack trace from previous location where exception was thrown ---
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeFilterPipelineAsync&gt;g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
   at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.&lt;InvokeAsync&gt;g__Awaited|17_0(ResourceInvoker invoker, Task task, IDisposable scope)
   at Microsoft.AspNetCore.Routing.EndpointMiddleware.&lt;Invoke&gt;g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
   at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Authentication.AuthenticationMiddleware.Invoke(HttpContext context)
   at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)

</code></pre>

## Answers
### Answer ID: 62183022
<p>Try to simplify the comparison like this:</p>

<pre><code>listQuery = listQuery
                    .AsQueryable()
                    .Where(x =&gt; x.PartNumber.ToLower()
                        .Contains(partParams.SearchString.ToLower())
                    || x.Description.ToLower()
                        .Contains(partParams.SearchString.ToLower()));
</code></pre>

<p>This kind of filter <code>.Contains(partParams.SearchString, StringComparison.OrdinalIgnoreCase)</code> doesn't work on Linq to Entities.</p>

<p>Hope it helps!</p>

