# Is Using EF Core Value Converter Preventing the Contains() LINQ Method from being Translated to SQL?
[Link to question](https://stackoverflow.com/questions/72054486/is-using-ef-core-value-converter-preventing-the-contains-linq-method-from-bein)
**Creation Date:** 1651218503
**Score:** 2
**Tags:** c#, linq, entity-framework-core, linq-to-entities
## Question Body
<p>I have a <code>Movie</code> class. It has a <code>Genres</code> property of type <code>List&lt;string&gt;</code>. I use this exact <a href="https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions?tabs=data-annotations#collections-of-primitives" rel="nofollow noreferrer">EF Core Value Conversion</a> to store it in the database as a comma-separated string.</p>
<p>In my method, I have <code>movies</code>, which is of type <code>IQueryable&lt;Movie&gt;</code>. The method receives genres as a <code>List&lt;string&gt;</code>, and I want to filter the movies according to the genres.</p>
<p>When I apply this filter, this query fails to translate to the database.</p>
<pre><code>var genre = &quot;Drama&quot;;
movies = movies.Where(m =&gt; m.Genres.Contains(genre));
</code></pre>
<p>The filter works if I apply <code>.ToListAsync()</code> to <code>movies</code> and pull all the movies to the client-side. But I'm trying to find a way to do this on the database-side.</p>
<p>I've also tried these variations:</p>
<pre><code>movies = movies.Where(m =&gt; m.Genres.Any(g =&gt; g.Contains(genre)));
movies = movies.Where(m =&gt; m.Genres.Any(g =&gt; g == genre));
</code></pre>
<p>I'm pasting in the error message below:</p>
<blockquote>
<p>.Where(m =&gt; m.Genres
.Contains(__genre_0))' could not be translated. Additional information: Translation of method 'System.Linq.Enumerable.Contains' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>If you want to reproduce it on your computer:</p>
<ul>
<li>Clone <a href="https://github.com/erhanalankus/FreeFlix/tree/filter-translation-issue" rel="nofollow noreferrer">this github repository</a> (filter-translation-issue branch)</li>
<li>Put a breakpoint on <code>SearchMoviesExtendedQuery.cs</code>, line 53.</li>
<li>Run the project(<code>API</code> should be the startup project), it will create the <code>FreeFlixDatabase</code> SQL Server database and seed ten movies, then it will open Swagger UI.</li>
<li>In the Swagger UI, run the <code>/api/catalog/MoviesSearch</code> POST method with the message body: <code>{&quot;genres&quot;:[&quot;string&quot;]}</code></li>
</ul>

## Answers
### Answer ID: 74153608
<p><strong>Approach 1:</strong> As mentioned by John above, you can cast to a string an compare in that way:</p>
<p><code>queryable.Where(x =&gt; ((string)(object)p.ConvertibleProperty) == &quot;sup&quot;)</code></p>
<p><strong>Approach 2:</strong>
I see that this cannot be done directly on the db-side right now. But as you mention, it can be done on the server-side (you called this client side) after a <code>ToListAsync()</code>.</p>
<pre><code>        var r = _context.TblExample.Where(w =&gt; w.Filter == filter);
        if (await r.AnyAsync())
        {
            var rs = await r.ToListAsync();
            var w = rs.Where(w =&gt; w.Categories.Contains(category));
            return w.ToList();
        }
</code></pre>
<p><strong>Another approach:</strong> Not sure of your exact requirements, but you could also consider a timed job to sync the data from this table into another table specially structured for filtering.</p>

