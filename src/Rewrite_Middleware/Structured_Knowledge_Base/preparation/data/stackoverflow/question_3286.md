# Linq to entity enum not comparing
[Link to question](https://stackoverflow.com/questions/75161184/linq-to-entity-enum-not-comparing)
**Creation Date:** 1674053942
**Score:** 0
**Tags:** asp.net, postgresql, entity-framework, entity-framework-core
## Question Body
<p>Here is my Enum:</p>
<pre><code>public enum AdvertStatus
{
   Active,
   Archived
}
</code></pre>
<p>And my entity type:</p>
<pre><code>public record Advertisement
{
...
    public AdvertStatus Status { get; set; }
...
}
</code></pre>
<p>In database it's stored as int, Database is Postgree</p>
<p>When I try to compare it like so:</p>
<pre><code>data = data.Where(x =&gt; x.Status == searchValues.Status);
</code></pre>
<p>Entity Framework throws an exception sayng:</p>
<blockquote>
<p>.Status == (int)__searchValues_Status_3)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I tried solutions from this question: <a href="https://stackoverflow.com/questions/50551107/linq-to-entity-cannot-compare-to-enumeration-types">LINQ TO ENTITY cannot compare to enumeration types</a> but it did't work.</p>
<p>EDIT 1:<br>
<code>data</code> is database table context <code>IQueryable&lt;AdvertisementDTO&gt;</code> <br>
searchValues.Status is type of <code>AdvertStatus</code> from search filter</p>

## Answers
### Answer ID: 75175990
<p>It was all my mistake in higher repo <code>Select</code> projection.
<br>Thanks you all for help. Cheers.</p>

### Answer ID: 75165653
<p>The issue may be higher up in your Linq query, such as you are attempting to project with a <code>Select</code> or <code>ProjectTo</code> before filtering. For simple types like <code>int</code>/<code>string</code> this should work, but depending on how your DTO is declared you might be introducing problems for mpgsql.</p>
<p>For instance if your query is something like:</p>
<pre><code>var query = _context.Advertisements
    .Select(x =&gt; new AdvertisementDTO
    {
        // populate DTO
    }).Where(x =&gt; x.Status == searchValues.Status)
    // ....
</code></pre>
<p>then npgsql may be having issues attempting to resolve the types between what is in the DTO and the enumeration in your searchValues. From what the exception detail looks like, npgsql is trying to be &quot;safe&quot; with the enum and casting to <code>int</code>but feeding that to PostgreSQL that results in invalid SQL. I did some quick checks and the DTO would need to be using the same Enum type (C# complains if the DTO cast the value to <code>int</code>, cannot use <code>==</code> between AdvertStatus and <code>int</code> fortunately) The project may have something like a value converter or other hook trying to translate enumerations which is getting brought into the mix and gunking up the works.</p>
<p>Try performing the <code>Where</code> conditions prior to projection:</p>
<pre><code>var query = _context.Advertisements
    .Where(x =&gt; x.Status == searchValues.Status)
    .Select(x =&gt; new AdvertisementDTO
    {
        // populate DTO
    })
    // ....
</code></pre>
<p>If the data value is stored as an Int then this should work out of the box. npgsql does support mapping to string (which would require a ValueConverter) as well as database declared enumerations. (<a href="https://www.postgresql.org/docs/current/datatype-enum.html" rel="nofollow noreferrer">https://www.postgresql.org/docs/current/datatype-enum.html</a>) However, Int columns should work fine /w enums.</p>
<p>If that doesn't work, I'd try with a new DbContext instance pointed at the DB and a simple entity with that Enum to load a row from that table to eliminate whether npgsql is translating the enum correctly, just to eliminate any possible converters or other code that the main DbContext/models/DTOs may be contributing.</p>

