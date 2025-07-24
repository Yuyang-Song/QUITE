# LINQ fails to translate an SqlFunctions method
[Link to question](https://stackoverflow.com/questions/78278590/linq-fails-to-translate-an-sqlfunctions-method)
**Creation Date:** 1712305035
**Score:** 1
**Tags:** c#, sql-server, linq, entity-framework-core
## Question Body
<p>I have a problem with my C# app. I am trying to fetch an item from the SQL Server database, in the database I can use the following query:</p>
<pre class="lang-sql prettyprint-override"><code>SELECT *
FROM [table]
WHERE [field] IS NOT NULL 
    AND [field] != '' 
    AND CONCAT(REPLICATE('0', 10 - LEN([field])), [field]) = 'literal'
</code></pre>
<p>This works perfectly and returns the desired row on the table, so I KNOW for a fact that the item exists.</p>
<p>Then I try to access the same data from my C# backend I do so through a LINQ expression as follows:</p>
<pre class="lang-cs prettyprint-override"><code>var literal = 'xxxxx'
desired = dbContext.dbSet.Where(x =&gt; x.field != null &amp;&amp; x.field != &quot;&quot; &amp;&amp; (
    string.Concat(SqlFunctions.Replicate(&quot;0&quot;, 10 - x.CodigoProductoCia.Length), x.CodigoProductoCia) == literal
)
</code></pre>
<p>The previous snippet of code produces the following exception message:</p>
<blockquote>
<p>The LINQ expression</p>
<p><code>DbSet&lt;Entity&gt;().Where(p =&gt; p.field != null &amp;&amp; p.field != &quot;&quot; &amp;&amp; SqlFunctions.Replicate(target: &quot;0&quot;, count: (int?)(10 - p.CodigoProductoCia.Length)) + p.CodigoProductoCia == &quot;&quot;)</code> could not be translated.</p>
<p>Additional information: Translation of method 'System.Data.Entity.SqlServer.SqlFunctions.Replicate' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.'</p>
</blockquote>
<p>My understanding is that LINQ cannot translate the query to SQL, which is fair and all, but in honesty, I'm only using methods that work in LINQ, and <code>string.Concat()</code> produces the same result as simply a <code>+</code>.</p>
<p>In fact, the error is specifically complaining about <code>SqlFunctions#Replicate</code> which is a method SPECIFICALLY impossible to invoke outside of &quot;LINQ to Entities&quot; queries, which makes this even more confusing.</p>
<p>Any advice?</p>

## Answers
### Answer ID: 78278732
<p><a href="https://learn.microsoft.com/en-us/dotnet/api/system.data.objects.sqlclient.sqlfunctions.replicate?view=netframework-4.8.1" rel="nofollow noreferrer"><code>SqlFunctions.Replicate</code></a> is part of the <code>System.Data</code> and is not translated. EF Core analog is <a href="https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.ef.functions?view=efcore-8.0" rel="nofollow noreferrer"><code>EF.Functions</code></a> but currently it does not have an option for <code>REPLICATE</code> for SQL Server (see <a href="https://github.com/dotnet/efcore/issues/25470" rel="nofollow noreferrer">this github issue</a>).</p>
<p>As workaround you can consider writing a <a href="https://learn.microsoft.com/en-us/ef/core/querying/user-defined-function-mapping" rel="nofollow noreferrer">user-defined function mapping</a>  for now. For example:</p>
<pre class="lang-cs prettyprint-override"><code>class MyContext : DbContext
{  
    [DbFunction(&quot;REPLICATE&quot;, IsBuiltIn = true)]
    public static string Replicate(string s, int i) =&gt; throw new Exception();
    // ...
}

var firstOrDefault = myContext.Entities
    .Where(k =&gt; k.SomeId == 255080)
    .Select(k =&gt; new
    {
        k.SomeId,
        S = MyContext.Replicate(k.SomeString, 10 - k.SomeInt)
    })
    .FirstOrDefault();
</code></pre>
<p>See also:</p>
<ul>
<li><a href="https://learn.microsoft.com/en-us/ef/core/providers/sql-server/functions" rel="nofollow noreferrer">Function Mappings of the Microsoft SQL Server Provider</a></li>
<li><a href="https://learn.microsoft.com/en-us/dotnet/api/microsoft.entityframeworkcore.sqlserverdbfunctionsextensions?view=efcore-8.0" rel="nofollow noreferrer"><code>SqlServerDbFunctionsExtensions</code></a>:
<blockquote>
<p>Provides CLR methods that get translated to database functions when used in LINQ to Entities queries. The methods on this class are accessed via <code>Functions</code>.</p>
</blockquote>
</li>
</ul>

