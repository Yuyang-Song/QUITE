# Linq GroupBy query not working with EF Core InMemory Database
[Link to question](https://stackoverflow.com/questions/75257150/linq-groupby-query-not-working-with-ef-core-inmemory-database)
**Creation Date:** 1674816953
**Score:** 1
**Tags:** linq, unit-testing, .net-core, group-by, in-memory-database
## Question Body
<p>I am testing my .Net7 Web API repository with an InMemoryDB. The query compiles and works with actual DB but does not work when testing with InMemoryDB.</p>
<p>Package Version of the Repository Project:</p>
<pre><code>&lt;PackageReference Include=&quot;Microsoft.EntityFrameworkCore.Design&quot; Version=&quot;7.0.0&quot;&gt;
      &lt;IncludeAssets&gt;runtime; build; native; contentfiles; analyzers; buildtransitive&lt;/IncludeAssets&gt;
      &lt;PrivateAssets&gt;all&lt;/PrivateAssets&gt;
    &lt;/PackageReference&gt;
    
    &lt;PackageReference Include=&quot;Microsoft.EntityFrameworkCore.InMemory&quot; Version=&quot;7.0.0&quot; /&gt;
</code></pre>
<p>Error Message When Running the Test:</p>
<pre><code> Error Message:
   System.InvalidOperationException : The LINQ expression 'DbSet&lt;TestSession&gt;()
    .GroupBy(t =&gt; t.DutModel)' could not be translated. Additional information: A 'GroupBy' operation which is not composed into aggregate or projection of elements is not supported. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
  Stack Trace:
</code></pre>
<p>The Test Class looks like this: I am using xUnit Collection Feature to get a single Test DB instance.</p>
<pre><code>[Collection(&quot;Database collection&quot;)]
class RepoTests
{
    [Fact]
    public async Task Test12322()
    {
        // Arrange
        var repo = new SessionRepository(_fixture.DbContext);
        var sessionParams = new SessionParams();

        // Act
        var dutModelGroup = await repo.Test(sessionParams);

        // Assert
        Assert.Equal(0, dutModelGroup.Count);
    }
}
</code></pre>
<p>The Repository Class is as below</p>
<p>This Implementation of the Test Method fails the test.
This exact methods works with actual SQL Database</p>
<pre><code>class SessionRepo 
{
    public async Task&lt;dynamic&gt; Test(SessionParams sessionParams)
    {
        var result = await _context
                            .TestSessions
                            .GroupBy(s =&gt; s.DutModel)
                            .ToListAsync();

        return result;
    }
}
</code></pre>
<p>This Implementation of the Test Method passes the test.</p>
<pre><code>class SessionRepo 
{
  public async Task&lt;dynamic&gt; Test(SessionParams sessionParams)
     {
        var result = await _context
                            .TestSessions
                            .ToListAsync();

        return result.GroupBy(s =&gt; s.DutModel).ToList();
    }
}
</code></pre>

