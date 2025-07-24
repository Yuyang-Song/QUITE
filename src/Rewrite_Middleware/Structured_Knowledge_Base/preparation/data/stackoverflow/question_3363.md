# ExecuteDeleteAsync throws error on inmemory db
[Link to question](https://stackoverflow.com/questions/77277868/executedeleteasync-throws-error-on-inmemory-db)
**Creation Date:** 1697087802
**Score:** 1
**Tags:** c#, entity-framework, .net-6.0, in-memory-database, ef-core-7.0
## Question Body
<p>I was implementing the latest ef core 7 features ExecuteDeleteAsync(). Since that my test is failing. But is working on a real MsSql Server. I'm using an <em><strong>inmemory db</strong></em> and I am not sure if this is not working because of this statement:</p>
<blockquote>
<p>However, it is sometimes useful to execute update or delete commands on the database without involving the change tracker. EF7 enables this with the new ExecuteUpdate and ExecuteDelete methods. These methods are applied to a LINQ query and will update or delete entities in the database based on the results of that query.</p>
</blockquote>
<p>In Memory DB is Microsoft.EntityFrameworkCore.InMemory and in it's latest version.</p>
<pre><code>public async Task&lt;int&gt; DeleteWhere(Expression&lt;Func&lt;T, bool&gt;&gt; predicate)
{
  var amount = await _dbSet.Where(predicate).ExecuteDeleteAsync();
  return amount;
}
</code></pre>
<p>Here is my db context:</p>
<pre><code> public DashboardDbContext CreateDashboardContext()
    {
        var dbName = $&quot;xUnitTest{_instanceCount++}&quot;;
        var builder = new DbContextOptionsBuilder&lt;DashboardDbContext&gt;();

        builder.UseInMemoryDatabase(dbName);

        return new DashboardDbContext(builder.Options);
    }
</code></pre>
<p>Exception:</p>
<blockquote>
<p>{&quot;The LINQ expression 'DbSet()\r\n<br />
.Where(b =&gt; b.ModifiedTime &lt; __dateToKeepData_0)\r\n    .ExecuteDelete()' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;}</p>
</blockquote>

## Answers
### Answer ID: 77277961
<p>Assuming <code>ModifiedTime</code> is a DateTime field in your model and correctly represents your database and <code>dateToKeepData</code> is a local DateTime variable in your code, it <em>should</em> work.</p>
<p>But please note that you should not use the InMemory Database for your unit tests. Quoting Microsoft themselves:</p>
<blockquote>
<p>While some users use the in-memory database for testing, this is discouraged.</p>
</blockquote>
<p>You can use other in memory databases, like SQLite. That should work. I'm doing exaxtly that in my code and with SQLite it works fine. Maybe time to heed Microsofts warning and switch to a proper in memory database, not just Microsofts mock version of one.</p>

