# .NetCore8 - Entity Framework - Mysql
[Link to question](https://stackoverflow.com/questions/77794323/netcore8-entity-framework-mysql)
**Creation Date:** 1704898741
**Score:** -1
**Tags:** c#, mysql, asp.net-core, pomelo-entityframeworkcore-mysql, asp.net-core-8
## Question Body
<p>Can you help me solve the problem with my code in .NetCore 8 with Entity Framework, database MySql where I use package Pomelo.EntityFrameworkCore.MySql.</p>
<p><strong>Models</strong>:</p>
<pre><code>public abstract class EntityBase
{
    public int Id { get; set; }
    public DateTime Created { get; protected set; } = DateTime.UtcNow;
    public DateTime Updated { get; set; } = DateTime.UtcNow;
}

public class Employee : EntityBase
{
    public string Name { get; set; }
    public PersonalData PersonalData { get; set; }
} 

public class PersonalData
{
    public Address Address { get; set; }    
    public IEnumerable&lt;Child&gt; Children { get; set; }
}

public class Child
{
    public string Name { get; set; }
    public DateTime DateOfBirth { get; set; }
    public int Height { get; set; }
}

public class Address
{
    public string Street { get; set; }
    public string City { get; set; }
    public int PostalCode { get; set; }
}
</code></pre>
<p><strong>Packages</strong> (up to date):</p>
<pre><code>&lt;ItemGroup&gt;
    &lt;PackageReference Include=&quot;Ardalis.SmartEnum&quot; Version=&quot;7.0.0&quot; /&gt;
    &lt;PackageReference Include=&quot;AutoMapper&quot; Version=&quot;12.0.1&quot; /&gt;
    &lt;PackageReference Include=&quot;AutoMapper.Extensions.Microsoft.DependencyInjection&quot; Version=&quot;12.0.1&quot; /&gt;
    &lt;PackageReference Include=&quot;Microsoft.AspNetCore.OpenApi&quot; Version=&quot;8.0.1&quot; /&gt;
    &lt;PackageReference Include=&quot;Microsoft.EntityFrameworkCore&quot; Version=&quot;8.0.1&quot; /&gt;
    &lt;PackageReference Include=&quot;Microsoft.EntityFrameworkCore.Design&quot; Version=&quot;8.0.1&quot;&gt;
      &lt;IncludeAssets&gt;runtime; build; native; contentfiles; analyzers; buildtransitive&lt;/IncludeAssets&gt;
      &lt;PrivateAssets&gt;all&lt;/PrivateAssets&gt;
    &lt;/PackageReference&gt;
    &lt;PackageReference Include=&quot;Microsoft.EntityFrameworkCore.Relational&quot; Version=&quot;8.0.1&quot; /&gt;
    &lt;PackageReference Include=&quot;Newtonsoft.Json&quot; Version=&quot;13.0.3&quot; /&gt;
    &lt;PackageReference Include=&quot;Pomelo.EntityFrameworkCore.MySql&quot; Version=&quot;8.0.0-beta.2&quot; /&gt;
    &lt;PackageReference Include=&quot;Pomelo.EntityFrameworkCore.MySql.Json.Microsoft&quot; Version=&quot;8.0.0-beta.2&quot; /&gt;
    &lt;PackageReference Include=&quot;Swashbuckle.AspNetCore&quot; Version=&quot;6.5.0&quot; /&gt;
  &lt;/ItemGroup&gt;
</code></pre>
<p><strong>AppDbContext.cs</strong></p>
<pre><code>public class AppDbContext : DbContext
{

    public AppDbContext(DbContextOptions&lt;AppDbContext&gt; options)
        : base(options)
    {}

    public DbSet&lt;Employee&gt; Employees =&gt; Set&lt;Employee&gt;();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());        
    }

    public override async Task&lt;int&gt; SaveChangesAsync(CancellationToken cancellationToken = new CancellationToken())
    {
        return await base.SaveChangesAsync(cancellationToken).ConfigureAwait(false);
    }

    public override int SaveChanges()
    {
        return SaveChangesAsync().GetAwaiter().GetResult();
    }
}
</code></pre>
<p><strong>EmployeeConfiguration.cs</strong></p>
<pre><code>public class EmployeeConfiguration : IEntityTypeConfiguration&lt;Employee&gt;
{
    public void Configure(EntityTypeBuilder&lt;Employee&gt; builder)
    {
        builder.Property(e =&gt; e.PersonalData)
            .HasConversion(
                v =&gt; ConvertToDatabase(v),
                v =&gt; ConvertFromDatabase(v))
            .HasColumnType(&quot;json&quot;); 
    }
            
    private static string ConvertToDatabase(PersonalData personalData)
    {
        return JsonSerializer.Serialize(personalData, default(JsonSerializerOptions));
    }

    private static PersonalData ConvertFromDatabase(string jsonData)
    {
        var result = JsonSerializer.Deserialize&lt;PersonalData&gt;(jsonData, default(JsonSerializerOptions));
        if (result == null)
        {
            throw new SerializationException(&quot;Unable to deserialize provided string&quot;);
        }
        return result;
    }
}
</code></pre>
<p>Query</p>
<pre><code>public async Task&lt;IEnumerable&lt;EmployeeResponse&gt;&gt; GetEmployeeChildAfterYear(int afterYear)
    {       
        var employees = await _context.Employees
             .Where(i =&gt; i.PersonalData.Children != null &amp;&amp; i.PersonalData.Children.Any(c =&gt; c.DateOfBirth.Year &gt;= afterYear))
             .ToListAsync(); 

        return _mapper.Map&lt;IEnumerable&lt;EmployeeResponse&gt;&gt;(employees);
    }
</code></pre>
<p>I'm getting an error:</p>
<blockquote>
<p>The LINQ expression 'c =&gt; c.DateOfBirth.Year &gt;= __afterYear_0' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>If I use:</p>
<pre><code>builder.OwnsOne(e =&gt; e.PersonalData, b =&gt; {
            b.ToJson(); 
            b.OwnsMany(p =&gt; p.Children);
            b.OwnsOne(e =&gt; e.Address);
        });
</code></pre>
<p>I'm getting an error:</p>
<blockquote>
<p>The EF Core 7.0 JSON support isn't currently implemented. Instead, there is support for a more extensive implementation.</p>
</blockquote>
<p>But I`m using:</p>
<blockquote>
<p>Entity Framework Core .NET Command-line Tools
8.0.1</p>
</blockquote>
<p>And ToJson() still isn`t supported in pomelo: <a href="https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql/issues/1752" rel="nofollow noreferrer">https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql/issues/1752</a></p>

## Answers
### Answer ID: 77824855
<p>I edited
<strong>Employee model</strong></p>
<pre><code>public class Employee : EntityBase
{    
    public string Name { get; set; } = null!;  
    public Address Address { get; set; }
    public IEnumerable&lt;Child&gt;? Children { get; set; }
} 
</code></pre>
<p><strong>EmployeeConfiguration.cs</strong></p>
<pre><code>    public class EmployeeConfiguration : IEntityTypeConfiguration&lt;Employee&gt;
    {
        public void Configure(EntityTypeBuilder&lt;Employee&gt; builder)
        {
            // MySQL
            builder.Property(e =&gt; e.Address)
                .HasColumnType(&quot;json&quot;);                    
            
            builder.Property(e =&gt; e.Children)
                .HasColumnType(&quot;json&quot;)
                .UseJsonChangeTrackingOptions(MySqlCommonJsonChangeTrackingOptions.RootPropertyOnly);
        }
    }
</code></pre>
<p><strong>Query</strong></p>
<pre><code>    public async Task&lt;IEnumerable&lt;EmployeeResponse&gt;&gt; GetEmployeesChildAfterYear(int afterYear)
    {   
        DateTime afterYearDate = new DateTime(afterYear,1,1);

        var employees = await _context.Employees
                                    .Where(i =&gt; i.Children != null &amp;&amp; 
                                                EF.Functions.JsonExtract&lt;DateTime&gt;(i.Children, &quot;$[0].DateOfBirth&quot;) &gt; afterYearDate)
                                    .ToListAsync();

        return _mapper.Map&lt;IEnumerable&lt;EmployeeResponse&gt;&gt;(employees);
    }
</code></pre>

