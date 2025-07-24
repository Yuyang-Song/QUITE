# MongoDB and LINQ: &quot;NOT IN&quot; clause
[Link to question](https://stackoverflow.com/questions/71199361/mongodb-and-linq-not-in-clause)
**Creation Date:** 1645396000
**Score:** 2
**Tags:** c#, mongodb, linq
## Question Body
<p>I have two collections, one is a list of image names, the second is a subset of that list. When a task has been completed its name is inserted into the second collection.</p>
<p>I need to retrieve a set of not yet completed image names from the first collection. I have achieved this successfully with:</p>
<pre><code>var processedNames = processed.AsQueryable().Select(x =&gt; x.ImageName).ToArray();
foreach (var result in results.Where(x =&gt; !processedNames.Contains(x.ImageName))
</code></pre>
<p>However this brings a large list of strings back from the database and then sends it back to the database in a single document, which as well as being inefficient will break eventually.</p>
<p>So I tried to rewrite it so it's all performed server side with:</p>
<pre><code>            var results = from x in captures
                          join complete in processed.AsQueryable() on x.ImageName equals complete.ImageName into completed
                          where !completed.Any()
                          select x;
</code></pre>
<p>This fails with:</p>
<p>System.NotSupportedException: '$project or $group does not support {document}.'</p>
<p>I also tried using the non LINQ API:</p>
<pre><code>                var xs = capturesCollection.Aggregate()
                    .Lookup(&quot;Processed&quot;, &quot;ImageName&quot;, &quot;ImageName&quot;, @as: &quot;CompletedCaptures&quot;)
                    .Match(x =&gt; x[&quot;CompletedCaptures&quot;] == null)
                    .ToList();
</code></pre>
<p>This fails with:</p>
<pre><code>MongoDB.Bson.BsonSerializationException: 'C# null values of type 'BsonValue' cannot be serialized using a serializer of type 'BsonValueSerializer'.'
</code></pre>
<p>How can I achieve this query completely server side with the C# driver? A pure LINQ solution is preferable for portability.</p>

## Answers
### Answer ID: 71199669
<p>I worked out how to do it with the <code>Aggregate</code> API:</p>
<pre><code>                var results = capturesCollection.Aggregate()
                    .As&lt;CaptureWithCompletions&gt;()
                    .Lookup(processed, x =&gt; x.ImageName, x =&gt; x.ImageName, @as:(CaptureWithCompletions x) =&gt; x.CompletedCaptures)
                    .Match(x =&gt; !x.CompletedCaptures.Any())
                    //.Limit(2)
                    .ToList();
</code></pre>

