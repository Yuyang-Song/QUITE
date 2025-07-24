# EF Core 3.1 does not allow Contains search on Enum property
[Link to question](https://stackoverflow.com/questions/61161068/ef-core-3-1-does-not-allow-contains-search-on-enum-property)
**Creation Date:** 1586626760
**Score:** 7
**Tags:** c#, enums, entity-framework-core, entity-framework-core-3.1
## Question Body
<p>I'm trying to do a contains search on <code>enum</code> property in my <code>DbSet</code> and EF Core 3.1 throws the below error</p>

<blockquote>
  <p>The LINQ expression 'DbSet .Where(d =>
  d.Position.ToString().Contains("acc"))' could not be translated.
  Either rewrite the query in a form that can be translated, or switch
  to client evaluation explicitly by inserting a call to either
  AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()</p>
</blockquote>

<p>Entity:</p>

<pre class="lang-cs prettyprint-override"><code>public class DemoEntity
{
    [Key]
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public Position Position { get; set; }
}
</code></pre>

<p>Enum - Position:</p>

<pre class="lang-cs prettyprint-override"><code>public enum Position
{
    [Display(Name = "Accountant")]
    Accountant,
    [Display(Name = "Chief Executive Officer (CEO)")]
    ChiefExecutiveOfficer,
    [Display(Name = "Integration Specialist")]
    IntegrationSpecialist,
    [Display(Name = "Junior Technical Author")]
    JuniorTechnicalAuthor,
    [Display(Name = "Pre Sales Support")]
    PreSalesSupport,
    [Display(Name = "Sales Assistant")]
    SalesAssistant,
    [Display(Name = "Senior Javascript Developer")]
    SeniorJavascriptDeveloper,
    [Display(Name = "Software Engineer")]
    SoftwareEngineer
}
</code></pre>

<p>DbContext:</p>

<pre class="lang-cs prettyprint-override"><code>public class DemoDbContext : DbContext
{
    public DemoDbContext(DbContextOptions options)
        : base(options) { }

    public DbSet&lt;DemoEntity&gt; Demos { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder
            .Entity&lt;DemoEntity&gt;()
            .Property(e =&gt; e.Position)
            .HasConversion&lt;string&gt;();
    }
}
</code></pre>

<p>When I query the table as follows I'm getting the error</p>

<pre class="lang-cs prettyprint-override"><code>try
{
    var test = await _context.Demos.Where(x =&gt; x.Position.ToString().Contains("acc")).ToListAsync();
}
catch (System.Exception e)
{
    //throw;
}
</code></pre>

<p>The Position is of type <code>NVARCHAR(MAX)</code> in my database.</p>

<p><a href="https://i.sstatic.net/y9eSd.png" rel="noreferrer"><img src="https://i.sstatic.net/y9eSd.png" alt="enter image description here"></a></p>

<p><a href="https://i.sstatic.net/0jPdz.png" rel="noreferrer"><img src="https://i.sstatic.net/0jPdz.png" alt="enter image description here"></a></p>

<p>This is not possible? If so please can you help me with explanation?</p>

## Answers
### Answer ID: 61579224
<p>This issue has been logged in <a href="https://github.com/dotnet/efcore/issues/20604" rel="nofollow noreferrer">efcore github repo</a> and here is the workaround for this now. The <code>enum</code> property needs to be casted into <code>object</code> and then to <code>string</code></p>
<pre class="lang-cs prettyprint-override"><code>var test = await _context.Demos.Where(x =&gt; ((string) (object)x.Position).Contains(&quot;acc&quot;)).ToListAsync();
</code></pre>
<p>Hope this helps someone out there.</p>

