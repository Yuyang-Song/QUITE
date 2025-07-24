# LINQ group by in Entity Framework Core 3.1
[Link to question](https://stackoverflow.com/questions/60002713/linq-group-by-in-entity-framework-core-3-1)
**Creation Date:** 1580468860
**Score:** 7
**Tags:** c#, asp.net-core, .net-core, entity-framework-core, ef-core-3.1
## Question Body
<p>I have a database table to connect data between user and clients.</p>

<pre><code>db: class UserClientCorporate{
 int UserId; 
 User User;
 int ClientCorporateId;
 ClientCorporate ClientCorporate;
}
</code></pre>

<p>I want to query to get list of <code>ClientCorporates</code> grouped by <code>userid</code>. I have follow some example on Stack Overflow like <a href="https://stackoverflow.com/questions/7325278/group-by-in-linq">Group by in LINQ</a></p>

<p>and here is my query:</p>

<pre><code>var data3 = from db in _context.UserClientCorporate
            group db.ClientCorporateId by db.UserId into g
            select new { UserId = g.Key, Clients = g.ToList() };

return Ok(await data3.ToListAsync());
</code></pre>

<p>When I run this, I got error:</p>

<blockquote>
  <p>fail: Microsoft.AspNetCore.Server.Kestrel[13]
        Connection id "0HLT67LJQA4IP", Request id "0HLT67LJQA4IP:0000000F": An unhandled exception was thrown by the
  application. System.InvalidOperationException: The LINQ expression
  'ToList(GroupByShaperExpression: KeySelector: u.UserId,
  ElementSelector:ProjectionBindingExpression: EmptyProjectionMember )'
  could not be translated. Either rewrite the query in a form that can
  be translated, or switch to client evaluation explicitly by inserting
  a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or
  ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
  more information.</p>
</blockquote>

<p>How to solve this problem?</p>

<p>SOLVED !
After I did more research it seems EF Core has limitation doing this query on  database server. so I need to get the data first and processed it on my dotnet server (client). </p>

<p>Here is the </p>

<pre><code>var data = await _context.UserClientCorporate.Include(x =&gt; x.User).Include( x =&gt; x.ClientCorporate).
var res2 = from db in data 
            group db by db.UserId into g
            select new {UserId = g.Key, Clients = g};
</code></pre>

## Answers
### Answer ID: 65716739
<p>Client side GroupBy is not supported in .netcore 3.1</p>
<p>You may write your query as simple as this:</p>
<pre><code>var data3 = __context.UserClientCorporate.ToList().GroupBy(x =&gt; x.UserId);
</code></pre>
<p>Code writter in C# is client side.</p>

### Answer ID: 60002995
<p>Delete this <strong>.ToList()</strong>:</p>

<pre><code>var data3 = from db in _context.UserClientCorporate
            group db.ClientCorporateId by db.UserId into g
            select new { UserId = g.Key, Clients = g };

return Ok(await data3.ToListAsync());
</code></pre>

