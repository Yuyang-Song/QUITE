# Where to fetch user entity when users are stored in Active Directory?
[Link to question](https://stackoverflow.com/questions/76565014/where-to-fetch-user-entity-when-users-are-stored-in-active-directory)
**Creation Date:** 1687869992
**Score:** 0
**Tags:** asp.net-core, entity-framework-core, blazor, automapper
## Question Body
<p>Sometimes we have entities in the domain layer that are linked to users.</p>
<p>For instance:</p>
<pre><code>class SomeEntity
{
    public User User { get; set; }
}
</code></pre>
<p>A user might look like the following:</p>
<pre><code>class User
{
    public Guid Id { get; set; }
    public string DisplayName { get; set; }
}
</code></pre>
<p>Now we want to store entities of type <code>SomeEntity</code> in our own database, but users should be stored in Active Directory.</p>
<p>To support this, we modify our <code>SomeEntity</code> class to look like this:</p>
<pre><code>class SomeEntity
{
    public Guid UserId { get; set; }

    [NotMapped]
    public User User { get; set; }
}
</code></pre>
<p>When we fetch entities of type <code>SomeEntity</code>, we can complement this with users from active directory to get the full domain model.</p>
<p>For instance:</p>
<pre><code>SomeEntity entity = await _dbContext.SomeEntities.FindAsync(id);
User user = await _identityService.GetUserById(entity.UserId);
entity.User = user;
</code></pre>
<p>This should work, but when we have many different queries that fetch (subsets of) <code>SomeEntity</code>, we are going to rewrite the same fetching logic over and over again. When <code>SomeEntity</code> is an object that is nested within other objects, the fetching logic becomes even worse.</p>
<p>Is there any way we can make sure that when <code>SomeEntity</code> is fetched, we always also fetch <code>User</code>?</p>
<hr />
<p>Some other things I've tried or seen online, that didn't fully solve the problem:</p>
<ul>
<li>Give <code>User</code> a getter that fetches that user once the property is used (This adds fetching logic to our domain model, which violates clean architecture principles). <a href="https://stackoverflow.com/questions/24420581/how-to-store-active-directory-user-guid-using-entity-framework">Example</a>.</li>
<li>Only including the <code>UserId</code> in the domain model and fetching the User once it's needed. (we'll have to rewrite logic, becomes especially difficult once objects are nested.)</li>
<li>Doing the fetching with Entity Framework or Automapper. Seems dirty. Might work. Also asked <a href="https://stackoverflow.com/questions/72001885/relationships-in-entity-framework-with-users-from-azuread">here</a> but didn't receive answers.</li>
</ul>
<p>Technologies used:</p>
<ul>
<li>ASP.NET Core</li>
<li>Blazor</li>
<li>Entity Framework</li>
<li>Automapper</li>
</ul>

## Answers
### Answer ID: 76593799
<p>It seems like <code>SomeEntity</code> is a ef core model. While <code>User</code> is not. And it seems you have no plans to store the information of <code>User</code> in the Database maybe except the Identifier. So I would take your second option:</p>
<blockquote>
<p>Only including the UserId in the domain model and fetching the User
once it's needed. (we'll have to rewrite logic, becomes especially
difficult once objects are nested.)</p>
</blockquote>
<p>Don't try to force the models into the design if it simply doesn't make sence.
The design should be based on the requirements and not vice versa.</p>
<p>The alternative option would be to store the User data in the DB and treat it like a database entity. But you would have to handle a sync/refresh between what is in your DB and what is in the AD if someone marry's or leaves for example.</p>

