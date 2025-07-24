# Comparing decimals within a LINQ query using a SQLite-database fails with operators but works with .CompareTo
[Link to question](https://stackoverflow.com/questions/79271856/comparing-decimals-within-a-linq-query-using-a-sqlite-database-fails-with-operat)
**Creation Date:** 1733923117
**Score:** 1
**Tags:** c#, .net, sqlite, entity-framework, entity-framework-core
## Question Body
<p>In my SQLite database, I have a table <code>foo</code> that contains a column <code>bar</code> that is of data type <code>decimal</code>. I want to retreive all rows, where the value of <code>bar</code> is <code>&gt; 100</code>.</p>
<p>If I try to execute the query like this:</p>
<pre class="lang-cs prettyprint-override"><code>var result = from r in db.Foo
             where r.Bar &gt; 100
             select Bar;
</code></pre>
<p>I get the following error:</p>
<pre><code>The LINQ expression 'DbSet&lt;Foo&gt;.Where(r =&gt; r.Bar &gt; 100)' could not be translated. 

Either rewrite the query in a form that can be translated, 
or switch to client evaluation explicitly by inserting a call to either 
AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). 
See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>
<p>However, if I rewrite the query to use <code>.CompareTo()</code> instead of <code>&gt;</code>, it works without a problem:</p>
<pre class="lang-cs prettyprint-override"><code>var result = from r in db.Foo
             where r.Bar.CompareTo(100) &gt; 0
             select r;
</code></pre>
<p>I don't quite get why the first query works but the second one does not since they basically do the same things. Does <code>.CompareTo()</code> trigger client-side evaluation?</p>

## Answers
### Answer ID: 79272207
<p>SQLite doesn't natively support <code>decimal</code>, however, EF Core can read and write values of these types, and querying for <strong>equality</strong>. [<a href="https://learn.microsoft.com/en-us/ef/core/providers/sqlite/limitations#query-limitations" rel="nofollow noreferrer">Source</a>] This is why <code>Bar &gt; 100</code> does not work and is throwing an error.</p>
<p>The reason why <code>Bar.CompareTo(100) &gt; 0</code> works, is, because entity framework translates <code>.CompareTo</code> into the following query:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT 
    &quot;p&quot;.&quot;Bar&quot;
FROM 
    &quot;Foo&quot; AS &quot;p&quot;
WHERE
    CASE
        WHEN &quot;p&quot;.&quot;Bar&quot; = '100.0' THEN 0
        WHEN &quot;p&quot;.&quot;Bar&quot; &gt; '100.0' THEN 1
        WHEN &quot;p&quot;.&quot;Bar&quot; &lt; '100.0' THEN -1
    END &gt; 0
</code></pre>
<p>Here, entity framework converts the <code>100</code> to a <code>TEXT</code> and does the comparison that way.</p>
<p>This is probably not a very efficient way of handling the comparison. A better way would be to convert <code>Bar</code> to a <code>double</code> like so:</p>
<pre class="lang-cs prettyprint-override"><code>var result = from r in db.Foo
             where (double)r.Bar &gt; 100
             select Bar;
</code></pre>
<p>The resulting SQL-query is:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT 
    &quot;p&quot;.&quot;Bar&quot; 
FROM 
    &quot;Foo&quot; AS &quot;p&quot; 
WHERE 
    CAST(&quot;p&quot;.&quot;Bar&quot; AS REAL) &gt; 100.0
</code></pre>

