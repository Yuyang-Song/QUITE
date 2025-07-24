# Is it possible to rewrite complex EF Core &quot;.Include&quot; calls to &quot;Join&quot; calls?
[Link to question](https://stackoverflow.com/questions/65747968/is-it-possible-to-rewrite-complex-ef-core-include-calls-to-join-calls)
**Creation Date:** 1610787535
**Score:** 3
**Tags:** c#, linq, asp.net-core, entity-framework-core
## Question Body
<p>I have two EF Core entity models named Service and ServiceBranch:</p>
<pre><code>public class Service
{
    public Guid ID { get; set; }
    public Guid? ParentServiceID { get; set; } // foreign key to the same table
    public string Name { get; set; }
    public DateTime? DateDeleted { get; set; }

    public virtual ICollection&lt;Service&gt; InverseParent { get; set; } // navigation property
    public virtual ICollection&lt;ServiceBranch&gt; ServiceBranches { get; set; } // navigation property
}

public class ServiceBranch
{
    public Guid ID { get; set; }
    public Guid ServiceID { get; set; } // foreign key
    public string Name { get; set; }
    public DateTime? DateDeleted { get; set; }

    public virtual Service Service { get; set; } // navigation property
}
</code></pre>
<p>For simplicity, let's say parent Service can have only one level of children Services. both parent and children services are being referenced by a lot of service branches.</p>
<p>I want to update DateDeleted field for a specific Service ID and update DateDeleted in all other rows that are referencing it (if that field doesn't already have a value).</p>
<p>Currently my call to bring all the required entities looks like this:</p>
<pre><code>var serviceEntity = _context.Set&lt;Service&gt;().Where(x =&gt; x.ID == neededID &amp;&amp; x.DateDeleted == null)
                .Include(x =&gt; x.ServiceBranches)
                .Include(x =&gt; x.InverseParent)
                    .ThenInclude(InverseParent =&gt; InverseParent.ServiceBranches)
                .FirstOrDefault();
</code></pre>
<p>I use Where clause for the main entity but unfortunately I cannot use Where inside .Includes since we haven't upgraded to EF Core 5.0 yet (which supports filtering inside .Includes).</p>
<p>Thus I bring too many unneeded rows (where DateDeleted already has a value) from the database and then filter them within a foreach loop by comparing that field to null:</p>
<pre><code>if (myentity.DateDeleted == null) myentity.DateDeleted = DateTime.Now;
</code></pre>
<p>I want to rewrite my query so that I use &quot;join&quot; instead of &quot;.Include&quot;, something like this:</p>
<pre><code>var serviceEntity = from service in _context.Set&lt;Service&gt;()
                where service.ID == neededID &amp;&amp; service.DateDeleted == null
                join branches in _context.Set&lt;ServiceBranch&gt;() on service.ID equals branches.ServiceID
                where branches.DateDeleted == null // filter which I cannot use with .Include-s
                let // whatever, can't make it work
                select // etc
</code></pre>
<p>I can't get my head around how to rewrite it. Or if it is even possible to do it with joins.</p>

## Answers
### Answer ID: 65753698
<p>In this particular case you don't need joins, but flat list containing the desired <code>Service</code> entity plus all its children. In general this requires recursive query (not supported by LINQ / EF Core), but for single level it is a matter of simple filter like</p>
<pre><code>service.ID == neededID || service.ParentServiceID == neededID
</code></pre>
<p>Then you could apply the additional <code>DateDeleted</code> criteria. Finally, to get the related <code>ServiceBranch</code> entities with <code>DateDeleted</code> filter, instead of <code>Include</code> just use projection (<code>Select</code>).</p>
<p>And when processing the returned data, use the projected entities and ignore their navigation properties. e.g.</p>
<pre><code>var itemsToUpdate = _context.Set&lt;Service&gt;()
    .Where(service =&gt; (service.ID == neededID || service.ParentServiceID == neededID)
        &amp;&amp; service.DateDeleted == null)
    .Select(service =&gt; new
    {
        Service = service,
        ServiceBrances = service.ServiceBranches
            .Where(branch =&gt; branch.DateDeleted == null),
    });

foreach (var item in itemsToUpdate)
{
    item.Service.DateDeleted = DateTime.Now;
    foreach (var branch in item.ServiceBrances)
        branch.DateDeleted =  DateTime.Now;
}
</code></pre>

### Answer ID: 65753487
<p><code>Include</code> puts the loaded objects directly on your Entity Framework model, and that model is really supposed to directly represent what's in the database. If you're wanting a filtered collection, I'd recommend coming up with a different model that represents what you're trying to represent, and then using Select to project to that model. Something like this:</p>
<pre><code>var serviceEntity = _context.Set&lt;Service&gt;()
    .Where(x =&gt; x.ID == neededID &amp;&amp; x.DateDeleted == null)
    .Select(x =&gt; new // you can make this a named type if necessary
        {
           Service = x,
           ActiveBranches = x.ServiceBranches.Where(b =&gt; b.DateDeleted == null),
           InverseParent,
           InverseParentServiceBranches = x.InverseParent.ServiceBranches
        })
    .FirstOrDefault();
</code></pre>

