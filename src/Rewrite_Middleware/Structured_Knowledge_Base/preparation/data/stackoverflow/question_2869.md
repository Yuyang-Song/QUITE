# Need help converting a Neo4j Cypher script to Gremlin
[Link to question](https://stackoverflow.com/questions/56378406/need-help-converting-a-neo4j-cypher-script-to-gremlin)
**Creation Date:** 1559219572
**Score:** 1
**Tags:** cypher, gremlin
## Question Body
<p>I can't figure out how to rewrite my Cypher script in Gremlin.</p>

<p>First we used the .Net Neo4j client to connect to our Neo4j database and run Cypher queries on it. Then we decided to add an abstraction layer and connect to a Gremlin server instead (which, for now, hosts the same Neo4j database). So now I need to translate our queries from Cypher to Gremlin and I am finding it rather difficult. </p>

<p>Here's one of them:</p>

<pre><code>MATCH (pc:ProductCategory)-[:HasRootCategory]-&gt;(r:RootCategory)
WHERE NOT (:ProductCategory)-[]-&gt;(pc) 
AND pc.Id = r.RootId 
RETURN pc;
</code></pre>

<p>One of my failed attempts: 
<code>g.V().match(as("pc").out("HasRootCategory").as("r"),as("pc").in().has('label', 'ProductCategory').count().is(0))).select("pc", "r").where("pc.Id", eq("r.RootId")).select("pc")</code></p>

<p>I found an example on stackoverflow using this 'match(as' construct, but it must be depracated or something, because I'm getting an error. Also, not sure how to compare properties with different names on nodes with different labels (I'm sure the 'where' is wrong...)</p>

<p>Any help would be appreciated.</p>

## Answers
### Answer ID: 56380296
<p>The following traversal should be equivalent:</p>

<pre><code>g.V().hasLabel("ProductCategory").as("pc").
  not(__.in().hasLabel("ProductCategory")).
  out("HasRootCategory").as("r").
  where("pc", eq("r")).
    by("Id").
    by("RootId").
  select("pc")
</code></pre>

<p>Since you don't really need the <code>r</code> label, the query can be tweaked a bit:</p>

<pre><code>g.V().hasLabel("ProductCategory").as("pc").
  not(__.in().hasLabel("ProductCategory")).
  filter(out("HasRootCategory").
         where(eq("pc")).
           by("Id").
           by("RootId"))
</code></pre>

<p>Last thing to mention: If a <code>ProductCategory</code> vertex can be connected to another <code>ProductCategory</code> vertex by only one (or more) specific edge label, that can lead nowhere else, it would be better to do:</p>

<pre><code>g.V().hasLabel("ProductCategory").as("pc").
  not(inE("KnownLabelBetweenCategories")).
  filter(out("HasRootCategory").
         where(eq("pc")).
           by("Id").
           by("RootId"))
</code></pre>

<p>On a different note, <code>match()</code> is not deprecated. I guess you tried to run your traversal in Groovy and it just failed because you didn't use <code>__.as()</code> (<code>as</code>, among others, is a reserved keyword in Groovy).</p>

