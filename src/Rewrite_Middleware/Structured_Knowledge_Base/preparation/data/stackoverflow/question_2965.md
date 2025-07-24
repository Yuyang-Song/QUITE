# The LINQ expression &#39;DbSet&lt;Contacts&gt;\n .Where(c =&gt; __res_RelatedContacts_0\n.Any(r =&gt; r.IdVal.Equals(c.ContactId)))&#39; could not be translated
[Link to question](https://stackoverflow.com/questions/60440462/the-linq-expression-dbsetcontacts-n-wherec-res-relatedcontacts-0-n-any)
**Creation Date:** 1582831748
**Score:** 0
**Tags:** c#, entity-framework-core, ef-core-3.1
## Question Body
<p>I am using asp.net core 3.1 and EFCore 3.1.1.</p>

<p>Code :</p>

<pre><code>public class SampleDbContext : DbContext
{
    public DbSet&lt;Articles&gt; Articles
    {
        get;
        set;
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var converter = new NumberToStringConverter&lt;int&gt;();
        // For Articles
        modelBuilder.Entity&lt;Articles&gt;().OwnsMany(p =&gt; p.RelatedCountries, a =&gt;
        {
            a.WithOwner().HasForeignKey("Articlesid");
            a.Property&lt;int&gt;("id");
            a.Property(o =&gt; o.IdVal);
        }

        );
    }
}

public class Articles
{
    public int ArticleId
    {
        get;
        set;
    }

    public ICollection&lt;RelatedEntityId&gt; RelatedContacts
    {
        get;
        set;
    }
}

public class RelatedEntityId
{
    public int IdVal
    {
        get;
        set;
    }
}
</code></pre>

<p>My Service class :</p>

<pre><code>public class ArticleService : IArticleService
{
    private readonly SampleDbContext _dbContext;
    private readonly ICacheService&lt;Images, ImageDTO&gt; _imageCacheService;
    private readonly ICacheService&lt;Countries, CountryDTO&gt; _countryCacheService;
    private readonly ICommonService _commonService;
    private readonly IMapper _mapper;
    public ArticleService(SampleDbContext dbContext, ICacheService&lt;Images, ImageDTO&gt; imageCacheService, ICacheService&lt;Countries, CountryDTO&gt; countryCacheService, ICommonService commonService, IMapper mapper)
    {
        _dbContext = dbContext ?? throw new ArgumentNullException(nameof(dbContext));
        _imageCacheService = imageCacheService ?? throw new ArgumentNullException(nameof(imageCacheService));
        _countryCacheService = countryCacheService ?? throw new ArgumentNullException(nameof(countryCacheService));
        _commonService = commonService ?? throw new ArgumentNullException(nameof(commonService));
        _mapper = mapper ?? throw new ArgumentNullException(nameof(mapper));
    }

    public async Task&lt;ArticleDTO&gt; GetArticleDetailsAsync(int articleId, int defaultLanguageId, List&lt;int&gt; localeLanguageIdList)
    {
        // Get articles
        var articles = await _dbContext.Articles.Where(a =&gt; a.ArticleId.Equals(articleId) &amp;&amp; a.IsPublished.Equals(true)).OrderByDescending(a =&gt; a.ArticleId).Select(a =&gt; new
        {
        a.ArticleId, a.PublishedDate, a.Author, a.ImageId, a.State, a.Type, a.SubType, a.ResourcePosition, a.DisclaimerId, a.CreatedDate, a.UpdatedDate, a.NotificationSentDate, a.Title, a.TeaserText, a.Content, a.RelatedContacts, a.LanguageId
        }

        ).AsNoTracking().ToListAsync();
        var res = articles.Where(a =&gt; a.LanguageId.Equals(defaultLanguageId) &amp;&amp; Convert.ToDateTime(a.PublishedDate) &lt;= DateTime.UtcNow).FirstOrDefault();
        var contacts = new List&lt;ContactDTO&gt;();
        if (res.RelatedContacts.Count &gt; 0)
        {
            contacts = await _dbContext.Contacts.Where(co =&gt; res.RelatedContacts.Any(r =&gt; r.IdVal.Equals(co.ContactId))).ToListAsync();
        }
    }
}
</code></pre>

<p>Error Message:</p>

<blockquote>
  <p>"message": "GraphQL.ExecutionError: The LINQ expression 'DbSet\n    .Where(c => __res_RelatedContacts_0\n        .Any(r => r.IdVal.Equals(c.ContactId)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.\n ---> System.InvalidOperationException: The LINQ expression 'DbSet\n    .Where(c => __res_RelatedContacts_0\n        .Any(r => r.IdVal.Equals(c.ContactId)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;>c__DisplayClass8_0&amp; )\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\n   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)\n   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)\n   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\n   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;>c__DisplayClass12_0<code>1.&lt;ExecuteAsync&gt;b__0()\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func</code>1 compiler)\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func<code>1 compiler)\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable</code>1.GetAsyncEnumerator(CancellationToken cancellationToken)\n   at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable<code>1.GetAsyncEnumerator()\n   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsync[TSource](IQueryable</code>1 source, CancellationToken cancellationToken)\n   at Author.Query.Persistence.ArticleService.GetArticleDetailsAsync(Int32 articleId, Int32 defaultLanguageId, List<code>1 localeLanguageIdList) in /src/QueryStack/Author.Query.Persistence/ArticleService.cs:line 88\n   at Author.Query.Persistence.ArticleService.GetArticleAsync(Int32 articleId, String countryName) in /src/QueryStack/Author.Query.Persistence/ArticleService.cs:line 47\n   at GraphQL.DataLoader.DataLoaderBase</code>1.DispatchAsync(CancellationToken cancellationToken)\n   at Author.Query.New.API.GraphQL.Resolvers.ArticlesResolver.&lt;>c__DisplayClass3_1.&lt;b__2>d.MoveNext() in /src/QueryStack/Author.Query.New.API/GraphQL/Resolvers/ArticlesResolver.cs:line 41\n--- End of stack trace from previous location where exception was thrown ---\n   at GraphQL.Types.ResolveFieldContext<code>1.TryAsyncResolve[TResult](Func</code>2 resolve, Func`2 error)\n   --- End of inner exception stack trace ---"</p>
</blockquote>

<p>Can anyone help me to know how to fix this issue?</p>

