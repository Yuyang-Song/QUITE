# how to concatenate the string in AsQueryable to search by the name, by null checking
[Link to question](https://stackoverflow.com/questions/68751021/how-to-concatenate-the-string-in-asqueryable-to-search-by-the-name-by-null-chec)
**Creation Date:** 1628736586
**Score:** 1
**Tags:** c#, linq
## Question Body
<p>I want to search by a <code>name</code>, which is the input from the  UI, however, I have the separate fields for the name in the database, which are firstname, lastname and middle initial.</p>
<p>So far what i have tried:</p>
<pre><code>
var filtered = (from c in _dbContext.Address
                join i in _dbContext.Customers.Where(a =&gt; !request.AccountNumbers.Any() || 
                request.AccountNumbers.Contains(a.AccountNum)) on c.FkParent equals i.Id
                select new ContactRequestListModel
                {
                    Id = c.ID,
                    FirstName = c.FirstName,
                    LastName = c.LastName,
                    MiddleInitial = c.MiddleInitial
                });

 var query = filtered.AsQueryable();

if (request.Names.Any())
    query = query.Where(x =&gt; request.Names.Contains(x.FullName));

</code></pre>
<p><strong>ContactListRequestModel</strong></p>
<pre><code>public class ContactRequestListModel : ContactRequestModel

{
    public int Id { get; set; }
    public string FullName =&gt; string.Join(&quot; &quot;, new string[] { FirstName, MiddleInitial, LastName }.Where(s =&gt; !string.IsNullOrEmpty(s)));
}
</code></pre>
<p>The middle initial could be null, so which could add the double spaces while concatenating the string, so I have tried to omit the spaces in the <code>name</code>. But this query has given me the error.</p>
<blockquote>
<p>The LINQ expression ... could not be translated. Either rewrite the
query in a form that can be translated, or switch to client evaluation
explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable',
'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I didn't want to convert the query to ToList() and filter by name.</p>
<p>But is there any way to query by null checking the <code>MiddleInitial</code> and query as <code>AsQueryable</code>. What is the workaround in this case?</p>

## Answers
### Answer ID: 68755704
<p>Did you try to use + operator:</p>
<pre><code>public string FullName {
      get {
         return FirstName + MiddleInitial ?? &quot;&quot; + LastName ;
      }
}
</code></pre>

