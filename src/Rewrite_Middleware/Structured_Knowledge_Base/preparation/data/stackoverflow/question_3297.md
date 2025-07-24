# SQlite EntityframeworkCore Linq query on column not working: InvalidOperationException
[Link to question](https://stackoverflow.com/questions/75324171/sqlite-entityframeworkcore-linq-query-on-column-not-working-invalidoperationexc)
**Creation Date:** 1675346046
**Score:** 0
**Tags:** c#, sqlite, entity-framework-core
## Question Body
<h5>The Exception:</h5>
<blockquote>
<p>System.InvalidOperationException: 'The LINQ expression 'DbSet()
.Where(k =&gt; (GroupAddress)k.Address == __notification_Destination_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<h5>The source code which leads to the aforementioned exception</h5>
<pre class="lang-cs prettyprint-override"><code>// works
var x = await dbContext.AddressConfigurations.SingleOrDefaultAsync(c =&gt; c.Id == 1);

// fails with the exception below
// Single() or First() makes no difference regarding the exception. Should be Single() but I have no unique constraint so far.
var y = await dbContext.AddressConfigurations.FirstOrDefaultAsync(c =&gt; c.Address == notification.Destination);
</code></pre>
<h5>The database model</h5>
<pre><code>public class AddressConfiguration
{
    public AddressConfiguration(string address, string dataType)
    {
        Address = address;
        DataType = dataType;
    }

    public int Id { get; set; }

    public string Address { get; set; }

    public string DataType { get; set; }

    public string? Location { get; set; }
}
</code></pre>
<p>Is there anything I'm missing here? Do I need to define an index for that column?</p>

## Answers
### Answer ID: 75324314
<p>Based on the exception specifying cast to <code>GroupAddress</code> it seems that <code>notification.Destination</code> is a <code>GroupAddress</code> and there is implicit cast from <code>string</code> to it. Comparison of two arbitrary custom types can't be translated by EF AFAIK, so you need to convert <code>notification.Destination</code> to <code>string</code>. Depending on <code>GroupAddress</code> implementation you can try just an explicit cast (if it is implemented):</p>
<pre class="lang-cs prettyprint-override"><code>var y = await dbContext.AddressConfigurations
    .FirstOrDefaultAsync(c =&gt; c.Address == (string)notification.Destination);
</code></pre>
<p>Or <code>ToString()</code>:</p>
<pre class="lang-cs prettyprint-override"><code>var y = await dbContext.AddressConfigurations
    .FirstOrDefaultAsync(c =&gt; c.Address == notification.Destination.ToString());
</code></pre>
<p>Or you will need to construct a valid searchable string manually:</p>
<pre class="lang-cs prettyprint-override"><code>var y = await dbContext.AddressConfigurations
    .FirstOrDefaultAsync(c =&gt; c.Address == notification.Destination.SomeProp + &quot; &quot; + notification.Destination.SomeOtherProp);
</code></pre>

