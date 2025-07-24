# Express Trees: Rewrite query predicates to use joins
[Link to question](https://stackoverflow.com/questions/49870019/express-trees-rewrite-query-predicates-to-use-joins)
**Creation Date:** 1523939709
**Score:** 1
**Tags:** c#, linq, expression-trees
## Question Body
<p>I want to intercept a query to a database sent via Entity Framework and convert from something like</p>

<pre><code>SELECT * FROM EntityA where (EntityA.Title Like "foo" 
OR EntityA.Description Like "foo") and EntityA.Prop1 in (1,2,3)
</code></pre>

<p>to </p>

<pre><code>SELECT * FROM EntityA INNER JOIN EntityB on EntityA.ID = EntityB.ID 
WHERE (EntityB.Title Like "foo" or EntityB.Description Like "foo") and 
EntityA.Prop1 in (1,2,3)
</code></pre>

<p>I am using ExpressionTrees to pass in the predicates and using <code>ExpressionVisitor</code> I can </p>

<pre><code>override Expression VisitBinary(BinaryExpression b) 
</code></pre>

<p>to access the <code>Or</code> node. </p>

<p>I have a working implementation whereby I issue two separate calls to the db, one to get the ids of EntityA that meet the criteria title search criteria and 
another that combines that expression with the other predicates targeting properties on EntityA.</p>

<p>I would prefer to simply issue a single call with a rewritten query that leverages a <code>JOIN</code> but it's not clear how to rewrite the <code>Or</code> to create a join to an Entity type that was not a part of the original expression.</p>

<p><strong>Updated:</strong> Typos in original post - Its the expression that has the wrong type for subsequent use.</p>

<pre><code>// This doesn't work as it creates an Expression of the wrong type
Expression&lt;Func&lt;IEnumerable&lt;EntityA&gt;, IEnumerable&lt;EntityB&gt;, IEnumerable&lt;EntityA&gt;&gt;&gt; expa = 
(mvs, fts) =&gt; mvs.Join(fts, mv=&gt; mv.ID, f =&gt; f.ID, (mv1, fts1) =&gt; new { FTS=fts1, MV=mv1})
.Where(fts1 =&gt; fts1.FTS.Title.Contains("foo") &amp;&amp; fts1.FTS.Description.Contains("foo")).Select(a =&gt; a.MV); 
</code></pre>

