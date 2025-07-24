# Transparently converting nullable values into non-nullable values in Entity Framework
[Link to question](https://stackoverflow.com/questions/10335838/transparently-converting-nullable-values-into-non-nullable-values-in-entity-fram)
**Creation Date:** 1335451594
**Score:** 2
**Tags:** entity-framework, expression-trees, entity-framework-ctp5
## Question Body
<p>I am currently in the process of attempting to integrate an Entity Framework application with a legacy database that is about ten years old or so. One of the many problems that this database has (alongside having no relations or constraints whatsoever) is that almost every column is set to null, even though in almost all cases, this wouldn't make sense.</p>

<p>Invariably, I will encounter an exception along these lines:</p>

<blockquote>
  <p>The 'SortOrder' property on 'MyRecord' could not be set to a 'null' value. You must set this property to a non-null value of type 'Int32'.</p>
</blockquote>

<p>I have seen many questions that refer to the exception above, but these all seem to be genuine mistakes where the developer did not write classes that properly represent the data in the database. I would like to deliberately write a class that does not properly represent the data in the database. I am fully aware that this is against the rules of Entity Framework, and that is most likely why I am having so much difficulty doing it.</p>

<p>It is not possible to change the schema at this point as it will break existing applications. It is also not possible to fix the data, because new data will be inserted by old applications. I would like to map the database with Entity Framework as it should be, slowly move all the applications over the next couple of years or so to rely on it for data access before finally being able to move on to the database redesign phase.</p>

<p>One method I have used to get around this is to transparently proxy the variable:</p>

<pre><code>internal int? SortOrderInternal { get; set; }

public int SortOrder
{
    get { return this.SortOrderInternal ?? 0; }
    set { this.SortOrderInternal = value; }
}
</code></pre>

<p>I can then map the field in CodeFirst:</p>

<pre><code>entity.Ignore(model =&gt; model.SortOrder);
entity.Property(model =&gt; model.SortOrderInternal).HasColumnName("SortOrder");
</code></pre>

<p>Using the <code>internal</code> keyword in this method does allow me to nicely encapsulate this nastiness so I can at the very least keep it from leaking outside my data access assembly.</p>

<p>But unfortunately I am now unable to use the proxy field in a query as a <code>NotSupportedException</code> will be thrown:</p>

<blockquote>
  <p>The specified type member 'SortOrder' is not supported in LINQ to Entities. Only initializers, entity members, and entity navigation properties are supported.</p>
</blockquote>

<p>Perhaps it might be possible to transparently rewrite the expression once it is received by the DbSet? I would be interested to hear if this would even work; I'm not skilled enough with expression trees to say. I have so far been unsuccessful in finding a method in DbSet that I could override to manipulate the expression, but I'm not above making a new class that implements IDbSet and passes through to DbSet, horrible though that would be.</p>

<p>Whilst investigating the stack trace, I found a reference to an internal Entity Framework concept called a Shaper, which appears to be the thing that takes the data and inputs it to  A quick bit of Googling on this concept doesn't yield anything, but investigating System.Data.Entity.dll with dotPeek indicates that this would certainly be something that would help me... assuming <code>Shaper&lt;T&gt;</code> wasn't internal and sealed. I'm almost certainly barking up the wrong tree here, but I'd be interested to hear if anyone has encountered this before.</p>

## Answers
### Answer ID: 10338707
<p>That's a fairly tough nut to crack, but you might be able to do it via <a href="http://damieng.com/blog/2009/06/24/client-side-properties-and-any-remote-linq-provider" rel="nofollow">Microsoft.Linq.Translations</a>.</p>

