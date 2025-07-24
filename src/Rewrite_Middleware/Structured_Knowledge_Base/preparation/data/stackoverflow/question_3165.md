# Entity Framework problem with reducing projection
[Link to question](https://stackoverflow.com/questions/69673521/entity-framework-problem-with-reducing-projection)
**Creation Date:** 1634890445
**Score:** 0
**Tags:** sql, sql-server, entity-framework, entity-framework-5
## Question Body
<p>I've been working on improving performance for our .NET core API with EF 5.0.11 by reducing the projection of our queries, but I'm currently stuck with the following scenario:</p>
<p>I improved the projection of the queries like this:</p>
<pre><code>var employeeEmailQuery = context.Employee
                .Where(e =&gt; e.Active == true)
                .Select(e =&gt; new EmployeeEmailView
                {
                    Name = e.FullName,
                    Email = e.Email
                });
</code></pre>
<p>This reduces the select query to just the two columns I need instead of a SELECT * on 80+ columns in the database.</p>
<p>In my database, I also have columns with translated descriptions. It looks like this:
<a href="https://i.sstatic.net/RqzXk.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/RqzXk.png" alt="enter image description here" /></a></p>
<p>What I would like to do is select the relevant translated description, based on the current culture, so I added the following code:</p>
<pre><code> var culture = CultureInfo.DefaultThreadCurrentUICulture;
 var employeeEmailQuery = context.Employee
            .Where(e =&gt; e.Active == true)
            .Select(e =&gt; new EmployeeEmailView
            {
                Name = e.FullName,
                Email = e.Email,
                this.SetDescription(e, culture);
            });
</code></pre>
<p>The SetDescription method checks the culture and picks the correct column to set a Description property in the EmployeeEmailView. However, by adding this code, the query is now once again doing a SELECT *, which I don't want.</p>
<p>Does anybody have an idea on how to dynamically include a select column using EF without rewriting everything into raw SQL?</p>
<p>Thanks in advance.</p>

## Answers
### Answer ID: 69678542
<p>I think the only way is to use an <a href="https://learn.microsoft.com/en-us/ef/core/logging-events-diagnostics/interceptors" rel="nofollow noreferrer">Interceptor</a> to modify the query, or dynamically generate the EF IQueryable with Expressions.</p>

