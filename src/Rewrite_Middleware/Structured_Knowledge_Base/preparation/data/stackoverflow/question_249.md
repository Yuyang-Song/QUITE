# Is it possible to build and incrementally evaluate/mutate expression trees in Boost.Proto?
[Link to question](https://stackoverflow.com/questions/18034557/is-it-possible-to-build-and-incrementally-evaluate-mutate-expression-trees-in-bo)
**Creation Date:** 1375544981
**Score:** 1
**Tags:** c++, expression-trees, boost-proto
## Question Body
<p>Is it possible to extract parts of a Boost.Proto expression tree, evaluate them individually (externally), and then mutate the expression tree, replacing the extracted parts with a result?</p>

<p>In my specific case, I'm trying to evaluate if I could rewrite some legacy code that repeatedly:</p>

<ol>
<li>generates sql</li>
<li>queries a database</li>
<li>uses the result to generate a new sql query</li>
<li>queries the database again
...
(and so on)</li>
</ol>

<p>What I was hoping to do, was to:
1. Generate a single, large expression tree
2. Get the SQL from the expression tree. This consists of:
    b. visit the tree and check for sub-queries that must be evaluated before the resulting, single sql can be generated
    c. if there are sub-queries, create the sql and return as a string, evaluate the sql externally, and mutate the tree, replacing the sub-queries with the results</p>

<p>(also, I'd like to identify identical sub-queries, and evaluate them only once if it is possible)</p>

<p>Is this possible to do? Will it require code that is hard to understand/learn?</p>

<p>I've skimmed the Boost.Proto documentation, but I'm not sure if it is intended for this scenario where I need to externally evaluate subtrees, and replace it with a result until the whole tree is reduced to a single query.</p>

<p>EDIT:</p>

<p>Lets say I have the following tables:</p>

<p>objects
id | name</p>

<p>attribute_link
objectid | attributeid</p>

<p>attributes
id | parentid | name | value</p>

<p>My queries come in as a custom "query" object -- a (binary) tree with multiple AND,OR clauses.</p>

<p>Example:
query1 = object.id=10 OR (attribute.name = "name" OR attribute.name = "name2")</p>

<p>This translates to: get the attribute(s) for object 10 where the attribute's name is "name". Notice the parentid field, which means that the attribute.name we are looking for <em>can be nested, and not directly linked to our object</em>.</p>

<p>What I need to do is:
1. Translate this into an expression tree with enough information
2. Send this tree to the db layer
3. Process the tree (sometimes in multiple stages) as explained above</p>

<p>Perhaps the expression tree would look something like:</p>

<p>find_attributes( object_id = 10 AND attribute_name = ( "name" OR "name2") )</p>

<p>There are multiple databases where the SQL syntax differs, which is why I want to do it this way. Therefore, I need to be able to override some of the processing steps based on the database.</p>

<p>For e.g. PostgreSQL :</p>

<ol>
<li><p>the processing would first recognize the find_attributes node, and know that we are searching for attributes</p></li>
<li><p>looking further, the attribute needs to be linked to object.id = 10, we generate and run a query right away to get all attributes with object.id = 10, and replace the object_id = 10 node in the expression tree with the actual attribute ids (object_id = 10) => (attribute_id = (20 OR 21)).</p></li>
<li><p>then, we find the attribute_name node and since attributes are nested, we need to find all the attribute rows that have name = "name" or "name2"</p></li>
<li><p>as an (optional) optimization step, since there are millions of attributes, we need to merge the attribute_id and attribute_name nodes into a single query</p></li>
</ol>

<p>The resulting queries could look something like:</p>

<ol>
<li><p>(find attributeids) SELECT id FROM attributes WHERE objectid = 10)</p></li>
<li><p>(final query) ---</p>

<p>WITH<br>
  get_roots AS (SELECT * FROM attributes WHERE (id=20 OR id=21)),<br>
  get_childs AS (SELECT * FROM get_roots, attributes WHERE attributes.parentid = get_roots.id),<br>
  get_grandchilds AS (SELECT * FROM get_childs, attributes WHERE attributes.parentid = get_childs.id)</p>

<p>SELECT * FROM get_roots 
UNION<br>
SELECT * FROM get_childs 
UNION<br>
SELECT * FROM get_grandchilds</p></li>
</ol>

<p>(assuming the attributes are only three levels deep here, it might be rewritten as a recursive CTE)</p>

<p>I guess it might be possible, but would it be too much work? There are a limited set of queries, and the one presented here is the most complicated.</p>

## Answers
### Answer ID: 18387605
<p>Proto tree structure is set at compile-time and thus non mutable. Usually what you do is regenerate a new tree with the elements you need. This can be trivially done as a proto transform takign a tree and returning a new tree.</p>

