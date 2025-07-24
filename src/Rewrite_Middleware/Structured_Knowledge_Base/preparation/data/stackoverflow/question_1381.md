# How to write this linq query so it isn&#39;t so slow
[Link to question](https://stackoverflow.com/questions/73586315/how-to-write-this-linq-query-so-it-isnt-so-slow)
**Creation Date:** 1662140818
**Score:** 0
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>I have this SQL statement which is pretty instantaneous when running it:</p>
<pre><code>select Distinct statuses.Description, count(*) as count 
from referrals 
inner join statuses on referrals.StatusId = statuses.id
group by statuses.Description
</code></pre>
<p>But when I run the below linq code with Entity Framework Core, it takes almost 5 minutes to run and there are only 680 rows in the database.</p>
<pre><code>var data = context.Referrals
                  .Include(s =&gt; s.Status).AsEnumerable()
                  .GroupBy(r =&gt; r.Status)
                  .Select(g =&gt; new StatusCountItem 
                                   { 
                                       Status = g.Key.Description, 
                                       Count = g.Select(r =&gt; r).Count() 
                                   }).ToList();
</code></pre>
<p>Is there a way to write a similar Linq statement that won't take forever to run or do I need to figure out a different way to do what I want?</p>
<p><strong>EDIT</strong>: when I don't have the <code>AsEnumerable</code> I get this error message which is why I added it:</p>
<blockquote>
<p>The LINQ expression 'DbSet().Join(inner: DbSet(),<br />
outerKeySelector: r =&gt; EF.Property&lt;int?&gt;(r, &quot;StatusId&quot;),<br />
innerKeySelector: s =&gt; EF.Property&lt;int?&gt;(s, &quot;Id&quot;),<br />
resultSelector: (o, i) =&gt; new TransparentIdentifier&lt;Referral,   Status&gt;(Outer = o, Inner = i))<br />
.GroupBy(r =&gt; r.Inner)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync</p>
</blockquote>

## Answers
### Answer ID: 73586769
<p>Use this one, it is simple and will improve query performance.</p>
<pre><code>from r in context.Referrals
join s in context.statuses on r.StatusId equals s.Id
select new { s.Description, r.StatusId , S.Id) into result
group result by new { s.Description } into g
select new {
   CompanyName = g.Key.Description,
   Count = g.Count()
}
</code></pre>

### Answer ID: 73586924
<p>Try this:</p>
<pre><code>var data = context.Referrals
    .GroupBy(r =&gt; r.StatusId) // notice the change here, you need to group by the id
    .Select(g =&gt; new StatusCountItem()
    {
        Status = g.First().Status.Description,
        Count = g.Count()
    }).ToList();
</code></pre>

### Answer ID: 73586492
<p>Your Sql query is built based on <code>context.Referrals.Include(s =&gt; s.Status).AsEnumerable()</code>, which is equivalent to:</p>
<pre><code>select *
from referrals 
    inner join statuses on referrals.StatusId = statuses.id
</code></pre>
<p>Note the star, you're querying <em>every</em> column. In other words, remove the random <code>AsEnumerable()</code> in the middle of your query.</p>

