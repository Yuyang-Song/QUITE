# EF Core 3 - Simple &#39;Where&#39; Query throwing Error?
[Link to question](https://stackoverflow.com/questions/64379600/ef-core-3-simple-where-query-throwing-error)
**Creation Date:** 1602795645
**Score:** 1
**Tags:** c#, entity-framework-core, azure-functions
## Question Body
<p>I've built a small Http Azure Function which queries a database. I'm doing a query like so...</p>
<pre><code>var item = await DbContext.Items
                          .Where(x =&gt; x.ItemId == itemId &amp;&amp; x.IsActive)
                          .ToListAsync();
</code></pre>
<p>Now when I do this it throws an error:</p>
<blockquote>
<p>System.Private.CoreLib: Exception while executing function: Test. Microsoft.EntityFrameworkCore: The LINQ expression 'DbSet
[2020-10-15T20:56:40.424]     .Where(r =&gt; r.ItemId== __itemId_0 &amp;&amp; r.IsActive == True)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>Once I remove the <code>&amp;&amp;</code> and make it querying a singular property then it works. I've looked at other posts where they get the same error message but they're using more complex operations in their queries. Here, it's simple and I know it can be done as the Entity Framework Core documentation even uses an example such as this. I've also tried using <code>ToListAsync()</code> on the <code>IQueryable</code> and still nothing. <code>FirstOrDefault()</code>, <code>FirstOrDefaultAsync()</code> have also both been tried.</p>
<p>Here is my DbContext...</p>
<pre><code>public class ApplicationDbContext : IdentityDbContext&lt;ApplicationUser, ApplicationRole, int&gt;
{
    #region DbSets 

    public DbSet&lt;Item&gt; Items { get; set; }

    #endregion

    #region Constructors

    public ApplicationDbContext(DbContextOptions&lt;ApplicationDbContext&gt; options)
        : base(options)
    {
    }

    #endregion
}
</code></pre>
<p>and here is my item entity...</p>
<pre><code>public class Item
{
    #region Column Definitions

    [Key]
    public int Id { get; set; }

    public int ItemId { get; set; }

    public bool IsActive { get; set; }

    #endregion
}
</code></pre>

