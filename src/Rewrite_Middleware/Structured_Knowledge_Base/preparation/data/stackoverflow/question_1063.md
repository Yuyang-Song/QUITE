# Creating a Second -- and Even Third -- DbContext
[Link to question](https://stackoverflow.com/questions/57193076/creating-a-second-and-even-third-dbcontext)
**Creation Date:** 1564017840
**Score:** 0
**Tags:** entity-framework-core
## Question Body
<p>I have a project that is using EFCore.  In my controller, I have a DbContext that is being passed in through DI (I.e. In my ConfigureServices in Startup.cs I am calling services.AddDbContext(...)).</p>

<p>It's pretty simple.  However, in my controller I'm making three calls to the database to create a SINGLE object.  Unfortunately, it's not done through a LINQ join.  Here's a small example...</p>

<pre><code>var user = this.Context.Users.FirstOrDefault(...);
var room = this.Context.Rooms.FirstOrDefault(...);
var util = this.Context.Utilities.FirstOrDefault(...);

return new
{
  User = user,
  Room = room,
  Util = util
};
</code></pre>

<p>Granted, it's not that simple, but you get the idea; I had THREE different DB calls running synchronously under ONE DbContext.  However, the calls are all independent, so I thought I could expedite the process, and I used Task.WaitAll(...).</p>

<pre><code>var user = this.Context.Users.FirstOrDefaultAsync(...);
var room = this.Context.Rooms.FirstOrDefaultAsync(...);
var util = this.Context.Utilities.FirstOrDefaultAsync(...);

Task.WaitAll(user, room, util);

return new
{
  User = user.Result,
  Room = room.Result,
  Util = util.Result
};
</code></pre>

<p>This is what's getting me into trouble.  I'm getting the error:</p>

<blockquote>
  <p>A second operation started on this context before a previous operation completed. This is usually caused by different threads using the same instance of DbContext, however instance members are not guaranteed to be thread safe. This could also be caused by a nested query being evaluated on the client, if this is the case rewrite the query avoiding nested invocations.</p>
</blockquote>

<p>I realize the context is being run on multiple threads, but how do I accomplish expediting the three queries?  In my scenario, I'm using DI, so only ONE instance of my DbContext was created and injected.  Additionally, it looks sloppy creating multiple instances of a DbContext especially if I'm already using DI.  Suggestions and recommendations are greatly appreciated.  Maybe creating those localized instances of the DbContext is the only way?</p>

## Answers
### Answer ID: 57301236
<p>If there is no relation between the tables, then you can't do that with Entity Framework.</p>

<p>What you can do instead -if you're insistent on reducing the number of database round trips, and you're okay with introducing additional dependencies in your project- is to use <a href="https://github.com/StackExchange/Dapper#multiple-results" rel="nofollow noreferrer">Dapper</a>, it provides a <code>QueryMultiple</code> API that returns multiple results in a single round trip.</p>

