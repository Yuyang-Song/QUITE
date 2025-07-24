# Query performance with not existing relationship check in Neo4j
[Link to question](https://stackoverflow.com/questions/72351642/query-performance-with-not-existing-relationship-check-in-neo4j)
**Creation Date:** 1653321984
**Score:** 1
**Tags:** performance, graph, neo4j, query-optimization
## Question Body
<p>we are trying to optimize a query but the time explodes (~20 seconds) when having around 40K nodes in the database, but it should be way faster.</p>
<p>First, I will describe a simplified description of our schema. We have the following nodes:</p>
<ul>
<li>Usergroup</li>
<li>Feature</li>
<li>Asset</li>
<li>Section</li>
</ul>
<p>We also have the following relationships:</p>
<ul>
<li>A Feature has only one Section (IS_IN_SECTION)</li>
<li>A Feature has one or more Asset (CONTAINS_ASSET)</li>
<li>An asset may be restricted for a Usergroup (HAS_RESTRICTED_ASSET)</li>
<li>A Feature may be restricted for a Usergroup (HAS_RESTRICTED_FEATURE)</li>
<li>A Section, and therefore, all the Feature of that Section, may be restricted for a Usergroup (HAS_RESTRICTED_SECTION)</li>
<li>A Usergroup may have a parent Usergroup (HAS_PARENT_GROUP) and it should fulfill its restrictions and those of its parents</li>
</ul>
<p>The goal is, given a Usergroup, to list the top 20 assets ordered by date, that don't have any restrictions with the Usergroup.</p>
<p>The current query is similar to:</p>
<pre><code>(1)
MATCH path=(:UserGroup {uid: $usergroup_uid})-[:HAS_PARENT_GROUP*0..]-&gt;(root:UserGroup)
  WHERE NOT (root)-[:HAS_PARENT_GROUP]-&gt;(:UserGroup)
  WITH nodes(path) AS usergroups
  UNWIND usergroups AS ug

(2)
MATCH (node:Asset)
  WHERE NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)-[:IS_IN_SECTION]-&gt;(:Section)&lt;-[:HAS_RESTRICTED_SECTION {restriction_type: &quot;view&quot;}]-(ug) 
  AND NOT (node)&lt;-[:HAS_RESTRICTED_ASSET {restriction_type: &quot;view&quot;}]-(ug)
  AND NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)&lt;-[:HAS_RESTRICTED_FEATURE {restriction_type: &quot;view&quot;}]-(ug)

RETURN DISTINCT node 
ORDER BY node.date DESC
SKIP 0
LIMIT 20
</code></pre>
<p>We have a few more types of restrictions but here we have the main idea.</p>
<p>Some observations we have made are:</p>
<ul>
<li>If we execute the query part (1) adding <code>return ug</code> after unwind, this query is solved in 1ms</li>
<li>If we change the query part (1) to <code>MATCH (ug:Usergroup {uid: $usergroup_uid})</code> ignoring the parent groups, the query is solved in around 800ms. And if we add back the original part (1) it is solved in 8 seconds even if the Usergroup has no parents.</li>
</ul>
<p>Currently, our database is small compared to the expected number of nodes (~6 millions), and the number of restrictions will grow, and we need to optimize this kind of queries.</p>
<p>For that, we have these questions:</p>
<ul>
<li>The <code>NOT &lt;restrictions&gt;</code> (ex: <code>NOT (node)&lt;-[:HAS_RESTRICTED_ASSET {restriction_type: &quot;view&quot;}]-(ug)</code>) conditions is correct in this kind of situation or are there other approachs to get the job done more efficiently?</li>
<li>Do we need any type of index?</li>
<li>Is the structure of the schema right, or are there any inefficiencies?</li>
<li>How can we rewrite the part (1) of the query or what do you thinks is causing the overhead with it?</li>
</ul>
<p>The database version is Neo4j 3.5.X</p>
<p>Thanks in advance.</p>

## Answers
### Answer ID: 72375048
<p>Let me answer your questions one by one:</p>
<ol>
<li><p>The <code>NOT &lt;restrictions&gt;</code> type of conditions can prove to be inefficient if provide a set of paths within restrictions because it can lead to duplicate work. Consider the following two sets of restrictions in your query.</p>
<p><code>NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)-[:IS_IN_SECTION]-&gt;(:Section)&lt;-[:HAS_RESTRICTED_SECTION {restriction_type: &quot;view&quot;}]-(ug)</code>
and <code>NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)&lt;-[:HAS_RESTRICTED_FEATURE {restriction_type: &quot;view&quot;}]-(ug)</code></p>
</li>
</ol>
<p>In both of these checks, neo4j might look for the relationship <code>CONTAINS_ASSET</code> and nodes of type <code>Feature</code> separately, once for the first path match and then for the second. This duplicate processing should be reduced if it happens. You should profile your query in Neo4j Browser, to see how the query planner plans and executes the query.</p>
<ol start="2">
<li><p>In terms of indexes you can create two indexes, the first is on the <code>Usergroup uid</code> field, and the second on the <code>date</code> field of the <code>Asset</code> node, this might help if you have a lot of asset nodes and date key stores a string. Again, profile your query to see what indexes are coming into play during execution.</p>
</li>
<li><p>In terms of schema, I noticed that in second part of your query
<code>NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)-[:IS_IN_SECTION]-&gt;(:Section)&lt;-[:HAS_RESTRICTED_SECTION {restriction_type: &quot;view&quot;}]-(ug)  AND NOT (node)&lt;-[:HAS_RESTRICTED_ASSET {restriction_type: &quot;view&quot;}]-(ug) AND NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)&lt;-[:HAS_RESTRICTED_FEATURE {restriction_type: &quot;view&quot;}]-(ug) </code>, all these three checks are basically looking for whether an asset is restricted for a user group, either directly, via a feature, or via a section. One thing we can do here is to create intermediate relationships, between an Asset and UserGroup node. For example, we can have <code>IS_RESTRICTED_DUE_TO_A_FEATURE</code> relationship between an asset and user group node, if an asset is part of a feature for which the user group has restricted access. In this way, your path match reduces from <code>NOT (node)&lt;-[:CONTAINS_ASSET]-(:Feature)&lt;-[:HAS_RESTRICTED_FEATURE {restriction_type: &quot;view&quot;}]-(ug)</code> to <code>NOT (node)&lt;-[:IS_RESTRICTED_DUE_TO_A_FEATURE]-(ug)</code>, which should be faster. Obviously, this change will impact your other CRUD operations, and you might want to store some properties in the new relationships as well.</p>
</li>
<li><p>For this part, I am not sure, what is causing the overhead, but I suggest you add the index on the Usergroup uid field, if not present, and then modify your first part to this:</p>
<p><code>MATCH (ug:UserGroup {uid: $usergroup_uid})-[:HAS_PARENT_GROUP*0..]-&gt;(root:UserGroup) WHERE NOT (root)-[:HAS_PARENT_GROUP]-&gt;(:UserGroup) RETURN ug</code></p>
</li>
</ol>
<p>If it performs well, then try modifying your second part to this:</p>
<pre><code>MATCH (node:Asset)
OPTIONAL MATCH (node)&lt;-[rel1:CONTAINS_ASSET]-(f:Feature)-[rel2:IS_IN_SECTION]-&gt;(s:Section) 
  WITH node
  WHERE (s IS NULL OR NOT (s)&lt;-[:HAS_RESTRICTED_SECTION {restriction_type: &quot;view&quot;}]-(ug)) 
  AND NOT (node)&lt;-[:HAS_RESTRICTED_ASSET {restriction_type: &quot;view&quot;}]-(ug)
  AND (f IS NULL OR NOT (f)&lt;-[:HAS_RESTRICTED_FEATURE {restriction_type: &quot;view&quot;}]-(ug))

RETURN DISTINCT node 
ORDER BY node.date DESC
SKIP 0
LIMIT 20
</code></pre>
<p>Please try out the above suggestions, also the above queries are not tested, so please modify them a bit, if the output format is unexpected. Do profile them out, to figure out the slowest part, in the queries. Hopefully, it helps.</p>

