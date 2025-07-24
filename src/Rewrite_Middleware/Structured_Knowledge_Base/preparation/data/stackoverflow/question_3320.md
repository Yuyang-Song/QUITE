# EF Core 7 Json column projections - LINQKit - LINQ expression could not be translated
[Link to question](https://stackoverflow.com/questions/76271775/ef-core-7-json-column-projections-linqkit-linq-expression-could-not-be-trans)
**Creation Date:** 1684324165
**Score:** 2
**Tags:** .net, entity-framework, entity-framework-core, linqkit, ef-core-7.0
## Question Body
<p>I have an issue with mapping an EF Core 7 Json column into an class. I am presented with the following exception.</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'JsonQueryExpression(p.Addresses, $.AddressList)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>The code below is the projection that is mapping the queried <code>AddressesData</code> class to the <code>Addresses</code> class.  (Which the <code>Addresses</code> is an EF Core 7 Json column, see DBContext at the bottom)</p>
<pre class="lang-cs prettyprint-override"><code>public static class AddressesDataExpressions
{
    public static class Projections
    {
        private static Expression&lt;Func&lt;AddressesData, Addresses&gt;&gt; Projection()
        {
            return a =&gt; new()
            {
                AllAddresses = a.AddressList.AsQueryable().AsEnumerable().Select(ad =&gt; new Address
                {
                    City = ad.City,
                    CountryCode = ad.CountryCode,
                    FirstLine = ad.FirstLine,
                    PostCode = ad.PostCode,
                    SecondLine = ad.SecondLine
                }).ToList(),
                PrimaryAddressIndex = a.Primary
            };
        }
        private static Func&lt;AddressesData, Addresses&gt;? _project;
        [Expandable(nameof(Projection))]
        public static Addresses Project(AddressesData data)
        {
            _project ??= Projection().Compile();

            return _project(data);
        }
    }
}
</code></pre>
<p>Below is the method that contains the EF Query</p>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;CustomerSettings?&gt; GetSettingsAsync(int customerId, CancellationToken cancellationToken = default)
{
    var customerSettings = await _appDbContext.Customers
        .Where(c =&gt; c.ResourceId == customerId)
        .Select(c =&gt; new CustomerSettings
        {
            Addresses = ADE.Projections.Project(c.Addresses),
            Privacy = CPE.Projections.Project(c.Privacy),
            SocialMedia = new()
            {
                Facebook = c.SocialMedia.Facebook,
                Instragam = c.SocialMedia.Instragam,
                Twitter = c.SocialMedia.Twitter
            }
        })
        .FirstOrDefaultAsync(cancellationToken);

    return customerSettings;
}
</code></pre>
<p>However, as you can see in the above code, I'm also using a projection for <code>Privacy</code> which I've converted back to an original Relational Database format with a table instead of Json column to test this issue, and this works without any issues.</p>
<p>I was just wondering if there's currently no support for EF Core 7 Json columns?</p>
<p>Below is the <code>AddressesData</code> database model class &amp; the <code>Addresses</code> it is being mapped into.</p>
<pre class="lang-cs prettyprint-override"><code>public class AddressesData
{
    public int? Primary { get; set; }
    public ICollection&lt;AddressData&gt; AddressList { get; set; } = new List&lt;AddressData&gt;();
}
</code></pre>
<pre class="lang-cs prettyprint-override"><code>public class Addresses
{
    public Addresses()
    {
        AllAddresses = new List&lt;Address&gt;();
    }
    public Addresses(IEnumerable&lt;Address&gt; addresses)
    {
        AllAddresses = new List&lt;Address&gt;();
        AllAddresses.AddRange(addresses);
    }

    public int? PrimaryAddressIndex { get; set; }
    public List&lt;Address&gt; AllAddresses { get; set; }
}

</code></pre>
<p>And here's the EF Db context config too</p>
<pre class="lang-cs prettyprint-override"><code>public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions&lt;AppDbContext&gt; options) : base(options)
    {

    }

    public DbSet&lt;ResourceData&gt; Resources { get; set; }
    public DbSet&lt;DepartmentData&gt; Departments { get; set; } = null!;
    public DbSet&lt;PersonData&gt; People { get; set; } = null!;
    public DbSet&lt;StaffMemberData&gt; StaffMembers { get; set; } = null!;
    public DbSet&lt;CustomerData&gt; Customers { get; set; } = null!;
    public DbSet&lt;CustomerPrivacyData&gt; CustomerPrivacyData { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity&lt;DepartmentData&gt;().OwnsOne(p =&gt; p.Address, options =&gt; options.ToJson());

        // Have to use TPH if we're using a base class with JSON columns, TPC is not currently supported
        modelBuilder.Entity&lt;PersonData&gt;().OwnsOne(p =&gt; p.SocialMedia, options =&gt; options.ToJson());
        modelBuilder.Entity&lt;PersonData&gt;().OwnsOne(p =&gt; p.Addresses, builder =&gt;
        {
            builder.ToJson();
            builder.OwnsMany(a =&gt; a.AddressList);
        });

        modelBuilder.Entity&lt;StaffMemberData&gt;().OwnsMany(p =&gt; p.Certifications, options =&gt; options.ToJson());
        modelBuilder.Entity&lt;StaffMemberData&gt;().OwnsMany(p =&gt; p.Titles, options =&gt; options.ToJson());

        //modelBuilder.Entity&lt;CustomerData&gt;().OwnsOne(p =&gt; p.Privacy, options =&gt; options.ToJson());
    }
}

</code></pre>
<p>I still receive the same error after removing <code>.AsQueryable().AsEnumerable()</code> from the projection and also removing just <code>.AsEnumerable()</code></p>
<p>Thanks in advance!</p>

