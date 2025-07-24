# ASP.NET Core OData $expand with FluentValidation not working
[Link to question](https://stackoverflow.com/questions/63896140/asp-net-core-odata-expand-with-fluentvalidation-not-working)
**Creation Date:** 1600150479
**Score:** 2
**Tags:** c#, asp.net-core, entity-framework-core, odata, fluentvalidation
## Question Body
<p>I'm trying to query with OData using the <strong>$expand</strong> operator but when using <strong>AbstractValidator</strong> inheritance, I'm receiving a <em>System.InvalidOperationException: When called from 'VisitLambda', rewriting a node of type 'System.Linq.Expressions.ParameterExpression' must return a non-null value of the same type. Alternatively, override 'VisitLambda' and change it to not visit children of this type</em>. However without <strong>AbstractValidator</strong> inheritance, the query go successfully.</p>
<p>The request I'm trying to execute is:
https://localhost:44316/developer/oncontextpaging?$expand=Goal</p>
<p>The full code is on my github, the configuration is already set, just need to run: <strong>update-database</strong> and simulate the above request.
<a href="https://github.com/adlerpagliarini/ODataSamples/tree/1643ca615de346613081c34a58f1166ec741c42b" rel="nofollow noreferrer">https://github.com/adlerpagliarini/ODataSamples/tree/1643ca615de346613081c34a58f1166ec741c42b</a></p>
<pre><code>public abstract class Identity&lt;TEntity&gt; : AbstractValidator&lt;TEntity&gt;
{
    protected Identity() { }
    public int Id { get; set; }
}

public class Developer : Identity&lt;Developer&gt;
{
    public string Name { get; set; }
    public Goal Goal { get; set; }
}

public class Goal : Identity&lt;Goal&gt;
{
    public string Title { get; set; }
    public int UserId { get; set; }
}
</code></pre>

