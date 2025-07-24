# How to use DbContext with TPL (Tasks)?
[Link to question](https://stackoverflow.com/questions/56276960/how-to-use-dbcontext-with-tpl-tasks)
**Creation Date:** 1558620026
**Score:** 0
**Tags:** c#, entity-framework, asp.net-core, task-parallel-library
## Question Body
<p>I'm trying to attempt to use TPL to decrease runtime for an application. The application uses a DbContext, and the Task itself queries the database about three times using async methods (<code>FirstOrDefaultAsync</code>). I started getting Exceptions such as:</p>

<pre><code>"System.InvalidOperationException: A second operation started on this context before a previous operation completed. This is usually caused by different threads using the same instance of DbContext, however instance members are not guaranteed to be thread safe. This could also be caused by a nested query being evaluated on the client, if this is the case rewrite the query avoiding nested invocations."
</code></pre>

<p>This led me to realize that <code>DbContext</code> is not Thread Safe, and I needed a solution.</p>

<p>I have tried to create a new instance of the database for each context, but I don't think that I'm doing it properly. I'll show some code below to demonstrate my <code>DbContext</code> creation, it is different than what I've seen elsewhere on StackOverflow and other websites.
<code></p>

<pre><code>public static async Task Main()
{
    var host = new WebHostBuilder()
               .UseEnvironment("Test")
                   .ConfigureAppConfiguration((builderContext, config) =&gt;
                   {
                       var env = builderContext.HostingEnvironment;
                       config.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true).AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true, reloadOnChange: true);
                   }).UseStartup&lt;Startup&gt;();

    var testServer = new TestServer(host);

    var database = testServer.Host.Services.GetService&lt;CustomDbContext&gt;();
    database.Database.EnsureCreated();

    var httpClient = testServer.CreateClient();
    httpClient.DefaultRequestHeaders.Add(ApiConstants.General.APIKeyHeaderParm, tenant.APISecurityGuid.ToString()); // this works

    var builder = new ConfigurationBuilder()
               .SetBasePath(Directory.GetCurrentDirectory())
                   .AddJsonFile("appsettings.json");

    var configuration = builder.Build();

    var tasks = new List&lt;Task&gt;();
    foreach (var obj in database.Objects)
    {
        tasks.Add(CustomAsyncMethod(obj.Name, database, configuration, httpClient));
    }
    try
    {
        Task.WaitAll(tasks.ToArray());
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.ToString());
        Console.ReadKey();
    }

    //Some other normal code
}

public static async Task CustomAsyncMethod(string name, CustomDbContext database, IConfigurationRoot configuration, HttpClient httpClient)
{
    //Lines of normal code stuff
    //Inside of nested for loops here
    var first = await database.History.FirstOrDefaultAsync(x =&gt; x.Id == id);
    var second = await database.OtherTable.FirstOrDefaultAsync(y =&gt; y.Name == first.Name);
    // End nested for loops
    // Lines of other normal code stuff
}
</code></pre>

<p></code>
In the fooreach loop (<code>foreach (var obj in database.Objects)</code>), I have tried creating multiple <code>WebHostBuilders</code>, multiple <code>TestServers</code>, and multiple <code>httpClients</code> to use for the <code>CustomAsyncMethod</code>, but all those attempts seemed to make it worse. As it stands currently, I get the <code>InvalidOperationException</code> thrown multiple times every time I run the program, and the program breaks probably 70% of the time. 30% of the time it will finish successfully.</p>

<p>How can I eliminate the exceptions properly, without running the entire thing without TPL?</p>

## Answers
### Answer ID: 56277181
<p>Just instantiate it manually</p>

<pre><code>public class Data
{
    public async Task&lt;History&gt; GetHistoryById(int id)
    {
        using (var context = CreateDbContext())
        {
            return await context.History.FirstOrDefaultAsync(h =&gt; h.Id == id);
        }
    }

    public async Task&lt;History&gt; GetOtherByName(string name)
    {
        using (var context = CreateDbContext())
        {
            return await context.OtherTable.FirstOrDefaultAsync(o =&gt; o.Name == name);
        }            
    }

    public async Task&lt;IEnumerable&lt;MyObject&gt;&gt; GetObjects()
    {
        using (var context = CreateDbContext())
        {
            return await context.Objects.ToListAsync();
        }            
    }

    private CustomDbContext CreateDbContext()
    {
         var options = new DbContextOptionsBuilder&lt;CustomDbContext&gt;()
             .UseSqlServer(_connectionString)
             .Options;

         return new CustomDbContext(options);
    }
}
</code></pre>

<p>Then execute queries simultaneously, notice it will still run on one thread. You don't want to run it on multiple threads, because if IO operations it would be wasting of threads, which doing nothing - just waiting for the response.</p>

<pre><code>public static async Task CustomAsyncMethod(int id, Data data)
{
    //  ...

    var first = await data.GetHistoryById(id);
    var second = await data.GetOtherByName(first.Name);

    // ...
}
</code></pre>

<p>In main</p>

<pre><code>public static async Task Main()
{
    // Configurations ....

    var data = new Data();
    var objects = await data.GetObjects();

    var tasks = objects.Select(o =&gt; CustomAsyncMethod(o.Id, data)).ToArray();

    await Tasks.WhenAll(tasks);
}
</code></pre>

### Answer ID: 56277112
<p>The simplest fix for your problem as stated is to create a new instance of the DB context within your loop and use that for each task, e.g.</p>

<pre><code>var database = testServer.Host.Services.GetService&lt;CustomDbContext&gt;();

foreach (var obj in database.Objects)
    {
        var taskDbContext = testServer.Host.Services.GetService&lt;CustomDbContext&gt;();
        tasks.Add(CustomAsyncMethod(obj.Name, taskDbContext , configuration, httpClient));
    }
</code></pre>

