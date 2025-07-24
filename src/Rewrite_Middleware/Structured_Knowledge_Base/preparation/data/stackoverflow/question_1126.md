# Entity Framework Core and Cosmos DB. Using LINQ expressions to read entities
[Link to question](https://stackoverflow.com/questions/60222577/entity-framework-core-and-cosmos-db-using-linq-expressions-to-read-entities)
**Creation Date:** 1581668922
**Score:** 3
**Tags:** c#, azure, entity-framework-core, azure-cosmosdb, entity-framework-core-3.1
## Question Body
<p>In our solution we´re using the package <code>Microsoft.EntityFrameworkCore.Cosmos 3.1.1</code> to do operations against our cosmos databases and containers in Azure. We have a fairly easy object structure. An object containg a list of other objects. </p>

<pre><code>public class ExampleEntity : Entity
{
    public string TestProperty { get; set; }
    public IEnumerable&lt;SubEntity&gt; SubEntities { get; set; }

    protected override IEnumerable&lt;object&gt; GetEqualityComponents()
    {
            yield return TestProperty;
    }
}

public class SubEntity : Entity
{
    public bool IsActive { get; set; }

    protected override IEnumerable&lt;object&gt; GetEqualityComponents()
    {
        yield return IsActive;
    }
}
</code></pre>

<p>We´ve configured the <code>DbContext</code> for EntityFramework like this: </p>

<pre><code>builder.Entity&lt;ExampleEntity&gt;().ToContainer(nameof(ExampleEntity));
builder.Entity&lt;ExampleEntity&gt;().HasKey(p =&gt; p.id);
builder.Entity&lt;ExampleEntity&gt;().OwnsMany(p =&gt; p.SubEntities);
</code></pre>

<p>The json structure in cosmos looks like this:</p>

<pre><code>{
    "id": "51099fa9-5d71-4181-93b1-2c8cc0482a95",
    "CreatedAt": "2020-02-14T08:11:06.701659Z",
    "Discriminator": "ExampleEntity",
    "TestProperty": "Property1",
    "UpdatedAt": "0001-01-01T00:00:00",
    "SubEntities": [
        {
            "id": "9a120613-c42a-4399-a660-e6228cfce0ad",
            "CreatedAt": "2020-02-14T08:11:06.70457Z",
            "ExampleEntityid": "51099fa9-5d71-4181-93b1-2c8cc0482a95",
            "IsActive": false,
            "UpdatedAt": "0001-01-01T00:00:00"
        },
        {
            "id": "21b86b53-2d6a-4b31-a60b-8d31cfd04734",
            "CreatedAt": "2020-02-14T08:11:06.705145Z",
            "ExampleEntityid": "51099fa9-5d71-4181-93b1-2c8cc0482a95",
            "IsActive": true,
            "UpdatedAt": "0001-01-01T00:00:00"
        }
    ],
    "_rid": "R343APAECLsBAAAAAAAAAA==",
    "_self": "dbs/R343AA==/colls/R343APAECLs=/docs/R343APAECLsBAAAAAAAAAA==/",
    "_etag": "\"06001f30-0000-0d00-0000-5e46561b0000\"",
    "_attachments": "attachments/",
    "_ts": 1581667867
}
</code></pre>

<p>Now, we want to search after <code>ExampleEntities</code> where <code>SubEntities</code> has the boolean value of <code>IsActive</code> set to true. This is where our problems starts.</p>

<p>We have a generic repository, where the Read method looks like this:</p>

<pre><code>/// &lt;summary&gt;
/// Get an entity from the database
/// &lt;/summary&gt;
/// &lt;param name="predicate"&gt;A predicate to decide which entity to get&lt;/param&gt;
/// &lt;param name="children"&gt;Child entities to included in the DbSet&lt;/param&gt;
/// &lt;returns&gt;All entities that matches the predicate&lt;/returns&gt;
public async Task&lt;IEnumerable&lt;TEntity&gt;&gt; ReadAsync(Expression&lt;Func&lt;TEntity, bool&gt;&gt; predicate, params Expression&lt;Func&lt;TEntity, object&gt;&gt;[] children)
{
    var dbSet = _dbContext.Set&lt;TEntity&gt;();
    children.ToList().ForEach(p =&gt; dbSet.Include(p));

    var entities = dbSet.Where(predicate);
    return await entities.ToListAsync();
}
</code></pre>

<p>Using the following code like this in a IntegrationTest:</p>

<pre><code>[Test]
public async Task EntityFramework_Should_Return_Object_Based_On_Property_In_SubEntity()
{
    var uow = Container.Resolve&lt;IUnitOfWork&lt;ExampleEntity&gt;&gt;();
    var entity1 = new ExampleEntity
    {
        TestProperty = "Property1",
        SubEntities = new List&lt;SubEntity&gt;
        {
            new SubEntity
            {
                IsActive = false
            },
            new SubEntity
            {
                IsActive = true
            }
        }
    };

    await uow.Repository.CreateAsync(entity1);
    await uow.CommitAsync();

    var readEntity = uow.Repository.ReadAsync(p =&gt; p.SubEntities.Any(p =&gt; p.IsActive), p =&gt; p.SubEntities);
    readEntity.Should().NotBeNull();
}
</code></pre>

<p>The problem occurs at this line here where I use the Read method from the repository above:</p>

<pre><code>var readEntity = uow.Repository.ReadAsync(p =&gt; p.SubEntities.Any(p =&gt; p.IsActive), p =&gt; p.SubEntities);
</code></pre>

<p>It results in the following exception:</p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;ExampleEntity&gt;
    .Where(e =&gt; EF.Property&lt;IEnumerable&lt;SubEntity&gt;&gt;(e, "SubEntities")
        .AsQueryable()
        .Any(o =&gt; o.IsActive))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().
</code></pre>

<p>I find it quite strange that a simple query like this isn´t supported in Entity Framework Cosmos. Obviously I can do a <code>AsEnumerable()</code>, but then I will download all the data from the database and do the filtering client side and not on the database side, which will have a huge performance impact when the database contains 100´000s of records..</p>

<p><strong>How can I rewrite my repository to do such filtering on the database side? Is it possible at all with Entity Framework Cosmos?</strong></p>

## Answers
### Answer ID: 60234887
<p>As per <a href="https://learn.microsoft.com/en-us/ef/core/providers/cosmos/limitations" rel="nofollow noreferrer">current limitations</a> <code>Include</code> and <code>join</code> are not supported yet.</p>

