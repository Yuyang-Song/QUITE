# EF Core filter Enums stored as string with LIKE operator
[Link to question](https://stackoverflow.com/questions/64514805/ef-core-filter-enums-stored-as-string-with-like-operator)
**Creation Date:** 1603551955
**Score:** 8
**Tags:** c#, .net-core, entity-framework-core, ef-core-3.1
## Question Body
<p>I have a <code>Person</code> model with a <code>Gender</code> enum poperty which is stored as a string in the database.
I want to make a query to filter the data by a substring of the gender. For example if the <code>query.SearchLike</code> is <code>&quot;Fe&quot;</code> or <code>&quot;em&quot;</code>, I'd like to get back every Female persons.
Unfortunately the code below throws an exception.</p>
<pre class="lang-cs prettyprint-override"><code>builder.Entity&lt;Person&gt;().Property(x =&gt; x.Gender).HasConversion&lt;string&gt;();
</code></pre>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IList&lt;Person&gt;&gt; ListAsync(PersonsQuery query)
{
  IQueryable&lt;Person&gt; queryable = _context.Persons.AsNoTracking();

  return await queryable
    .Where(x =&gt; x.Gender.ToString().Contains(query.SearchLike))
    .ToListAsync();
}
</code></pre>
<p>Exception:</p>
<blockquote>
<p>The LINQ expression 'DbSet\r\n    .Where(x =&gt;
x.Gender.ToString().Contains(__query_SearchLike_0))' could not be
translated. Either rewrite the query in a form that can be translated,
or switch to client evaluation explicitly by inserting a call to
either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
more information.</p>
</blockquote>

## Answers
### Answer ID: 64522768
<p>You can use <code>FromSql</code> method to execute a raw SQL statement</p>
<pre><code>public async Task&lt;IList&lt;Person&gt;&gt; ListAsync(PersonsQuery query)
{    
    var param = $&quot;%{query.SearchLike}%&quot;
    return await _context.Persons
        .FromSql(&quot;SELECT * FROM Persons WHERE Gender LIKE {0}&quot; , param)
        .ToListAsync();
}
</code></pre>

### Answer ID: 64522644
<p>I found the solution.
First need to cast the enum to <code>object</code> and then to <code>string</code>.</p>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IList&lt;Person&gt;&gt; ListAsync(PersonsQuery query)
{
  IQueryable&lt;Person&gt; queryable = _context.Persons.AsNoTracking();

  return await queryable
    .Where(x =&gt; ((string)(object)x.Gender).Contains(query.SearchLike))
    .ToListAsync();
}
</code></pre>
<p>Related question in the <a href="https://github.com/dotnet/efcore/issues/20604" rel="noreferrer">EF Core Github repo</a>.</p>

### Answer ID: 64517393
<p>From my understending, you should use EF Like functions. Try something like this:</p>
<pre><code>public async Task&lt;IList&lt;Person&gt;&gt; ListAsync(PersonsQuery query)
{
  IQueryable&lt;Person&gt; queryable = _context.Persons.AsNoTracking();

  return await queryable
    .Where(x =&gt; EF.Functions.Like(x.Gender, &quot;%&quot; + query.SearchLike + &quot;%&quot;)
    .ToListAsync();
}
</code></pre>

