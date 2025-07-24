# Is there a way to construct database query, where I can apply condition based on values in a list?
[Link to question](https://stackoverflow.com/questions/65683310/is-there-a-way-to-construct-database-query-where-i-can-apply-condition-based-on)
**Creation Date:** 1610452007
**Score:** 1
**Tags:** c#, sql-server, linq, .net-core, entity-framework-core
## Question Body
<pre><code>var contacts = await dbContext.Registration.Where(x =&gt; visited.Any(y =&gt; y.Id == x.Id)
                &amp;&amp; visited.Any(y =&gt; (x.OutDate &gt;= y.InDate &amp;&amp; x.OutDate &lt;= y.OutDate)
                || (x.InDate &gt;= y.InDate &amp;&amp; x.OutDate &lt;= y.OutDate)
                || (x.InDate &gt;= y.InDate &amp;&amp; x.InDate &lt;= y.OutDate)
                || (x.InDate &lt;= y.InDate &amp;&amp; x.OutDate &gt;= y.OutDate)))
                .ToListAsync()
</code></pre>
<p>This query gives error that, &quot;The LINQ Query could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().&quot;</p>
<p>Here <em><strong>visited is a list of Object that has property Id, InDate and OutDate</strong></em>.
Visited has been already fetched from DB and is present in ,memory.
I want to filter my database results based on the values present in these objects.</p>
<p>One way could be Iterating through each object and getting all tuples according to a single object and repeating the same for other objects in the list. This would involve multiple Network Calls and would be very inefficient.</p>
<p>Is there any way in which I get all the results in 1 Network call ?</p>

## Answers
### Answer ID: 65684235
<p>based on part of your statement I assume that <code>visited</code> is somewhere persisted in db.</p>
<p>therefore visited could be queried</p>
<pre><code>//requery visitations;
var visited = dbContext.Visited.Where(v=&gt; v.visited).Select(v=&gt; {v.Id, v.InDate, v.OutDate })
</code></pre>
<p>and then registration query</p>
<pre><code>var query = dbContext.Registration
            .Join(visited, 
                reg =&gt; reg.Id,
                visit =&gt; visit.Id,
                (reg, visit) =&gt; new {Registration = reg, Visit = visit})
            .Where(regAndVisit =&gt;
                (regAndVisit.Registration.OutDate &gt;= regAndVisit.Visit.InDate &amp;&amp;
                 regAndVisit.Registration.OutDate &lt;= regAndVisit.Visit.OutDate)
                || (regAndVisit.Registration.InDate &gt;= regAndVisit.Visit.InDate &amp;&amp;
                    regAndVisit.Registration.OutDate &lt;= regAndVisit.Visit.OutDate)
                || (regAndVisit.Registration.InDate &gt;= regAndVisit.Visit.InDate &amp;&amp;
                    regAndVisit.Registration.InDate &lt;= regAndVisit.Visit.OutDate)
                || (regAndVisit.Registration.InDate &lt;= regAndVisit.Visit.InDate &amp;&amp;
                    regAndVisit.Registration.OutDate &gt;= regAndVisit.Visit.OutDate));
</code></pre>
<p>possible to add <code>GroupBy</code> or <code>Distinct</code> if you want to avoid duplicated not sure what is connection between visits and registration</p>

### Answer ID: 65683868
<p>Assuming that x.OutDate &gt; x.InDate and y.OutDate &gt; y.InDate you can reduce to following :</p>
<pre><code>             var contacts = dbContext.Registration.SelectMany(x =&gt; visited.Where(y =&gt; (y.Id == x.Id)
                &amp;&amp; ((x.InDate &gt;= y.InDate &amp;&amp; x.OutDate &lt;= y.OutDate)
                || (x.InDate &lt;= y.InDate &amp;&amp; x.OutDate &gt;= y.OutDate))));
</code></pre>
<hr />
<p>Where comparing two ranges of dates there are 7 combinations</p>
<p><a href="https://i.sstatic.net/dAXeU.jpg" rel="nofollow noreferrer"><img src="https://i.sstatic.net/dAXeU.jpg" alt="enter image description here" /></a></p>

