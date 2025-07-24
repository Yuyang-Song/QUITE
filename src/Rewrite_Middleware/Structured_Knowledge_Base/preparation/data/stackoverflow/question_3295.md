# Why is my Neo4J composite index not being used with MATCH and ORDER BY?
[Link to question](https://stackoverflow.com/questions/75278306/why-is-my-neo4j-composite-index-not-being-used-with-match-and-order-by)
**Creation Date:** 1675025503
**Score:** 0
**Tags:** neo4j
## Question Body
<p>I have a lot of nodes of label <code>Person</code> with properties <code>treeId</code>, <code>firstName</code>, <code>lastName</code>.
I am trying to implement a performant endless scroll of all Persons with some treeId, ordered alphabetically:</p>
<pre><code>MATCH (p:Person {treeId: &quot;admin&quot;}) RETURN p ORDER BY p.lastName, p.firstName SKIP 100 LIMIT 20
</code></pre>
<hr />
<p><strong>Question:</strong> What index do I need to create for this operation to run on indexes as much as possible?</p>
<p>I attempted to create such an index:</p>
<pre><code>CREATE INDEX personTreeLastNameFirstName FOR (p:Person) ON (p.treeId, p.lastName, p.firstName)
</code></pre>
<p>but with this index, the first operation is <code>NodeByLabelScan</code>, so the index is not used.</p>
<p>Another index I tried is more helpful:</p>
<pre><code>CREATE INDEX personTree FOR (p:Person) ON p.treeId
</code></pre>
<p>the first operation is <code>NodeIndexSeek</code> when using it, but it doesn't include the names, so every Person with the specified treeId needs to be read from the database.</p>
<p>What index do I need to create, or how do I need to rewrite the query for it to be more performant on large amounts of Persons with the same treeId?</p>

## Answers
### Answer ID: 75280853
<p>The index :</p>
<pre><code>CREATE INDEX personTree FOR (p:Person) ON p.treeId
</code></pre>
<p>only indexes <code>treeId</code>, hence it can only be used to sort and search on <code>treeIds</code>.</p>
<p>The composite index:</p>
<pre><code>CREATE INDEX personTreeLastNameFirstName FOR (p:Person) ON (p.treeId, p.lastName, p.firstName)
</code></pre>
<p>indexes <code>treeId</code>, <code>lastName</code> and <code>firstName</code>, but the catch here is it will only be used if all the three indexed keys are present in the search clause, that's why you are getting <code>NodeByLabelScan</code>. To allow neo4j to use your composite index, you should add some search criteria for <code>firstName</code> and <code>lastName</code>. Like this:</p>
<pre><code>MATCH (p:Person) 
WHERE p.treeId= &quot;admin&quot; AND p.firstName &gt; &quot;&quot; AND p.lastName &gt; &quot;&quot; 
RETURN p 
ORDER BY p.lastName, p.firstName 
SKIP 100 LIMIT 20
</code></pre>

