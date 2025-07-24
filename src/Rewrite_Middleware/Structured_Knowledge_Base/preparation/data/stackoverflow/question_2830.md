# LINQ conditional query where value might be null
[Link to question](https://stackoverflow.com/questions/54476125/linq-conditional-query-where-value-might-be-null)
**Creation Date:** 1549011880
**Score:** 1
**Tags:** c#, .net, entity-framework, linq
## Question Body
<p>I'm trying to write a query to select data from database. I have the following code : </p>

<pre><code> from notes in ctx.Notes
 .Where(x =&gt; x.UserId== user.UserId 
 || x.UserId == user.FamilyId 
 || x.UserId == user.CompanyId).DefaultIfEmpty()
</code></pre>

<p>The problem with this is that the FamilyId and CompanyId are both nullable types and may not have any value at all which corrupts the whole query. How can I rewrite it so it only looks for FamilyId/CompanyId if they have values? </p>

## Answers
### Answer ID: 54476507
<p>Simple, just add an AND clause to check if it's not null:</p>

<pre><code> from notes in ctx.Notes.Where(x =&gt; x.UserId== user.UserId || (user.FamilyId ! =null &amp;&amp; x.UserId == user.FamilyId) || (user.CompanyId !=null &amp;&amp; x.UserId == user.CompanyId)).DefaultIfEmpty()
</code></pre>

### Answer ID: 54476197
<p>Create condition query:</p>

<pre><code>var users = ctx.Notes.Where(x =&gt; x.UserId == user.UserId);

if (user.FamilyId != null)
{
    users = users.Union(ctx.Notes.Where(x =&gt; x.UserId == user.FamilyId));
}

if (user.CompanyId != null)
{
    users = users.Union(ctx.Notes.Where(x =&gt; x.UserId == user.CompanyId ));
}

var result = users.ToArray();
</code></pre>

