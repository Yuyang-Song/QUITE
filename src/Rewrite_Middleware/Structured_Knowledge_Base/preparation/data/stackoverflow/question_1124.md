# EF Core FromSQLRaw is not calling the database?
[Link to question](https://stackoverflow.com/questions/60160180/ef-core-fromsqlraw-is-not-calling-the-database)
**Creation Date:** 1581379036
**Score:** 0
**Tags:** asp.net-core-webapi, ef-core-3.1
## Question Body
<p>I need to rewrite an old web service because the team that supported the old one no longer wants to support it with their new tool. So I'm rewriting it using ASP.NET Core WebAPI and EF Core 3.1.</p>

<p>The majority of the logic for the service is stuck in stored procedures written years ago. Nothing super complex, but don't really think it's a good idea to start rewriting everything. </p>

<p>The problem is that EF Core's support for stored procs seems lacking at best. I got one working using Database.ExecuteSqlRaw which returns the results as output parameters, but I'm having trouble with another that returns the results as a dataset. (Actually two, but let's not get ahead of ourselves... I've commented it so it's only returning one right now.)</p>

<p>The (current) problem with the .FromSqlRaw query is that it doesn't appear to be querying the database at all when I watch for it in XEvent Profiler. (SQL Server 2016.)</p>

<p>Here's the code I'm using to call the proc:</p>

<pre><code>var bundle_id = new SqlParameter("bundle_id", bundleID) { Direction = ParameterDirection.Input };

var result = this.BundleUserGuideDetails.FromSqlRaw("EXEC dbo.p_fetch_user_guide_details @bundle_id", bundle_id);

var deets = result.FirstOrDefault&lt;BundleUserGuideDetail&gt;();
</code></pre>

<p>I did create a DBSet for it in the DBContext class:</p>

<pre><code>public DbSet&lt;BundleUserGuideDetail&gt; BundleUserGuideDetails { get; set; }
</code></pre>

<p>And since it's a keyless type I've got this per Microsoft's Keyless Entity guide:</p>

<pre><code>protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity&lt;BundleUserGuideDetail&gt;(eb =&gt;
       {
           eb.HasNoKey();                   
       });
    }
</code></pre>

<p>The model I created has all the same field names as the data being returned as well. </p>

<p>So why is the DB not even getting called for this? </p>

<p>EDIT: Forgot to write that the call to FirstOrDefault is throwing "System.InvalidOperationException: 'Sequence contains no elements'"</p>

<p>EDIT: Here is the full exception text:</p>

<pre><code>System.InvalidOperationException: Sequence contains no elements
   at System.Linq.ThrowHelper.ThrowNoElementsException()
   at System.Linq.Enumerable.Aggregate[TSource](IEnumerable`1 source, Func`3 func)
   at Microsoft.EntityFrameworkCore.Query.ShapedQueryCompilingExpressionVisitor.EntityMaterializerInjectingExpressionVisitor.ProcessEntityShaper(EntityShaperExpression entityShaperExpression)
   at Microsoft.EntityFrameworkCore.Query.ShapedQueryCompilingExpressionVisitor.EntityMaterializerInjectingExpressionVisitor.VisitExtension(Expression extensionExpression)
   at System.Linq.Expressions.Expression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Linq.Expressions.ExpressionVisitor.VisitBinary(BinaryExpression node)
   at System.Linq.Expressions.BinaryExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Dynamic.Utils.ExpressionVisitorUtils.VisitBlockExpressions(ExpressionVisitor visitor, BlockExpression block)
   at System.Linq.Expressions.ExpressionVisitor.VisitBlock(BlockExpression node)
   at System.Linq.Expressions.BlockExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Linq.Expressions.ExpressionVisitor.VisitLambda[T](Expression`1 node)
   at System.Linq.Expressions.Expression`1.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.ShapedQueryCompilingExpressionVisitor.EntityMaterializerInjectingExpressionVisitor.Inject(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.ShapedQueryCompilingExpressionVisitor.InjectEntityMaterializers(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalShapedQueryCompilingExpressionVisitor.VisitShapedQueryExpression(ShapedQueryExpression shapedQueryExpression)
   at Microsoft.EntityFrameworkCore.Query.ShapedQueryCompilingExpressionVisitor.VisitExtension(Expression extensionExpression)
   at System.Linq.Expressions.Expression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at System.Linq.Queryable.FirstOrDefault[TSource](IQueryable`1 source)
   at MandTBank.BBFB.BPS.BPSWebAPI.Data.BundleSystemContext.FetchUserGuideDetails(String bundleID) in C:\Users\tdevmcr\Source\Workspaces\BBFB\NeedsAssessmentSystem\Main\Sourcecode\BBFB NAS - I3 - BundleUserGuide Service\MandTBank.BBFB.BPS.BPSWebAPI\Data\BundleSystemContext.cs:line 65
</code></pre>

## Answers
### Answer ID: 60175867
<p>Turns out I had made a simple mistake, and failed to make the fields in the model <code>public</code> </p>

<p>The exception being thrown certainly doesn't make that obvious though...</p>

<p>I also needed to add <code>AsEnumerable()</code> after the FromSqlRaw call for it to work, as per this question: <a href="https://stackoverflow.com/questions/59381530/include-with-fromsqlraw-and-stored-procedure-in-ef-core-3-1">Include with FromSqlRaw and stored procedure in EF Core 3.1</a></p>

