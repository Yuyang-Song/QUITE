# How to query SQL Server using DateOnly with ef core
[Link to question](https://stackoverflow.com/questions/73193111/how-to-query-sql-server-using-dateonly-with-ef-core)
**Creation Date:** 1659354131
**Score:** 5
**Tags:** c#, sql-server, linq, date, entity-framework-core
## Question Body
<p>I'm using .NET 6 and EF Core 6 with SQL Server and want to use the new <code>DateOnly</code> type.</p>
<p>I've been able to read and write data to the database using <a href="https://www.thetechplatform.com/post/using-dateonly-with-net-6-webapi-and-entity-framework" rel="nofollow noreferrer">this converter</a> however querying the table doesn't work because Linq doesn't know how to translate <code>DateOnly</code>.</p>
<p>Converter registration in <code>DbContext</code>:</p>
<pre><code>protected override void ConfigureConventions
(ModelConfigurationBuilder builder)        
{
    builder.Properties&lt;DateOnly&gt;()                
        .HaveConversion&lt;DateOnlyConverter&gt;()                
        .HaveColumnType(&quot;date&quot;);
    builder.Properties&lt;DateOnly?&gt;()                
        .HaveConversion&lt;NullableDateOnlyConverter&gt;()                
        .HaveColumnType(&quot;date&quot;);        
}
</code></pre>
<p>Example</p>
<pre><code>    public XXXXByDateSpec(DateOnly validFrom)
    {
        Query.Where(x =&gt; x.ValidFrom.Year &lt;= validFrom.Year);
    }
</code></pre>
<p>But this results in the following exception.</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet().Where(c =&gt; c.ValidFrom.Year &lt;= __validFrom_Year_1)' could not be translated.<br />
Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>And when I'm trying to first parse it to a <code>DateTime</code> results in a similar error.</p>
<pre><code>Query.Where(x =&gt; DateTime.Parse(x.ValidFrom.ToString()).Year &lt;= DateTime.Parse(validFrom.ToString()).Year);
</code></pre>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet().Where(c =&gt; DateTime.Parse(c.ValidFrom.ToString()).Year &lt;= __Parse_Year_0)' could not be translated. Additional information: Translation of method 'object.ToString' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information.<br />
Translation of method 'object.ToString' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>How can I tell Linq to do the same like EF Core and before translating the code to SQL do a type conversion to <code>DateTime</code>? Is this possible?</p>
<p>Or how can I register the <code>ToString()</code> call to Linq? The links from the exception don't really help me out.</p>

## Answers
### Answer ID: 76319615
<p>I ran into this problem today and couldn't change my where clause. I found a <a href="https://github.com/dotnet/efcore/issues/28111" rel="nofollow noreferrer">GitHub issue</a> with the fix.</p>
<ol>
<li>Inherit from the <code>&lt;Provider&gt;MemberTranslatorProvider</code> class, e.g. <code>Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerMemberTranslatorProvider</code></li>
<li>Peek inside the above class. You should find a member translator like <code>&lt;Provider&gt;DateTimeMemberTranslator</code>, e.g. <code>SqlServerDateTimeMemberTranslator</code>.</li>
<li>Copy <code>DateTimeMemberTranslator</code> into a new class, <code>DateOnlyMemberTranslator</code> and change the code accordingly (type check and remove all time code).</li>
<li>In the new class from step #1, call the base constructor and do a call to <code>AddTranslators</code> to add the new translator!</li>
<li>Finally, we have to use the translator provider by replacing the existing service:
<pre class="lang-cs prettyprint-override"><code>protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    base.OnConfiguring(optionsBuilder);
    optionsBuilder.ReplaceService&lt;Microsoft.EntityFrameworkCore.Query.IMemberTranslatorProvider, MyProviderMemberTranslatorProvider&gt;();
}
</code></pre>
</li>
</ol>
<p>The github issue also recommends writing a plugin, but the above solution was super quick to write 😁.</p>
<p>There is a warning for using efcore internal classes.</p>
<blockquote>
<p>EF1001: Microsoft.EntityFrameworkCore.SqlServer.Query.Internal.SqlServerMemberTranslatorProvider is an internal API that supports the Entity Framework Core infrastructure and not subject to the same compatibility standards as public APIs. It may be changed or removed without notice in any release.<br />
— <a href="https://github.com/dotnet/efcore/issues/12104" rel="nofollow noreferrer">Microsoft</a></p>
</blockquote>

### Answer ID: 73193372
<p>This should work, though not as readable. This benefits from using index if present. Also a contract with DateOnly as the parameter is confusing if only the year part is used.</p>
<pre><code> public XXXXByDateSpec(int year)
 {
    Query.Where(x =&gt; x.ValidFrom &lt; new DateOnly(year + 1, 1, 1);
 }
</code></pre>

