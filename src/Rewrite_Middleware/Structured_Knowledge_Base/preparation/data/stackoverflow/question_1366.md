# how do i identify that a cosmos db container is empty and needs to be seeded?
[Link to question](https://stackoverflow.com/questions/72769185/how-do-i-identify-that-a-cosmos-db-container-is-empty-and-needs-to-be-seeded)
**Creation Date:** 1656318948
**Score:** -1
**Tags:** c#, entity-framework-core, azure-functions, azure-cosmosdb
## Question Body
<p>I am via EF core accessing my cosmos db database.</p>
<p>I have via Ef core overriden the OnModelCreating to check whether the underlying database and container exists. but I am not sure How I should check whether it contains any data?</p>
<p>EfCore does not seem to have any count, or no way to check whether the underlying db is empty?</p>
<p>This what I have tried so far</p>
<pre><code>  protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var client = Database.GetCosmosClient();
        var dbResponse = client.CreateDatabaseIfNotExistsAsync(&quot;Db&quot;).Result.StatusCode;
        ContainerProperties containerProperties = new ContainerProperties(&quot;forms&quot;, &quot;/forms&quot;);
        var database = client.GetDatabase(&quot;Db&quot;);
        var containerResponse = database.CreateContainerIfNotExistsAsync(containerProperties).Result.StatusCode;

        //Database or container was recently created, hence reseed 
        if (dbResponse == System.Net.HttpStatusCode.Created
            || containerResponse == System.Net.HttpStatusCode.Created)
        {
            Console.WriteLine(&quot;Model created but need seeding&quot;);
    return;
        }

        var container = database.GetContainer(&quot;forms&quot;);
    //How to check data is in the container?            

    }
</code></pre>
<p>Based on the answer provided by @Svyatoslav Danyli i created two methods.</p>
<pre><code>using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace FormsRetriever
{
    public static class SeedingTools
    {
        public static void CheckDatabase(DbContext dbContext)
        {
            dbContext.Database.EnsureCreated();
            var client = dbContext.Database.GetCosmosClient();
            SeedData(dbContext);

        }

        private static void SeedData(DbContext dbContext)
        {

            bool a = dbContext.Set&lt;Forms&gt;().Any();
        }
    }
}
</code></pre>
<p>Which I call in the startup.</p>
<p>which in return gives me this error</p>
<pre><code>A host error has occurred during startup operation '50913447-b407-41a1-95bd-68918f9d3d4b'.
[2022-07-04T11:04:53.059Z] Microsoft.EntityFrameworkCore: The LINQ expression 'DbSet&lt;Forms&gt;()
[2022-07-04T11:04:53.059Z]     .Any()' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
</code></pre>

## Answers
### Answer ID: 72770776
<p>Move check code to appropriate function and execute when EF Core is properly configured:</p>
<pre class="lang-cs prettyprint-override"><code>public static class DatabaseTools
{
    public static void CheckDatabase(DbContext context)
    {
        // EF Core will create database and containters
        context.Database.EnsureCreated();

        // Cosmos provider do not supports Any
        if (dbContext.Set&lt;Form&gt;().FirstOrDefault() == null)
        {
            // seed data
            context.Set&lt;Form&gt;().AddRange(
                new []
                {
                    new Form{},
                    new Form{},
                    new Form{},
                }
            );

            context.SaveChanges();
        }
    }
}
</code></pre>

