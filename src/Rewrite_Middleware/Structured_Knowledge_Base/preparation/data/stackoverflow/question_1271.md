# How to create a reusable &#39;Contains&#39; expression for EF Core
[Link to question](https://stackoverflow.com/questions/67585220/how-to-create-a-reusable-contains-expression-for-ef-core)
**Creation Date:** 1621337023
**Score:** 2
**Tags:** c#, lambda, entity-framework-core, linq-expressions
## Question Body
<h2>Problem</h2>
<p>I need to execute a partial text search, alongside other filters, via a generic repository using expressions.</p>
<h2>State of current code</h2>
<p>I have a generic method that returns paged results from my database (via a common repository layer).</p>
<p>In the following working example;</p>
<ul>
<li><code>PagedRequest</code> contains the current pagesize and page number, and is used during respective <code>Skip</code> / <code>Take</code> operations.</li>
<li><code>PagedResult</code> contains a collection of the results, along with the total number of records.</li>
</ul>
<pre class="lang-cs prettyprint-override"><code>public Task&lt;PagedResult&lt;Person&gt;&gt; GetPeopleAsync(PersonSearchParams searchParams,
    PagedRequest pagedRequest = null)
{
    ParameterExpression argParam = Expression.Parameter(typeof(Locum), &quot;locum&quot;);

    // start with a &quot;true&quot; expression so we have an expression to &quot;AndAlso&quot; with
    var alwaysTrue = Expression.Constant(true);
    var expr = Expression.Equal(alwaysTrue, alwaysTrue);

    if (searchParams != null)
    {
        BinaryExpression propExpr;

        if (searchParams.DateOfBirth.HasValue)
        {
            propExpr = GetExpression(searchParams.DateStart,
                nameof(Incident.IncidentDate), 
                argParam, 
                ExpressionType.GreaterThanOrEqual);

            expr = Expression.AndAlso(expr, propExpr);
        }

        if (searchParams.DateOfDeath.HasValue)
        {
            propExpr = GetExpression(searchParams.DateEnd,
                nameof(Incident.IncidentDate), 
                argParam, 
                ExpressionType.LessThanOrEqual);

            expr = Expression.AndAlso(expr, propExpr);
        }

        if (searchParams.BranchId.HasValue &amp;&amp; searchParams.BranchId.Value != 0)
        {
            propExpr = GetExpression(searchParams.BranchId, 
                nameof(Incident.BranchId), argParam);

            expr = Expression.AndAlso(expr, propExpr);
        }
    }

    var lambda = Expression.Lambda&lt;Func&lt;Locum, bool&gt;&gt;(expr, argParam);
    return _unitOfWork.Repository.GetAsync(filter: lambda, pagedRequest: pagedRequest);
}
</code></pre>
<p>This is using my static <code>GetExpression</code> method for <code>Expression.Equal</code>, <code>Expression.GreaterThanOrEqual</code> and <code>Expression.LessThanOrEqual</code> queries as follows;</p>
<pre class="lang-cs prettyprint-override"><code>private static BinaryExpression GetExpression&lt;TValue&gt;(TValue value,
    string propName, ParameterExpression argParam, ExpressionType? exprType = null)
{
    BinaryExpression propExpr;

    var prop = Expression.Property(argParam, propName);
    var valueConst = Expression.Constant(value, typeof(TValue));

    switch (exprType)
    {
        case ExpressionType.GreaterThanOrEqual:
            propExpr = Expression.GreaterThanOrEqual(prop, valueConst);
            break;
        case ExpressionType.LessThanOrEqual:
            propExpr = Expression.LessThanOrEqual(prop, valueConst);
            break;
        case ExpressionType.Equal:
        default:// assume equality
            propExpr = Expression.Equal(prop, valueConst);
            break;
    }
    return propExpr;
}
</code></pre>
<p>NOTE: this code is working correctly.</p>
<h2>Problem</h2>
<p>Using example from other SO answers I have tried the following;</p>
<h3>Expressions</h3>
<p>I have tried getting the contains via an <code>Expression</code>;</p>
<pre class="lang-cs prettyprint-override"><code>static Expression&lt;Func&lt;bool&gt;&gt; GetContainsExpression&lt;T&gt;(string propertyName, 
    string propertyValue)
{
    var parameterExp = Expression.Parameter(typeof(T), &quot;type&quot;);
    var propertyExp = Expression.Property(parameterExp, propertyName);
    MethodInfo method = typeof(string).GetMethod(&quot;Contains&quot;, new[] { typeof(string) });
    var someValue = Expression.Constant(propertyValue, typeof(string));
    var containsMethodExp = Expression.Call(propertyExp, method, someValue);
    return Expression.Lambda&lt;Func&lt;bool&gt;&gt;(containsMethodExp);
}
</code></pre>
<p>This has to be converted to a <code>BinaryExpression</code> so it can be added to the expression tree using <code>AndAlso</code>. I've tried to compare the <code>Expression</code> with a <code>true</code> value, but this isn't working</p>
<pre class="lang-cs prettyprint-override"><code>if (searchParams.FirstName.IsNotNullOrWhiteSpace())
{
    var propExpr = GetContainsExpression&lt;Locum&gt;(nameof(Locum.Firstname), 
        searchParams.FirstName);

    var binExpr = Expression.MakeBinary(ExpressionType.Equal, propExpr, propExpr);
    expr = Expression.AndAlso(expr, binExpr);
}
</code></pre>
<h3>MethodCallExpression</h3>
<p>I also tried returning the <code>MethodCallExpression</code> (instead of the Lambda above), using the following;</p>
<pre class="lang-cs prettyprint-override"><code>static MethodCallExpression GetContainsMethodCallExpression&lt;T&gt;(string propertyName, 
    string propertyValue)
{
    var parameterExp = Expression.Parameter(typeof(T), &quot;type&quot;);
    var propertyExp = Expression.Property(parameterExp, propertyName);
    MethodInfo method = typeof(string).GetMethod(&quot;Contains&quot;, new[] { typeof(string) });
    var someValue = Expression.Constant(propertyValue, typeof(string));
    var containsMethodExp = Expression.Call(propertyExp, method, someValue);

    return containsMethodExp;
}
</code></pre>
<p>I used this as follows;</p>
<pre class="lang-cs prettyprint-override"><code>if (searchParams.FirstName.IsNotNullOrWhiteSpace())
{
    var propExpr = GetContainsMethodCallExpression&lt;Person&gt;(nameof(Person.FirstName), 
        searchParams.FirstName);

    var binExpr = Expression.MakeBinary(ExpressionType.Equal, propExpr, alwaysTrue);
    expr = Expression.AndAlso(expr, binExpr);
}
</code></pre>
<h3>Exceptions</h3>
<p>These expression are passed to a generic method that pages information out of the database, and the exceptions are thrown during the first execution of the query when I <em>Count</em> the total matching number of record on the constructed <code>query</code>.</p>
<blockquote>
<p>System.InvalidOperationException: 'The LINQ expression 'DbSet()
.Where(p =&gt; True &amp;&amp; p.FirstName.Contains(&quot;123&quot;) == True)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable ', 'AsAsyncEnumerable ', 'ToList ', or 'ToListAsync '. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.'</p>
</blockquote>
<p>This exception is thrown on a <code>Count</code> method I am using in my paging code. This code is already working without any filters, and with the <code>ExpressionType</code> filters described at the top, so I haven't included this code as I don't believe it is relevant.</p>
<pre class="lang-cs prettyprint-override"><code>pagedResult.RowCount = query.Count();
</code></pre>

## Answers
### Answer ID: 67589641
<blockquote>
<p>This has to be converted to a BinaryExpression so it can be added to the expression tree using <code>AndAlso</code></p>
</blockquote>
<p>Negative. There is no requirement <code>Expression.AndAlso</code> (or <code>Expression.OrElse</code>) <em>operands</em> to be binary expressions (it would have been strange like requiring left or right operand of <code>&amp;&amp;</code> or <code>||</code> to be always comparison operators). The only requirement is them to be <code>bool</code> returning expressions, hence <em>call</em> to string <code>Contains</code> is a perfectly valid operand expression.</p>
<p>So start by changing the type of the inner local variable from <code>BinaryExpression</code> to <code>Expression</code>:</p>
<pre><code>if (searchParams != null)
{
    Expression propExpr;
    
    // ...
}
</code></pre>
<p>The same btw applies for the initial expression - you don't need <code>true == true</code>, simple
<code>Expression expr = Expression.Constant(true);</code> would do the same.</p>
<p>Now you could emit method call to <code>string.Contains</code> in a separate method similar to the other that you've posted (passing the <code>ParameterExpression</code> and building property selector expression) or inline similar to:</p>
<pre><code>if (searchParams.FirstName.IsNotNullOrWhiteSpace())
{
    var propExpr = Expression.Property(argParam, nameof(Person.FirstName));
    var valueExpr = Expression.Constant(searchParams.FirstName);
    var containsExpr = Expression.Call(
        propExpr, nameof(string.Contains), Type.EmptyTypes, valueExpr);
    expr = Expression.AndAlso(expr, containsExpr);
}
</code></pre>

