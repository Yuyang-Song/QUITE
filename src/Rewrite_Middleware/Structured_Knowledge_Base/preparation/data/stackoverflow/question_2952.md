# LINQ statement is not translatable
[Link to question](https://stackoverflow.com/questions/59961674/linq-statement-is-not-translatable)
**Creation Date:** 1580279952
**Score:** 2
**Tags:** c#, linq, ef-core-3.1
## Question Body
<p>I have the following code containing LINQ statements:</p>

<pre><code>public async Task&lt;HashSet&lt;long&gt;&gt; GetMembersRecursive(IEnumerable&lt;long&gt; groupIds)
{
    var containsGroupId = InExpression&lt;Group&gt;("Id", groupIds);
    var containsParentId = InExpression&lt;RecursiveGroupModel&gt;("ParentId", groupIds);

    var groupIdsArray = groupIds as long[] ?? groupIds.ToArray();
    return new HashSet&lt;long&gt;(await MyContext
        .Groups
        .Where(containsGroupId)
        .Select(a =&gt; new
        {
            Members = MyContext
                .ViewWithRecursiveGroups
                .Where(containsParentId)
                .SelectMany(c =&gt; c.Group.Members)
                .Union(a.Members)
                .Where(b =&gt; !b.User.IsActive)
        })
        .SelectMany(a =&gt; a.Members.Select(b =&gt; b.MemberId))
        .Distinct()
        .ToListAsync());
}

private static Expression&lt;Func&lt;T, bool&gt;&gt; InExpression&lt;T&gt;(string propertyName, IEnumerable&lt;long&gt; array)
{
    var p = Expression.Parameter(typeof(T), "x");
    var contains = typeof(Enumerable).GetMethods(BindingFlags.Static | BindingFlags.Public)
        .Single(x =&gt; x.Name == "Contains" &amp;&amp; x.GetParameters().Length == 2)
        .MakeGenericMethod(typeof(long));
    var property = Expression.PropertyOrField(p, propertyName);
    var body = Expression.Call(
        contains
        , Expression.Constant(array)
        , property
    );

    return Expression.Lambda&lt;Func&lt;T, bool&gt;&gt;(body, p);
}
</code></pre>

<p>The error I receive is:</p>

<pre><code>Microsoft.EntityFrameworkCore: Processing of the LINQ expression 'DbSet&lt;RecursiveGroupModel&gt;
     .Where(b =&gt; __groupIdsArray_1
         .Contains(b.ParentId))
     .SelectMany(c =&gt; c.Group.GroupMembers)
     .Union((MaterializeCollectionNavigation(
         navigation: Navigation: Group.GroupMembers,
         subquery: (NavigationExpansionExpression
             Source: DbSet&lt;GroupMember&gt;
                 .Where(l0 =&gt; EF.Property&lt;Nullable&lt;long&gt;&gt;(l, "Id") != null &amp;&amp; EF.Property&lt;Nullable&lt;long&gt;&gt;(l, "Id") == EF.Property&lt;Nullable&lt;long&gt;&gt;(l0, "GroupId1"))
             PendingSelector: l0 =&gt; (NavigationTreeExpression
                 Value: (EntityReference: GroupMember)
                 Expression: l0)
         )
             .Where(i =&gt; EF.Property&lt;Nullable&lt;long&gt;&gt;((NavigationTreeExpression
                 Value: (EntityReference: Group)
                 Expression: l), "Id") != null &amp;&amp; EF.Property&lt;Nullable&lt;long&gt;&gt;((NavigationTreeExpression
                 Value: (EntityReference: Group)
                 Expression: l), "Id") == EF.Property&lt;Nullable&lt;long&gt;&gt;(i, "GroupId1"))))' by 'NavigationExpandingExpressionVisitor' failed. This may indicate either a bug or a limitation in EF Core. See https://go.microsoft.com/fwlink/?linkid=2101433 for more detailed information.
</code></pre>

<p>The view:</p>

<pre><code>CREATE VIEW [dbo].[View_WithRecursiveGroups] AS
     WITH RecursiveGroups (GroupId, ParentId) AS
    (
        SELECT Id, ParentId
        FROM Group
        WHERE ParentId IS NOT NULL
        UNION ALL
        SELECT Group.Id, t.ParentId
        FROM GroupTree t
        JOIN Group ON t.GroupId = Group.ParentId
    )

    SELECT * FROM RecursiveGroups
</code></pre>

<p>Apologies in advance if some variable names don't match up- I had to sanitize before posting.</p>

<p>I understand that it cannot convert code to SQL and so it's asking me to enumerate early or rewrite so that it's translatable. I have tired rearranging the query and breaking it up into smaller queries but the <code>SelectMany</code> on the recursive view seems to not be possible to convert to SQL.</p>

<p>Is there a way to get this working in-database? Or am I going about this completely the wrong way?</p>

## Answers
### Answer ID: 59962836
<p>give that if you want to convert this view to Linq...</p>

<hr>

<pre><code>CREATE VIEW [dbo].[View_WithRecursiveGroups] AS
     WITH RecursiveGroups (GroupId, ParentId) AS
    (
        SELECT Id, ParentId
        FROM Group
        WHERE ParentId IS NOT NULL
        UNION ALL
        SELECT Group.Id, t.ParentId
        FROM GroupTree t
        JOIN Group ON t.GroupId = Group.ParentId
    )
</code></pre>

<hr>

<pre><code>var data1 = db.Group.where(x=&gt;x.ParentId != nul)
            .Select(x=&gt;new {x.Id, x.ParentId})
            .Tolist()

var data2 = (from g in db.Groups
            join gt in db.GroupTree on g.ParentId equals gt.GroupId
            select new { d.Id, ParentId })
            .ToList();
</code></pre>

<p>create a class reprocenting the data and have the query return as List of known type and 
just union the two lists.</p>

<p>linqpad is a very useful tool for learn how to create the linq which give you the sql you want.</p>

### Answer ID: 59962583
<p>Yeah, welcome to the wonderfull world of EfCore 3.1 where all you can do is "Hello world".</p>

<p>Your query has various "problems" because EfCore does not really do LINQ processing except for super easy cases.</p>

<p>.Union(a.Members)</p>

<p>Can not be translated to run server side and client side processing is not enabled. Your only choises are:</p>

<ul>
<li>Force server execution for both parts (using AsEnumerable) then Union on the client. That only works if you do not use that as part of a larger statement (i.e. intersect) otherwise it is "pull all the data to the client" time and that is not good.</li>
</ul>

<p>At the current point in time I can only advice you to throw out EfCore and use EntityFramework which - as per framework 3.1 - is again available. Or use Entity Framework Classic which is a port that runs on netstandard 2.0 and has global query filters (which are THE ONE feature of EfCore I like). At last this is what I am currently getting to because - well - "better but without any features and not working" is not cutting it for me.</p>

<p>Whether or not EfCore will be extended (they seem not to see it as a fix) to handle anything except the most basic LINQ statements (and sometimes even not those) is unknown at this point - a lot of the changes in 3.1 are quite discouraging.</p>

<p>You MAY be able to move it into views etc. - but you may find out quite fast that EfCore has even more limitations and maintaining all the views gets quite tendious, too. I run into serious problems with the fact that I can not put any condition in front of any projection even in the most simple cases. And even simple bugs get commented on "we do not feel comfortable changing the pipeline, please wait for version 5 in november". Example? <a href="https://github.com/dotnet/efcore/issues/15279" rel="nofollow noreferrer">https://github.com/dotnet/efcore/issues/15279</a>.</p>

### Answer ID: 59962200
<p>As an alternative, you can use raw sql query. In Entity Framework Code, we need to define a POCO class and a DbSet for that class. In your case you will need to define some <code>YourClass</code>:</p>

<pre><code>public DbQuery&lt;YourClass&gt; YourClasses { get; set; }
</code></pre>

<p>and code to execute:</p>

<pre><code>var result = context.YourClasses.FromSql("YOURSQL_SCRIPT").ToList();
var asyncresult = await context.YourClasses.FromSql("YOURSQL_SCRIPT").ToListAsync();
</code></pre>

