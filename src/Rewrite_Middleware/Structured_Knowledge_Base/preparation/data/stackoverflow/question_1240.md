# Query cannot be translated
[Link to question](https://stackoverflow.com/questions/65609880/query-cannot-be-translated)
**Creation Date:** 1610012423
**Score:** 0
**Tags:** c#, entity-framework, linq, ef-core-5.0
## Question Body
<p>I have the following class:</p>
<pre><code>class document
{
    int Id;
    List&lt;Tag&gt; Tags;
}

class Tag
{
    int Id;
}
</code></pre>
<p>I want to get all the documents that have at least one of the tags that the user selects.</p>
<p>I have written the following linq query:</p>
<pre><code>List&lt;int&gt; tagIds = tags.Select (x =&gt; x.Id).ToList ();

query.Where (doc =&gt; tagIds.Any (x =&gt; doc.Tags.Select (y =&gt; y.Id).Contains (x)));
</code></pre>
<p>If I execute it against a list of documents, it works, but if I execute it against a sqlite database using efcore 5 I get the following error:</p>
<pre><code>System.InvalidOperationException: 'The LINQ expression 'DbSet&lt;DemaDocument&gt;()
    .Where(d =&gt; __tagIds_0
        .Any(x =&gt; DbSet&lt;Dictionary&lt;string, object&gt;&gt;(&quot;DemaDocumentDemaTag&quot;)
            .Where(d0 =&gt; EF.Property&lt;Nullable&lt;int&gt;&gt;(d, &quot;Id&quot;) != null &amp;&amp; object.Equals(
                objA: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(d, &quot;Id&quot;), 
                objB: (object)EF.Property&lt;Nullable&lt;int&gt;&gt;(d0, &quot;DocumentsId&quot;)))
            .Join(
                inner: DbSet&lt;DemaTag&gt;(), 
                outerKeySelector: d0 =&gt; EF.Property&lt;Nullable&lt;int&gt;&gt;(d0, &quot;TagsId&quot;), 
                innerKeySelector: d1 =&gt; EF.Property&lt;Nullable&lt;int&gt;&gt;(d1, &quot;Id&quot;), 
                resultSelector: (d0, d1) =&gt; new TransparentIdentifier&lt;Dictionary&lt;string, object&gt;, DemaTag&gt;(
                    Outer = d0, 
                    Inner = d1
                ))
            .Select(ti =&gt; ti.Inner.Id)
            .Any(p =&gt; p == x)))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.'
</code></pre>
<p>How can I rewrite the query using fluent LINQ so that it will work? Is it possible, or do I have to retrieve the documents in memory and then run the query? This would not be ideal, because the documents will grow over time...</p>
<p>Thanks in advance</p>

## Answers
### Answer ID: 65611290
<p><code>.Contains</code> should be translated as a SQL <code>IN</code> statement, i.e. <code>x IN 1, 2, 3</code>. This requires the list to be constant. In your example <code>doc.Tags.Select (y =&gt; y.Id)</code> is unique for each document, so it cannot be translated to a constant list.</p>
<p>What you are doing is more or less checking if two lists intersects, so we should be able to reverse the order of the two lists:</p>
<pre><code>query.Where(doc =&gt; doc.Tags.Any(x =&gt; tagIds.Contains(x.Id)))
</code></pre>
<p>Now the tagIds is constant for the query, and the <code>.Contains</code> statement can be properly translated.</p>

