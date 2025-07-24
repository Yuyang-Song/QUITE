# Can&#39;t search on List&lt;KeyValuePair&gt; saved as JSON string on DB using expression on ASP.NET Core using Entity Framework Core
[Link to question](https://stackoverflow.com/questions/79105135/cant-search-on-listkeyvaluepair-saved-as-json-string-on-db-using-expression-o)
**Creation Date:** 1729347181
**Score:** 0
**Tags:** c#, asp.net-core, entity-framework-core
## Question Body
<p>I have table in my database which has a nullable string column <code>ExtraInfo</code>. Its value is JSON of <code>List&lt;KeyValuePair&gt;</code>, for example like this</p>
<pre><code>{ &quot;StaffCode&quot;: &quot;123&quot; }
</code></pre>
<p>As we added pagination for search we send filter as expression.</p>
<p>Here is my code:</p>
<pre><code>public async Task&lt;List&lt;CusFinRequest&gt;&gt; GetDealsWithPagination(int organiztionId,string staffCode, int index, int size)
{
    var filter = PredicateBuilder.New&lt;CusFinRequest&gt;();
    
    if (organiztionId != default(int))
    {
        filter.And(x =&gt; x.Organization == organiztionId);
    }

    if (!string.IsNullOrEmpty(staffCode))
    {
        filter.And(x =&gt; x.ExtraInfo != null &amp;&amp;
                        Newtonsoft.Json.JsonConvert.DeserializeObject&lt;List&lt;KeyValuePair&lt;string, string&gt;&gt;&gt;(x.ExtraInfo).ToList().FirstOrDefault(x =&gt; x.Key == &quot;StaffCode&quot;).Value == staffCode);
    }

    Func&lt;IQueryable&lt;CusFinRequest&gt;, IOrderedQueryable&lt;CusFinRequest&gt;&gt; orderBy = q =&gt; q.OrderByDescending(e =&gt; e.CreationDate);5

    return (await GetPaged(filter, orderBy, index, size, null, 0, &quot;RequestHistory&quot;, &quot;UserCart&quot;, &quot;UserCart.BusinessLine&quot;)).ToList();
}

public async virtual Task&lt;List&lt;TEntity&gt;&gt; GetPaged(Expression&lt;Func&lt;TEntity, bool&gt;&gt; filter = null,
           Func&lt;IQueryable&lt;TEntity&gt;, IOrderedQueryable&lt;TEntity&gt;&gt; orderBy = null,
           int pageIndex = 0, int pageSize = 0,
           string sortColumnName = &quot;&quot;, int sortDirection = 0,
           params string[] includes)
{
    IQueryable&lt;TEntity&gt; query = dbSet;

    if (includes != null)
    {
        foreach (string include in includes)
            query = query.Include(include);
    }

    if (filter != null)
        query = query.Where(filter);

    if (orderBy != null)
        query = orderBy(query);

    if (pageIndex != default(int) &amp;&amp; pageSize != default(int))
    {
        if (pageSize != -1) // Check if pageIndex is not -1 to retrieve all data
        {
            query = query.Skip((pageIndex - 1) * pageSize).Take(pageSize);
        }
    }

    return await query.ToListAsync();
}
</code></pre>
<p>I got this issue after I looked for staff code.</p>
<p>I tried to update my expression to handle null keyvaluepair of Staffcode but I got a build error</p>
<pre><code>{
  &quot;StackTrace&quot;: &quot; at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\r\n at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\r\n at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\r\n at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()\r\n at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)\r\n at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)\r\n at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)\r\n at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)\r\n at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1.GetAsyncEnumerator()\r\n at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)\r\n at Ifin.Persistence.Repositories.BaseRepository`1.GetPaged(Expression`1 filter, Func`2 orderBy, Int32 pageIndex, Int32 pageSize, String sortColumnName, Int32 sortDirection, String[] includes) in D:\\CoreProject\\Ifin.Repositories\\Repositories\\BaseRepository.cs:line 146\r\n at Ifin.Persistence.Repositories.CusFinRequestRepository.GetByAdvancedSearchPaginated(String customerId, String mobile, Nullable`1 BankId, String status, Int32 organiztionId, Nullable`1 startDate, Nullable`1 endDate, Nullable`1 maxAmount, Nullable`1 minAmount, String customerCIF, String staffCode, Int32 index, Int32 size) in D:\\CoreProject\\Ifin.Repositories\\Repositories\\CusFinRequestRepository.cs:line 91\r\n at Ifin.Business.Service.InquairyService.PaginatedSearch(Request`1 request) in D:\\CoreProject\\Ifin.Business\\Service\\InquairyService.cs:line 367\r\n at Ifin.Api.Controllers.InquiryController.PaginatedSearch(Request`1 request) in D:\\CoreProject\\Ifin.Api\\Controllers\\InquiryController.cs:line 77&quot;,
  &quot;Message&quot;: &quot;The LINQ expression 'DbSet&lt;CusFinRequest&gt;\r\n .Where(c =&gt; c.ExtraInfo == null ? False : JsonConvert.DeserializeObject&lt;List&lt;KeyValuePair&lt;string, string&gt;&gt;&gt;(c.ExtraInfo)\r\n  .Where(x =&gt; x.Key == \&quot;StaffCode\&quot;)\r\n  .Select(s =&gt; s.Value)\r\n  .FirstOrDefault() == __staffCode_0 &amp;&amp; c.Organization == __organiztionId_1)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.&quot;,
  &quot;Data&quot;: {},
  &quot;InnerException&quot;: null,
  &quot;HelpLink&quot;: null,
  &quot;Source&quot;: &quot;Microsoft.EntityFrameworkCore&quot;,
  &quot;HResult&quot;: -2146233079
}
</code></pre>
<p>from this</p>
<pre><code>The LINQ expression 'DbSet\r\n .Where(c =&gt; c.ExtraInfo == null ? False : JsonConvert.DeserializeObject&lt;List&lt;KeyValuePair&lt;string, string&gt;&gt;&gt;(c.ExtraInfo)\r\n .Where(x =&gt; x.Key == &quot;StaffCode&quot;)\r\n .Select(s =&gt; s.Value)\r\n .FirstOrDefault() == __staffCode_0 &amp;&amp; c.Organization == __organiztionId_1)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>
<p>I can understand that linq expression couldn't translated to find value by key in this JSON.</p>
<p>What is the right solution for this scenario?</p>

