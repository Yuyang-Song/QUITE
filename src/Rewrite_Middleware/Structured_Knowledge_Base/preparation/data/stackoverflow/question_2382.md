# Add related database entry in Azure Mobile Services controller
[Link to question](https://stackoverflow.com/questions/32181294/add-related-database-entry-in-azure-mobile-services-controller)
**Creation Date:** 1440416004
**Score:** 3
**Tags:** entity-framework, azure-mobile-services
## Question Body
<p>In my Azure Mobile Service I have a controller class <code>UserController : TableController&lt;User&gt;</code> and in it is a get method:</p>

<pre class="lang-cs prettyprint-override"><code>// GET tables/User/48D68C86-6EA6-4C25-AA33-223FC9A27959
public SingleResult&lt;User&gt; GetUser(string id)
{
    return Lookup(id);
}
</code></pre>

<p>I want to record each time a user is accessed and so I add a simple type to the model:</p>

<pre class="lang-cs prettyprint-override"><code>public class UserVisit : Microsoft.WindowsAzure.Mobile.Service.EntityData
{
    public string VisitingUser { get; set; }
    public DateTime TimeOfVisit { get; set; }
}
</code></pre>

<p>and include the property <code>public DbSet&lt;UserVisit&gt; UserVisits { get; set; }</code> in my <code>VCollectAPIContext : DbContext</code> class (and update the database with a code-first migration).</p>

<p>To add a UserVisit to the database when a user id is queried I change my controller method to</p>

<pre class="lang-cs prettyprint-override"><code>// GET tables/User/48D68C86-6EA6-4C25-AA33-223FC9A27959
public async Task&lt;SingleResult&lt;User&gt;&gt; GetUser(string id)
{
    var userVisit = new UserVisit { VisitingUser = id, TimeOfVisit = DateTime.UtcNow };
    context.UserVisits.Add(userVisit);
    await context.SaveChangesAsync();
    return Lookup(id);
}
</code></pre>

<p>But the <code>SaveChangesAsync</code> fails with a <code>System.Data.Entity.Validation.DbEntityValidationException</code>. Digging around in the exception's <code>EntityValidationErrors</code> property I find that the problem is "The Id field is required."</p>

<p>That's a little odd. The Id field is one of the properties in the base-class <code>Microsoft.WindowsAzure.Mobile.Service.EntityData</code> that I would expect to be added automatically on insert. No matter, I can add it and several of the other base-class's properties thus:</p>

<pre class="lang-cs prettyprint-override"><code>// GET tables/User/48D68C86-6EA6-4C25-AA33-223FC9A27959
public async Task&lt;SingleResult&lt;User&gt;&gt; GetUser(string id)
{
    var userVisit = new UserVisit { Id = Guid.NewGuid().ToString(), Deleted = false, VisitingUser = id, TimeOfVisit = DateTime.UtcNow, CreatedAt = DateTimeOffset.Now };
    context.UserVisits.Add(userVisit);
    await context.SaveChangesAsync();
    return Lookup(id);
}
</code></pre>

<p>This time I get a <code>System.Data.Entity.Infrastructure.DbUpdateException</code> because we "Cannot insert the value NULL into column 'CreatedAt'". It was not null in the call to <code>Add</code>. So <code>CreatedAt</code> has been set to null somewhere outside my code and then the insert fails as a result! </p>

<p>I also tried setting up an <code>EntityDomainManager&lt;UserVisit&gt; userVisitDomainManager;</code> instance variable in the controller's initializer, and then rewriting my controller get method as</p>

<pre class="lang-cs prettyprint-override"><code>// GET tables/User/48D68C86-6EA6-4C25-AA33-223FC9A27959
public async Task&lt;SingleResult&lt;User&gt;&gt; GetUser(string id)
{
    var userVisit = new UserVisit { VisitingUser = id, TimeOfVisit = DateTime.UtcNow };
    await userVisitDomainManager.InsertAsync(userVisit);
    return Lookup(id);
}
</code></pre>

<p>That fails with the same message, "Cannot insert the value NULL into column 'CreatedAt'"</p>

<p>How should I perform the seemingly simple task of inserting a related data item within my controller method?</p>

## Answers
### Answer ID: 32467380
<p>To fix the problem of "<strong>The Id field is required</strong>" following <strong><a href="https://stackoverflow.com/a/32332740/2476450">brettsam</a></strong>'s instructions.</p>

<p>Add this in your model:</p>

<pre class="lang-cs prettyprint-override"><code>[Key]
[DatabaseGenerated(DatabaseGeneratedOption.Identity)]
[TableColumn(TableColumnType.Id)]
public new string Id { get; set; }
</code></pre>

<p>It will auto generate a GUID when you add an entity.</p>

### Answer ID: 32332740
<p>The solution is likely similar to <a href="https://stackoverflow.com/a/32214696/3516125">this answer</a>. I'm guessing that your migration is not using the Mobile Services SqlGenerator so some of the custom SQL settings aren't getting applied. What that means is that:</p>

<ul>
<li>Id doesn't get a default value of NEWID() -- this explains your "Id field is required" error.</li>
<li>CreatedAt doesn't get a default value of SYSUTCDATETIME() -- this, combined with the [DatabaseGenerated] attribute on EntityData.CreatedAt, explains the "NULL CreatedAt" error.</li>
</ul>

<p>Try updating your migration according to the link above and see if that works for you.</p>

