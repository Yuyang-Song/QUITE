# Entity Framework Core : filter by 3 fields
[Link to question](https://stackoverflow.com/questions/78991746/entity-framework-core-filter-by-3-fields)
**Creation Date:** 1726519677
**Score:** 0
**Tags:** c#, entity-framework-core
## Question Body
<p>I'm trying to query some subscriptions from the database using Entity Framework Core. A subscription is equal to another subscription if the <code>userId</code>, the <code>NotificationType</code> and the <code>Channel</code> match.</p>
<p>I'm attempting it like this:</p>
<pre><code>// Create a list of anonymous objects that combine the three fields for comparison
var subscriptionKeys = subscriptions
    .Select(s =&gt; new { s.UserId, s.NotificationType, s.Channel })
    .ToList();
       
// Fetch all existing subscriptions where the combination of UserId,  NotificationType, and Channel match
var existingSubscriptions = await this.context.Subscriptions
    .Where(s =&gt; subscriptionKeys.Contains(new { s.UserId, s.NotificationType, s.Channel })).ToListAsync();
</code></pre>
<p>But I'm getting this exception:</p>
<blockquote>
<p>System.InvalidOperationException   HResult=0x80131509   Message=The LINQ expression '__subscriptionKeys_0<br />
.Contains(new {<br />
UserId = StructuralTypeShaperExpression:<br />
Micro.NotificationService.Models.Subscription<br />
ValueBufferExpression:<br />
ProjectionBindingExpression: EmptyProjectionMember<br />
IsNullable: False<br />
.UserId,<br />
NotificationType = StructuralTypeShaperExpression:<br />
Micro.NotificationService.Models.Subscription<br />
ValueBufferExpression:<br />
ProjectionBindingExpression: EmptyProjectionMember<br />
IsNullable: False<br />
.NotificationType,<br />
Channel = StructuralTypeShaperExpression:<br />
Micro.NotificationService.Models.Subscription<br />
ValueBufferExpression:<br />
ProjectionBindingExpression: EmptyProjectionMember<br />
IsNullable: False<br />
.Channel<br />
})' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
<p>Source=Microsoft.EntityFrameworkCore</p>
<p>StackTrace:<br />
at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)</p>
</blockquote>
<p>How can I do this type of query? Btw the subscriptions enumerable and the <code>DbSet</code> <code>Subscriptions</code> are not the same type of entity. One is a message the other one the actual entity saved in the database.</p>
<p>Could I do something like mapping one to the other one and just use <code>Contains</code>?</p>

## Answers
### Answer ID: 78991865
<p>As I tested, you are only left with <a href="https://learn.microsoft.com/pl-pl/dotnet/api/microsoft.entityframeworkcore.relationalqueryableextensions.fromsqlraw?view=efcore-8.0" rel="nofollow noreferrer"><code>FromSqlRaw</code></a>:</p>
<pre class="lang-cs prettyprint-override"><code>var whereClause = string.Join(
    &quot; OR &quot;,
    subscriptions.Select(s =&gt; $&quot;(UserId={s.UserId} AND NotificationType='{s.NotificationType}' AND Channel='{s.Channel}')&quot;));

// Fetch all existing subscriptions where the combination of UserId, NotificationType, and Channel match
var existingSubscriptions = await this.context.Subscriptions
    .FromSqlRaw(&quot; SELECT * FROM Subscriptions WHERE &quot; + whereClause)
    .ToListAsync();
</code></pre>
<p>Of course, be mindful of <a href="https://en.wikipedia.org/wiki/SQL_injection" rel="nofollow noreferrer">SQL injection</a> and sanitize your string appropriately.</p>

