# Neo4j cypher query for updating nodes taking a long time
[Link to question](https://stackoverflow.com/questions/45618847/neo4j-cypher-query-for-updating-nodes-taking-a-long-time)
**Creation Date:** 1502381929
**Score:** 1
**Tags:** performance, neo4j, cypher, database-performance, neo4j-apoc
## Question Body
<p>I have a graph with the following:</p>

<p>(:Customer)-[:MATCHES]->(:Customer)</p>

<p>This is not limited to two customers but the depth does not exceed 5. The following also exists:</p>

<p>(:Customer)-[:MATCHES]->(:AuditCustomer)</p>

<p>There is a label :Master that needs to be added to one customer node in a matching set depending on some criteria.</p>

<p>My query therefore needs to find all sets of matching customers where none have the label master and add that label to one node in the set. There are a large number of customer nodes and doing it all in one go causes the database to become very slow.</p>

<p>I have attempted to do it using apoc.periodic.commit:</p>

<pre><code>CALL apoc.periodic.commit("MATCH (c:Customer) 
WHERE NOT c:Master AND NOT (c)-[:MATCHES*0..5]-(:Master) WITH c limit {limit} 
CALL apoc.path.expand(c, 'MATCHES', '+Customer', 0, -1) 
YIELD path UNWIND NODES(path) AS nodes WITH c,nodes 
order by nodes:Searchable desc, nodes.createdTimestamp asc 
with c, head(collect(distinct nodes)) as collectedNodes 
set collectedNodes:Master 
return count(collectedNodes)", {limit:100})
</code></pre>

<p>However this still causes the database to become very slow even if the limit parameter is set to 1. I read that apoc.periodic.commit is a blocking process so this may be causing a problem. Is there a way to do this that is not so resource intensive and the DB can continue to process other transactions while this is running?</p>

<p>The slowest part of the query is the initial match:</p>

<pre><code>MATCH (c:Customer) 
    WHERE NOT c:Master AND NOT (c)-[:MATCHES*0..5]-(:Master) WITH c limit {limit}
</code></pre>

<p>This takes around 3.5s and the entire query takes about 4s. There is very little difference between limit 1 and limit 20. Maybe if there is a way to rewrite this so it is faster, it might be a better approach?</p>

<p>Also, if it is of any use, the following returns ~70K</p>

<pre><code>MATCH (c:Customer) 
WHERE NOT c:Master AND NOT (c)-[:MATCHES*0..5]-(:Master)
RETURN COUNT(c)
</code></pre>

