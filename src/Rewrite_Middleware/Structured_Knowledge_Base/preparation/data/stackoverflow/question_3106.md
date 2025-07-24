# .NET Core runtime error: LINQ expression could not be translated
[Link to question](https://stackoverflow.com/questions/66809226/net-core-runtime-error-linq-expression-could-not-be-translated)
**Creation Date:** 1616717020
**Score:** -1
**Tags:** c#, entity-framework, linq
## Question Body
<p>I have encountered this issue a lot recently. I have also found several posts on Stack Overflow about it, but none really managed to answer the root question of what is causing this error and how to fix it.</p>
<p>It's quite frustrating. I create a LINQ query in Visual Studio. It works perfectly when I test it in LINQ Pad. It compiles with no errors. But during runtime, it crashes with the following error:</p>
<blockquote>
<p>System.InvalidOperationException: 'The LINQ expression [...] could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>
<p>The error indicates that you can solve the issue by using <code>.AsEnumerable()</code> or <code>.ToList()</code> when performing your query.
The problem is, <em>almost every LINQ Query I build uses</em> <code>.ToList()</code> or <code>.ToListAsync()</code>!</p>
<p>I know there are performance concerns regarding client evaluation. But performing complex queries with multiple layers of logic spanning several database tables is what LINQ is best at. Crashing for a reason that doesn't explain the problem makes development of complex systems that much harder.</p>
<p>Has anyone else found this to be a recurring problem? Does anyone know what the cause is and what, if anything, the solution is?</p>
<p>Or am I just missing something?</p>
<p>Here is my issue that I had with this: <a href="https://stackoverflow.com/questions/66808898/net-core-3-1-linq-expression-from-could-not-be-translated-for-lists-within-a-li">.NET Core 3.1 LINQ expression from could not be translated for lists within a list</a></p>

## Answers
### Answer ID: 66810197
<p>There is no group join in entity framework as this is something that just has no 1 to 1 equivalent in sql. You have a couple options here you could select results with group by then join the same table on the results.. or we could use a little memory to do some work wrote this off the cuff so difficult to say if it will run as is but something like this</p>
<hr />
<pre><code>var posts =
  (await (from x in _context.UserPosting
          where PostedByList.Contains(x.Posting.PostingId)
          &amp;&amp; x.Approved == &quot;A&quot;
          &amp;&amp; x.User.Active == true
          select new
          {
              FirstName = x.User.FirstName,
              LastName = x.User.LastName,
              UserEmail = x.User.UserId,
          }).ToListAsync()) // Force enumeration.. aka run query
  // Group here once results are in memory
  .GroupBy( e =&gt; new { FirstName = e.User.FirstName, LastName = x.User.LastName, UserId = x.User.UserId }, 
    new { FirstName = e.User.FirstName, LastName = x.User.LastName, UserId = x.User.UserId })
  .Select(e =&gt; new UserPostDTO
  {
    FirstName = e.Key.FirstName,
    LastName = e.Key.LastName,
    UserId = e.Key.UserId,
    PostsByUser = e.ToList()
  });
</code></pre>

