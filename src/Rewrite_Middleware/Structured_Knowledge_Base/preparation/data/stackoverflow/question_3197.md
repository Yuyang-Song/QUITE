# AWS Neptune performance / Comparing to Neo4j AuraDB
[Link to question](https://stackoverflow.com/questions/70880522/aws-neptune-performance-comparing-to-neo4j-auradb)
**Creation Date:** 1643294575
**Score:** 1
**Tags:** database, amazon-web-services, performance, amazon-neptune
## Question Body
<p>We use Neo4j AuraDB for our graph database but there we have issues with data upload. So, we decided to move to AWS Neptune using the migration tool.</p>
<p>We have 3.7M nodes and 11.2M relations in our database. The DB instance is db.r5.large with 2 CPUs and 16GiB RAM.</p>
<p>The same AWS Neptune OpenCypher queries are much slower than AuraDB Cypher queries (about 7-10 times slower). Also, we tried to rewrite the queries to Gremlin and test performance but it is still very slow. We have node and lookup indexes on AuraDB but we can't create them on AWS Neptune as it handles them automatically.</p>
<p>Is there any way to reach better performance on AWS Neptune?</p>
<p><strong>UPDATE:</strong></p>
<p>Example of Gremlin query:
<code>g.V().hasLabel('Member').has('address', eq('${address}')).outE('HAS').as('member_has').inV().as('token').hasLabel('Token').inE('HAS').as('other_member_has').outV().as('other_member').hasLabel('Member').where(__.select('member_has').where(neq('other_member_has'))).select('other_member', 'token').group().by(__.select('other_member').local(__.properties().group().by(__.key()).by(__.map(__.value())))).by(__.fold().project('member', 'number_of_tokens').by(__.unfold().select('other_member').choose(neq('cypher.null'), __.local(__.properties().group().by(__.key()).by(__.map(__.value()))))).by(__.unfold().select('token').count())).unfold().select(values).order().by(__.select('number_of_tokens'), desc).limit(20)</code></p>
<p>Example of Cypher query:
<code>MATCH (member:Member { address: '${address}' })-[:HAS]-&gt;(token:Token)&lt;-[:HAS]-(other_member:Member) RETURN PROPERTIES(other_member) as member, COUNT(token) AS number_of_tokens ORDER BY number_of_tokens DESC LIMIT 20</code></p>

## Answers
### Answer ID: 70934537
<p>As discussed in the comments, as of this moment, the openCypher support is a preview, not quite GA level. The more recent engine versions do have some significant improvements but more are yet to be delivered. As to the Gremlin query, tools that convert Cypher to Gremlin tend to build quite complex queries. I think the Gremlin equivalent to the Cypher query is going to look something like this.</p>
<pre class="lang-java prettyprint-override"><code>g.V().has('Member','address', address).as('m').
      out('HAS').hasLabel('Token').as('t').
      in('HAS').hasLabel('Member').as('om').
      where(neq('m')).
      group().
        by('om').
        by(select('t').count()).
      order(local).
        by(values,desc).
      limit(20) 

</code></pre>
<p>and if you want all of the properties just add a <code>valueMap</code> as in:</p>
<pre class="lang-java prettyprint-override"><code>g.V().has('Member','address', address).as('m').
      out('HAS').hasLabel('Token').as('t').
      in('HAS').hasLabel('Member').as('om').
      where(neq('m')).
      group().
        by(select('om').valueMap(true)).
        by(select('t').count()).
      order(local).
        by(values,desc).
      limit(20) 
</code></pre>

