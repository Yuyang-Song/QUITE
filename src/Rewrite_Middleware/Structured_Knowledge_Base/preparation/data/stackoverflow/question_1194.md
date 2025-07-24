# Does whereEqualTo support HashMap equality?
[Link to question](https://stackoverflow.com/questions/62782128/does-whereequalto-support-hashmap-equality)
**Creation Date:** 1594148443
**Score:** 0
**Tags:** android, kotlin, google-cloud-firestore, hashmap, equality
## Question Body
<p>The <a href="https://firebase.google.com/docs/reference/kotlin/com/google/firebase/firestore/Query#whereequalto" rel="nofollow noreferrer"><code>whereEqualTo</code></a> API can take <code>Any</code> as its argument. Does this mean that I can pass it a <code>HashMap&lt;K, V&gt;</code> and it will compare its matching fields with that of a field of <code>map</code> type in the <code>Firestore</code> database or do I have to manually compare each property of the map?</p>
<p>I've build a query like this one</p>
<pre><code>collection.whereEqualTo(&quot;meta&quot;, hashMapOf( // &lt;-- using full hash-map for matching
    &quot;user&quot; to &quot;JD&quot;,
    &quot;name&quot; to &quot;John&quot;
))
</code></pre>
<p>where <code>meta</code> is a <code>map</code>-type field with two key/value pairs.</p>
<p>The document I'm trying to match has this structure:</p>
<pre><code>{
    &quot;createdOn&quot;: as timestamp
    ...other properties
    &quot;meta&quot;: as map
    {
        &quot;user&quot;: &quot;JD&quot;, as string
        &quot;name&quot;: &quot;John&quot; as string
    }
}
</code></pre>
<p>The criteria I use should yield some results but it doesn't (without crashing) so I was wondering whether I made a mistake somewhere else or is this type of a query simply not supported? The result is empty.</p>
<p>I might also be searching only for the <code>name</code> property with a simpler query like this one to find all <em>Johns</em></p>
<pre><code>collection.whereEqualTo(&quot;meta&quot;, hashMapOf( // &lt;-- using parcial hash-map for matching

    &quot;name&quot; to &quot;John&quot;
))
</code></pre>
<p>Will it match only <code>name</code> fields or does it require a full-map?</p>
<p>I mean, should the previous query work or do I need to rewrite as this?</p>
<pre><code>collection
    .whereEqualTo(&quot;meta.user&quot;, &quot;JD&quot;)
    .whereEqualto(&quot;meta.name&quot;, &quot;John&quot;)
</code></pre>

## Answers
### Answer ID: 62785349
<p>Firestore can compare items of a map in your client code with a map in a document. But the maps must be completely equivalent, so you must specify all properties in your code. So something like this should work:</p>
<pre><code>collection.whereEqualTo(&quot;meta&quot;, hashMapOf( // &lt;-- using parcial hash-map for matching
    &quot;user&quot; to &quot;JD&quot;,
    &quot;name&quot; to &quot;John&quot;
))
</code></pre>
<p>If you can't get this to work, edit your question to include a screenshot of the document you think this should match and I'll have another look.</p>
<p>There is no way specify partial map matches for a field, so if that's what you need, you'll indeed need to add separate conditions for each nested field.</p>

