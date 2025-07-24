# TimeSpan Issue in EF Core 3.1
[Link to question](https://stackoverflow.com/questions/59520997/timespan-issue-in-ef-core-3-1)
**Creation Date:** 1577635504
**Score:** 5
**Tags:** c#, postgresql, entity-framework-core, timespan
## Question Body
<p>I have a problem querying PostgreSQL database using EF Core 3.1.</p>

<p>The query is very simple</p>

<pre><code>var gamesQuery = this.dbContext.Games.Where(game =&gt; game.StartTime &gt; DateTime.Now).AsQueryable();

// 'request.TimeFrom' is of type System.TimeSpan and the value is populated
gamesQuery = gamesQuery.Where(game =&gt; game.StartTime.TimeOfDay &gt;= request.TimeFrom);

// .ToList()-int here causes the exception.
var games = gamesQuery.ToList();
</code></pre>

<p>The exception message clearly states that the query can not be translated:</p>

<p><em>"The LINQ expression 'DbSet\r\n    .Where(g => g.StartTime > DateTime.Now)\r\n    .Where(g => g.StartTime.TimeOfDay >= __request_TimeFrom_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information."</em></p>

<p>The problem is that the same query works fine in .NET Core 2.2.
I haven't found anything about the problem yet.</p>

<p>Someone know what is the reason about this one or am I missing something?</p>

## Answers
### Answer ID: 63400660
<p>I haven't tried this yet but one solution could be to save TimeOfDay into database beside of DateTime property. Then you just compare it with your TimeSpan variable.</p>

### Answer ID: 59521511
<p>Currently PostgreSQL EF Core 3.x query provider does not support translation of <code>DateTime.TimeOfDay</code> - see the <code>TODO</code> comment in the <a href="https://github.com/npgsql/efcore.pg/blob/dev/src/EFCore.PG/Query/ExpressionTranslators/Internal/NpgsqlDateTimeMemberTranslator.cs#L69" rel="nofollow noreferrer">source code</a>.</p>

<p>Most likely it "worked" in 2.x by silently using client evaluation. But implicit client evaluation <a href="https://learn.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.0/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client" rel="nofollow noreferrer">has been removed in 3.0</a> and there is no way to turn it back on.</p>

<p>You can try the following equivalent construct:</p>

<pre><code>.Where(game =&gt; (game.StartTime - game.StartTime.Date) &gt;= request.TimeFrom)
</code></pre>

<p>At least it doesn't produce the aforementioned exception.</p>

<p>If it doesn't work, take their advice and switch explicitly to client evaluation by inserting <code>AsEnumerable()</code> in the appropriate place before the non translatable expression.</p>

