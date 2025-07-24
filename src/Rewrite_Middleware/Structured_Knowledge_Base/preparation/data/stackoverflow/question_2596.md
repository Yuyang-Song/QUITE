# Neo4j slower than MySQL in performing recursive query
[Link to question](https://stackoverflow.com/questions/41943800/neo4j-slower-than-mysql-in-performing-recursive-query)
**Creation Date:** 1485803965
**Score:** 4
**Tags:** database, performance, neo4j, cypher
## Question Body
<p>I would like to compare Neo4j(<strong>ver. 3.1</strong>) and MySQL in performing recursive queries. Therefore I created two tables in MySQL database - <code>Customer</code> and <code>CustomerFriend</code>.</p>

<p>Second table consists of <code>CustomerID</code> and <code>FriendID</code> columns, both of them point to <code>CustomerID</code> column in <code>Customer</code> table. In Neo4j were created corresponding entities:</p>

<p><code>Customer</code> nodes and <code>FRIEND_OF</code> relations <code>(c:Customer)-[f:FRIEND_OF]-&gt;(cc:Customer)</code>. Databases are filled with the same data: 
100000 Customers, each Customer has 100 relations.
Executed below queries:</p>

<p>MySQL   (<strong>60s</strong>)</p>

<pre><code>SELECT distinct cf4.FriendID FROM customerfriend cf1
join customerfriend cf2 on cf1.FriendID = cf2.CustomerID
join customerfriend cf3 on cf2.FriendID = cf3.CustomerID
join customerfriend cf4 on cf3.FriendID = cf4.CustomerID
where cf1.CustomerID =99;
</code></pre>

<p>Neo4j   (<strong>240s</strong>)</p>

<pre><code>match (c:Customer{CustomerID:99})-[:FRIEND_OF*4]-&gt;(cc:Customer)
return distinct cc.CustomerID;
</code></pre>

<p>Queries are run from simple Java app, which just connect to database (using available connectors), run queries, and measure execution times.</p>

<p>Measured times clearly indicate that Neo4j is slower in performing above queries than MySQL (MySQL 60s, Neo4j 240s). I have tested above queries for 50 relations per Customer and I achieved same results (MySQL <strong>7s</strong> faster than Neo4j <strong>17s</strong> ).</p>

<p>I read some articles about performing recursive queries in Neo4j which indicate that Neo4j should manage better for this type of queries than MySQL. That's why I have started wondering if I'm doing something wrong or
execution times are proper (<strong>??</strong>).</p>

<p>I'm wondering if in Neo4j exists any possibilities to tune system performance. In case of MySQL I set up <code>innodb_buffer_pool_size</code> to 3g which affected better query performance(shorter execution time).</p>

<p>--------------------------------<strong>EDIT</strong>---------------------------</p>

<p>I have considered below suggestions to rewrite my Noe4j query to new form:</p>

<pre><code>match (c:Customer{CustomerID:99})-[:FRIEND_OF]-&gt;(c1)-[:FRIEND_OF]-&gt;(c2)
with distinct c2
match (c2)-[:FRIEND_OF]-&gt;(c3)
with distinct c3
match (c3)-[:FRIEND_OF]-&gt;(cc:Customer)
with distinct cc
return cc.CustomerID;
</code></pre>

<p>And achieved better query time: <strong>40s</strong>  </p>

<p>In case of MySQL I have figured out way to optimise previous query, similar to idea of Neo4j query optimisation:</p>

<pre><code>select distinct FriendID as depth4
from customerfriend
where CustomerID in
(select distinct FriendID as depth3
from customerfriend
where CustomerID in
(select distinct FriendID as depth2
from customerfriend
where CustomerID in
(select distinct FriendID as depth
from customerfriend
where CustomerID =99
)));
</code></pre>

<p>And execution of this query took <strong>24s</strong></p>

<p>Neo4j still worse than MySQL...  </p>

## Answers
### Answer ID: 42059680
<p>You can make a small modification to make neo4j about 50% faster, or for even more speed, use the bitset dance shown on the bottom of this blog post => <a href="https://maxdemarzi.com/2013/12/31/the-power-of-open-source-software/" rel="nofollow noreferrer">https://maxdemarzi.com/2013/12/31/the-power-of-open-source-software/</a> </p>

<p><strong>Update:</strong></p>

<p>I went ahead and built a custom procedure for you.</p>

<p>You can grab it in the releases tab of <a href="https://github.com/maxdemarzi/distinct_network" rel="nofollow noreferrer">https://github.com/maxdemarzi/distinct_network</a></p>

<p>It takes 2.9 seconds on my laptop with 10002045 relationships.</p>

<p><strong>Second Update:</strong></p>

<p>Wrote a blog post on the subject: <a href="https://maxdemarzi.com/2017/02/06/neo4j-is-faster-than-mysql-in-performing-recursive-query/" rel="nofollow noreferrer">https://maxdemarzi.com/2017/02/06/neo4j-is-faster-than-mysql-in-performing-recursive-query/</a></p>

### Answer ID: 41945063
<p>Can you try:</p>

<pre><code>match (c:Customer{CustomerID:99})-[:FRIEND_OF]-&gt;(c1)-[:FRIEND_OF]-&gt;(c2)
with distinct c2
match (c2)-[:FRIEND_OF]-&gt;(c3)
with distinct c3
match (c3)-[:FRIEND_OF]-&gt;(cc)
with distinct cc
return cc.CustomerID;
</code></pre>

<p>and share your query plan and the query plan for this query?</p>

<h3>Update</h3>

<p>To just measure the query time without wire transport, can you try to run this one:</p>

<pre><code>match (c:Customer{CustomerID:99})-[:FRIEND_OF]-&gt;(c1)-[:FRIEND_OF]-&gt;(c2)
with distinct c2
match (c2)-[:FRIEND_OF]-&gt;(c3)
with distinct c3
match (c3)-[:FRIEND_OF]-&gt;(cc)
with distinct cc
with cc.CustomerID 
return count(*);
</code></pre>

### Answer ID: 41945539
<p>I'd recommend installing <a href="https://neo4j-contrib.github.io/neo4j-apoc-procedures/" rel="nofollow noreferrer">APOC Procedures</a> for this one, the Path Expander functionality is a more efficient means of finding nodes along a path without the extra cost of finding all possible paths.</p>

<pre><code>match (c:Customer{CustomerID:99})
call apoc.path.expandConfig(c, {relationshipFilter:"FRIEND_OF&gt;", minLevel:4, maxLevel:4}) yield path
with distinct last(nodes(path)) as cc
where cc:Custumer
return cc.CustomerID
</code></pre>

<p>EDIT</p>

<p>Looks like NODE_GLOBAL uniqueness won't work in this case. I typically use it when getting all nodes in subgraphs, but it won't apply to this particular case and removed it to use default uniqueness settings. </p>

<p>Unsure how this compares to the equivalent variable-length pattern match. DB hits will be lower, as a procedure call only counts as one db hit and abstracts out the work it's doing, but unsure if it's faster.</p>

### Answer ID: 41944574
<p>Don't know what version of Neo4j you're running, but this might improve your speed while reducing db hits:</p>

<pre><code>MATCH (c:Customer{CustomerID:99})
MATCH (c)-[:FRIEND_OF*4]-&gt;(cc:Customer)
return distinct cc.CustomerID;
</code></pre>

