# Improving a LINQ query so that it executes completely in the database
[Link to question](https://stackoverflow.com/questions/24100141/improving-a-linq-query-so-that-it-executes-completely-in-the-database)
**Creation Date:** 1402164214
**Score:** 2
**Tags:** c#, linq, entity-framework, linq-to-entities
## Question Body
<p>I have an <code>Address</code> model (simplified)...</p>

<pre><code>public class Address
{
    public int AddressId { get; set; }
    public string City { get; set; }
}
</code></pre>

<p>...and a <code>DbContext</code> derived class that contains a set of <code>Addresses</code>:</p>

<pre><code>public DbSet&lt;Address&gt; Addresses { get; set; }
</code></pre>

<p>Then I have this query which is supposed to retrieve one or no <code>address</code> (<code>_context</code> is an instance of my database context class):</p>

<pre><code>public Address GetAddress(string city, int addressId)
{
    Address address = null;

    // this is a database query
    var addresses = _context.Addresses.Where(a =&gt; a.City == city).ToList();

    // the rest queries in memory
    if (addresses.Count &lt;= 1)
        address = addresses.FirstOrDefault();
    else
    {
        address = addresses.FirstOrDefault(a =&gt; a.AddressId == addressId);
        if (address == null)
            address = addresses.FirstOrDefault();
    }

    return address;
}
</code></pre>

<p>The query is a bit weird. The logic is simply:</p>

<ul>
<li>If there is only one (or no) address in the database table with the requested <code>city</code> take this address as result.</li>
<li>If there are multiple addresses with the requested <code>city</code> prefer the one that has the given <code>addressId</code>. If none of the result addresses has this <code>addressId</code> just take the first one.</li>
</ul>

<p>Disturbing is that the <code>.ToList()</code> call potentially loads a lot of addresses into memory I'm not interested in. In the end I filter only one of the loaded addresses in memory as the final result.</p>

<p>Is there a way to rewrite this query (with LINQ-to-Entities) so that it runs completely in the database and returns only one or no address (with a single database roundtrip)?</p>

## Answers
### Answer ID: 24100220
<p>Your logic can be interpreted as preferring the address with a given ID and if none matches jut picking any at all. Your query does not enforce any order for that case.</p>

<pre><code>var addressesInCity = _context.Addresses.Where(a =&gt; a.City == city);
var addrByID = addressesInCity.Where(a =&gt; a.AddressId == addressId);
var anyAddr = addressesInCity.Take(1);
</code></pre>

<p>You can write this with two queries:</p>

<pre><code>addrByID.FirstOrDefault() ?? anyAddr.FirstOrDefault();
</code></pre>

<p>You can combine those into a single query:</p>

<pre><code>addrByID.Select(a =&gt; new { Priority = 1, a })
.Concat(anyAddr.Select(a =&gt; new { Priority = 2, a }))
.OrderBy(x =&gt; x.Priority)
.Take(1)
.Select(x =&gt; x.a)
.FirstOrDefault();
</code></pre>

<p>This saves a roundtrip and SQL Server understands the sorting by a constant. It will run efficiently. Not <em>necessarily</em> more efficiently than the first form but not significantly worse.</p>

<p>Note, that the order of results returned by <code>UNION (ALL)</code> is undefined. We need to enforce order by introducing a <code>Priority</code> field.</p>

