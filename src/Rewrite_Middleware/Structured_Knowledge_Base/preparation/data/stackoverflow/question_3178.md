# Dynamic GreaterThanOrEqual using Expressions in ASP.NET Core
[Link to question](https://stackoverflow.com/questions/70200060/dynamic-greaterthanorequal-using-expressions-in-asp-net-core)
**Creation Date:** 1638450446
**Score:** 0
**Tags:** c#, linq, lambda, expression, predicate
## Question Body
<p>I'm facing a little problem I'm stuck on.
I'm building queries dynamically, they will be used by LINQ to query the database. The calculation must be done on the database side (client-side evaluation is not efficient, therefore I would like no to use it)</p>
<p>I have two Expressions that are used to compute a special mathematical operation (For this context, it has been simplified). They are represented as :</p>
<pre><code>public static Expression&lt;Func&lt;Circle, float&gt;&gt; REAL_HEIGHT_EXPR = circle =&gt; circle.Diameter * circle.Paper.Height;
public static Expression&lt;Func&lt;Circle, float&gt;&gt; REAL_Y_EXPR = circle =&gt; circle.Y * circle.Paper.Height - REAL_HEIGHT_EXPR.Invoke(circle) * (float)0.5;
</code></pre>
<p>I'm searching for records in the database that are in a min-max range. Since there will be multiple pairs of min-max, I'm also using LinqKit (<a href="https://github.com/scottksmith95/LINQKit" rel="nofollow noreferrer">https://github.com/scottksmith95/LINQKit</a>) with <code>PredicateBuilder</code>. This <code>PredicateBuilder</code> will be built gradually and then used in a LINQ .Where(predicate).</p>
<p>Let's say, for example, that we have two pairs of min-max with the values <code>[0,1]</code> and <code>[4,5]</code>. The SQL query that should be executed would be :</p>
<pre><code>(REAL_Y_EXPR &gt;= 0 AND REAL_Y_EXPR &lt;= 1) OR (REAL_Y_EXPR &gt;= 4 AND REAL_Y_EXPR &lt;= 5)
</code></pre>
<p>Where REAL_Y_EXPR is the result of the expression defined above, using the Circle class and parameters. (The result of the computation, which is a float, and executed in the database side)</p>
<p>Here's a snippet of the function building the predicate:</p>
<pre><code>public static ExpressionStarter&lt;Circle&gt; GetMinMaxPredicate(List&lt;SearchMinMax&gt; searchList, Expression&lt;Func&lt;Circle, float&gt;&gt; expr)
        {
            var allParametersSearch = PredicateBuilder.New&lt;Circle&gt;();
            if (searchList != null)
            {
                searchList.ForEach(value =&gt;
                {
                    var searchPredicateAND = PredicateBuilder.New&lt;Circle&gt;();
                    if (value.Min != null)
                    {
                        searchPredicateAND = searchPredicateAND.And(circle =&gt; expr.Invoke(circle) &gt;= value.Min);
                    }

                    if (value.Max != null)
                    {
                        searchPredicateAND = searchPredicateAND.And(circle =&gt; expr.Invoke(circle) &lt;= value.Max);
                    }

                    allParametersSearch = allParametersSearch.Or(searchPredicateAND);
                });
            }

            return allParametersSearch;
        }
</code></pre>
<p>The main reason I'm doing all of that, is to have a fully reusable code and prevent rewriting the expression multiple times.</p>
<p>However, this code is not working, since I'm forced to call .Invoke(), LINQ will throws that I need to call ToList() or other methods to do a client-side evaluation. (I have also tested using REAL_HEIGHT_EXPR which doesn't have an <code>Invoke()</code>, and it's the same error, so not coming from that part)</p>
<p>The main problem I'm having is the <code>&lt;=</code> and <code>&gt;=</code>. Since it changes and I would like to use the same expression without having to rewrite all of them multiple times with the operand included.</p>
<p>I have tried to use <code>Expression.GreaterThanOrEqual</code> with the expression already written (which would be great!)</p>
<pre><code>Expression searchAND = Expression.Empty();
searchAND = Expression.AndAlso(searchAND, Expression.GreaterThanOrEqual(Expression.Constant(value.Min), REAL_Y_EXPR);
</code></pre>
<p>However, the <code>searchAND</code> line throws the following error :</p>
<pre><code>Exception has occurred: CLR/System.InvalidOperationException
Exception thrown: 'System.InvalidOperationException' in System.Linq.Expressions.dll: 'The binary operator GreaterThanOrEqual is not defined for the types 'System.Single' and 'System.Func`2[My.NameSpace.Circle,System.Single]'.'
   at System.Linq.Expressions.Expression.GetUserDefinedBinaryOperatorOrThrow(ExpressionType binaryType, String name, Expression left, Expression right, Boolean liftToNull)
   at System.Linq.Expressions.Expression.GetComparisonOperator(ExpressionType binaryType, String opName, Expression left, Expression right, Boolean liftToNull)
   at System.Linq.Expressions.Expression.GreaterThanOrEqual(Expression left, Expression right, Boolean liftToNull, MethodInfo method)
   at System.Linq.Expressions.Expression.GreaterThanOrEqual(Expression left, Expression right)
</code></pre>
<p>Would anyone have an idea on how to solve that ?</p>

