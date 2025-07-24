# When I retrieve GetAllAsQueryable from the repository and add a where clause, I get an error. Either rewrite the query
[Link to question](https://stackoverflow.com/questions/77984193/when-i-retrieve-getallasqueryable-from-the-repository-and-add-a-where-clause-i)
**Creation Date:** 1707770142
**Score:** 0
**Tags:** c#, .net, linq, repository, asqueryable
## Question Body
<pre><code>public async Task&lt;IEnumerable&lt;T&gt;&gt; GetAllAsync() {
    var dataAsQueryable = repository.GetAllAsQueryable();
    if (typeof(TenantEntity).IsAssignableFrom(typeof(T))) {
        var tenantId = currentUserService.GetCurrentTenantId();

        if (tenantId is null or 0) {
            return await dataAsQueryable.ToListAsync();
        }

        var tenantIdProperty = typeof(T).GetProperty(&quot;TenantId&quot;, BindingFlags.Public | BindingFlags.Instance);
        if (tenantIdProperty != null) {
            dataAsQueryable = dataAsQueryable.Where(entity =&gt; (long)tenantIdProperty.GetValue(entity) == (long)tenantId);
        }
    }
    return dataAsQueryable;
}
</code></pre>
<p><code> public IQueryable&lt;TEntity&gt; GetAllAsQueryable() { return _dbSet.AsQueryable(); }</code></p>
<p>TenantId cannot be null in database and type is long.
When try to get this query throwing exception like this:
Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>

## Answers
### Answer ID: 78150045
<p>This line cannot be translated into a sql call because of the reflection used for accessing the property:</p>
<pre><code>dataAsQueryable = dataAsQueryable.Where(entity =&gt; (long)tenantIdProperty.GetValue(entity) == (long)tenantId);
</code></pre>
<p>If reflection is required (unlikely), then you'll have to do the filtering outside of the query:</p>
<pre><code>dataAsQueryable = dataAsQueryable.ToArray().Where(entity =&gt; (long)tenantIdProperty.GetValue(entity) == (long)tenantId);
</code></pre>
<p>I recommend you investigate <a href="https://stackoverflow.com/questions/50814131/c-sharp-dynamic-database-filtering-with-linq-expression">Expressions</a> to do the filtering which would allow a completely sql-side execution and maximum performance.</p>

