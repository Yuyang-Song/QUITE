# Using a LINQ ExpressionVisitor to replace primitive parameters with property references in a lambda expression
[Link to question](https://stackoverflow.com/questions/11164009/using-a-linq-expressionvisitor-to-replace-primitive-parameters-with-property-ref)
**Creation Date:** 1340398617
**Score:** 14
**Tags:** c#, linq, lambda, expression, visitor-pattern
## Question Body
<p>I'm in the process of writing a data layer for a part of our system which logs information about automated jobs that run every day - name of the job, how long it ran, what the result was, etc.</p>

<p>I'm talking to the database using Entity Framework, but I'm trying to keep those details hidden from higher-level modules and I don't want the entity objects themselves to be exposed.</p>

<p>However, I would like to make my interface very flexible in the criteria it uses to look up job information. For example, a user interface should allow the user to execute complex queries like "give me all jobs named 'hello' which ran between 10:00am and 11:00am that failed." Obviously, this looks like a job for dynamically-built <code>Expression</code> trees.</p>

<p>So what I'd like my data layer (repository) to be able to do is accept LINQ expressions of type <code>Expression&lt;Func&lt;string, DateTime, ResultCode, long, bool&gt;&gt;</code> (lambda expression) and then behind the scenes convert that lambda to an expression that my Entity Framework <code>ObjectContext</code> can use as a filter inside a <code>Where()</code> clause.</p>

<p>In a nutshell, I'm trying to convert a lambda expression of type <code>Expression&lt;Func&lt;string, DateTime, ResultCode, long, bool&gt;&gt;</code> to <code>Expression&lt;Func&lt;svc_JobAudit, bool&gt;&gt;</code>, where <code>svc_JobAudit</code> is the Entity Framework data object which corresponds to the table where job information is stored. (The four parameters in the first delegate correspond to the name of the job, when it ran, the result, and how long it took in MS, respectively)</p>

<p>I was making very good progress using the <code>ExpressionVisitor</code> class until I hit a brick wall and received an <code>InvalidOperationException</code> with this error message:</p>

<blockquote>
  <p>When called from 'VisitLambda', rewriting a node of type
  'System.Linq.Expressions.ParameterExpression' must return a non-null
  value of the same type. Alternatively, override 'VisitLambda' and
  change it to not visit children of this type.</p>
</blockquote>

<p>I'm completely baffled. Why the heck won't it allow me to convert expression nodes which reference parameters to nodes which reference properties? Is there another way to go about this?</p>

<p>Here is some sample code:</p>

<pre><code>namespace ExpressionTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Expression&lt;Func&lt;string, DateTime, ResultCode, long, bool&gt;&gt; expression = (myString, myDateTime, myResultCode, myTimeSpan) =&gt; myResultCode == ResultCode.Failed &amp;&amp; myString == "hello";
            var result = ConvertExpression(expression);
        }

        private static Expression&lt;Func&lt;svc_JobAudit, bool&gt;&gt; ConvertExpression(Expression&lt;Func&lt;string, DateTime, ResultCode, long, bool&gt;&gt; expression)
        {
            var newExpression = Expression.Lambda&lt;Func&lt;svc_JobAudit, bool&gt;&gt;(new ReplaceVisitor().Modify(expression), Expression.Parameter(typeof(svc_JobAudit)));
            return newExpression;
        }
    }

    class ReplaceVisitor : ExpressionVisitor
    {
        public Expression Modify(Expression expression)
        {
            return Visit(expression);
        }

        protected override Expression VisitParameter(ParameterExpression node)
        {
            if (node.Type == typeof(string))
            {
                return Expression.Property(Expression.Parameter(typeof(svc_JobAudit)), "JobName");
            }
            return node;
        }
    }
}
</code></pre>

## Answers
### Answer ID: 11164662
<p>The problem was two-fold:</p>

<ul>
<li><p>I was misunderstanding how to visit the Lambda expression type. I was still returning a lambda which matched the old delegate instead of returning a new lambda to match the new delegate.</p></li>
<li><p>I needed to hold a reference to the new <code>ParameterExpression</code> instance, which I wasn't doing.</p></li>
</ul>

<p>The new code looks like this (notice how the visitor now accepts a reference to a <code>ParameterExpression</code> matching the Entity Framework data object):</p>

<pre><code>class Program
{
    const string conString = @"myDB";

    static void Main(string[] args)
    {
        Expression&lt;Func&lt;string, DateTime, byte, long, bool&gt;&gt; expression = (jobName, ranAt, resultCode, elapsed) =&gt; jobName == "Email Notifications" &amp;&amp; resultCode == (byte)ResultCode.Failed;
        var criteria = ConvertExpression(expression);

        using (MyDataContext dataContext = new MyDataContext(conString))
        {
            List&lt;svc_JobAudit&gt; jobs = dataContext.svc_JobAudit.Where(criteria).ToList();
        }
    }

    private static Expression&lt;Func&lt;svc_JobAudit, bool&gt;&gt; ConvertExpression(Expression&lt;Func&lt;string, DateTime, byte, long, bool&gt;&gt; expression)
    {
        var jobAuditParameter = Expression.Parameter(typeof(svc_JobAudit), "jobAudit");
        var newExpression = Expression.Lambda&lt;Func&lt;svc_JobAudit, bool&gt;&gt;(
            new ReplaceVisitor()
               .Modify(expression.Body, jobAuditParameter), jobAuditParameter);
        return newExpression;
    }
}

class ReplaceVisitor : ExpressionVisitor
{
    private ParameterExpression parameter;

    public Expression Modify(Expression expression, ParameterExpression parameter)
    {
        this.parameter = parameter;
        return Visit(expression);
    }

    protected override Expression VisitLambda&lt;T&gt;(Expression&lt;T&gt; node)
    {
        return Expression.Lambda&lt;Func&lt;svc_JobAudit, bool&gt;&gt;(Visit(node.Body), Expression.Parameter(typeof(svc_JobAudit)));
    }

    protected override Expression VisitParameter(ParameterExpression node)
    {
        if (node.Type == typeof(string))
        {
            return Expression.Property(parameter, "JobName");
        }
        else if (node.Type == typeof(DateTime))
        {
            return Expression.Property(parameter, "RanAt");
        }
        else if (node.Type == typeof(byte))
        {
            return Expression.Property(parameter, "Result");
        }
        else if (node.Type == typeof(long))
        {
            return Expression.Property(parameter, "Elapsed");
        }
        throw new InvalidOperationException();
    }
}
</code></pre>

### Answer ID: 36462181
<p>The accepted answer is 'hardcoded' to some specific types. Here's a more general expression rewriter than can substitute a parameter for any other expression (lambda, constant, ...). In the case of a lambda expression the expression's signature needs to change to incorporate the parameters needed by the substituted value.</p>

<pre><code>public class ExpressionParameterSubstitute : System.Linq.Expressions.ExpressionVisitor
{
    private readonly ParameterExpression from;
    private readonly Expression to;
    public ExpressionParameterSubstitute(ParameterExpression from, Expression to)
    {
        this.from = from;
        this.to = to;
    }

    protected override Expression VisitLambda&lt;T&gt;(Expression&lt;T&gt; node)
    {
        if (node.Parameters.All(p =&gt; p != this.from))
            return node;

        // We need to replace the `from` parameter, but in its place we need the `to` parameter(s)
        // e.g. F&lt;DateTime,Bool&gt; subst F&lt;Source,DateTime&gt; =&gt; F&lt;Source,bool&gt;
        // e.g. F&lt;DateTime,Bool&gt; subst F&lt;Source1,Source2,DateTime&gt; =&gt; F&lt;Source1,Source2,bool&gt;

        var toLambda = to as LambdaExpression;
        var substituteParameters = toLambda?.Parameters ?? Enumerable.Empty&lt;ParameterExpression&gt;();

        ReadOnlyCollection&lt;ParameterExpression&gt; substitutedParameters
            = new ReadOnlyCollection&lt;ParameterExpression&gt;(node.Parameters
                .SelectMany(p =&gt; p == this.from ? substituteParameters : Enumerable.Repeat(p, 1) )
                .ToList());

        var updatedBody = this.Visit(node.Body);        // which will convert parameters to 'to'
        return Expression.Lambda(updatedBody, substitutedParameters);
    }

    protected override Expression VisitParameter(ParameterExpression node)
    {
        var toLambda = to as LambdaExpression;
        if (node == from) return toLambda?.Body ?? to;
        return base.VisitParameter(node);
    }
}
</code></pre>

