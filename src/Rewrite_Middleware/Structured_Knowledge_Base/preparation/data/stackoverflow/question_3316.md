# EF Core 6 - Server evaluation based on client sided list of objects
[Link to question](https://stackoverflow.com/questions/75993372/ef-core-6-server-evaluation-based-on-client-sided-list-of-objects)
**Creation Date:** 1681287845
**Score:** 0
**Tags:** c#, sql-server, entity-framework-core, ef-core-6.0
## Question Body
<p>In my ASP.NET Core web application, I have a client sided list of <code>Roles</code> objects. Each of those objects contains three string properties and a string list containing the role names. I need to query entities of type <code>Notification</code> from a SQL Server database using EF Core and filter based on those roles. To do this, I need to check if the list contains any single object where the three properties match the three column values of the entity in the database. Additionally, the string list also needs to contain a string which matches the value of the <code>SendToRole</code> column in the database. To make this more clear, here is how I attempted to do this:</p>
<pre><code>public async Task&lt;List&lt;Notification&gt;&gt; GetNotificationsForUser(List&lt;Roles&gt; roles)
{
    return await Context.Notifications
        .Where(x =&gt; roles.Any(r =&gt;
            r.Property1 == x.Property1 &amp;&amp;
            r.Property2 == x.Property2 &amp;&amp;
            r.Property3 == x.Property3 &amp;&amp;
            r.Roles.Any(r =&gt; r == x.SendToRole)))
        .ToListAsync();
}
</code></pre>
<p>My problem is that this LINQ expression cannot be translated into SQL and throws the following exception:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'System.InvalidOperationException: The LINQ expression 'r =&gt; r.Property1 == EntityShaperExpression:
.Notification
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.Property1 &amp;&amp; r.Property2 == EntityShaperExpression:
.Notification
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.Property2 &amp;&amp; r.Property3 == EntityShaperExpression:
.Notification
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.Property3 &amp;&amp; r.Roles
.Any(r =&gt; r == EntityShaperExpression:
.Notification
ValueBufferExpression:
ProjectionBindingExpression: EmptyProjectionMember
IsNullable: False
.SendToRole)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.' could not
be translated. Either rewrite the query in a form that can be
translated, or switch to client evaluation explicitly by inserting a
call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or
'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for
more information.</p>
</blockquote>
<p>I know that I could solve this with client sided filtering, but I am concerned about the performance here because the number of notifications might get quite high in the database at some point and I do not want this code to become a bottleneck in the future.</p>
<p>How can I fix this query so it can be evaluated on the server (database) side?</p>

