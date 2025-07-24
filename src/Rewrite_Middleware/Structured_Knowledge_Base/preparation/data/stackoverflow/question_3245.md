# Resolve Generic Properties in Expression to use in LINQ
[Link to question](https://stackoverflow.com/questions/73318134/resolve-generic-properties-in-expression-to-use-in-linq)
**Creation Date:** 1660209068
**Score:** 0
**Tags:** c#, linq, generics, reflection, expression
## Question Body
<p>We are currently rewriting a lot of duplicate code to manage our Database Queries (with EF) in a very generic fashion. Right now, we are facing some problems with resolving the correct Property Value to use in Expressions.</p>
<pre><code>private Expression&lt;Func&lt;TEntity, bool&gt;&gt; BuildGenericSearchExpression()
{
    Expression&lt;Func&lt;TEntity, bool&gt;&gt; expression = x =&gt; false;
    
    var searchFields = GenericTableOptions.SearchColumns;
    var propertyInfos = GetSearchColumnsAsProperties(typeof(TEntity), searchFields).ToList();

    if (propertyInfos.Count ==  0)
    {
        return expression;
    }
    
    foreach (var propertyInfo in propertyInfos)
    {
        var value = propertyInfo.Name;

        expression = x =&gt; propertyInfo.GetValue(x, null).ToString().Contains(&quot;Hans&quot;);
    }

    return expression;
}

private static IEnumerable&lt;PropertyInfo&gt; GetSearchColumnsAsProperties(Type targetType,  IEnumerable&lt;string&gt; properties)
{
    IList&lt;PropertyInfo&gt; propertyInfos = new List&lt;PropertyInfo&gt;();
    
    if (targetType == null)
    {
        throw new GenericTableException($&quot;Type has no value set&quot;);
    }
    
    foreach (var property in properties)
    {
        var propertyInfo = targetType?.GetProperty(property);
        
        if (propertyInfo == null)
        {
            throw new GenericTableException($&quot;Property {property} is not available on Type {targetType}&quot;);
        }
        
        propertyInfos.Add(propertyInfo);
    }
    
    return propertyInfos;
}
</code></pre>
<p>For a quick Test, I have created a basic User class.</p>
<pre><code>public class User
{
    public string FirstName { get; set; }
}
</code></pre>
<p>FirstName is set as the Search Column and &quot;Hans&quot; is used as the search term.</p>
<p>The internal test list uses two users with different FirstNames, but it always returns both of them.</p>
<pre><code>public Task&lt;IList&lt;User&gt;&gt; FindPaginatedAsync(Expression&lt;Func&lt;User, bool&gt;&gt; predicate, int page, int size)
{
    IList&lt;User&gt; users = new List&lt;User&gt; { new User { FirstName = &quot;Hans&quot; }, new User { FirstName = &quot;Franz&quot; }};

    IList&lt;User&gt; result = users.AsQueryable().Where(predicate);
    
    return Task.FromResult(result);
}
</code></pre>
<p>The created Expression is passed as the predicate, page and size aren't used yet. Any Ideas on that how to get me out of that rabbit hole.</p>

## Answers
### Answer ID: 73319509
<p>Ok, just if anyone falls into the same trap.</p>
<p><code>AsQueryable</code> returns an <code>IEnumerable</code> which does not execute the Query immediately. When you eventually convert it to a List the query gets executed and works as expected.</p>
<p>In our case, this will do the trick.</p>
<p><code>var result = users.AsQueryable().Where(predicate).ToList();</code></p>
<p>In the end we will keep working with the <code>IEnumerable</code> and convert it as late as possible.</p>

