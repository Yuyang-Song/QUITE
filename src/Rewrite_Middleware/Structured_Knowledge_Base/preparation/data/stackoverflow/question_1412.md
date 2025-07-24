# EF Core enum collection property comparing
[Link to question](https://stackoverflow.com/questions/75246630/ef-core-enum-collection-property-comparing)
**Creation Date:** 1674738891
**Score:** 0
**Tags:** .net, enums, entity-framework-core, code-first
## Question Body
<p>I'm using code first with Entity Framework Core for handling som addresses in an application.
These addresses all have a HousingTypes property which is a collection of enums that can by any of the available enum types.</p>
<pre class="lang-cs prettyprint-override"><code>public enum HousingType
{
    Condominium = 1,
    SummerHouse = 2,
    StudentApartment = 3,
    ServiceHousing = 4
}

public class Address
{
    public int Id { get; set; }
    public ICollection&lt;HousingType&gt; HousingTypes { get; set; }
}
</code></pre>
<p>I've created a ValueConverter and ValueComparer as described by others previously to convert these value to comma separated strings in the database like this in the DatabaseContext:</p>
<pre class="lang-cs prettyprint-override"><code>ModelBuilder.Entity&lt;Address&gt;().Property(nameof(HousingTypes))
    .HasConversion(
        x =&gt; string.Join(&quot;,&quot;, x),
        x =&gt; string.IsNullOrWhiteSpace(x) ? new List&lt;HousingType&gt;() : x.Split(new[] { ',' }).ToList()))
    .Metadata.SetValueComparer(new ValueComparer&lt;ICollection&lt;HousingType&gt;&gt;(
        (x, y) =&gt; x.SequenceEqual(y),
        x =&gt; x.Aggregate(0, (a, v) =&gt; HashCode.Combine(a, v.GetHashCode())),
        x =&gt; x.ToList()););
</code></pre>
<p>This is all and well, and I can read and write data as normal. But I've come to a point where the user needs to filter out addresses depending on selected HousingTypes. Now Entity Framework does not know how to compare multiple housing types to each other.</p>
<pre class="lang-cs prettyprint-override"><code>// Only receive addresses that has any of these housing types included
var filterExample = new HousingType[] { HousingType.Condominium, HousingType.SummerHouse };

await _context.Addresses
    .Where(a =&gt; a.HousingTypes.Any(ht =&gt; filterExample.Contains(ht))) // Entity Framework does not like this!
    .ToListAsync;
</code></pre>
<p>When retrieving the data I get the following error message:</p>
<blockquote>
<p>The LINQ expression 'ht =&gt; __filterExample_3.Contains(ht)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I would rather not inserting a call to ToList earlier, since that would load in all addresses (lots amounts of data) that is not needed, and makes it problematic to use paging and such when retrieving data.</p>

## Answers
### Answer ID: 75332160
<p>First I tried using Flags with the enum, but this complicated a lot of the code (specially to make it compatible with the front-end).</p>
<p>Also, it's not intuitive how to make comparisons between two enums and compare wether they are included in each other or not, etc. This could of course be made simpler with help or extension methods.</p>
<p>But I ended up using foreign key tables for this instead. Adding a AddressHousingType model which contains a normal enum and a foreign key to Address (one to many relation).</p>
<p>This solution is not ideal either, but works and is simpler to understand. I think that if this was a new project I would consider comparing bitwise and creating help methods for this, but since this is a project that has been in development for quite some time this felt like the best solution this time.</p>

