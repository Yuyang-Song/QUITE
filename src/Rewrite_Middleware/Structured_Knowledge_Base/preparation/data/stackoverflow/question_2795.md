# Error When trying to use an Expression Tree in a Where() clause when using EFCore
[Link to question](https://stackoverflow.com/questions/52637169/error-when-trying-to-use-an-expression-tree-in-a-where-clause-when-using-efcor)
**Creation Date:** 1538611334
**Score:** 2
**Tags:** c#, entity-framework, linq, expression
## Question Body
<p>I'm getting an error while tring to compose an <code>Expression&lt;Func&lt;ApplicationUser, bool&gt;&gt;</code> by combining other expressions. The intent is to use it in the where() clause of an EFCore query. Example:</p>

<pre><code>// Only get users that have been forwarded the request...
var request = GetSomeRequestToFilterOn();
var filter = HasRequestBeenForwaredToUserExpression().ReplaceParameter(request);
var results = _context.ApplicationUsers.Where(filter).ToList();
</code></pre>

<p>In the example above I am converting an <code>Expression&lt;Func&lt;ApplicationUser, TransferRequest, bool&gt;&gt;</code> into and <code>Expression&lt;Func&lt;ApplicationUser, bool&gt;&gt;</code> by replacing the TransferRequest parameter in the expression with the one provided. This works great in my unit tests, but EFCore doesn't seem to like it, and I get this error when running against the actual database:</p>

<blockquote>
  <p>System.InvalidOperationException: Rewriting child expression from type <code>System.Nullable&lt;System.DateTime&gt;</code> to type <code>System.Collections.Generic.IEnumerable&lt;System.Nullable&lt;System.DateTime&gt;&gt;</code>
  is not allowed, because it would change the meaning of the operation.
  If this is intentional, override 'VisitUnary' and change it to allow
  this rewrite. at
  System.Linq.Expressions.ExpressionVisitor.ValidateChildType(Type
  before, Type after, String methodName) at
  System.Linq.Expressions.ExpressionVisitor.ValidateUnary(UnaryExpression
  before, UnaryExpression after) at
  System.Linq.Expressions.ExpressionVisitor.VisitUnary(UnaryExpression
  node) at
  System.Linq.Expressions.UnaryExpression.Accept(ExpressionVisitor
  visitor) at System.Linq.Expressions.ExpressionVisitor.Visit(Expression
  node) at...</p>
</blockquote>

<p>Basically, a person is considered to have been 'forwarded' the transfer request if there are any 'forwarded' events after the last 'awaiting approval' event, i.e. when there is a new 'awaiting approval' event the previous 'forwarded' events don't count anymore (but still exist).</p>

<p>Here is my Filter.</p>

<pre><code>internal static Expression&lt;Func&lt;ApplicationUser, TransferRequest, bool&gt;&gt; HasRequestBeenForwaredToUserExpression()
{
    //only "Forwarded" events after the last "Awaiting Approval" event count.
    //so we need to get the last "Awaiting Approval" event from the request.
    var projection = LastAwaitingApprovalEvent();

    var userParam = Expression.Parameter(typeof(ApplicationUser));
    var requestParam = Expression.Parameter(typeof(TransferRequest));
    var requestToEvent = projection.Body.ReplaceParameter(projection.Parameters[0], requestParam);

    Expression&lt;Func&lt;ApplicationUser, TransferRequest, TransferRequestEvent, bool&gt;&gt; condition =
       (user, rqst, evt) =&gt; evt != null &amp;&amp; rqst.TransferRequestEvents
            .Any(e2 =&gt;
                Equals(e2.EventType, EventType.Forwarded) &amp;&amp;
                Equals(e2.User, user) &amp;&amp;
                e2.EventDateTime &gt; evt.EventDateTime);

    var body = condition.Body
            .ReplaceParameter(condition.Parameters[0], userParam)
            .ReplaceParameter(condition.Parameters[1], requestParam)
            .ReplaceParameter(condition.Parameters[2], requestToEvent);
    return Expression.Lambda&lt;Func&lt;ApplicationUser, TransferRequest, bool&gt;&gt;(body, userParam, requestParam);
}
</code></pre>

<p>This method gets the last "Awaiting Approval" event</p>

<pre><code>internal static Expression&lt;Func&lt;TransferRequest, TransferRequestEvent&gt;&gt; LastAwaitingApprovalEvent()
{
    return t =&gt; t.TransferRequestEvents
        .OrderBy(e =&gt; e.EventDateTime).ThenBy(e =&gt; e.Id)
        .LastOrDefault(e =&gt; Equals(e.EventType, EventType.AwaitingReview));
}
</code></pre>

<p>I have an ExpressionUtility class that does the work of replacing parameters:</p>

<pre><code>public class ExpressionUtility
{
    public static Expression ReplaceParameter(this Expression expression,
        ParameterExpression toReplace,
        Expression newExpression)
    {
        return new ParameterReplaceVisitor(toReplace, newExpression)
            .Visit(expression);
    }

    public static Expression&lt;Func&lt;TArg2, TReturn&gt;&gt; ReplaceParameter&lt;TArg1, TArg2, TReturn&gt;(this Expression&lt;Func&lt;TArg1, TArg2, TReturn&gt;&gt; source, TArg1 arg1)
    {
        var t1Param = Expression.Constant(arg1);
        var t2Param = Expression.Parameter(typeof(TArg2));
        var body = source.Body
                    .ReplaceParameter(source.Parameters[0], t1Param)
                    .ReplaceParameter(source.Parameters[1], t2Param);
        return Expression.Lambda&lt;Func&lt;TArg2, TReturn&gt;&gt;(body, t2Param);
    }

    public static Expression&lt;Func&lt;TArg1, TReturn&gt;&gt; ReplaceParameter&lt;TArg1, TArg2, TReturn&gt;(this Expression&lt;Func&lt;TArg1, TArg2, TReturn&gt;&gt; source, TArg2 arg2)
    {
        var t1Param = Expression.Parameter(typeof(TArg1));
        var t2Param = Expression.Constant(arg2);
        var body = source.Body
                    .ReplaceParameter(source.Parameters[0], t1Param)
                    .ReplaceParameter(source.Parameters[1], t2Param);
        return Expression.Lambda&lt;Func&lt;TArg1, TReturn&gt;&gt;(body, t1Param);
    }
}

public class ParameterReplaceVisitor : ExpressionVisitor
{
    private ParameterExpression from;
    private Expression to;
    public ParameterReplaceVisitor(ParameterExpression from, Expression to)
    {
        this.from = from;
        this.to = to;
    }
    protected override Expression VisitParameter(ParameterExpression node)
    {
        return node == from ? to : base.VisitParameter(node);
    }
}
</code></pre>

<h2><strong><em>edit</em></strong></h2>

<p>When I print the final Expression's ToString to the Console. I get </p>

<blockquote>
  <p>{Param_0 =>
  ((value(Debugging.Models.TransferRequest).TransferRequestEvents.OrderBy(e
  => e.EventDateTime).ThenBy(e => e.Id).LastOrDefault(e => Equals(e.EventType, EventType.AwaitingReview)) != null) AndAlso
  value(Debugging.Models.TransferRequest).TransferRequestEvents.Any(e2
  => ((Equals(e2.EventType, EventType.Forwarded) AndAlso Equals(e2.User, Param_0)) AndAlso (e2.EventDateTime >
  value(Debugging.Models.TransferRequest).TransferRequestEvents.OrderBy(e
  => e.EventDateTime).ThenBy(e => e.Id).LastOrDefault(e => Equals(e.EventType, EventType.AwaitingReview)).EventDateTime))))}</p>
</blockquote>

<p>Also, the following code works just fine </p>

<pre><code>Expression&lt;Func&lt;string, ApplicationUser, bool&gt;&gt; filter = (s, u) =&gt; u.FirstName.Contains(s);
var whereClause= filter.ReplaceParameter("mark");
_context.AppicationUsers.Where(whereClause).ToList();
</code></pre>

