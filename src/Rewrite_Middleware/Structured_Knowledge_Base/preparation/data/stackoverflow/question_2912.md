# How to modify expression-based filters to avoid client-side evaluation in Entity Framework Core 3.0
[Link to question](https://stackoverflow.com/questions/58302163/how-to-modify-expression-based-filters-to-avoid-client-side-evaluation-in-entity)
**Creation Date:** 1570617045
**Score:** 3
**Tags:** c#, entity-framework-core-3.0
## Question Body
<p>I have the following code that used to convert <code>Func</code>-based filters to <code>Expression</code> and filter the data in <em>Entity Framework Core 2.2</em>:</p>

<pre><code>public async Task&lt;TType&gt; GetDataAsync&lt;TType&gt;(Func&lt;TType, bool&gt; filtering = null) where TType : class
{
  Expression&lt;Func&lt;TType, bool&gt;&gt; filteringExpression = (type) =&gt; filtering(type);
  if (filtering != null)
    //return await myContext.Set&lt;TType&gt;().FirstOrDefaultAsync(filteringExpression);
    return await myContext.Set&lt;TType&gt;().Where(filteringExpression ).FirstOrDefaultAsync();
  return await myContext.Set&lt;TType&gt;().FirstOrDefaultAsync();
}
</code></pre>

<p>This is how I use it:</p>

<pre><code>public async Task&lt;DataLog&gt; GetDataLogByID(Guid dataLogID) =&gt; await GetDataAsync&lt;DataLog&gt;(dataLog =&gt; dataLog.ID == dataLogID);
</code></pre>

<p>(Un)fortunately, when I upgraded to <em>Entity Framework Core 3.0</em>, the code threw an <code>InvalidOperationException</code> as the expression can't be turned into SQL query (although it filters only a property that matches a database column):</p>

<blockquote>
  <p>System.InvalidOperationException: 'The LINQ expression
  'Where(
      source: DbSet, 
      predicate: (f) => Invoke(__filtering_0, f[DataLog]) )' could not be translated. Either rewrite the query in a form that can be
  translated, or switch to client evaluation explicitly by inserting a
  call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
  ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
  more information.</p>
</blockquote>

<p>So can you tell me, how I should modify the code to make sure that all (most) of the processing stay on the server side? What is the best practice to keep the generic code yet comply with the standards?</p>

## Answers
### Answer ID: 58304247
<p>Congratulations, you've discovered one of the breaking changes in EF Core 3.0 - <a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.0/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client" rel="nofollow noreferrer">LINQ queries are no longer evaluated on the client</a></p>
<blockquote>
<p><strong>Old behavior</strong></p>
<p>Before 3.0, when EF Core couldn't convert an expression that was part of a query to either SQL or a parameter, it automatically evaluated the expression on the client. By default, client evaluation of potentially expensive expressions only triggered a warning.</p>
<p><strong>New behavior</strong></p>
<p>Starting with 3.0, EF Core only allows expressions in the top-level projection (the last Select() call in the query) to be evaluated on the client. When expressions in any other part of the query can't be converted to either SQL or a parameter, an exception is thrown.</p>
</blockquote>
<p>See the docs (link above) for more info, but the warnings you experienced before upgrading are now generating InvalidOperationExceptions and has nothing to do with SQLite, you'd get the same issues with SQL Server.</p>
<p>Only way around this is to ensure that your filtering expression/func can be converted to appropriate SQL... or revert to EF Core &lt; 3.0</p>
<p><strong>UPDATE</strong></p>
<p>You could try <em>not</em> wrapping the passed Func and change the parameter type to <code>Expression&lt;Func&lt;TType, bool&gt;&gt;</code> (it shouldn't require any changes to code calling the method)</p>
<pre><code>public async Task&lt;TType&gt; GetDataAsync&lt;TType&gt;(Expression&lt;Func&lt;TType, bool&gt;&gt; filter = null)
    where TType : class
{
    var query = myContext.Set&lt;TType&gt;();

    if (filter != null)
        query = query.Where(filter);

    return await query.FirstOrDefaultAsync();
}
</code></pre>
<p>Just noticed that the call to <code>GetDataAsync</code> appears to be incorrect and has an extra type parameter <code>Guid</code> which should be removed from this example.</p>
<pre><code>public async Task&lt;DataLog&gt; GetDataLogByID(Guid dataLogID) =&gt;
    await GetDataAsync&lt;DataLog&gt;(dataLog =&gt; dataLog.ID == dataLogID);
</code></pre>

