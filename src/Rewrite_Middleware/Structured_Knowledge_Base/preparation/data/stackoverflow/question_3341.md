# Refactoring my repository from using Ardalis to only use .NET 6 library, strugling with &quot;Linq expression could not be translated&quot;
[Link to question](https://stackoverflow.com/questions/76866958/refactoring-my-repository-from-using-ardalis-to-only-use-net-6-library-strugli)
**Creation Date:** 1691577636
**Score:** 1
**Tags:** c#, .net, sql-server, entity-framework, linq
## Question Body
<p>I am refactoring a .NET 6/entity framework core 7 project which used to handle repository calls through Ardalis and Ardalis Specifications to add conditions to repository calls.</p>
<p>The idea of this refactoring is to only use Linq expressions and IQueryable instead of Ardalis specifications. I have a generic abstract repository class which all repositories can inherit of.</p>
<p>On paper, I was happy with the result and my code is compiling fine, unfortunatley when doing some tests on my API routes through Postman, I got the error : &quot;Linq Expression  could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'&quot;</p>
<p>I will show you the code I had at first:</p>
<pre class="lang-cs prettyprint-override"><code>public abstract class GenericDbContextRepository&lt;T, TKey&gt; : IRepository&lt;T, TKey&gt; where T : class
{
    protected readonly DbContext GenericDbContext;
    protected readonly DbSet&lt;T&gt; DbSet;

    protected GenericDbContextRepository(DbContext DbContext)
    {
        GenericDbContext = DbContext;
        DbSet = GenericDbContext.Set&lt;T&gt;();
    }

    public async Task&lt;IEnumerable&lt;T&gt;&gt; FindAsync(Expression&lt;Func&lt;T, bool&gt;&gt; expression, IQueryable&lt;T&gt; query)
    {
        var originalQuery = DbSet.AsQueryable();
        var finalQuery = originalQuery.Concat(query);
        return await finalQuery.Where(expression).ToListAsync();
    }
}
</code></pre>
<p>For example, my repository &quot;UserStoreRepository&quot; would call FindAsync and it would pass the following IQueryable :</p>
<pre class="lang-cs prettyprint-override"><code>public static IQueryable&lt;UserStore&gt; GetUserStoreWithItemsQuery()
{
    IQueryable&lt;UserStore&gt; initialQuery = Enumerable.Empty&lt;UserStore&gt;().AsQueryable();
    return initialQuery
        .OrderByDescending(x =&gt; x.CreationDate)
        .Take(1)
        .Include(UserStore =&gt; UserStore.Items);
}
</code></pre>
<p>On first try, I got the following error:</p>
<blockquote>
<p>&quot; The Linq Expression 'EnumerableQuery{}' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'&quot;</p>
</blockquote>
<p>One of my first idea to fix this issue was simply to follow the recommendation in the error message and use AsEnumerable() in my GetUserStoreWithItemsQuery() function, I ended up with the following code:</p>
<pre class="lang-cs prettyprint-override"><code>public static IQueryable&lt;UserStore&gt; GetUserStoreWithItemsQuery()
{
    IQueryable&lt;UserStore&gt; initialQuery = Enumerable.Empty&lt;UserStore&gt;().AsQueryable();
    
    return initialQuery
        .AsEnumerable()
        .OrderByDescending(x =&gt; x.CreationDate)
        .Take(1)
        .AsQueryable()
        //Include can only be used on IQueryable, not on IEnumerable
        .Include(UserStore =&gt; UserStore.Items);
}
</code></pre>
<p>The Linq expression's translation here worked and I ended up with a new error from my  FindAsync() function :</p>
<blockquote>
<p>&quot; The Linq Expression 'DbSet{}' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'&quot;</p>
</blockquote>
<p>I thought of applying the same fix with AsEnumerable():</p>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IEnumerable&lt;T&gt;&gt; FindAsync(Expression&lt;Func&lt;T, bool&gt;&gt; expression, IQueryable&lt;T&gt; query)
{
    var originalQuery = DbSet.AsEnumerable();
    var finalQuery = originalQuery.Concat(query.AsEnumerable());
    return await finalQuery.AsQueryable().Where(expression).ToListAsync();
}
</code></pre>
<p>But now I have the following error :</p>
<blockquote>
<p>The provider for the source 'IQueryable' doesn't implement 'IAsyncQueryProvider'. Only providers that implement 'IAsyncQueryProvider' can be used for Entity Framework asynchronous operations.</p>
</blockquote>
<p>I probably could &quot;bypass&quot; and implement 'IAsyncQueryProvider' but I feel like I should not have to, I am guessing there must be a better and cleaner way to achieve what I am trying to, and I am starting to think switching to Enumerable then back to IQueryable is probably not the good way of doing things, whether for code/database call performance and code quality. I welcome any advices and fixes.</p>
<p>Thank you all.</p>

## Answers
### Answer ID: 76867619
<p>I think, in your particular case, the <code>FindAsync</code> method could be similar to this one, please take a look:</p>
<pre class="lang-cs prettyprint-override"><code>public virtual Task&lt;IEnumerable&lt;TEntity&gt;&gt; FindAsync(
    Expression&lt;Func&lt;TEntity, bool&gt;&gt;? predicate = null,
    CancellationToken token = default,
    params Expression&lt;Func&lt;TEntity, object&gt;&gt;[] navigationProperties)
{
    IQueryable&lt;TEntity&gt; dbQuery = _dbSet.AsNoTracking();

    if (predicate != null)
    {
        dbQuery = dbQuery.Where(predicate);
    }

    return await navigationProperties
        .Aggregate(dbQuery, (current, navigationProperty) =&gt; current.Include(navigationProperty))
        .ToListAsync(token);
}
</code></pre>

