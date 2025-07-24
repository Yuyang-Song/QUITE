# EF Core 6 - when using Contains in the where clause causes an error &quot;could not be translated&quot;
[Link to question](https://stackoverflow.com/questions/72250003/ef-core-6-when-using-contains-in-the-where-clause-causes-an-error-could-not-b)
**Creation Date:** 1652630982
**Score:** 1
**Tags:** entity-framework, linq, entity-framework-core
## Question Body
<p>I am migrating from EF Core 2.1 to EF Core 6.</p>
<p>I have the following code:</p>
<pre><code>var currentCars = _context.Cars
                          .Include(x =&gt; x.Model)
                          .Where(x =&gt; currentModels.Contains(x.ModelId))
                          .ToList();
</code></pre>
<p><code>Cars</code> have a <code>ModelId</code>(long) that relates to a <code>Model</code> type.</p>
<p><code>CurrentModels</code> is a <code>List&lt;long&gt;</code>, being the current model type Ids we are interested in.</p>
<blockquote>
<p>The LINQ expression 'EnumerableQuery { 1 }<br />
.Contains(NavigationTreeExpression<br />
Value: EntityReference: AssetSP | IncludePaths:<br />
Root<br />
-&gt; Model<br />
Expression: a.ModelId)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I can't work out how to do the query on the database. I do not want to bring all the Cars back to the server to filter there.</p>
<p>In SQL it would be something like.</p>
<pre><code>Select * 
From Cars 
Where ModelId in (-- ids here --)
</code></pre>

