# How to optimize graph traversals in ArangoDB?
[Link to question](https://stackoverflow.com/questions/21020366/how-to-optimize-graph-traversals-in-arangodb)
**Creation Date:** 1389270721
**Score:** 15
**Tags:** graph-databases, arangodb, aql
## Question Body
<p>I primarily intended to ask this question : "Is ArangoDB a true graph database ?"</p>

<p>But, this question would sound quite offending.</p>

<p>You, peoples at triAGENS, did a really great job in creating a "multi-paradigm" database.
As a user of PostgreSQL, PostGIS, MongoDB and Neo4J/Titan, I really appreciate to see an "all-in-one" solution :)</p>

<p>But the question remains, basically creating a graph in ArangoDB requires to create two separate collections : one for edges and one for vertices, thus, as far as I understand, it already means that vertices and related edges are not "physically" neighbors.</p>

<p>Moreover, even after creating appropriate index, I'm facing some serious performance issues when doing this kind of stuff in Gremlin</p>

<pre><code>g.v('an_id').out('likes').in('likes').count()
</code></pre>

<p>Which returns a result after ~ 3 seconds (perceived time)</p>

<p>I assumed I poorly understood how Gremlin and Blueprint/ArangoDB worked so I tried to rewrite the same query using AQL :</p>

<pre><code>LET lst = (FOR e1 in NEIGHBORS(vertices, edges, "an_id", "outbound", [ { "$label": "likes" } ] )
    FOR e2 in NEIGHBORS(vertices, edges, e1.edge._to, "inbound", [ { "$label": "likes" } ] )
        RETURN 1
    )
RETURN length(lst)
</code></pre>

<p>Which gives me a delay of same order of magnitude.</p>

<p>If I tried to run the same query on a Titan or Neo4j database (with the very same data), queries returns almost immediately (perceived time : &lt;200ms)</p>

<p>So it seems to me that ArangoDB graph features are a "smart graph layer" above a "traditionnal document database" but that ArangoDB is not a "native" graph database.</p>

<p>To confirm this feeling, I transform data to load it in PostgreSQL and run a query (with a multiple table JOIN as you can assume) and got similar (to ArangoDB) execution delays</p>

<p>Did I do something wrong (in AQL query) ?</p>

<p>Is there a way to optimize the database to get better traversal times ?</p>

<p>In PostgreSQL, conceptually, I would mix edge and node and use a CLUSTER clause to physically order data, does something similar can be done in ArangoDB ? (I assume that it would be hard, as it would involve to "interlace" edges and nodes, just an intuition)</p>

## Answers
### Answer ID: 21042492
<p>i am a Core Developer of ArangoDB. Could you give me a bit more information ob the dimensions of data you are using?</p>

<ul>
<li>Amount of vertices</li>
<li>Amount of edges</li>
</ul>

<p>Then we can create our own setup with equal dimensions and optimize it.</p>

