# Conditional filtering an IQueryable&lt;T&gt; by expression and second object
[Link to question](https://stackoverflow.com/questions/55984869/conditional-filtering-an-iqueryablet-by-expression-and-second-object)
**Creation Date:** 1556989354
**Score:** 1
**Tags:** c#, entity-framework, linq
## Question Body
<p>What I am trying to achieve is to create a custom extension method on an <code>IQueryable&lt;T&gt;</code> where my expression selects a object of type <code>AgentEntity</code>, and the second parameter is of the same type, but used to do an conditional filtering.</p>
<p>Here is my code, which is not working but suggests what I would like to do.</p>
<pre><code>public static IQueryable&lt;T&gt; Where&lt;T&gt;(this IQueryable&lt;T&gt; profiles, Func&lt;AgentEntity, AgentEntity&gt; agentSelector, AgentEntity agent)
{
    if (string.IsNullOrEmpty(agent.Mbox))
    {
        return profiles.Where(agentSelector.Mbox == agent.Mbox);
    }

    if (string.IsNullOrEmpty(agent.Mbox_SHA1SUM))
    {
        return profiles.Where(agentSelector.Mbox_SHA1SUM == agent.Mbox_SHA1SUM);
    }

    if (string.IsNullOrEmpty(agent.OpenId))
    {
        return profiles.Where(agentSelector.OpenId == agent.OpenId);
    }

    if (string.IsNullOrEmpty(agent.Account.HomePage))
    {
        return profiles.Where(agentSelector.Account.HomePage == agent.Account.HomePage &amp;&amp; agentSelector.Account.Name == agent.Account.Name);
    }

    return profiles;
}
</code></pre>
<p><strong>Usage</strong></p>
<pre><code>AgentEntity agent = new AgentEntity(){
  Mbox = &quot;mailto:lorem@example.com&quot;
}
_dbContext.OtherEntity.Where(x=&gt; x.Agent, agent);
_dbContext.ThirdEntity.Where(x=&gt; x.Object.Agent, agent);
</code></pre>
<p>How do I convert <code>agentSelector</code> to the following expression <code>x=&gt; x.Mbox == agent.Mbox</code> or one of the other conditions, to use in Where clause to filter profiles.</p>
<p>The <code>profiles.Where</code> clause expects <code>Expression&lt;Func&lt;T, bool&gt;&gt; predicate</code></p>
<h2>Updae</h2>
<p>After testing answer below I found EntityFramework cannot convert the following expressions into SQL. And throws the following error:</p>
<pre><code>The LINQ expression 'Where&lt;AgentEntity&gt;(\r\n    source: DbSet&lt;AgentEntity&gt;, \r\n    predicate: (a) =&gt; (int)Invoke(__agentSelector_0, a[AgentEntity])\r\n    .ObjectType == (int)(Unhandled parameter: __agent_ObjectType_1))' could not be translated.
Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.

Summary:
### Explicit client evaluation
You may need to force into client evaluation explicitly in certain cases like following

The amount of data is small so that evaluating on the client doesn't incur a huge performance penalty.
The LINQ operator being used has no server-side translation.
In such cases, you can explicitly opt into client evaluation by calling methods like `AsEnumerable` or `ToList` (`AsAsyncEnumerable` or `ToListAsync` for async). 
By using `AsEnumerable` you would be streaming the results, but using ToList would cause buffering by creating a list, which also takes additional memory. Though if you're enumerating multiple times, then storing results in a list helps more since there's only one query to the database. Depending on the particular usage, you should evaluate which method is more useful for the case.
</code></pre>

## Answers
### Answer ID: 56007969
<p>An <code>IQueryable</code> can be filtered using the <code>Where</code> method. This method also returns an <code>IQueryable</code>, so if you want (and I often do) you can chain these together to filter multiple times - I find that leads to more readable code, and also you can branch code between these filters (to add conditions to whether you filter or not). That might look something like this (untested code):</p>
<pre><code>IQueryable&lt;Foo&gt; foos = _dbContext.Foos;
foos = foos.Where(f =&gt; f.Bar == myBar);

if(!string.IsNullOrNothing(myBaz)){
    foos = foos.Where(f =&gt; f.Baz == myBaz)
}
</code></pre>
<p>So in this code, the set of <code>Foo</code> objects is always filtered for when their <code>Bar</code> property equals <code>myBar</code>, but the second filtering is only applied when <code>myBar</code> is <strong>not</strong> null and <strong>not</strong> nothing (note the <code>!</code> making these not, which is one thing dotNet and both think looks like is missing in your original code)</p>
<p>Now let me try and apply that to the extension method you're trying to create. The complication is that there are different mappings to get from <code>OtherEntity</code> or <code>ThirdEntity</code> and the <code>AgentEntity</code> and we want to use a <code>Func&lt;T, AgentEntity&gt;</code> to define that mapping (note that we're mapping from generic type 'T')</p>
<pre><code>public static IQueryable&lt;T&gt; Where&lt;T&gt;(this IQueryable&lt;T&gt; profiles, Func&lt;T, AgentEntity&gt; mapping, AgentEntity agent)
{
    if (!string.IsNullOrEmpty(agent.MBox))
    {
        profiles = profiles.Where(p =&gt; mapping(p).MBox == agent.MBox);
    }

    return profiles;
}
</code></pre>
<p>Note that we use the mapping function passed in to convert each profile to an agent that we use for the filter. It gets called just like in your original question:</p>
<p><code>_dbContext.OtherEntity.Where(x=&gt; x.Agent, agent);</code></p>
<p>Also note that I don't return until the end of the function - that may or may not be what you're actually after - you may actually want to return as soon as you found one criteria you can filter on!</p>

