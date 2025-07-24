# I am getting &quot;The LINQ expression could not be translated&quot; exception
[Link to question](https://stackoverflow.com/questions/71970628/i-am-getting-the-linq-expression-could-not-be-translated-exception)
**Creation Date:** 1650638747
**Score:** 0
**Tags:** c#, entity-framework, linq, .net-core, entity-framework-core
## Question Body
<p>When I want to use <code>Any()</code> expression in the <code>Where()</code> filtering that I send to the database, I get the following exception.</p>
<p><strong>Exception :</strong></p>
<blockquote>
<p>The LINQ expression could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>If I filter with <code>Where()</code> after getting all the records from the database it works correctly. But I want to get filtered data from database.</p>
<p><strong>My codes that I got the exception are as follows.</strong></p>
<pre><code>var firstList = await _firstRepository
                     .FilterByAsync(x =&gt; x.IsActive);

var secondList = await _secondRepository
                       .FilterByAsync(x =&gt; !firstList
                                           .Any(y =&gt;
                                                y.CategoryId == x.CategoryId &amp;&amp;
                                                y.Type == x.Type)
                                      );
</code></pre>
<p><strong>Note : There are 2 different repositories as the queries have to go to 2 different tables.</strong></p>
<p><strong>Also, I have a filter method inside my generic repository.</strong></p>
<pre><code>public async Task&lt;List&lt;TEntity&gt;&gt; FilterByAsync(Expression&lt;Func&lt;TEntity, bool&gt;&gt; predicate)
{
    return await _entities.Where(predicate).ToListAsync();
}
</code></pre>
<p>I hope I have expressed my problem well.</p>
<p>Thanks in advance for the answers.</p>

