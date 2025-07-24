# Linq to entities - Query elements where List&lt;string&gt; property has at least an element that matches other element in an in memory list
[Link to question](https://stackoverflow.com/questions/69441695/linq-to-entities-query-elements-where-liststring-property-has-at-least-an-el)
**Creation Date:** 1633377248
**Score:** 0
**Tags:** c#, .net, entity-framework, linq
## Question Body
<p>A bit of a <strong>context</strong> for the problem:</p>
<p>I have an entity (Person) in my database that has a one to many relationship with another (Phone).</p>
<pre><code>    public class Person
    {
        [Key]
        public int Id { get; set; }
        .
        .
        .
        [ForeignKey(&quot;PersonId&quot;)]
        public virtual List&lt;Phone&gt; Phones { get; set; }
    }

    public class Phone
    {
        [Key]
        public int Id { get; set; }
        .
        .
        .
        public string PhoneNumber { get; set; }

        public int PersonId { get; set; }

        public virtual Person Person { get; set; }
    }
</code></pre>
<p>Secondly I'm receiving a filter that includes a list of strings.</p>
<p><strong>The Problem:</strong></p>
<p>I'm trying to get from the DB all the Persons that have at least a PhoneNumber that matches (by like) any of the filter's phone numbers.</p>
<p>So far I've tryed this:</p>
<pre><code>var query = _dbContext.Person
                .Include(x =&gt; x.PhoneNumbers)
                .AsNoTracking();
                .Where(x =&gt; x.Phones
                             .Any(y =&gt; filter.Phones
                                             .Any(z =&gt; y.PhoneNumber.Contains(z))));
</code></pre>
<p>This query throws an error:</p>
<p><em>The LINQ expression {my expression here} could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.&quot;</em></p>
<p><strong>Thanks you!</strong></p>

## Answers
### Answer ID: 69442612
<p>If you use a standardized format for your recorded phone numbers (I.e. strip all separators and include a standard area code etc.) then you can format your search list of phone numbers to conform to the format and use:</p>
<pre><code>.Where(x =&gt; x.Phones.Any(y =&gt; filter.Phones.Contains(y.PhoneNumber)));
</code></pre>
<p>The issue is that you cannot apply a Linq2Entity <code>Any</code> against the in-memory collection. You can use <code>Contains</code> against the collection but the phone numbers would have to match exactly. (so no inner <code>LIKE</code> type comparison)</p>
<p>If you have a reasonable number of search phone numbers and want to do the <code>LIKE</code> type search across the phone numbers then you can leverage LinqKit's PredicateBuilder to prepare a suitable condition. This requires marking the query as &quot;Expandable&quot; so the dynamic predicate can be built.</p>
<pre><code>var query = _dbContext.Person
    .Include(x =&gt; x.PhoneNumbers)
    .AsNoTracking()
    .AsExpandable();

if (filter.Phones.Any())
{
    var predicate = PredicateBuilder.New&lt;Person&gt;();
    foreach(var phone in filter.Phones)
        predicate = predicate.Or(x =&gt; x.Phones.Any(p =&gt; p.Contains(phone)));
    query = query.Where(predicate);
}
</code></pre>

