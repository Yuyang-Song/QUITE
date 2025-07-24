# EF Core 5.0.x QueryFilter for Collection Property with ValueConversion
[Link to question](https://stackoverflow.com/questions/66952750/ef-core-5-0-x-queryfilter-for-collection-property-with-valueconversion)
**Creation Date:** 1617624226
**Score:** 0
**Tags:** c#, linq, entity-framework-core, .net-5, global-query-filter
## Question Body
<p>I've got an <code>Url</code> entity with a string collection property which holds role names:</p>
<pre><code>public class Url : BaseEntity
    {
         public ICollection&lt;string&gt; Roles { get; private set; } = new HashSet&lt;string&gt;();
    }
</code></pre>
<p>In the database this is a <code>string</code> field. It gets converted to the <code>HashSet</code> using a <code>ValueConverter</code>:</p>
<pre><code>    var splitStringConverter = new ValueConverter&lt;ICollection&lt;string&gt;, string&gt;(
        collection =&gt; string.Join(&quot;;&quot;, collection),
        commaSeparatedString =&gt; string.IsNullOrWhiteSpace(commaSeparatedString)
            ? new HashSet&lt;string&gt;()
            : commaSeparatedString.Split(new[] { ';' }).ToHashSet());

    var valueComparer = new ValueComparer&lt;ICollection&lt;string&gt;&gt;(
        (collection1, collection2) =&gt; collection1.SequenceEqual(collection2),
        collection =&gt; collection.Aggregate(0, (a, item) =&gt; HashCode.Combine(a, item.GetHashCode())),
        collection =&gt; collection);

    builder
        .Property(e =&gt; e.Roles)
        .HasMaxLength(500)
        .HasConversion(splitStringConverter)
        .Metadata.SetValueComparer(valueComparer);
</code></pre>
<p>What I need is a global query filter for the Url entity like this:</p>
<pre><code>builder.Entity&lt;Url&gt;()
                .HasQueryFilter(url =&gt; !url.Deleted &amp;&amp; (url.Roles.Count == 0 || url.Roles.Intersect(_tokenAccessor.UserRoles).Any()));
</code></pre>
<p>where <code>_tokenAccessor</code> is injected to the <code>DbContext</code> and provides the role names from the current JWT token.
Unfortunately this query filter does not work because EF Core is not able to perform this query on the server:</p>
<blockquote>
<p>The LINQ expression 'DbSet()
.Where(u =&gt; !(u.Deleted) &amp;&amp; u.Roles.Count == 0 || u.Roles
.Intersect(__ef_filter__UserRoles_0)
.Any())' could not be translated. Additional information: Translation of method 'System.Linq.Enumerable.Intersect' failed.</p>
</blockquote>
<p>But the <code>Intersect</code> method is not the main issue - the following simplified query filter is also failing:</p>
<pre><code>builder.Entity&lt;Url&gt;()
                .HasQueryFilter(url =&gt; !url.Deleted &amp;&amp; (url.Roles.Count == 0));
</code></pre>
<blockquote>
<p>The LINQ expression 'DbSet()
.Where(u =&gt; !(u.Deleted) &amp;&amp; u.Roles.Count == 0)' could not be translated. Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to
'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>Is there a way to access the <code>Roles</code> property in the global query filter?</p>

