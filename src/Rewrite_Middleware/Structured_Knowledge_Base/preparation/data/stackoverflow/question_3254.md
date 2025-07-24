# Entity Framework query using TimeZoneInfo cannot be translated to SQL Server query
[Link to question](https://stackoverflow.com/questions/73756646/entity-framework-query-using-timezoneinfo-cannot-be-translated-to-sql-server-que)
**Creation Date:** 1663432438
**Score:** 1
**Tags:** c#, sql-server, entity-framework-core, timezone
## Question Body
<p>I am working with time zones in my .NET application. I followed the best practices regarding time zones according to Microsoft (link below):</p>
<p><a href="https://learn.microsoft.com/en-us/previous-versions/dotnet/articles/ms973825(v=msdn.10)" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/previous-versions/dotnet/articles/ms973825(v=msdn.10)</a></p>
<p>Here you can read that the best option is to store the time zone in the database with the time in that time zone and perform calculations transforming it to UTC. I was trying to filter the records based on the date using the following piece of code:</p>
<pre><code>var result = ContextClassObject.Entity
                               .Where(e =&gt; TimeZoneInfo.ConvertTimeToUtc(e.Date) &gt; DateTime.UtcNow)
                               .ToList();
</code></pre>
<p>I get the following error message:</p>
<blockquote>
<p>System.InvalidOperationException: „The LINQ expression 'DbSet()
.Where(a =&gt; TimeZoneInfo.ConvertTimeToUtc(a.Date) &gt; DateTime.UtcNow)' could not be translated. Additional information:
Translation of method 'System.TimeZoneInfo.ConvertTimeToUtc' failed. If this method can be mapped to your custom function, see <a href="https://go.microsoft.com/fwlink/?linkid=2132413" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2132413</a> for more information. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'</p>
</blockquote>
<p>I think it means that my query cannot be translated to a SQL query so I have to tell it directly how to translate it or materialize the data and then filter it in C#, which I don't want to do because it's gonna be slower than SQL Server could do it and premature materialization isn't a good thing to do.</p>
<p>Is there a way to make it work without mapping the function to a SQL query directly which would be quite complicated for a simple operation? Should I just store any DateTime in UTC, which is supposed to be a good method too and save myself the trouble?</p>
<p>Below is the example row of a database. The date is in the time zone, which id is stored right next to it:</p>
<p><a href="https://i.sstatic.net/eLcZb.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/eLcZb.png" alt="Example of a row in the database" /></a></p>
<p>I have tried storing it with DateTimeOffset like that:</p>
<p><a href="https://i.sstatic.net/gtonZ.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/gtonZ.png" alt="enter image description here" /></a></p>
<p>Then the query below produces the same error:</p>
<pre><code>TimeZoneInfo userTimeZone = TimeZoneInfo.FindSystemTimeZoneById(&quot;Alaskan Standard Time&quot;);
            DateTime userDate = new DateTime(2022, 09, 27, 11, 58, 12);
            DateTime dateInUTC = TimeZoneInfo.ConvertTimeToUtc(userDate, userTimeZone);

            var result = await _dataContext.DateEntity
                .Where(e =&gt; e.Date.Add(e.Date.Offset) &gt; dateInUTC)
                .ToListAsync();
</code></pre>
<p>I have tried different methods to add or subtract the offset and found out that only accessing the Offset property of the DateTimeOffset class cannot be translated. Using raw numbers works just fine.</p>

