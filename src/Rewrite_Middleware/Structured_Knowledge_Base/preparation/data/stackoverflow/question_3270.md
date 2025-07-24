# Linq GroupBy throws an exception in .NET 6
[Link to question](https://stackoverflow.com/questions/74512131/linq-groupby-throws-an-exception-in-net-6)
**Creation Date:** 1668979544
**Score:** 0
**Tags:** c#, .net, linq, entity-framework-core
## Question Body
<p>I had the following query running successfully in old .NET framework 4.7.2 project, but the following query breaks in .NET 6 in migrated project</p>
<pre><code>var query = from x in dbContext.table1 
            join y in dbContext.table2 
                   on x.AccountId equals y.AccountId
            join dbContext.v on x.RecId = v.RecId
            group new 
                  {
                      x,
                      y.Name,
                      y.Email,
                      v.SecretKey
                  }
            by new 
               {
                   x.CreatedDate,
                   y.Name   
               }     
            into grp
            orderby grp.Key.Name,
            select grp;
</code></pre>
<p>It throws this error:</p>
<blockquote>
<p>OrderBy(grp =&gt; grp.Key.Name)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.'</p>
</blockquote>
<p>And I can't use <code>ToList()</code> on just the join because on production there are millions of records in database which cannot be fetched each time in client side to apply group by operation.</p>
<p>How can I restructure the query to get it to work in .NET 6 ?</p>
<p><strong>Note</strong>: the variable name taken as example as it is not possible to post company code here</p>

