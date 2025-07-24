# TimeOfDay issue in EF Core 6 and SQLite
[Link to question](https://stackoverflow.com/questions/73488706/timeofday-issue-in-ef-core-6-and-sqlite)
**Creation Date:** 1661435307
**Score:** 0
**Tags:** c#, sqlite, entity-framework-core
## Question Body
<p>I have a problem querying a SQLite database using EF Core 6.</p>
<p>The query is pretty simple:</p>
<pre><code>_context.SomeTable
        .AsNoTracking()
        .Where(x =&gt; x.SomeDateTimeColumn.Value.TimeOfDay &lt;= DateTime.Now.TimeOfDay)
        .ToList();
</code></pre>
<p>The exception message states that the query could not be translated:</p>
<blockquote>
<p>The LINQ expression 'DbSet().Where(t =&gt; t.SomeDateTimeColumn.Value.TimeOfDay &lt;= DateTime.Now.TimeOfDay)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation...</p>
</blockquote>
<p>My problem is that, according to the documentation, <code>DateTime.TimeOfDay</code> should be supported by the SQLite database provider. See here: <a href="https://learn.microsoft.com/en-us/ef/core/providers/sqlite/functions#date-and-time-functions" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/ef/core/providers/sqlite/functions#date-and-time-functions</a></p>
<p>Does anyone know the reason for this or could point me to what I'm missing?</p>

## Answers
### Answer ID: 73490205
<p><code>TimeSpan</code> values are not yet supported by EF Core. Please upvote issue <a href="https://github.com/dotnet/efcore/issues/18844" rel="nofollow noreferrer">#18844</a>.</p>
<p>Hmm, you might be able to do it using <code>Ticks</code>. But the precision might be kinda bad.</p>
<pre><code>x.SomeDateTimeColumn.Value.Ticks % 864000000000 &lt;= DateTime.Now.Ticks % 864000000000
</code></pre>
<p>For better precision, you can <a href="https://learn.microsoft.com/ef/core/querying/user-defined-function-mapping" rel="nofollow noreferrer">manually map</a> the <code>julianday</code> function.</p>

### Answer ID: 73488938
<p>I think it might be related to the way DateTime works.</p>
<p>Instead of using:</p>
<pre><code>_context.SomeTable
    .AsNoTracking()
    .Where(x =&gt; x.SomeDateTimeColumn.Value.TimeOfDay &lt;= DateTime.Now.TimeOfDay)
    .ToList();
</code></pre>
<p>Try this:</p>
<pre><code>_context.SomeTable
    .AsNoTracking()
    .Where(x =&gt; x.SomeDateTimeColumn &lt;= DateTime.Now)
    .ToList();
</code></pre>

