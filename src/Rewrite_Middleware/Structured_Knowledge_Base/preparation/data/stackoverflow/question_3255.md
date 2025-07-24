# Adding all expressions inside the loop as OR condition to the IQueryable object C#
[Link to question](https://stackoverflow.com/questions/73826143/adding-all-expressions-inside-the-loop-as-or-condition-to-the-iqueryable-object)
**Creation Date:** 1663927701
**Score:** 1
**Tags:** c#, linq, expression
## Question Body
<p>Adding all expressions inside the loop as OR condition to the IQueryable object</p>
<p>I have a database table and I want to check whether there is a name within the keywords given by the user from the names in the table.</p>
<p>For example;
Database table name: Users
Column names: Id, Name
The data inside is: (Id:1, Name:Tom), (Id:2, Name: John), (Id:3, Name: Harry)</p>
<p>And the keywords from the user: &quot;to&quot; and &quot;harr&quot;
Values ​​that should return: Tom and Harry</p>
<p>The code I tried:</p>
<pre><code>var queryableUsers = db.Users.AsQueryable();
queryableUsers = queryableUsers .Where(x =&gt; values.Any(v =&gt; x.Name.ToLower().Contains(v)));
</code></pre>
<p>But here I am getting error:</p>
<blockquote>
<p>.Name.ToLower().Contains(v)' could not be translated. Either rewrite
the query in a form that can be translated, or switch to client
evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>Here is what I want to do:</p>
<pre><code>Expression&lt;Func&lt;User, bool&gt;&gt; predicate = (User) =&gt; false;
foreach(var v in values)
    predicate = predicate.Or(x =&gt; x.Name.Contains(term));
</code></pre>
<p>But Or is not working. How do I make this possible in c#?</p>

