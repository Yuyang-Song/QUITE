# EF Core - Unable to query if entity.Name exists in List&lt;string&gt;
[Link to question](https://stackoverflow.com/questions/63599482/ef-core-unable-to-query-if-entity-name-exists-in-liststring)
**Creation Date:** 1598450956
**Score:** 0
**Tags:** sql-server, .net-core, linq-to-sql, entity-framework-core
## Question Body
<p>Using <strong>Entity Framework Core 3.1.7</strong></p>
<p>I have a table in the database containing Products.</p>
<pre><code>public class Product 
{
   public int Id {get; set;}
   public string Name {get; set;}
}
</code></pre>
<p>I then want the user to be able to use a search field to find certain Products in a UI table.
When the query comes in I try to do the following:</p>
<pre><code>var searchParameters = query.SearchParameters.ToLower().Split(' ', ',', '+').Distinct();

var result = _context.Products
                    .Where(p =&gt; searchParameters.Any()
                    &amp;&amp; (searchParameters.Any(x =&gt; p.Name.ToLower().Contains(x)) //Version 1
                    ).ToList();
</code></pre>
<p>or an alternative</p>
<pre><code>searchParameters.Any(x =&gt; EF.Functions.Like(p.Name, &quot;%&quot; + x + &quot;%&quot;)) //Version 2
</code></pre>
<p>But however I tweak this seemingly simple thing I get:</p>
<blockquote>
<p>The LINQ expression 'DbSet
.Where(p =&gt; __searchParameters_0
.Any(x =&gt; p.Name.ToLower().Contains(x)))' could not be translated. Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to
either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()</p>
</blockquote>
<p>I realize the <code>.ToLower()</code> is going to be a problem so I wanted to run a LIKE statement for Case Insensitive search as for SQL Queries. But even so, the <code>List&lt;string&gt;</code> is not being translated.</p>

## Answers
### Answer ID: 63621745
<p>If you are willing to use <a href="https://github.com/scottksmith95/LINQKit" rel="nofollow noreferrer">LINQKit</a> (or simulate the predicate builder parts), you can use an extension method to expand the <code>Any(</code>...<code>Contains)</code> expression into an &quot;or&quot; expression:</p>
<pre><code>public static class LinqKitExt { // using LINQKit
    // keyFne - extract string key from row
    // searchTerms - IEnumerable&lt;string&gt; where one must be contained by a row's key
    // dbq.Where(r =&gt; searchTerms.Any(s =&gt; keyFne(r).Contains(s)))
    public static IQueryable&lt;T&gt; WhereContainsAny&lt;T&gt;(this IQueryable&lt;T&gt; dbq, Expression&lt;Func&lt;T,string&gt;&gt; keyFne, IEnumerable&lt;string&gt; searchTerms) {
        var pred = PredicateBuilder.New&lt;T&gt;();
        foreach (var s in searchTerms)
            pred = pred.Or(r =&gt; keyFne.Invoke(r).Contains(s));

        return dbq.Where((Expression&lt;Func&lt;T,bool&gt;&gt;)pred.Expand());
    }
}
</code></pre>
<p>(And the 51 other variations of Where/OrderBy[Descending] Any/All Contains/StartsWith.)</p>
<p>Then you can use it like this</p>
<pre><code>var result = _context.Products
                     .WhereContainsAny(r =&gt; r.Name, searchParameters)
                     .ToList();
</code></pre>
<p>PS Pursuing another answer, I realized that pulling the test to the caller eliminated most variations:</p>
<pre><code>// searchTerms - IEnumerable&lt;TKey&gt; where all must be in a row's key
// testFne(row,searchTerm) - test one of searchTerms against a row
// dbq.Where(r =&gt; searchTerms.Any(s =&gt; testFne(r,s)))
public static IQueryable&lt;T&gt; WhereAny&lt;T,TKey&gt;(this IQueryable&lt;T&gt; dbq, IEnumerable&lt;TKey&gt; searchTerms, Expression&lt;Func&lt;T, TKey, bool&gt;&gt; testFne) {
    var pred = PredicateBuilder.New&lt;T&gt;();
    foreach (var s in searchTerms)
        pred = pred.Or(r =&gt; testFne.Invoke(r, s));

    return dbq.Where((Expression&lt;Func&lt;T,bool&gt;&gt;)pred.Expand());
}
</code></pre>
<p>Then you just call:</p>
<pre><code>var result = _context.Products
                     .WhereAny(searchParameters, (r,s) =&gt; r.Name.Contains(s))
                     .ToList();
</code></pre>

