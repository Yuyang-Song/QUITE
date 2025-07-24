# The LINQ expression could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation (CosmosDb)
[Link to question](https://stackoverflow.com/questions/77785709/the-linq-expression-could-not-be-translated-either-rewrite-the-query-in-a-form)
**Creation Date:** 1704793068
**Score:** 0
**Tags:** c#, entity-framework-core, azure-cosmosdb
## Question Body
<p>I'm encountering an issue with LINQ in Azure Cosmos DB, specifically a 'System.InvalidOperationException.' Notably, my LINQ queries work fine with EF Core In-Memory DB in tests but throw this error with Cosmos DB. Have there been any known challenges or differences when using LINQ with Cosmos DB?</p>
<pre><code>fail: Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware[1]
  An unhandled exception has occurred while executing the request.
  System.InvalidOperationException: The LINQ expression 'DbSet&lt;Media&gt;()' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitExtension(Expression extensionExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Visit(Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Visit(Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Visit(Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Visit(Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
     at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Visit(Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
     at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
     at Microsoft.EntityFrameworkCore.Cosmos.Query.Internal.CosmosQueryableMethodTranslatingExpressionVisitor.Visit(Expression expression)
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
</code></pre>
<p>and here is my code</p>
<pre><code>var messages =await _context.Messages
    .Where(x =&gt; x.RoomChatId == roomId)
    .OrderByDescending(x =&gt; x.CreatedDate)
    .Select(message =&gt;
        new MessageResponse
        {
            id = message.id,
            CreatedDate = message.CreatedDate,
            MediaList = message.MediaList!.Select(x =&gt; new MediaResponse
            {
                Id = x.Id,
                Type = (MediaTypeResponse)x.Type,
                BlurHash = x.BlurHash,
                Path = x.Path
            }).ToList(),

            Text = message.Text,
            GroupInviteToken = message.GroupInvitationToken,
            ModifiedDate = message.ModifiedDate,
            ReplyMessageId = message.ReplyMessageId,
            UserSender = _context.Users.Where(x =&gt; x.id == message.UserSenderId).Select(x =&gt; new PreviewUserResponse()
            {
                Id = x.id,
                Name = x.FullName,
                ProfileImage = FileStorageHelper.GetUrl(x.ProfileImage)
            }).Single()
        }).ToListAsync();
</code></pre>
<p>and this is my message Entity and Media is inside message and it's not apart entity</p>
<pre><code>public class Message : BaseEntity
{
    public Guid RoomChatId { get; set; }

    public string? Text { get; set; }

    public Guid UserSenderId { get; set; }

    public string? GroupInvitationToken { get; set; }

    public Guid? ReplyMessageId { get; set; }

    public ICollection&lt;Media&gt;? MediaList { get; set; }
}
</code></pre>

