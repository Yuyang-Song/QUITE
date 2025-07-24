# Enforce order of relations in multipath queries
[Link to question](https://stackoverflow.com/questions/55813748/enforce-order-of-relations-in-multipath-queries)
**Creation Date:** 1556030588
**Score:** 1
**Tags:** neo4j, cypher
## Question Body
<p>I'm looking into neo4j as a Graph database, and variable length path queries will be a very important use case. I now <em>think</em> I've found an example query that Cypher will not support.</p>

<p>The main issue is that I want to treat composed relations as a single relation. Let my give an example: finding co-actors. I've done this using the standard database of movies. The goal is to find all actors that have acted alongside Tom Hanks. This can be found with the query:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN]-&gt;()&lt;-[:ACTED_IN]-(a:Person) return a
</code></pre>

<p>Now, what if we want to find co-actors of co-actors recursively.
We can rewrite the above query to:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN*2]-(a:Person) return a
</code></pre>

<p>And then it becomes clear we can do this with </p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN*]-(a:Person) return a
</code></pre>

<p>Notably, all odd-length paths are excluded because they do not end in a <code>Person</code>.</p>

<p>Now, I have found a query that I cannot figure out how to make recursive:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN]-&gt;()&lt;-[:DIRECTED]-()-[:DIRECTED]-&gt;()&lt;-[:ACTED_IN]-(a:Person) return DISTINCT a
</code></pre>

<p>In words, all actors that have a director in common with Tom Hanks.</p>

<p>In order to make this recursive I tried:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN|DIRECTED*]-(a:Person) return DISTINCT a
</code></pre>

<p>However, (besides not seeming to complete at all). This will also capture co-actors.
That is, it will match paths of the form</p>

<pre><code>()-[:ACTED_IN]-&gt;()&lt;-[:ACTED_IN]-()
</code></pre>

<p>So what I am wondering is:
can we somehow restrict the order in which relations occur in a multi-path query?
Something like:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"}){-[:ACTED_IN]-&gt;()&lt;-[:DIRECTED]-()-[:DIRECTED]-&gt;()&lt;-[:ACTED_IN]-}*(a:Person) return DISTINCT a
</code></pre>

<p>Where the * applies to everything in the curly braces.</p>

## Answers
### Answer ID: 55821048
<p>The <a href="https://neo4j-contrib.github.io/neo4j-apoc-procedures/#path-expander" rel="nofollow noreferrer">path expander procs</a> from <a href="https://neo4j-contrib.github.io/neo4j-apoc-procedures/" rel="nofollow noreferrer">APOC Procedures</a> should help here, as we added the ability to express repeating sequences of labels, relationships, or both.</p>

<p>In this case, since you want to match on the actor of the pattern rather than the director (or any of the movies in the path), we need to specify which nodes in the path you want to return, which requires either using the <code>labelFilter</code> in addition to the <code>relationshipFilter</code>, or just to use the combined <code>sequence</code> config property to specify the alternating labels/relationships expected, and making sure we use an end node filter on the :Person node at the point in the pattern that you want.</p>

<p>Here's how you would do this after installing APOC:</p>

<pre><code>MATCH (tom:Person {name: "Tom Hanks"})
CALL apoc.path.expandConfig(tom, {sequence:'&gt;Person, ACTED_IN&gt;, *, &lt;DIRECTED, *, DIRECTED&gt;, *, &lt;ACTED_IN', maxLevel:12}) YIELD path
WITH last(nodes(path)) as person, min(length(path)) as distance
RETURN person.name
</code></pre>

<p>We would usually use <code>subgraphNodes()</code> for these, since it's efficient at expanding out and pruning paths to nodes we've already seen, but in this case, we want to keep the ability to revisit already visited nodes, as they may occur in further iterations of the sequence, so to get a correct answer we can't use this or any of the procs that use NODE_GLOBAL uniqueness.</p>

<p>Because of this, we need to guard against exploring too many paths, as the permutations of relationships to explore that fit the path will skyrocket, even after we've already found all distinct nodes possible. To avoid this, we'll have to add a maxLevel, so I'm using 12 in this case.</p>

<p>This procedure will also produce multiple paths to the same node, so we're going to get the minimum length of all paths to each node.</p>

<p>The <a href="https://neo4j-contrib.github.io/neo4j-apoc-procedures/#_sequences" rel="nofollow noreferrer">sequence</a> config property lets us specify alternating label and relationship type filterings for each step in the sequence, starting at the starting node. We are using an end node filter symbol, <code>&gt;</code> before the first Person label (<code>&gt;Person</code>) indicating that we only want paths to the Person node at this point in the sequence (as the first element in the sequence it will also be the last element in the sequence as it repeats). We use the wildcard <code>*</code> for the label filter of all other nodes, meaning the nodes are whitelisted and will be traversed no matter what their label is, but we don't want to return any paths to these nodes.</p>

### Answer ID: 55820101
<p>If you want to see all the actors who acted in movies directed by directors who directed Tom Hanks, but who have never acted with Tom, here is one way:</p>

<pre><code>MATCH (tom {name: "Tom Hanks"})-[:ACTED_IN]-&gt;(m)
MATCH (m)&lt;-[:ACTED_IN]-(ignoredActor)
WITH COLLECT(DISTINCT m) AS ignoredMovies, COLLECT(DISTINCT ignoredActor) AS ignoredActors
UNWIND ignoredMovies AS movie
MATCH (movie)&lt;-[:DIRECTED]-()-[:DIRECTED]-&gt;(m2)
WHERE NOT m2 IN ignoredMovies
MATCH (m2)&lt;-[:ACTED_IN]-(a:Person)
WHERE NOT a IN ignoredActors
RETURN DISTINCT a
</code></pre>

<p>The top 2 <code>MATCH</code> clauses are deliberately not combined into one clause, so that the Tom Hanks node will be captured as an <code>ignoredActor</code>. (A <code>MATCH</code> clause filters out any result that use the same relationship twice.)</p>

