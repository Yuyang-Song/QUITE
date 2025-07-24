# Flatten properties into List in EF Core
[Link to question](https://stackoverflow.com/questions/72597382/flatten-properties-into-list-in-ef-core)
**Creation Date:** 1655089163
**Score:** 0
**Tags:** linq, entity-framework-core
## Question Body
<p>Lets say I have an entity which can reference other rows in its table, defined like this:</p>
<pre class="lang-cs prettyprint-override"><code>MyEntity
{
    public string Id { get; set; }
    public string ParentId { get; set; }
    public bool isRelevant { get; set; }

    public virtual List&lt;MyEntity&gt; Children
}
</code></pre>
<p>Attempting something like:</p>
<pre class="lang-cs prettyprint-override"><code>var result = await MyEntities
                    .SelectMany(o =&gt; new List&lt;string&gt; { o.Id, o.ParentId })
                    .ToListAsync();
</code></pre>
<p>This however results in a runtime error:</p>
<blockquote>
<p>The LINQ expression could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable'...</p>
</blockquote>
<p>How can I select all of the <code>MyEntity</code> <code>Id</code> AND <code>ParentId</code> values as a single list without reverting to client-side evaluation?</p>
<p>To be clear, I would like the result from the database to be something like:</p>
<p><code>[&quot;Id1&quot;, &quot;parentId1&quot;, &quot;Id2&quot;, &quot;ParentId2&quot;]</code></p>

## Answers
### Answer ID: 72602103
<p>I assume just the parents not the children</p>
<p>create class:</p>
<pre><code>public class Parent{

public string Id {get;set;}
public string ParentId {get;set;}

}
</code></pre>
<p>then</p>
<pre><code>var result = MyEntities.select(x =&gt; new Parent(){Id = x.Id, ParentId = x.ParentId}).toList();
</code></pre>
<p>edit:</p>
<p>To flatten to string list something like this, though you would run it against the ef resultset not directly against ef,</p>
<p>Though i cant think of any reason you would want to do that, this will do all the properties in the class, if i understood question this will do list of all values:</p>
<pre><code>var properties = result.SelectMany(x =&gt; x.GetType().GetProperties().Select(y =&gt; y.GetValue(x))).ToList();
</code></pre>
<p>you would probaly need to tweak it, adding a where clause, to ignore the properties you dont want included as this one will do all the properties, also might need to add toString() to getValue</p>
<p>so in your case:</p>
<pre><code>var properties = result.SelectMany(x =&gt; x.GetType().GetProperties().Where(i =&gt; i.Name == &quot;Id&quot; || i.Name == &quot;ParentId&quot;).Select(y =&gt; y.GetValue(x))).ToList();
</code></pre>

### Answer ID: 72608797
<p>You cannot use <strong>List</strong> of <strong>String</strong> to store an anonymous value object.</p>
<p>Please use <strong>object</strong>  or <strong>Parent class</strong> including id and parent id as properties.</p>
<p>My opinion is to use class called  &quot;Parent&quot;</p>
<p><code>.Select(o =&gt; new { o.Id, o.ParentId })</code></p>
<p>or</p>
<p><code>.Select(o =&gt; new Parent { Id = o.Id, ParentId = o.ParentId })</code></p>

