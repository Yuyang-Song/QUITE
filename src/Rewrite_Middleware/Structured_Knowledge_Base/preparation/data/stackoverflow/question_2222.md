# Querying by nested pointers?
[Link to question](https://stackoverflow.com/questions/24602151/querying-by-nested-pointers)
**Creation Date:** 1404698616
**Score:** 0
**Tags:** parse-platform
## Question Body
<p>I'm rewriting a "Yelp for Dorm rooms" web app in Node/Express with a Parse backend (PHP version <a href="http://dormsdb.alexthemitchell.com" rel="nofollow">here</a> for context).</p>

<p>Since I am very used to SQL databases, I have organized my data into four tables of one-to-many pointers:</p>

<pre><code>Rooms
Halls
Clusters
Campuses
</code></pre>

<p>Every room has a pointer to its hall, each hall has a pointer to its cluster (a small group of halls) and each cluster has a pointer to its campus.</p>

<p>However, since each hall/cluster/campus has its own culture, I want to be able to search by each level (e.g. I want to live on South campus, or Norris Hall). However, since the pointers are nested three levels deep, I'm having a problem searching by campus and returning rooms. I'd hate to have to duplicate data and copy/paste cluster and campus data into each room object. </p>

<p>Searching for a cluster is easy. I can just:</p>

<pre><code>var clusterQuery = new Parse.Query("clusters");
clusterQuery.equalTo("cluster", req.params.cluster);
var hallsQuery = new Parse.Query("halls");
hallsQuery.matchesQuery("cluster", clusterQuery);
query.matchesQuery("hall", hallsQuery);
</code></pre>

<p>So I figured doing a campus search would be simply</p>

<pre><code>var campusQuery = new Parse.Query("campuses");
campusQuery.equalTo("cluster", req.params.campus);
var clusterQuery = new Parse.Query("clusters");
clusterQuery.matchesQuery("campus", campusQuery);
var hallsQuery = new Parse.Query("halls");
hallsQuery.matchesQuery("cluster", clusterQuery);
query.matchesQuery("hall", hallsQuery);
</code></pre>

<p>But of course, that would be too easy. </p>

<p>Instead, I get an error 154: Query had too many nested queries.</p>

<p>So my question for you, almighty Stackoverflow community: What should I do instead?</p>

## Answers
### Answer ID: 24606602
<p>It makes more sense to name your classes with singular names, <code>Campus</code> rather than <code>Campuses</code>. So, I will go with singular names. </p>

<p>Your model is a tree structure and there are some patterns for it. The one you use is keeping parent references, that is simple but requires multiple queries for subtrees as you realized. Since Parse is using MongoDB, you can check use cases and model patterns of MongoDB, such as <a href="http://docs.mongodb.org/ecosystem/use-cases/product-catalog/" rel="nofollow">Product Catalog</a> and <a href="http://docs.mongodb.org/manual/tutorial/model-tree-structures-with-parent-references/" rel="nofollow">Model Tree Structures</a>.</p>

<p>Consider <a href="http://docs.mongodb.org/manual/tutorial/model-tree-structures-with-ancestors-array/" rel="nofollow">Array of Ancestors pattern</a> where you have something like <code>{_id: "Room1", ancestors: [pointerToAHall, pointerToACluster, pointerToACampus], parrent: pointerToAHall}</code>. </p>

<p>You can find rooms where <code>ancestors</code> array contains a campus: </p>

<pre><code>var query = new Parse.Query("Room");
query.equalTo("ancestors", aCampusObject)
</code></pre>

<p>Note that <code>equalTo</code> knows that <code>ancestors</code> is an array. You may want to check Parse docs for <a href="https://parse.com/docs/js_guide#queries-arrays" rel="nofollow">queries on array</a>. </p>

