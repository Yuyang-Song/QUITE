# EF Core 3.1 Fail to query on Json Serialized Object
[Link to question](https://stackoverflow.com/questions/64204010/ef-core-3-1-fail-to-query-on-json-serialized-object)
**Creation Date:** 1601882290
**Score:** 0
**Tags:** sql-server, entity-framework, asp.net-core, entity-framework-core, jsonserializer
## Question Body
<p>I used json serialization to store list on ids in a field</p>
<p>Model:</p>
<pre><code>public class Video
{
    public int Id { get; set; }
    public string Name { get; set; }
    public virtual IList&lt;int&gt; AllRelatedIds { get; set; }
}

</code></pre>
<p>Context:</p>
<pre><code>modelBuilder.Entity&lt;Video&gt;(entity =&gt;
{
    entity.Property(p =&gt; p.AllRelatedIds).HasConversion(
    v =&gt; JsonConvert.SerializeObject(v, new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore }),
    v =&gt; JsonConvert.DeserializeObject&lt;IList&lt;int&gt;&gt;(v, new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore })
    );
});
</code></pre>
<p>It works fine, Adding, Editing, Deleting items  is easy and in SQL Database it stores as json like<br />
<code> [11000,12000,13000]</code></p>
<p>Everything is fine BUT!! as soon as want to query on this list I get weird responses.</p>
<p><strong>Where:</strong></p>
<p><code>_context.Set&lt;Video&gt;().Where(t=&gt;t.AllRelatedIds.contains(11000)) </code> returns <strong>null</strong> however if I ask to return all <strong>AllRelatedIds</strong> items some records have 11000 value exp.</p>
<p><strong>Count:</strong></p>
<p><code>_context.Set&lt;Video&gt;().Count(t=&gt;t.AllRelatedIds.contains(11000))</code> returns <strong>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</strong></p>
<p>What's the matter with EF Core? I even tested <code>t=&gt;t.AllRelatedIds.ToList().contains(11000)</code> but made no difference</p>
<p>What I should do? I don't want to have more tables, I used this methods hundreds of times but seems never queried on them.</p>

## Answers
### Answer ID: 64206519
<p>The Json Serialization/Deserialization happens at application level. EF Core serializes the <code>IList&lt;int&gt;</code> object to value <code>[11000,12000,13000]</code> <em>before</em> sending it to database for storing, and deserializes the value <code>[11000,12000,13000]</code> to <code>IList&lt;int&gt;</code> object <em>after</em> retrieving it from the database. Nothing happens inside the database. Your database cannot operate on <code>[11000,12000,13000]</code> as a collection of number. To the database, its a single piece of data.</p>
<p>If you try the following queries -</p>
<pre class="lang-cs prettyprint-override"><code>var videos = _context.Set&lt;Video&gt;().ToList();
var video = _context.Set&lt;Video&gt;().FirstOrDefault(p=&gt; p.Id == 2);
</code></pre>
<p>you'll get the expected result, EF Core is doing it's job perfectly.</p>
<p>The problem is, when you query something like -</p>
<pre class="lang-cs prettyprint-override"><code>_context.Set&lt;Video&gt;().Where(t=&gt; t.AllRelatedIds.Contains(11000))
</code></pre>
<p>EF Core will fail to translate the <code>t.AllRelatedIds.Contains(11000)</code> part to SQL. EF Core can only serialize/deserialize it because you told it to (and how). But as I said above, your database cannot operate on <code>[11000,12000,13000]</code> as a collection of integer. So EF Core cannot translate the <code>t.AllRelatedIds.Contains(11000)</code> to anything meaningful to the database.</p>
<p>A solution will be to fetch the list of all videos, so that EF Core can deserialize the <code>AllRelatedIds</code> to <code>IList&lt;int&gt;</code>, then you can apply LINQ on it -</p>
<pre class="lang-cs prettyprint-override"><code>var allVideos = _context.Set&lt;Video&gt;().ToList();
var selectedVideos = allVideos.Where(t=&gt; t.AllRelatedIds.Contains(11000)).ToList();
</code></pre>
<p>But isn't fetching ALL videos each time unnecessary/overkill or inefficient from performance perspective? Yes, of course. But as the comments implied, your database design/usage approach has some flaws.</p>

