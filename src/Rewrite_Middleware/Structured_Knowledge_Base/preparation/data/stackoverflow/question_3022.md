# Filtering by an untranslatable method using EF Core 3.1
[Link to question](https://stackoverflow.com/questions/62632760/filtering-by-an-untranslatable-method-using-ef-core-3-1)
**Creation Date:** 1593413811
**Score:** 1
**Tags:** c#, sql-server, .net-core, ef-core-3.1
## Question Body
<p>In a web application with a SQL Server database, I have implemented the data access layer using the &quot;Repository Pattern&quot;. For filtering a <code>User</code> based on its email, I'm using an expression like this:</p>
<pre><code>var emailFilter = &quot;user@example.com&quot;;
var query = _dbContext.Set&lt;User&gt;().Where(x =&gt; x.Email.Normalize() == emailFilter.Normalize());
var result = query.ToListAsync(); 
</code></pre>
<p>But EF Core throws an exception which says:</p>
<blockquote>
<p>... could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync()</p>
</blockquote>
<p>I have more than 200k users in the users' table and I don't want to filter data on the client-side.</p>
<p><strong>The mentioned code is only an example but I mean other use cases with more complex methods.</strong></p>
<p>Now, how can I use complex functions to filter data on the server-side?</p>

## Answers
### Answer ID: 62635161
<p>For non standard go with plain sql queries...</p>
<pre><code>var emailFilter = &quot;user@example.com&quot;;
var result = await _dbContext.Users.FromSqlRaw($&quot;SELECT * FROM dbo.Users WHERE LOWER(Email) = {emailFilter}&quot;).ToListAsync(); 
</code></pre>
<p>Or use Functions</p>
<pre><code>var emailFilter = &quot;user@example.com&quot;;
var result = await _dbContext.Users.Where(x =&gt; EF.Functions.Like(x.Email, $&quot;%{emailFilter}%&quot;)).ToListAsync(); 
</code></pre>
<p>With the penalty of the performance...</p>

### Answer ID: 62633022
<p>I suggest to you, first normalize your email in db by bulk update :</p>
<p>by <a href="https://www.nuget.org/packages/Z.EntityFramework.Plus.EFCore/" rel="nofollow noreferrer">Z.EntityFramework.Plus.EFCore</a></p>
<pre><code>_dbContext.Set&lt;User&gt;().update(x =&gt; new User {Email =  x.Email.Normalize()}  ;
</code></pre>
<p>then</p>
<pre><code>emailFilter = (&quot;user@example.com&quot;).Normalize();
var query = _dbContext.Set&lt;User&gt;().Where(x =&gt; x.Email  == emailFilter);
var result = query.ToListAsync(); 
</code></pre>
<blockquote>
<p>it's an instance solution</p>
</blockquote>

