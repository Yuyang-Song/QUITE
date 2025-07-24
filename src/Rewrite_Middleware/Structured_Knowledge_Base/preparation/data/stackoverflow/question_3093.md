# Why could the F# LINQ expression not be translated - at least partially?
[Link to question](https://stackoverflow.com/questions/66232611/why-could-the-f-linq-expression-not-be-translated-at-least-partially)
**Creation Date:** 1613511805
**Score:** 4
**Tags:** linq, f#, entity-framework-core, ef-code-first
## Question Body
<h1>Issue</h1>
<p>I’m using an existing code first approach in order to acquire data from an existing database. This project is encapsulated in a .NET C# project and contains the model as well as the configuration descriptions.</p>
<p><strong>My aim is to use the existing database context implementation for a F# project.</strong> I have been testing many times the database access with a XUnit test project which is also written in F#.</p>
<p><strong>My problem is an unexpected behaviour</strong>, when I try to select the last name and the person’s id.</p>
<p>In order to explain my implementation and illustrate the issue I implemented four test functions of which only the first two are executed successfully. The last two test functions fail.</p>
<p><strong>The following error appears</strong></p>
<pre class="lang-ml prettyprint-override"><code>System.InvalidOperationException : The LINQ expression 'LastName' could not
be translated. Either rewrite the query in a form that can be translated, or 
switch to client evaluation explicitly by inserting a call to 'AsEnumerable',
'AsAsyncEnumerable', 'ToList', or 'ToListAsync'*
</code></pre>
<p>I do not understand the error because I am not actually using any client specific implementation for the query evaluation. So normally the LINQ-Provider should convert it into a database appropriate SQL definition. For the tests I am using the Entity Framework memory database instance. On top of that, please note that the error also exists on the real database.</p>
<p>Another issue that I do not understand is why the second test works while the third one fails. I changed only the last name select with the id select.</p>
<p>However, I also added a F# query expression since this is actually recommended from the <a href="https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/query-expressions" rel="nofollow noreferrer">documentation</a>, but with no success.</p>
<p>Is the main problem the usage of the Entity Framework context? If so, how can I then reuse the implementation of the EF database context?</p>
<h2>Test and evaluation with LINQPad 6</h2>
<p>I tested the behaviour with LINQPad in order to make the use case more simple. Therefore, I used the DemoDB which should be available for everyone.</p>
<p>Apart from that I’m trying to make it reproduceable for a larger community. Unfortunately, the outcome of my test is the same. So, I created a simple database query and changed the order of the named selections. If I change the alphabetical order of the column names, the error appears. Therefore, <strong>why is the alphabetical order important in order to have a valid select statement?</strong></p>
<p>I found another closed issue on stackoverflow which describes the usage of anonymous records but the different order is not treated (<a href="https://stackoverflow.com/questions/21879859/f-query-expression-select-operator-changing-column-headings-in-result">F# Query Expression / select operator / changing column headings in result</a>).</p>
<pre class="lang-ml prettyprint-override"><code>// successful query
query { 
    for c in this.Categories do
    select {| A = c.CategoryID; B = c.CategoryName; |}
}
</code></pre>
<pre class="lang-ml prettyprint-override"><code>// failed query
query { 
    for c in this.Categories do
    select {| B = c.CategoryID; A = c.CategoryName; |}
}

The argument 'value' was the wrong type. Expected 
'System.Func`2[System.Int32,&lt;&gt;f__AnonymousType1383943985`2[System.String,System.Int32]]'. 
Actual '&lt;&gt;f__AnonymousType1383943985`2[System.String,System.Int32]'.
</code></pre>
<h2>Test and evaluation with a F# unit test project</h2>
<h3>Test result summary</h3>
<p>I tested the behaviour with .NET 3.1 and .NET 5.0 (projects as well as LINQPad 6). Furthermore, all dependencies have been adjusted accordingly (e.g. Entity Framework 5.0 or 3.1).</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>Test</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td>A anonymous record</td>
<td>successful</td>
</tr>
<tr>
<td>B anonymous record</td>
<td>successful</td>
</tr>
<tr>
<td>C anonymous record</td>
<td>failed</td>
</tr>
<tr>
<td>D anonymous record</td>
<td>failed</td>
</tr>
<tr>
<td>E partial person type</td>
<td>failed</td>
</tr>
<tr>
<td>F partial person type</td>
<td>successful</td>
</tr>
<tr>
<td>G partial person type</td>
<td>successful</td>
</tr>
<tr>
<td>H partial person type</td>
<td>failed</td>
</tr>
<tr>
<td>I partial person type</td>
<td>failed</td>
</tr>
</tbody>
</table>
</div><h3>Test outcome</h3>
<pre class="lang-ml prettyprint-override"><code>System.InvalidOperationException : The LINQ expression 'LastName' could not be translated. Either rewrite the query in a form that can be translated, or switch
    to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'
Entity Framework Core &quot;5.0.3&quot; initialized 
'&quot;TestContext&quot;' using provider '&quot;Microsoft.EntityFrameworkCore.InMemory&quot;'
</code></pre>
<h3>EF core code first database .NET 5 project</h3>
<pre class="lang-cs prettyprint-override"><code>public class Person
{
     public int Id { get; set; }
     public string LastName { get; set; }
}
...
public void Configure(EntityTypeBuilder&lt;Person&gt; builder)
{
      builder.ToTable(&quot;PERSON&quot;);
      builder.HasKey(x =&gt; x.Id);
      builder.Property(x =&gt; x.Id)
             .HasColumnName(&quot;ID&quot;)
             .ValueGeneratedNever();
      builder.Property(x =&gt; x.LastName)
             .HasColumnName(&quot;LASTNAME&quot;)
             .HasMaxLength(512)
             .IsUnicode(false);
}
...
public class TestContext : DbContext
{
     public DbSet&lt;Person&gt; Persons { get; private set; }
     public TestContext(DbContextOptions&lt;TestContext&gt; options) : base(options)
     {}
     protected override void OnModelCreating(ModelBuilder modelBuilder)
     {
          modelBuilder.ApplyConfiguration(new PersonConfig());
     }
}
</code></pre>
<h2>F# xunit test project in order to evaluate the EF core database context access</h2>
<pre class="lang-ml prettyprint-override"><code>type PartialPerson = { LastName: string; ID : int; }

type ``success database execution queries`` (output: ITestOutputHelper) =
    let sLogger =
        LoggerConfiguration()
            .MinimumLevel.Verbose()
            .MinimumLevel.Override(&quot;Microsoft&quot;, LogEventLevel.Information)
            .MinimumLevel.Override(&quot;Microsoft.EntityFrameworkCore&quot;, LogEventLevel.Information)
            .Enrich.FromLogContext()
            .WriteTo.TestOutput(output, Events.LogEventLevel.Verbose)
            .WriteTo.Debug()
            .CreateLogger()
    let loggerFactory =
        (new LoggerFactory())
            .AddSerilog(sLogger)
    let options = DbContextOptionsBuilder&lt;TestContext&gt;()
                      .EnableSensitiveDataLogging(true)
                      .UseLoggerFactory(loggerFactory)
                      .UseInMemoryDatabase(Guid.NewGuid().ToString())
                      .Options;
    let context = new TestContext(options)
    [&lt;Fact&gt;]
    let ``success person select lastname Test A`` () =
        let rs =
            context.Persons.Select(
                fun person -&gt; {| Name = person.LastName |} )
        rs |&gt; should be Empty // successful
    [&lt;Fact&gt;]
    let ``success person select id and lastname Test B`` () =
        let rs =
            context.Persons.Select(
                fun person -&gt;
                    {| ID = person.Id
                       LastName = person.LastName |})
        rs |&gt; should be Empty // successful
    [&lt;Fact&gt;]
    let ``success person select id and lastname Test C`` () =
        let rs =
            context.Persons.Select(
                fun person -&gt;
                    {| LastName = person.LastName
                       ID = person.Id |} )
        rs |&gt; should be Empty // failed
    [&lt;Fact&gt;]
    let ``success person select id and lastname Test D`` () =
        let rs =
            query {
                for person in context.Persons do
                select 
                    {| LastName = person.LastName
                       ID = person.Id |}
            }
        rs |&gt; should be Empty // failed

    // avoid anonymous record and use the partial person type
    // type PartialPerson = { LastName: string; ID : int; }
    [&lt;Fact&gt;]
    let ``success partial person select id and lastname Test E`` () =
        let rs =
            context.Persons.Select(
                fun person -&gt;
                    { ID = person.Id
                      LastName = person.LastName })
        rs |&gt; should be Empty // failed
    [&lt;Fact&gt;]
    let ``success partial person select id and lastname Test F`` () =
        let rs =
            context.Persons.Select(
                fun person -&gt;
                    { LastName = person.LastName
                      ID = person.Id } )
        rs |&gt; should be Empty // successful
    [&lt;Fact&gt;]
    let ``success partial person select id and lastname Test G`` () =
        let rs =
            query {
                for person in context.Persons do
                select 
                     { LastName = person.LastName
                       ID = person.Id }
            }
        rs |&gt; should be Empty // successful
    [&lt;Fact&gt;]
    let ``success partial person select id and lastname Test H`` () =
        let rs =
            query {
                for person in context.Persons do
                select 
                     { ID = person.Id
                       LastName = person.LastName }
            }
        rs |&gt; should be Empty // failed
    [&lt;Fact&gt;]
    let ``success partial person select id and lastname Test I`` () =
        let rs =
            query {
                for person in context.Persons do
                select 
                     { ID = person.Id
                       LastName = person.LastName }
            }
        rs.ToList() |&gt; should be Empty // failed
</code></pre>
<h2>Current findings</h2>
<p>It seems that this issue is related to the issues <a href="https://github.com/StackExchange/Dapper/issues/1226" rel="nofollow noreferrer">1226</a> and <a href="https://github.com/dotnet/fsharp/issues/3782" rel="nofollow noreferrer">3782</a>. Both issues describe some problems with the order of named selections.</p>
<p>The dapper issue <a href="https://github.com/StackExchange/Dapper/issues/1226" rel="nofollow noreferrer">1226</a> had a similar problem with the order of anonymous records for the query definition. However, thanks to Isaac Abraham (isaacabraham) who is using the <em>CLIMutable</em> decoration, I thought of turning off the ordering restrictions. So basically the idea was to try it for my tests since the query generation through the LINQ provider could have a positive effect. Unfortunately this was without success, maybe because of the implementation of the LINQ provider because the generation process is implemented with F# and that is the reason why the <em>CLIMutable</em> attribute does not affect it.</p>
<p>After continuing my search, I found another issue <a href="https://github.com/dotnet/fsharp/issues/3782" rel="nofollow noreferrer">3782</a> which indicates my problem. The issue has the main focus on the usage of tuples for the data selection but also the issue with records. So, I added another issue description <a href="https://github.com/dotnet/fsharp/issues/11131" rel="nofollow noreferrer">11131</a> in order to help with my current findings. Finally, I will keep track the outcome and add it to this issue.</p>

## Answers
### Answer ID: 68164890
<p>Does this still need answering?</p>
<p>As you already found out, F# anonymous types order fields by name (not by source code order of declaration, as C# anonymous types would do).</p>
<p>When writing <code>{| B = c.CategoryID; A = c.CategoryName; |}</code> in a LINQ query, this will not actually pass an anonymous type, rather the compiler creates an <code>System.Linq.Expressions.Expression</code> that describes how to construct the anonymous type, and later on the underlying framework implementing LINQ (e.g., the Entity Framework) will try to parse that expression (and create e.g. SQL code from it).</p>
<p>Problem here is, <code>c.CategoryID</code> and <code>c.CategoryName</code> may have side effects, hence the compiler will evaluate them in the order specified in the source code (first ID, then Name), but assign them in the order of the anonymous type.</p>
<p>Long story short, the generated <code>System.Linq.Expressions.Expression</code> first will evaluate <code>c.CategoryID</code>, assign the value to a temporary variable, evaluate <code>c.CategoryName</code>, assign that to the anonymous type's first field, and finally assign the temporary variable to the anonymous type's second field. And the EF translator later on does not know how to handle the temporary variable (e.g., how to translate that to SQL.)</p>
<p>(In C#, no field reordering happens, so no temporary variables are required to mask side effects, so the expression parser will not face that problem.) (The F# anonymous type at present is not fully fit for LINQ.)</p>

