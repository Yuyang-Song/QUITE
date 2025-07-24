# How can I convert a custom function to a sql expression for Entity Framework Core 3.1
[Link to question](https://stackoverflow.com/questions/62687811/how-can-i-convert-a-custom-function-to-a-sql-expression-for-entity-framework-cor)
**Creation Date:** 1593655063
**Score:** 3
**Tags:** c#, sql-server, entity-framework, linq-to-entities
## Question Body
<p>I am looking for some guidance/help on how to approach my problem as I'm running out of ideas.  I am trying to take a custom extension function and pass it to the database via Entity Framework (EF Core 3.1) using Linq to Entities but I am getting a &quot;{method} could not be translated&quot; error regardless of what I do.  I have tried using HasDbFunction along with HasTranslation using this link <a href="https://www.thinktecture.com/en/entity-framework-core/custom-functions-using-hasdbfunction-in-2-1/" rel="nofollow noreferrer">Thinktecture - Entity Framework Core - Custom Functions (using HasDbFunction)</a> to no avail.  I have also tried to registera custom DbCommandInterceptor with this link <a href="https://medium.com/aspnetcore/interception-in-entity-framework-core-862529b47f20" rel="nofollow noreferrer">Medium - Interception in Entity Framework Core</a> and it never hits the breakpoint or logs any of my debug statements.  I'm not sure what to try next but I'm looking for help on what I'm doing wrong or guidance on what to research next.</p>
<p>For some context with my problem I am using the class setup below:</p>
<pre><code>namespace Rebates.Models
{
    public class Rebate
    {
        public int Id { get; set; }
        public string ProductName { get; set; }
        public ActiveDateRange ActiveDateRange { get; set; }

        public decimal Discount { get; set; }
    }

    public class ActiveDateRange
    {
        public int StartMonth { get; set; }
        public int EndMonth { get; set; }
    }
}
</code></pre>
<p>DbContext:</p>
<pre><code>namespace Rebates.DB
{
    public class RebateContext : DbContext
    {
        public DbSet&lt;Rebate&gt; Rebates { get; set; }
    }

    protected override void OnConfiguring(DbContextOptionsBuilder options)
    {
        options.UseSqlServer(&quot;Server=(local);Database=Rebates;Trusted_Connection=True;&quot;);
    }
}
</code></pre>
<p>Extension Method I'm trying to turn into a SQL statement:</p>
<pre><code>namespace Rebates.ExtensionMethods
{
    public static class Extensions
    {
        public static bool IsActive(this Rebate rebate, DateTime date)
        {
            return date.Month &gt;= rebate.ActiveDateRange.StartMonth &amp;&amp; date.Month &lt;= rebate.ActiveDateRange.EndMonth;
        }
    }
}
</code></pre>
<p>Call I'm attempting to make in my program:</p>
<pre><code>using (var db = new RebateContext())
{
    var rebates = db.Rebates.Where(x =&gt; x.IsActive(DateTime.Now));
}
</code></pre>
<p>Error Received:</p>
<blockquote>
<p>System.InvalidOperationException: 'The LINQ expression 'DbSet
.Where(c =&gt; EF.Property(c, &quot;ActiveDateRange&quot;).IsActive(DateTime.Now))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.'</p>
</blockquote>
<p>I stripped out all of my failing code to hopefully make this cleaner but I can post my failed attempts as well if it will help, I just didn't want to clutter this already lengthy request.  I have read a little on how to build expression trees and how this translates in EF Core but I'm honestly lost as to where I would even intercept said expression tree to modify it for my goal.  Any help here would be greatly appreciated.</p>

## Answers
### Answer ID: 62708275
<p>An interesting question, that I wanted to solve so I could use it too.</p>
<p>UPDATE; in EF Core 7 I believe you could replace this with an <code>IQueryExpressionInterceptor</code> service.</p>
<p>First we need to add a hook early in the query compilation pipeline. Note that this bit may break in future if the internals of EF Core change;</p>
<pre class="lang-cs prettyprint-override"><code>    public class QueryCompilationFactory : IQueryCompilationContextFactory
    {
        private readonly QueryCompilationContextDependencies dependencies;

        public QueryCompilationFactory(QueryCompilationContextDependencies dependencies)
        {
            this.dependencies = dependencies;
        }

        public QueryCompilationContext Create(bool async) =&gt; new QueryCompilation(dependencies, async);
    }

    public class QueryCompilation : QueryCompilationContext
    {
        public QueryCompilation(QueryCompilationContextDependencies dependencies, bool async) : base(dependencies, async)
        {
        }

        public override Func&lt;QueryContext, TResult&gt; CreateQueryExecutor&lt;TResult&gt;(Expression query)
        {
            // TODO, modify the query here
            return base.CreateQueryExecutor&lt;TResult&gt;(query);
        }
    }

    // in startup...
    services.AddDbContextPool&lt;..&gt;(o =&gt;
    {
        o.ReplaceService&lt;IQueryCompilationContextFactory, QueryCompilationFactory&gt;();
        // ...
    }
</code></pre>
<p>Ok, so now we want a general way to replace a function call with an equivalent expression. That way the rest of the query pipeline can turn that into sql for us. Lets write an ExpressionVisitor that replaces method calls by inlining another LambdaExpression. Replacing the lambda parameters with the call arguments wherever they appear. Then we can use the visitor to replace the TODO above.</p>
<pre class="lang-cs prettyprint-override"><code>    private static Dictionary&lt;MethodInfo, LambdaExpression&gt; replacementExpressions = new Dictionary&lt;MethodInfo, LambdaExpression&gt;();

    public static void ReplaceMethod&lt;T&gt;(T method, Expression&lt;T&gt; replacement) where T : Delegate =&gt;
        replacementExpressions.Add(method.Method, replacement);

    public class ArgumentVisitor : ExpressionVisitor
    {
        private readonly Dictionary&lt;ParameterExpression, Expression&gt; parameters;
        public ArgumentVisitor(Dictionary&lt;ParameterExpression, Expression&gt; parameters)
        {
            this.parameters = parameters;
        }

        protected override Expression VisitParameter(ParameterExpression node)
        {
            if (parameters.TryGetValue(node, out var replacement))
                return replacement;
            return base.VisitParameter(node);
        }
    }

    public class MethodVisitor : ExpressionVisitor
    {
        protected override Expression VisitMethodCall(MethodCallExpression node)
        {
            if (replacementExpressions.TryGetValue(node.Method, out var lambda))
            {
                var args = new Dictionary&lt;ParameterExpression, Expression&gt;();
                for (var i = 0; i &lt; lambda.Parameters.Count; i++)
                    args[lambda.Parameters[i]] = node.Arguments[i];
                return new ArgumentVisitor(args).Visit(lambda.Body);
            }
            return base.VisitMethodCall(node);
        }
    }

    public override Func&lt;QueryContext, TResult&gt; CreateQueryExecutor&lt;TResult&gt;(Expression query)
    {
        query = new MethodVisitor().Visit(query);
        return base.CreateQueryExecutor&lt;TResult&gt;(query);
    }
</code></pre>
<p>Now we can define any static methods we want, and define a replacement expression to use when converting that method call into sql.</p>
<pre class="lang-cs prettyprint-override"><code>    public static bool IsActive(this Rebate rebate, DateTime date) =&gt;
        date.Month &gt;= rebate.ActiveDateRange.StartMonth &amp;&amp; date.Month &lt;= rebate.ActiveDateRange.EndMonth;
    
    static Extensions(){
        QueryCompilation.ReplaceMethod&lt;Func&lt;Rebate,DateTime,bool&gt;&gt;(IsActive, (Rebate rebate, DateTime date) =&gt;
            date.Month &gt;= rebate.ActiveDateRange.StartMonth &amp;&amp; date.Month &lt;= rebate.ActiveDateRange.EndMonth);
    }
</code></pre>

### Answer ID: 71560293
<p>Expanding on <a href="https://stackoverflow.com/a/62708275/5697">Jeremy Lakeman's answer</a>, it's not that difficult to expand this to work for instance methods as well. An additional <code>ReplaceMethod&lt;T&gt;</code> method needs to be added to <code>QueryCompilation</code> like so:</p>
<pre class="lang-cs prettyprint-override"><code>public static void ReplaceMethod&lt;T&gt;(Expression&lt;T&gt; expression, Expression&lt;T&gt; replacement)
    where T : Delegate
{
    if (expression.Body is not MethodCallExpression methodCall)
        throw new ArgumentException(&quot;Not a method call&quot;, nameof(expression));
    if (methodCall.Object != null &amp;&amp; !expression.Parameters[0].Type.IsAssignableFrom(methodCall.Object.Type))
        throw new ArgumentException(&quot;Instance method is for wrong type&quot;, nameof(expression));
    ReplacementExpressions.Add(methodCall.Method, replacement);
}
</code></pre>
<p>This could then be used for situations where you want to rewrite a method on an existing class within a query that Entity Framework does not recognize itself:</p>
<pre class="lang-cs prettyprint-override"><code>QueryCompilation.ReplaceMethod&lt;Func&lt;DateRange, DateTime, bool&gt;&gt;(
    (range, time) =&gt; range.Includes(time),
    (range, time) =&gt; range.Start &gt;= time &amp;&amp; range.End &lt;= time
);
</code></pre>

