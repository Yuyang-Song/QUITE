# How do I perform an ExecuteUpdate on a MySQL DB Context DbSet&lt;T&gt;, given a List&lt;T&gt; of the current information?
[Link to question](https://stackoverflow.com/questions/77607153/how-do-i-perform-an-executeupdate-on-a-mysql-db-context-dbsett-given-a-listt)
**Creation Date:** 1701787930
**Score:** 0
**Tags:** c#, mysql, linq, .net-7.0, pomelo-entityframeworkcore-mysql
## Question Body
<p>I have three separate databases (Site A, Site B, Site C), using the same database software with some minor structural differences, from which the same types of data need retrieving, in some cases combining (Site A and B), and putting up to a separate dashboard.</p>
<p>As this data refreshes daily, the data needs inserting when new, updating when changed, and deleted when no longer present in the live time period, either by being deleted outright or the data aging out.</p>
<p>Because of the three separate sites, and the databases involved being old, cumbersome, not developer friendly (there are no up to date nuget libraries for them, the database type is officially no longer supported etc), and servicing live environments, I'm pulling the data out into a separate MySQL DB to manipulate.</p>
<p>The existing process for populating the dashboards is manually extracting the data into CSVs, combining the CSVs where necessary, then replacing the CSVs stored against each dashboard. As the dashboard setups are accepted as they are, I have to keep the same overall format.</p>
<p>Since DbContexts love to have each table be its own object type and can't recognise the tables correctly without having specific types relevant to the table names, each table object type extends a base object type.</p>
<p>I have the following (simplified) MySQL DBContext:</p>
<pre><code>public class MySqlDbContext : DbContext
{
    public MySqlDbContext(DbContextOptions&lt;MySqlDbContext&gt; options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder builder)
    {
        builder.Entity&lt;Ball_A&gt;()
            .HasKey(nameof(Ball_A.Site),
                    nameof(Ball_A.ID));

        builder.Entity&lt;Ball_B&gt;()
            .HasKey(nameof(Ball_B.Site),
                    nameof(Ball_B.ID));

        builder.Entity&lt;Ball_AB&gt;()
            .HasKey(nameof(Ball_AB.Site),
                    nameof(Ball_AB.ID));

        builder.Entity&lt;Ball_C&gt;()
            .HasKey(nameof(Ball_C.Site),
                    nameof(Ball_C.ID));

        builder.Entity&lt;Box_A&gt;()
            .HasKey(nameof(Box_A.Site),
                    nameof(Box_A.ID));

        builder.Entity&lt;Box_B&gt;()
            .HasKey(nameof(Box_B.Site),
                    nameof(Box_B.ID));

        builder.Entity&lt;Box_AB&gt;()
            .HasKey(nameof(Box_AB.Site),
                    nameof(Box_AB.ID));

        builder.Entity&lt;Box_C&gt;()
            .HasKey(nameof(Box_C.Site),
                    nameof(Box_C.ID));
    }

    public DbSet&lt;Ball_A&gt; Ball_A { get; set; }
    public DbSet&lt;Ball_B&gt; Ball_B { get; set; }
    public DbSet&lt;Ball_AB&gt; Ball_AB { get; set; }
    public DbSet&lt;Ball_C&gt; Ball_C { get; set; }
    public DbSet&lt;Box_A&gt; Box_A { get; set; }
    public DbSet&lt;Box_B&gt; Box_B { get; set; }
    public DbSet&lt;Box_AB&gt; Box_AB { get; set; }
    public DbSet&lt;Box_C&gt; Box_C { get; set; }
}
</code></pre>
<p>The following objects relating to the above context:</p>
<pre><code>public class Ball
{
    public string Site { get; set; };
    public int ID { get; set; }
    public DateTime Created { get; set; }
    public DateTime LastBounced { get; set; }
    public int Radius { get; set; }
}

[Table(&quot;ball_a&quot;)]
public class Ball_A : Ball {}
[Table(&quot;ball_b&quot;)]
public class Ball_B : Ball {}
[Table(&quot;ball_ab&quot;)]
public class Ball_AB : Ball {}
[Table(&quot;ball_c&quot;)]
public class Ball_C : Ball {}

public class Box
{
    public string Site { get; set; };
    public int ID { get; set; }
    public DateTime Created { get; set; }
    public DateTime LastOpened { get; set; }
    public int Length { get; set; }
    public int Width { get; set; }
}

[Table(&quot;box_a&quot;)]
public class Box_A : Box {}
[Table(&quot;box_b&quot;)]
public class Box_B : Box {}
[Table(&quot;box_ab&quot;)]
public class Box_AB : Box {}
[Table(&quot;box_c&quot;)]
public class Box_C : Box {}
</code></pre>
<p>I'm able to successfully retrieve data from the site(s) and temporarily store information as a <code>List&lt;Ball_A&gt;</code>, <code>List&lt;Box_A&gt;</code> etc.
When I'm trying to update existing data in the (currently empty) MySQL database, however, I'm getting a problem with the join:</p>
<p>Example LINQ:</p>
<pre><code>List&lt;Ball_A&gt; latestBallA = new(); // confirmed as populated from the live Site A DB; for brevity, just showing the object type.

int ballUpdate = from existingBallData in _mySqlDbContext.Ball_A
                join latestBallData in latestBallA on new { existingBallData.Site, existingBallData.ID } equals new { latestBallData.Site, latestBallData.ID }
                select new { existingBallData, latestBallData }).ExecuteUpdate(s =&gt;
                s.SetProperty(x =&gt; x.existingBallData.LastBounced, x =&gt; x.latestBallData.LastBounced)
                s.SetProperty(x =&gt; x.existingBallData.Radius, x =&gt; x.latestBallData.Radius)
                );
</code></pre>
<p>The following InvalidOperationException is thrown:</p>
<pre><code>System.InvalidOperationException
  HResult=0x80131509
  Message=The LINQ expression 'DbSet&lt;Ball_A&gt;()
    .Join(
        inner: __p_0, 
        outerKeySelector: existingBallData =&gt; new { 
            Site = existingBallData.Site, 
            ID = existingBallData.ID
         }, 
        innerKeySelector: latestBallData =&gt; new { 
            Site = latestBallData.Site, 
            ID = latestBallData.ID
         }, 
        resultSelector: (existingBallData, latestBallData) =&gt; new { 
            existingBallData = existingBallData, 
            latestBallData = latestBallData
         })' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
  Source=Microsoft.EntityFrameworkCore
  StackTrace:
   at Microsoft.EntityFrameworkCore.Query.Internal.NavigationExpandingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Dynamic.Utils.ExpressionVisitorUtils.VisitArguments(ExpressionVisitor visitor, IArgumentProvider nodes)
   at System.Linq.Expressions.ExpressionVisitor.VisitMethodCall(MethodCallExpression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.NavigationExpandingExpressionVisitor.ProcessUnknownMethod(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.Internal.NavigationExpandingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.Internal.NavigationExpandingExpressionVisitor.Expand(Expression query)
   at Microsoft.EntityFrameworkCore.Query.QueryTranslationPreprocessor.Process(Expression query)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.RelationalQueryableExtensions.ExecuteUpdate[TSource](IQueryable`1 source, Expression`1 setPropertyCalls)
   at Example.BallAFetcher.&lt;Fetch&gt;d__6.MoveNext() in C:\GitHub\Example\BallAFetcher.cs:line 101

  This exception was originally thrown at this call stack:
    [External Code]
    Example.BallAFetcher.Fetch() in BallAFetcher.cs
</code></pre>
<p>Trying to &quot;switch to client evaluation explicitly&quot;, by making <code>int ballUpdate = from existingBallData in _mySqlDbContext.Ball_A</code> -&gt; <code>int ballUpdate = from existingBallData in _mySqlDbContext.Ball_A.AsEnumerable()</code> leads to <code>ExecuteUpdate</code> being flagged, as <code>IEnumerable</code> doesn't contain a definition for <code>ExecuteUpdate</code>. The same happens when trying to make the list <code>latestBallA</code> -&gt; <code>latestBallA.AsQueryable()</code>.</p>
<p>I don't know how to revise my query, as it follows the same format as the many examples out there (on SO, Microsoft documentation, generally on the internet) for joins on composite primary keys, as well as examples of joins for performing <code>ExecuteUpdate</code>.</p>
<p>I have tried reversing the order of the LINQ join, so it goes <code>List</code>-&gt;<code>DbSet</code> instead of <code>DbSet</code>-&gt;<code>List</code>, which gets past the initial InvalidOperationException, but provides a different InvalidOperationException - <code>There is no method 'ExecuteUpdate' on type 'Microsoft.EntityFrameworkCore.RelationalQueryableExtensions' that matches the specified arguments</code> - that I assume is because the application is thinking I'm trying to perform the ExecuteUpdate from the <code>List</code> perspective, despite the logic in the ExecuteUpdate.</p>
<p>From looking at the most similar questions, my problem seems to be because I'm joining a database <code>DbSet&lt;T&gt;</code> to an in-memory <code>List&lt;T&gt;</code>? Do I need to create a table (i.e. a &quot;temp_ball_a&quot;, with &quot;DbSet&lt;Temp_Ball_A&gt; Temp_Ball_A&quot;) to store the list data in and perform the CRUD operations between tables to keep it all in the DB context, or is there another (potentially better) way to accomplish this?</p>

