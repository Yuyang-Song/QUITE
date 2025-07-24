# Overriding GetRolesAsync
[Link to question](https://stackoverflow.com/questions/60653829/overriding-getrolesasync)
**Creation Date:** 1584014798
**Score:** 1
**Tags:** c#, asp.net-core, async-await
## Question Body
<p>What I'd like to do is</p>

<pre><code>public override Task&lt;IList&lt;string&gt;&gt; GetRolesAsync(ApplicationUser user, CancellationToken cancellationToken = default)
{
    return Context.UserOrganisationRole
        .Where(z =&gt; z.UserId == user.Id)
        .GroupBy(z =&gt; new { z.RoleId, z.Role })
        .Select(z =&gt; z.Key.Role.Name + "-" + string.Join(",", z.OrderBy(z =&gt; z.OrganisationId).Select(z =&gt; z.OrganisationId)))
        .ToListAsync();
}
</code></pre>

<p>But that doesn't work because <code>Task&lt;List&lt;string&gt;&gt;</code> can't be cast to <code>Task&lt;IList&lt;string&gt;&gt;</code>.</p>

<p>Therefore I tried adding</p>

<pre><code>.ContinueWith&lt;IList&lt;string&gt;&gt;(t =&gt; t.Result, TaskContinuationOptions.ExecuteSynchronously);
</code></pre>

<p>from <a href="https://stackoverflow.com/questions/20950908/type-conversion-error-with-async-programming">Type conversion error with async programming</a>
which compiles but doesn't run because:</p>

<blockquote>
  <p>The LINQ expression &lt;...> could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(),...</p>
</blockquote>

<p>Which I think means it's trying to do too much on the database. Fine. However, having added the requested <code>IEnumerable</code> it now appears to be impossible to get the required <code>Task&lt;IList&lt;string&gt;&gt;</code> to return</p>

<pre><code>return Context.UserOrganisationRole
    .Where(z =&gt; z.UserId == user.Id)
    .AsEnumerable()
    .GroupBy(z =&gt; new { z.RoleId, z.Role })
    .Select(z =&gt; z.Key.Role.Name + "-" + string.Join(",", z.OrderBy(z =&gt; z.OrganisationId).Select(z =&gt; z.OrganisationId)))
</code></pre>

<p>I.e., write this for me!</p>

<pre><code>public Task&lt;IList&lt;string&gt;&gt; ListToTaskIList (IList&lt;string&gt; list)
{

}
</code></pre>

## Answers
### Answer ID: 60654174
<p>Just <code>await</code> the result of the query:</p>

<pre><code>public async override Task&lt;IList&lt;string&gt;&gt; GetRolesAsync(ApplicationUser user, CancellationToken cancellationToken = default)
{
    return await Context.UserOrganisationRole
        .Where(z =&gt; z.UserId == user.Id)
        .GroupBy(z =&gt; new { z.RoleId, z.Role })
        .Select(z =&gt; z.Key.Role.Name + "-" + string.Join(",", z.OrderBy(z =&gt; z.OrganisationId).Select(z =&gt; z.OrganisationId)))
        .ToListAsync();
}
</code></pre>

