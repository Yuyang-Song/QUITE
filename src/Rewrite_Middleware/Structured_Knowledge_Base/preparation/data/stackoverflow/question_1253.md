# Error while flattening the IQueryable&lt;T&gt; after GroupBy()
[Link to question](https://stackoverflow.com/questions/66526675/error-while-flattening-the-iqueryablet-after-groupby)
**Creation Date:** 1615193131
**Score:** 2
**Tags:** c#, entity-framework, linq
## Question Body
<p>I am trying to get flattened object from the database, but I get an error. I want to get 2 books for all genres in the database, the code looks like this:</p>
<pre class="lang-cs prettyprint-override"><code>IQueryable&lt;Book&gt; query = _context.Books
                                 .GroupBy(b =&gt; b.Genre)
                                 .SelectMany(bc =&gt; bc.Select(b =&gt; b).Take(2));
</code></pre>
<p>Does anyone know what am I doing wrong in here?</p>
<p>I get this exception instead of a result :</p>
<blockquote>
<p>The LINQ expression '<code>bc =&gt; bc .AsQueryable() .Select(b =&gt; b) .Take(2)</code>' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See go.microsoft.com/fwlink/?linkid=2101038 for more information.</p>
</blockquote>
<p>I tried also something like that :</p>
<pre><code>IQueryable&lt;Book&gt; query = _context.Genres.GroupJoin(
     _context.Books,
     g =&gt; g,
     b =&gt; b.Genre,
     (g, books) =&gt; new
     {
         Genre = g,
         BookCollection = books
     }
    ).SelectMany(bc =&gt; bc.BookCollection.Select(b =&gt; b)
    .Take(2)).Include(b =&gt; b.Author).Include(b =&gt; b.Rating)
             .Include(b =&gt; b.BookISBNs).Include(b =&gt; b.Reviews)
             .ThenInclude(r =&gt; r.User);
</code></pre>

## Answers
### Answer ID: 66529949
<p>This attempt moves away from group by, which is restrictive in the database and EF query translation. Instead, we're going for a subquery.</p>
<pre><code>var genres = _context.Books.Select(b =&gt; b.Genre).Distinct();
var books =
  from genre in genres
  from book in _context.Books.Where(b =&gt; b.Genre == genre).Take(2)
  select book;

var results = books.ToArrayAsync();
</code></pre>
<p>Aiming for this kind of translation:</p>
<pre><code>SELECT c.*
FROM
  (SELECT DISTINCT Genre FROM Books) as a,
  (SELECT top 2 b.* FROM Books b WHERE b.Genre = a.Genre) as c
</code></pre>

### Answer ID: 66528394
<p>So, you want to group the <code>Book</code> entities by <code>Genre</code>, and then get a flat list of books containing two books from each group. I don't think you can express that with a <code>LINQ</code> query using <code>GroupBy()</code> which Entity Framework can translate to SQL.</p>
<p>But its not EF's fault or shortcoming. <code>GROUP BY</code> in SQL is restricted to return only the grouping key(s) and/or any aggregation performed on the group. For example, you can group the books by <code>Genre</code>, and then want the genre and total number of books per group -</p>
<pre class="lang-cs prettyprint-override"><code>var result = dbCtx.Books
    .GroupBy(p =&gt; p.Genre)
    .Select(g =&gt; new
    {
        Genre = g.Key,       // grouping key
        Count = g.Count()    // aggregation on group
    })
    .ToList();
</code></pre>
<p>EF can generate SQL for that -</p>
<pre class="lang-sql prettyprint-override"><code>SELECT [b].[Genre] AS [Key], COUNT(*) AS [Count]
FROM [Books] AS [b]
GROUP BY [b].[Genre]
</code></pre>
<p>This reference might help - <a href="https://learn.microsoft.com/en-us/ef/core/querying/complex-query-operators#groupby" rel="nofollow noreferrer">GroupBy</a></p>
<blockquote>
<p>Since no database structure can represent an IGrouping, GroupBy
operators have no translation in most cases. When an aggregate
operator is applied to each group, which returns a scalar, it can be
translated to SQL GROUP BY in relational databases. The SQL GROUP BY
is restrictive too. It requires you to group only by scalar values.
The projection can only contain grouping key columns or any aggregate
applied over a column.</p>
</blockquote>
<p>Therefore, for your query, you have to fetch the books and do the grouping on the client side, like -</p>
<pre class="lang-cs prettyprint-override"><code>var result = dbCtx.Books.AsEnumerable()
    .GroupBy(p =&gt; p.Genre)
    .SelectMany(g =&gt; g.Select(book =&gt; book).Take(2).ToList())
    .ToList();
</code></pre>

