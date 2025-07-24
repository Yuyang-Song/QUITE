# EF Core 8 - Union LINQ query method doesn&#39;t work against arbitrary data
[Link to question](https://stackoverflow.com/questions/79153265/ef-core-8-union-linq-query-method-doesnt-work-against-arbitrary-data)
**Creation Date:** 1730654474
**Score:** -1
**Tags:** c#, entity-framework-core
## Question Body
<p>I am using EF Core 8 with Npgsql, and I have a model class <code>Attempt</code>:</p>
<pre><code>public class Attempt(int Id, string UserId, int score)
{
    public int Id { get; set; } = Id;
    public string UserId { get; set; } = UserId!;
    public int score { get; set; } = score;
}
</code></pre>
<p>I am attempting to execute a query where I take an arbitrary attempt, (essentially just data, not specifically an existing row in the database) and <code>Union</code> it with the current values in the table as a basis for other queries, Similar to this SQL expression:</p>
<pre><code>SELECT *
FROM your_table
UNION
SELECT 'My_data', 56, 'Also_My_Data';
</code></pre>
<p>My EF Core query is as follows:</p>
<pre><code>Attempt newAttempt = new(7, &quot;Herb&quot;, 56);
var attemptsUnionOne = await db.Attempt.Union([newAttempt]).ToListAsync();
</code></pre>
<p>However, I instantly get an exception saying:</p>
<blockquote>
<p>The LINQ expression 'DbSet().Union(__p_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.</p>
</blockquote>
<p>Does anyone have an idea why <code>Union</code> cannot be translated in my case?</p>

## Answers
### Answer ID: 79153308
<p>You can't have an EF Core query which is partially server-side (the <code>db.Attempt</code> bit) and partially client-side (the <code>newAttempt</code> bit).</p>
<p>You need to first get the main list, then add to it.</p>
<pre><code>var attempts = await db.Attempt.ToListAsync();
var results = attempts.Union([newAttempt]);
</code></pre>
<p>Although it seems much more straightforward to just use <code>.Add</code> or <code>Append</code> with one item.</p>
<pre><code>var attempts = await db.Attempt.ToListAsync();
attempts.Add(newAttempt);
</code></pre>
<p>You possibly might want a hashset or dictionary instead (in order to de-duplicate against existing data), alternatively you might want to store the new data into the table first. It's not clear what you want.</p>

### Answer ID: 79153312
<p><code>Union</code> in yours example is executed on the DB side, so doing it with local that exists in yours app memory, but doesn't exists in the database can be unexpected thing for EF/Npgsql driver creators. It is better to do that on yours app side, what you can achieve using one of mentioned methods before the <code>Union</code> method.</p>

