# Creating nodes and relationships at the same time in neo4j
[Link to question](https://stackoverflow.com/questions/23336802/creating-nodes-and-relationships-at-the-same-time-in-neo4j)
**Creation Date:** 1398675772
**Score:** 16
**Tags:** neo4j, cypher
## Question Body
<p>I am trying to build an database in Neo4j with a structure that contains seven different types of nodes, in total around 4-5000 nodes and between them around 40000 relationships. The cypher code i am currently using is that i first create the nodes with the code:</p>

<pre><code>Create (node1:type {name:'example1', type:'example2'})
</code></pre>

<p>Around 4000 of that example with unique nodes.</p>

<p>Then I've got relationships stated as such:</p>

<pre><code>Create
(node1)-[:r]-(node51),
(node2)-[:r]-(node5),
(node3)-[:r]-(node2);
</code></pre>

<p>Around 40000 of such unique relationships.</p>

<p>With smaller scale graphs this has not been any problem at all. But with this one, the Executing query never stops loading.</p>

<p>Any suggestions on how I can make this type of query work? Or what i should do instead?</p>

<p>edit. What I'm trying to build is a big graph over a product, with it's releases, release versions, features etc. in the same way as the Movie graph example is built.</p>

<p>The product has about 6 releases in total, each release has around 20 releaseversion. In total there is 371 features and of there 371 features there is also 438 featureversions. ever releaseversion (120 in total) then has around 2-300 featureversions each. These Featureversions are mapped to its Feature whom has dependencies towards a little bit of everything in the db. I have also involed HW dependencies such as the possible hw to run these Features on, releases on etc. so basicaly im using cypher code such as:</p>

<pre><code>Create (Product1:Product {name:'ABC', type:'Product'})
Create (Release1:Release {name:'12A', type:'Release'})
Create (Release2:Release {name:'13A, type:'release'})
Create (ReleaseVersion1:ReleaseVersion {name:'12.0.1, type:'ReleaseVersion'})
Create (ReleaseVersion2:ReleaseVersion {name:'12.0.2, type:'ReleaseVersion'})    
</code></pre>

<p>and below those i've structured them up using </p>

<pre><code>Create (Product1)&lt;-[:Is_Version_Of]-(Release1),
(Product1)&lt;-[:Is_Version_Of]-(Release2),
(Release2)&lt;-[:Is_Version_Of]-(ReleaseVersion21),        
</code></pre>

<p>All the way down to features, and then I've also added dependencies between them such as:</p>

<pre><code>(Feature1)-[:Requires]-&gt;(Feature239),
(Feature239)-[:Requires]-&gt;(Feature51);       
</code></pre>

<p>Since i had to find all this information from many different excel-sheets etc, i made the code this way thinking i could just put it together in one mass cypher query and run it on the /browser on the localhost. it worked really good as long as i did not use more than 4-5000 queries at a time. Then it created the entire database in about 5-10 seconds at maximum, but now when I'm trying to run around 45000 queries at the same time it has been running for almost 24 hours, and are still loading and saying "executing query...". I wonder if there is anyway i can improve the time it takes, will the database eventually be created? or can i do some smarter indexes or other things to improve the performance? because by the way my cypher is written now i cannot divide it into pieces since everything in the database has some sort of connection to the product. Do i need to rewrite the code or is there any smooth way around?</p>

## Answers
### Answer ID: 73000389
<p>It is possible to use a single cypher query to create a new node as well as relate it to an existing now.</p>
<p>As an example, assume you're starting with:</p>
<ul>
<li>an existing &quot;One&quot; node which has an &quot;id&quot; property &quot;1&quot;</li>
</ul>
<p>And your goal is to:</p>
<ul>
<li>create a second node, let's call that &quot;Two&quot;, and it should have a property id:&quot;2&quot;</li>
<li>relate the two nodes together</li>
</ul>
<p>You could achieve that goal using a single Cypher query like this:</p>
<pre><code>MATCH (one:One {id:'1'})
CREATE (one) -[:RELATED_TO]-&gt; (two:Two {id:'2'})
</code></pre>

### Answer ID: 54897186
<p>If you have one of the nodes already created then a simple approach would be:</p>

<pre><code>MATCH (n: user {uid: "1"}) CREATE (n) -[r: posted]-&gt; (p: post {pid: "42", title: "Good Night", msg: "Have a nice and peaceful sleep.", author: n.uid});
</code></pre>

<p>Here the user node already exists and you have created a new relation and a new post node.</p>

### Answer ID: 23344988
<p>You can create multiple nodes and relationships interlinked with a single create statement, like this:</p>

<pre><code>create (a { name: "foo" })-[:HELLO]-&gt;(b {name : "bar"}),
       (c {name: "Baz"})-[:GOODBYE]-&gt;(d {name:"Quux"});
</code></pre>

<p>So that's one approach, rather than creating each node individually with a single statement, then each relationship with a single statement.</p>

<p>You can also create multiple relationships from objects by matching first, then creating:</p>

<pre><code>match (a {name: "foo"}), (d {name:"Quux"}) create (a)-[:BLAH]-&gt;(d);
</code></pre>

<p>Of course you could have multiple match clauses, and multiple create clauses there.</p>

<p>You might try to match a given type of node, and then create all necessary relationships from that type of node.   You have enough relationships that this is going to take many queries.  Make sure you've indexed the property you're using to  match the nodes.  As your DB gets big, that's going to be important to permit fast lookup of things you're trying to create new relationships off of.</p>

<p>You haven't specified which query you're running that isn't "stopping loading".   Update your question with specifics, and let us know what you've tried, and maybe it's possible to help.</p>

### Answer ID: 23360823
<p>If you're able to use the Neo4j 2.1 prerelease milestones, then you should try using the new <code>LOAD CSV</code> and <code>PERIODIC COMMIT</code> features. They are designed for just this kind of use case.</p>

<p><a href="http://docs.neo4j.org/chunked/milestone/cypherdoc-importing-csv-files-with-cypher.html" rel="nofollow"><code>LOAD CSV</code></a> allows you to describe the structure of your data with one or more Cypher patterns, while providing the values in CSV to avoid duplication.</p>

<p><a href="http://docs.neo4j.org/chunked/milestone/query-periodic-commit.html" rel="nofollow"><code>PERIODIC COMMIT</code></a> can help make large imports more reliable and also improve performance by reducing the amount of memory that is needed.</p>

### Answer ID: 23359954
<p>Another interesting approach might be to generate your statements directly in Excel, see <a href="http://blog.bruggen.com/2013/05/reloading-my-beergraph-using-in-graph.html?view=sidebar" rel="nofollow">http://blog.bruggen.com/2013/05/reloading-my-beergraph-using-in-graph.html?view=sidebar</a> for an example. You can run a lot of CREATE statements in one transaction, so this should not be overly complicated.</p>

