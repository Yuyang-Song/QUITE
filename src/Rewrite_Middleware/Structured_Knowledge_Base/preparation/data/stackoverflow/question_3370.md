# Adding UseProjection to Graphql Query Fails with Unexpected Execution Error in Linq Execution
[Link to question](https://stackoverflow.com/questions/77663444/adding-useprojection-to-graphql-query-fails-with-unexpected-execution-error-in-l)
**Creation Date:** 1702594118
**Score:** 0
**Tags:** .net-core, entity-framework-core, graphql, hotchocolate
## Question Body
<p>I am new to Graphql and wanted to try it in an API written in c#.</p>
<p>I am using HotChocolate, EFCore 8, dotnet 8.</p>
<p>I have the following Classes</p>
<pre class="lang-cs prettyprint-override"><code>public class Batch
{
    public Batch()
    {
    }

    public Batch(string batchId, string tenantId, int paymentsCount, decimal totalAmount, string status,
        string statusDescription)
    {
        BatchId = batchId;
        TenantId = tenantId;
        PaymentsCount = paymentsCount;
        TotalAmount = totalAmount;
        Status = status;
        StatusDescription = statusDescription;
    }

    public string BatchId { get; set; }
    public string TenantId { get; set; }
    public int PaymentsCount { get; set; }
    public decimal TotalAmount { get; set; }
    public string Status { get; set; }
    public string StatusDescription { get; set; }
    [UseFiltering]
    [UseSorting]
    public ICollection&lt;Payment&gt; Payments { get; set; }
}

public class Payment
{
    public Payment()
    {
    }

    public string Id { get; set; }
    public string PayeeName { get; set; }
    public string CheckNumber { get; set; }
    //public List&lt;string&gt; InvoiceNumbers { get; set; }
    public DateTime PaymentDate { get; set; }
    public string Status { get; set; }
    public string StatusDescription { get; set; }
    public decimal Amount { get; set; }
}
</code></pre>
<p>This is the Grapql Query</p>
<pre class="lang-cs prettyprint-override"><code>public class BatchesQuery
{
    // Resolver
    [UsePaging(IncludeTotalCount = true)]
    [UseProjection]
    [UseFiltering]
    [UseSorting]
    public IQueryable&lt;Batch&gt; Batches([Service] PaymentDbContext paymentDbContext, string tenantId, IResolverContext context)
    {
        var paymentBatchesQueryable = paymentDbContext.PaymentBatches
            .Where(pb =&gt; pb.TenantId == tenantId)
            .OrderByDescending(pb =&gt; pb.CreatedTimestamp)
            .AsNoTracking();
        var paymentRequests = paymentBatchesQueryable.SelectMany(pb =&gt; pb.PaymentRequests);
        var payments = paymentRequests.Select(pr =&gt; new Payment()
        {
            Id = pr.PaymentRequestExternalId,
            PayeeName = pr.Payee.Name,
            CheckNumber = pr.Number,
            //InvoiceNumbers = pr.RemittanceDetails.Select(rd =&gt; rd.Number).ToList(),
            PaymentDate = pr.RequestDate,
            Status = pr.PaymentRequestStatusType.ToString(),
            StatusDescription = pr.PaymentRequestStatusType.ToString(),
            Amount = pr.RemittanceDetails.Sum(rd =&gt; rd.Net)
        });

        var paymentBatches = paymentBatchesQueryable
            .Select(pb =&gt; new Batch(pb.PaymentBatchExternalId,
                pb.TenantId,
                pb.PaymentRequests.Count,
                pb.PaymentRequests
                    .SelectMany(pr =&gt; pr.RemittanceDetails)
                    .Sum(rd =&gt; rd.Net),
                pb.PaymentBatchStatusType.ToString(),
                pb.PaymentBatchStatusType.ToString())
            {
                Payments = payments.ToList()
      
            });
       

        return paymentBatches;
    }
}
</code></pre>
<p>This is my Setup in Program.cs</p>
<pre class="lang-cs prettyprint-override"><code>builder.Services.AddGraphQLServer()
    .AddQueryType&lt;BatchesQuery&gt;()
    .AddProjections()
    .AddFiltering()
    .AddSorting()
    .RegisterDbContext&lt;PaymentDbContext&gt;();
</code></pre>
<p>I get the following error when I run this query:</p>
<pre><code>query{
  batches(tenantId: &quot;yKYrJLSUrE6XDWkrQC0e&quot;){
    nodes{
      batchId
      payments{
        id
      }
    }
  }
}
</code></pre>
<p>Response:</p>
<pre class="lang-json prettyprint-override"><code>{
  &quot;errors&quot;: [
    {
      &quot;message&quot;: &quot;Unexpected Execution Error&quot;,
      &quot;locations&quot;: [
        {
          &quot;line&quot;: 2,
          &quot;column&quot;: 3
        }
      ],
      &quot;path&quot;: [
        &quot;batches&quot;
      ],
      &quot;extensions&quot;: {
        &quot;message&quot;: &quot;The LINQ expression 'p1 =&gt; new Payment{ Id = p1.Id }\r\n' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.&quot;,
        &quot;stackTrace&quot;: &quot;   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitLambda[T](Expression`1 lambdaExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerSqlTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateInternal(Expression expression, Boolean applyDefaultTypeMapping)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateProjection(Expression expression, Boolean applyDefaultTypeMapping)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)\r\n   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)\r\n   at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1.GetAsyncEnumerator()\r\n   at HotChocolate.Types.Pagination.QueryableCursorPagination`1.ExecuteAsync(IQueryable`1 query, Int32 offset, CancellationToken cancellationToken)\r\n   at HotChocolate.Types.Pagination.CursorPaginationAlgorithm`2.ApplyPaginationAsync(TQuery query, CursorPagingArguments arguments, Nullable`1 totalCount, CancellationToken cancellationToken)\r\n   at HotChocolate.Types.Pagination.QueryableCursorPagingHandler`1.ResolveAsync(IResolverContext context, IQueryable`1 source, CursorPagingArguments arguments, CancellationToken cancellationToken)\r\n   at HotChocolate.Types.Pagination.CursorPagingHandler.HotChocolate.Types.Pagination.IPagingHandler.SliceAsync(IResolverContext context, Object source)\r\n   at HotChocolate.Types.Pagination.PagingMiddleware.InvokeAsync(IMiddlewareContext context)\r\n   at HotChocolate.Utilities.MiddlewareCompiler`1.ExpressionHelper.AwaitTaskHelper(Task task)\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.ExecuteResolverPipelineAsync(CancellationToken cancellationToken)\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.TryExecuteAsync(CancellationToken cancellationToken)&quot;
      }
    }
  ],
  &quot;data&quot;: {
    &quot;batches&quot;: null
  }
}
</code></pre>
<p>I tried doing the recommendations provided in the response but none of them worked. This error goes away when I remove UseProjections annotation.</p>
<p>I am not sure what's happening. Could someone please explain ?</p>

## Answers
### Answer ID: 77688470
<p>In your example, you are trying to materialize a list within the IQueryable.  SQL does not understand this.</p>
<p>Try adding the .ToList() to your payments query like below:</p>
<pre><code>    var payments = paymentRequests.Select(pr =&gt; new Payment()
    {
        Id = pr.PaymentRequestExternalId,
        PayeeName = pr.Payee.Name,
        CheckNumber = pr.Number,
        //InvoiceNumbers = pr.RemittanceDetails.Select(rd =&gt; rd.Number).ToList(),
        PaymentDate = pr.RequestDate,
        Status = pr.PaymentRequestStatusType.ToString(),
        StatusDescription = pr.PaymentRequestStatusType.ToString(),
        Amount = pr.RemittanceDetails.Sum(rd =&gt; rd.Net)
    }).ToList();
</code></pre>
<p>And then remove the .ToList() from payments within the paymentBatches query:</p>
<pre><code>var paymentBatches = paymentBatchesQueryable
                .Select(pb =&gt; new Batch(pb.PaymentBatchExternalId,
                    pb.TenantId,
                    pb.PaymentRequests.Count,
                    pb.PaymentRequests
                        .SelectMany(pr =&gt; pr.RemittanceDetails)
                        .Sum(rd =&gt; rd.Net),
                    pb.PaymentBatchStatusType.ToString(),
                    pb.PaymentBatchStatusType.ToString())
                {
                    Payments = payments
          
                });
</code></pre>
<p>ToString() is also not supported when translating an IQueryable to SQL.  Try using SqlFunctions.StringConvert(pb.PaymentBatchStatusType) instead.  There may be other areas that are not translating, but this is a good start.</p>
<p>Might I also suggest creating SQL Views or Stored Procedures when having to create multiple work queries.  I find these query methods work best with HotChocolate when keeping it simple: one call to context and maybe a simple WHERE clause at the most.</p>

