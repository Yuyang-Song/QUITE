# Best way to represt n/ depth tree for use in PHP (MySQL / XML / ?)
[Link to question](https://stackoverflow.com/questions/339745/best-way-to-represt-n-depth-tree-for-use-in-php-mysql-xml)
**Creation Date:** 1228373365
**Score:** 3
**Tags:** php, mysql, xml, search, tree
## Question Body
<p>I am currently in the process of rewriting an application whereby teachers can plan curriculum online.</p>

<p>The application guides teachers through a process of creating a unit of work for their students. The tool is currently used in three states but we have plans to get much bigger than that.</p>

<p>One of the major draw cards of the application is that all of the student outcomes are preloaded into the system. This allows teachers to search or browse through and select which outcomes are going to be met in each unit of work.</p>

<p>When I originally designed the system I made the assumption that all student outcomes followed a similar Hierarchy. That is, there are named nested containers and then outcomes.</p>

<p>The original set of outcomes that I entered was three tiered. As such my database has the following structure:</p>

<p>=========================</p>

<p><em>Tables in bold</em></p>

<p><strong>h1</strong></p>

<p>id, Name</p>

<p><strong>h2</strong></p>

<p>id, parent___id (h1_id), Name</p>

<p><strong>h3</strong></p>

<p>id, parent___id (h2_id), Name</p>

<p><strong>outcome</strong></p>

<p>id, parent___id (h3_id), Name</p>

<p>=========================</p>

<p>Other than the obvious inability to add n/ levels of hierarchy this method also made it difficult to display a list of all of the standards without recursively querying the database.</p>

<p>Once the student outcomes (and their parent categories) have been added there is very little reason for them to be modified in any way. The primary requirement is that they are easy and efficient to read.</p>

<p>So far all of the student outcomes from different schools / states / countries have roughly followed my assumption. This may not always be the case.</p>

<p>All existing data must of course be transferred across from the current database.</p>

<p>Given the above, what is the best way for me to store all the different sets of student outcomes? Some of the ideas I have had are listed below.</p>

<ul>
<li><p>Continue using 4 tables in the database, when selecting either use recusion or lots of joins</p></li>
<li><p>Use nested sets</p></li>
<li><p>XML (Either a global XML file for all of the different sets or an XML file for each)</p></li>
</ul>

## Answers
### Answer ID: 1675311
<p>there is another way to handle trees in a database that is maybe not as "smart" than nested sets and other patterns described here, but that is really efficient and easy :</p>

<p>instead of storing the level (or depth) of an item, you can store the full path in the tree, like this :</p>

<pre><code>A
  B
  C
    D
  E
</code></pre>

<p>would be stored like this:</p>

<pre><code>item  |  parent  |  path
----------------------------
A     |  NULL    |  A
B     |  A       |  A--B
C     |  A       |  A--C
D     |  C       |  A--C--D
E     |  A       |  A--E
</code></pre>

<p>then you can easyly get:</p>

<ul>
<li>(pure SQL) all direct children of an item with a where parent = '' clause</li>
<li>(pure SQL) all direct and indirect children with a where path LIKE 'PARENT--%' clause</li>
<li>(PHP) the depth of the node (count(explode('--',$path))</li>
</ul>

<p>those features are good enough in most situations, and quite performant, even with several sublevels, as long as you create the good indices (PK, index on parent, index on path). For sure, this solution is demanding when deleting/moving nodes to update pathes...</p>

<p>I hope this helps!</p>

### Answer ID: 339914
<p>I agree with the other poster - nested sets is the way to go I think.</p>

<p>See here:</p>

<p><a href="http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/" rel="nofollow noreferrer">http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/</a></p>

<p>It explains the theory and compares it to what you are already using - which is a twist on adjacency really. It shows +/- of them all, and should help you reach a decision based on all of the subtleties of your project.</p>

<p>Another thing I've seen (in CakePHP's tree behaviour) is actually to use both at once. Sure its not great performance wise, but under this model, you insert/remove things just as you would with adjacency, and then there is a method to run to rebuild the left/right edge values to allow you to do the selects in a nested sets fashion. Result is you can insert/delete much more easily.</p>

<p><a href="http://book.cakephp.org/view/91/Tree" rel="nofollow noreferrer">http://book.cakephp.org/view/91/Tree</a></p>

### Answer ID: 339780
<p>I don't know that you actually need 4 tables for this. </p>

<p>If you have a single table that tracks the parent_id and a level you can have infinite levels. </p>

<blockquote>
  <p><strong>outcome</strong></p>
  
  <p>id, parent_id, level, name</p>
</blockquote>

<p>You can use recursion to track through the tree for any particular element (you don't actually need level, but it can be easier to query with it). </p>

<p>The alternative is nested sets. In this case you would still merge to a single table, but use the set stuff to track levels. </p>

<p>Which one to use depends on your application.</p>

<p>Read-intensive:  nested sets</p>

<p>Write-intensive: parent tree thingy</p>

<p>This is because with nested sets you can retrieve the entire tree with a single query but at the cost of reordering the entire tree every time you insert a new node.</p>

<p>When you just track the parent_id, you can move or delete nodes individually.</p>

<p>PS: I vote no to XML. You have the same recursive issues, plus the overhead of parsing the data as well as either storing it in the db or on the filesystem (which will cause concurrency issues).</p>

