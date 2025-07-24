# Entity Framework Core - select records from table only where column in table matches all strings in list
[Link to question](https://stackoverflow.com/questions/64223524/entity-framework-core-select-records-from-table-only-where-column-in-table-mat)
**Creation Date:** 1601978390
**Score:** 0
**Tags:** c#, sql-server, linq, entity-framework-core
## Question Body
<p>So with Entity Framework Core, I have set up a view in the database that concatenates an address into one column, with the unique ID of the address as well, so effectively the view contains:</p>
<ul>
<li><code>Id</code> (unique identifier of the address)</li>
<li><code>FullAddress</code> (concatenated column of the separate address columns, to allow it to be searched)</li>
</ul>
<p>This part is working fine, and I can do a SQL query against it like this to find all addresses in the view:</p>
<pre class="lang-sql prettyprint-override"><code>select distinct 
    V.Id
from
    dbo.View_AddressFull V 
where 
    V.FullAddress like '%64%' and V.FullAddress like '%townName%'
</code></pre>
<p>The problem I'm having is trying to replicate this query in LINQ, especially considering how there could be more than 2 search terms, since it's an &quot;Address&quot; search box, the user can type in any address they would like to try like &quot;15 MadeUpStreet TownName Country&quot; - if I was to do this in raw SQL this would just mean more <code>and V.FullAddress like</code> selectors, or someway of doing it from a list.</p>
<p>So this is the linq I've written to try and do this (<a href="https://stackoverflow.com/questions/27295702/how-do-you-check-if-a-string-contains-any-strings-from-a-list-in-entity-framewor">idea adapted from this post</a>):</p>
<pre class="lang-csharp prettyprint-override"><code>string[] splitAddress = query.Address.Split(new char[] { ' ' }, System.StringSplitOptions.RemoveEmptyEntries);

var matchingAddresses = await _dbContext.View_AddressFull
    .Where(data =&gt; splitAddress.All(x =&gt; data.FullAddress.Contains(x)))
    .Select(x =&gt; x.Id)
    .Distinct()
    .ToListAsync();
</code></pre>
<p>My hope with this is that it would do something similar to the SQL query above, unfortunately Entity Framework Core isn't able to translate the query and I get this error:</p>
<blockquote>
<p>The LINQ expression 'DbSet.Where(a =&gt; splitAddress.All(x =&gt; a.FullAddress.Contains(x)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.&quot;</p>
</blockquote>
<p>I did try switching to client evaluation as it suggests, by using an <code>AsEnumerable()</code>, but this didn't return any results, which leads me to believe I have done the where selector wrong which is also leading to the expression not being translateable in the first place?</p>
<p>My other idea, is to just give up trying to make this a linq query and execute this as RAW SQL via Entity Framework Core, and then do a further select to get only the distinct Id's from there... the only issue is, I can't think of how to do that without just concatenating more <code>and V.FullAddress like</code> onto the SQL search string for each search word that is entered - which potentially exposes me to SQL Injection?</p>

