# Query EF with a predicate
[Link to question](https://stackoverflow.com/questions/63148546/query-ef-with-a-predicate)
**Creation Date:** 1596008057
**Score:** 0
**Tags:** c#, generics, lambda, ef-core-3.1
## Question Body
<p>I've got following (generic) repository method:</p>
<pre><code>public async Task&lt;TEntity&gt; GetAsync(Expression&lt;Func&lt;TEntity, bool&gt;&gt; predicate, DateTime? asOf = null, IEnumerable&lt;string&gt; includeProperties = null,
                                    bool trackChanges = false)
{
    var query = Set.Include(includeProperties)
                   .AsOf(asOf);

    if (!trackChanges)
    {
        query = query.AsNoTracking();
    }

    return await query.SingleAsync(predicate);
}
</code></pre>
<p>When executing this test, it works fine</p>
<pre><code>[Fact]
public static async Task GetStoffByStoffId_ReturnsEntity_OK_Test()
{
    // Arrange
    var dbContext = new SaiTestContext();
    IRepository&lt;StoffEntity&gt; repository = new Repository&lt;StoffEntity&gt;(dbContext);

    const string stoffId = &quot;645106EF59801EE59EB22F1F93673380&quot;;

    // Act
    var entity = await repository.GetAsync(stoff =&gt; stoff.StoffId == stoffId);

    // Assert
    Assert.NotNull(entity);
}
</code></pre>
<p>When executing this one</p>
<pre><code>[Fact]
public static async Task GetStoffByStoffIdPredicate_ReturnsEntity_OK_Test()
{
    // Arrange
    var dbContext = new SaiTestContext();
    IRepository&lt;StoffEntity&gt; repository = new Repository&lt;StoffEntity&gt;(dbContext);

    var stoffUpdate = new StoffUpdateEntity
                      {
                          StoffId = &quot;645106EF59801EE59EB22F1F93673380&quot;
                      };

    Func&lt;StoffEntity, StoffUpdateEntity, bool&gt; stoffSeletor =
        (stoffEntity, updateEntity) =&gt; stoffEntity.StoffId == stoffUpdate.StoffId;

    // Act
    var entity = await repository.GetAsync(stoff =&gt; stoffSeletor(stoff, stoffUpdate));

    // Assert
    Assert.NotNull(entity);
}
</code></pre>
<p>This exception is being thrown</p>
<pre><code>System.InvalidOperationException : The LINQ expression 'DbSet&lt;StoffEntity&gt;
    .Where(s =&gt; Invoke(__stoffSeletor_0, s[StoffEntity], __stoffUpdate_1)
    )' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at EntityFrameworkCore.TemporalTables.Query.AsOfQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at EntityFrameworkCore.TemporalTables.Query.AsOfQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
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
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, LambdaExpression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.SingleAsync[TSource](IQueryable`1 source, Expression`1 predicate, CancellationToken cancellationToken)
   at Refdata.SAI.Data.Repositories.Repository`1.GetAsync(Expression`1 predicate, Nullable`1 asOf, IEnumerable`1 includeProperties, Boolean trackChanges) in C:\dev\Refdata.SAI\Source\Refdata.SAI.Data\Repositories\Repository.cs:line 75
   at Refdata.SAI.Data.Tests.Integration.RepositoryGetByPredicateTests.GetStoffByStoffIdPredicate_ReturnsEntity_OK_Test() in C:\dev\Refdata.SAI\Source\Refdata.SAI.Data.Tests.Integration\RepositoryGetByPredicateTests.cs:line 61
--- End of stack trace from previous location where exception was thrown ---
</code></pre>
<p>Can the second test be fixed to work when passing the function as parameter?</p>
<p>The underlying reason is that I want to use this function from a generic class, where the function is being specified by <code>protected abstract Func&lt;TEntity, TUpdateEntity, bool&gt; EntitySelector { get; }</code> implement in the specialized classes.</p>

## Answers
### Answer ID: 63149293
<p>Expression can be compiled to the function, but arbitrary function cannot be converted back to the expression. stoffSeletor should return expression, not a function:</p>
<pre><code>Func&lt;StoffUpdateEntity, Expression&lt;Func&lt;StoffEntity, bool&gt;&gt;&gt; stoffSelector = 
    (stoffUpdate) =&gt; ((StoffEntity stoffEntity) =&gt; stoffEntity.StoffId == stoffUpdate.StoffId);
</code></pre>
<p>then</p>
<pre><code>// create predicate expression
var predicate = stoffSelector(stoffUpdate);

// use predicate
var entity = await repository.GetAsync(predicate);
    
    
    
</code></pre>
<p>or short version</p>
<pre><code>var entity = await repository.GetAsync(stoffSelector(stoffUpdate));
</code></pre>

