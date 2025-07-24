# AWS Neptune Query is blocking all other queries
[Link to question](https://stackoverflow.com/questions/77451981/aws-neptune-query-is-blocking-all-other-queries)
**Creation Date:** 1699522486
**Score:** 0
**Tags:** amazon-web-services, graph-databases, amazon-neptune
## Question Body
<p>We are using AWS Neptune Graph database and need to query a subgraph.
We have about 300-400 independent graphs on our database and only need to query one of them at a time.</p>
<p>Our model is mainly this: <a href="https://i.sstatic.net/pfLz4.png" rel="nofollow noreferrer">graph model</a>
We have 300-400 &quot;A&quot; Vertices. This is our Top-level element and every graph starting with &quot;A&quot; is independent of the other graphs.
Every &quot;A&quot; vertex can have several(20-100) &quot;B&quot; vertices. Every &quot;B&quot; vertex can have several(2-10) &quot;C&quot; vertices.
So we have A, B, C as a hierarchy. Under that we have our &quot;data&quot; vertices, which is more or less several vertices (D,E,F,G) in a row and that could be for a couple of times (1-10). The last &quot;G&quot; vertex is connected to the next &quot;D&quot; vertex under the next &quot;B&quot; vertex.</p>
<p>We need to query a full graph starting from A or just some specific B's.</p>
<p>Currently we are using this query to get the whole graph (all vertices and edges) and then drop some of the connections. This query is the first query in our transaction. The transaction needs some time, because it will add a lot of vertices and egdes. This first query in our transaction blocks all other queries. We are getting a ConcurrentModificationException.</p>
<p>If the long transaction to query the graph for A(ID: 4711) is running:</p>
<ul>
<li>I cannot add a vertex (A, B, C, ..) over the Jupyter Notebook</li>
<li>I cannot run the same query for a different A vertex.</li>
</ul>
<p><strong>-&gt; The result is always a ConcurrentModificationException.</strong></p>
<p>It looks like the query is really blocking the complete index for all vertices. It is not possible to add any other vertices.</p>
<p>We have a background process which is updating the database and this transaction takes up to 30 seconds. We have then a lot of updates of this kind. Like every minute a different A subgraph gets updated. And on the other hand there a the users who uses the app and can also edit the data.
The current problem is that changing data of a A(ID:4711) subgraph is also blocking the changing of A(4712) subgraph even if there is absolutely no connection between them.</p>
<pre><code>g.V().hasLabel(&quot;A&quot;).has(&quot;v&quot;,4711).outE(&quot;s&quot;).inV()
.hasLabel(&quot;B&quot;).hasId(&quot;c4...a&quot;,&quot;a0...f&quot;,&quot;ac...3&quot;)
.outE(&quot;h&quot;).inV()
.bothE(&quot;sv&quot;,&quot;ev&quot;)
.bothV().not(hasLabel(&quot;C&quot;)).simplePath()
.barrier()
.repeat(outE().not(hasLabel(&quot;sv&quot;,&quot;ev&quot;)).simplePath().inV())
.until(or(outE().count().is(0),hasLabel(&quot;C&quot;),hasLabel(&quot;AP&quot;,&quot;AC&quot;).bothE(&quot;sv&quot;,&quot;ev&quot;).count().is(P.gt(0))))
.path().unfold().dedup().or(hasLabel(&quot;sp&quot;).has(&quot;ev&quot;),hasLabel(&quot;ev&quot;)).barrier()
.drop()
</code></pre>
<p>Is there any chance to rewrite this query that it will not block the database? I mean the subgraph are complete independent and I don't get why this query blocks the Index at full range.</p>
<p>If I run the query on our DEV environment with %%gremlin profile:</p>
<pre><code>Predicates
==========
# of predicates: 79

Results
=======
Count: 12

Index Operations
================
Query execution:
    # of statement index ops: 3283
    # of unique statement index ops: 1984
    Duplication ratio: 1.65
    # of terms materialized: 598
Serialization:
    # of statement index ops: 3
    # of unique statement index ops: 3
    Duplication ratio: 1.0
    # of terms materialized: 21
</code></pre>
<p>If I run that query even on a database with more data, I get this:</p>
<pre><code>Predicates
==========
# of predicates: 62

Results
=======
Count: 66

Index Operations
================
Query execution:
    # of statement index ops: 26412
    # of unique statement index ops: 9403
    Duplication ratio: 2.81
    # of terms materialized: 1706
Serialization:
    # of statement index ops: 3
    # of unique statement index ops: 3
    Duplication ratio: 1.0
    # of terms materialized: 94
</code></pre>
<p>For me it looks like we have far too many index operations with this query. Do you have any idea how we can prevent that query from scanning the database/index?</p>

## Answers
### Answer ID: 77694005
<p>Amazon Neptune will take locks when queries are updating the database. If two threads try to alter more or less the same part of the graph, concurrently, one of them will likely receive a Concurrent Modification Exception (CME). These are retryable exceptions. Typically it is recommended to retry using an exponential backoff approach.</p>
<p>If enough of the graph has been locked by one query, and kept locked for an extended period, other mutation requests can potentially receive a CME response, again, depending on what they are trying to modify.</p>
<p>When performing an operation like <code>drop()</code>, especially on vertices, keep in mind that this also requires dropping all adjacent edges, which can in turn impact the vertices on the other ends of those edges, in terms of locks.</p>
<p>One strategy to consider is to drop edges in batches before dropping vertices. This technique lends itself to a multi threaded approach where each thread drops edges in batches, and after the edges have been dropped, then the nodes can also be deleted.</p>
<p>The transaction semantics, isolation levels, and locking strategies, that Neptune uses are <a href="https://docs.aws.amazon.com/neptune/latest/userguide/transactions.html" rel="nofollow noreferrer">described here</a></p>

