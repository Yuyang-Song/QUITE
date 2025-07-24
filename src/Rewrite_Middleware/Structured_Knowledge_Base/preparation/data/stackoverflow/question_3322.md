# How do I project a collection inside a JSON column with EF Core 7?
[Link to question](https://stackoverflow.com/questions/76374551/how-do-i-project-a-collection-inside-a-json-column-with-ef-core-7)
**Creation Date:** 1685543179
**Score:** 1
**Tags:** entity-framework-core
## Question Body
<ul>
<li>EF Core version: 7.0.4</li>
<li>Database provider: Microsoft.EntityFrameworkCore.SqlServer (SQL Server 2019)</li>
<li>Target framework: .NET 7.0</li>
</ul>
<p>Given the following models, I am unable to project the <code>AddressesData.AddressList</code> property when it is stored as a JSON column.</p>
<pre class="lang-c# prettyprint-override"><code>public class AddressData
{
    public string FirstLine { get; set; } = null!;
    public string? SecondLine { get; set; }
    public string City { get; set; } = null!;
    public string PostCode { get; set; } = null!;
    public string CountryCode { get; set; } = null!;
}
</code></pre>
<pre class="lang-c# prettyprint-override"><code>public class AddressesData
{
    public int? Primary { get; set; }
    public ICollection&lt;AddressData&gt; AddressList { get; set; } = new List&lt;AddressData&gt;();
}
</code></pre>
<pre class="lang-c# prettyprint-override"><code>public class CustomerData
{
    public AddressesData Addresses { get; set; } = new();
}
</code></pre>
<p>Fluent Configuration</p>
<pre class="lang-c# prettyprint-override"><code>protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity&lt;CustomerData&gt;().OwnsOne(c =&gt; c.Addresses, builder =&gt;
    {
        builder.ToJson();
        builder.OwnsMany(a =&gt; a.AddressList);
    });
}
</code></pre>
<p>When I try to use the following projection I get an exception from EF Core, seems it's unable to translate the projection for the collection in the JSON column.</p>
<pre class="lang-c# prettyprint-override"><code>var customerSettings = await _appDbContext.Customers
    .Where(c =&gt; c.Id == customerId)
    .Select(c =&gt; new
    {
        PrimaryAddress = c.Addresses.Primary,
        AllAddresses = c.Addresses.AddressList.Select(a =&gt; new
        {
           a.City,
           a.CountryCode,
           a.FirstLine,
           a.PostCode,
           a.SecondLine
        })
    })
    .AsNoTracking()
    .FirstOrDefaultAsync(cancellationToken);
</code></pre>
<p>Exception</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'JsonQueryExpression(p.Addresses, $.AddressList)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I can project the <code>AddressList</code> into a property, but obviously this isn't converting the data inside it to a different type.</p>
<pre class="lang-c# prettyprint-override"><code>var customerSettings = await _appDbContext.Customers
    .Where(c =&gt; c.Id == customerId)
    .Select(c =&gt; new
    {
        PrimaryAddress = c.Addresses.Primary,
        AllAddresses = c.Addresses.AddressList
    })
    .AsNoTracking()
    .FirstOrDefaultAsync(cancellationToken);
</code></pre>
<p>Ideally I'm trying to keep the projections agnostic of the EF Core configuration. The <code>Addresses</code> and <code>AddressList</code> properties could be configured to have their own relational tables.</p>

