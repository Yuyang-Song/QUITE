# Storing an Array as comma separated, how to query with LINQ?
[Link to question](https://stackoverflow.com/questions/61400992/storing-an-array-as-comma-separated-how-to-query-with-linq)
**Creation Date:** 1587701365
**Score:** 1
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>I am storing a <code>List&lt;string&gt;</code> in SQL database as comma separated values using EF Core's <code>HasConversion</code> function.  I appreciate the simplicity of this, but now I am struggling to query on this property.  Right now I work around this by filtering after retrieving the records from the DB, but I would prefer to improve the query.  How could I write my LINQ query such that EF Core can translate this into a SQL statement?</p>

<p>The property:</p>

<pre class="lang-c prettyprint-override"><code>public List&lt;string&gt; AccountTypes { get; set; }
</code></pre>

<p>The configuration in DB context:</p>

<pre class="lang-c prettyprint-override"><code>modelBuilder.Entity&lt;Account&gt;().Property(c =&gt; c.AccountTypes).HasConversion(
        t =&gt; string.Join(',', t),
        t =&gt; t.Split(',', StringSplitOptions.RemoveEmptyEntries));
</code></pre>

<p>Example query that fails to be converted to SQL:</p>

<pre class="lang-c prettyprint-override"><code>IQueryable&lt;Account&gt; query = context.Accounts.Where(a =&gt; a.AccountTypes.Any(t =&gt; t == "A")).AsQueryable();
</code></pre>

<p>Error message:</p>

<blockquote>
  <p>The LINQ expression could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>

<p>I read the <a href="https://learn.microsoft.com/en-us/ef/core/querying/client-eval" rel="nofollow noreferrer">Microsoft article</a> related to Client vs Server evaluation, but I don't believe using Client side evaluation has any benefit over my current workaround of just filtering the results after the database query has returned.  My expectation is that inserting any of the suggested calls will just execute the SQL at that point, returning a large subset and only then applying the filter on <code>AccountTypes</code>.</p>

## Answers
### Answer ID: 73048318
<p>Simply cast the type to string (if no conversion exists, then first cast to object) and perform the comparison:</p>
<pre><code>IQueryable&lt;Account&gt; query = context.Accounts.Where(a =&gt; ((string)(object)a.AccountTypes).Contains(&quot;A&quot;)).AsQueryable();
</code></pre>

### Answer ID: 64311515
<p>Herohtar had provided an answer in the comment:</p>
<blockquote>
<p>You'll probably have to start storing the list differently. The split can't be done as part of a SQL query.</p>
</blockquote>

