# EF Core: filter condition for nested collection (Func&lt;&gt;) as a variable
[Link to question](https://stackoverflow.com/questions/70383336/ef-core-filter-condition-for-nested-collection-func-as-a-variable)
**Creation Date:** 1639676183
**Score:** 2
**Tags:** .net, entity-framework, linq, .net-core, entity-framework-core
## Question Body
<p>tl;dr;
I .Net6 I want to pass to dbcontext.Entities.Include(host =&gt; host.nestedeCollection.Where(element =&gt; )) func element =&gt;  via a variable Func&lt;ElementType, bool&gt;. It works with Z.Entityframework.Extensions, but cannot convert it to EF Core.</p>
<p>Long story.
Consider the following model:</p>
<pre><code>public class Attendance {
    public Guid Id { get; set; }
    public Guid StudentId { get; set; }
    public string Subject { get; set; }
    public decimal Rank { get; set; }
}

public class Student {
    public Guid Id { get; set; }
    public string Name { get; set; }
    public virtual ICollection&lt;Attendance&gt; Attendances { get; set; }
}

public class UniversityDbContext : DbContext {
    public DbSet&lt;Attendance&gt; Attendances { get; set; }
    public DbSet&lt;Student&gt; Students { get; set; }
...
    protected override void OnModelCreating(ModelBuilder modelBuilder) {
        modelBuilder.Entity&lt;Student&gt;()
            .HasMany(student =&gt; student.Attendances)
            .WithOne()
            .HasForeignKey(x =&gt; x.StudentId)
        ;
    }
}
</code></pre>
<p>I want to:</p>
<pre><code>var students = db
    .Students
    .Include(student =&gt; student.Attendances.Where(att =&gt; att.Rank &lt; 3.0m))
    .ToList()
;
</code></pre>
<p>At the moment I am using Z.EntityFramework.Extensions .IncludeOptimized. Since Net5 there is an EF-native feature to perform the same task, and the code above just works fine for scenarios like above {{Where(att =&gt; att.Rank &lt; 3.0m)}} . In real life I have quite a complex condition for .Where clause and I have to repeat it within multiple .Include and .ThenInclude statements when loading my data, and unfortunately global filters do not help in this case unless I totally refactor the app. What I did for Z.EntityFramework.Extensions is:</p>
<pre><code>Func&lt;Attendance, bool&gt; func = attendance =&gt; attendance.Rank &lt; 3.0m;
var students = db
    .Students
    .IncludeOptimized(student =&gt; student.Attendances.Where(func))
    .ToList()
;
</code></pre>
<p>It worked.</p>
<p>Now, I try the same with NET6 and latest available EF Core. All attempts fail:</p>
<pre><code>        Func&lt;Attendance, bool&gt; func_x = attendance =&gt; true;
        Func&lt;Attendance, bool&gt; func_y = attendance =&gt; attendance.Rank &lt; 3.0m;
        Expression&lt;Func&lt;Attendance, bool&gt;&gt; expr = att =&gt; att.Rank &lt; 3.0m; 

        //*
        using (var db = new UniversityDbContext(connString)) {
            var students_x = db
                .Students
                .Include(student =&gt; student.Attendances.Where(func_x))
                .ToList()
            ;
        }

        //**
        //using (var db = new UniversityDbContext(connString)) {
        //    var students_z = db
        //        .Students
        //        .Include(student =&gt; student.Attendances.Where(x =&gt; func_x(x)))
        //        .ToList()
        //    ;
        //}
        
        //***
        //using (var db = new UniversityDbContext(connString)) {
        //    var students_y = db
        //        .Students
        //        .Include(student =&gt; student.Attendances.Where(func_y))
        //        .ToList()
        //    ;
        //}

        //****
        //using (var db = new UniversityDbContext(connString)) {
        //    var students_z = db
        //        .Students
        //        .Include(student =&gt; student.Attendances.Where(Func_z))
        //        .ToList()
        //    ;
        //}
        
        //*****
        //using (var db = new UniversityDbContext(connString)) {
        //    var students_expr = db
        //        .Students
        //        .Include(student =&gt; student.Attendances.Where(expr))
        //        .ToList()
        //    ;
        //}
</code></pre>
<p>//* fails with</p>
<pre><code>System.ArgumentException: Expression of type 'System.Func`2[FuncInEFIncludeExample.Attendance,System.Boolean]' cannot be used for parameter of type 'System.Linq.Expressions.Expression`1[System.Func`2[FuncInEFIncludeExample.Attendance,System.Boolean]]' of method 'System.Linq.IQueryable`1[FuncInEFIncludeExample.Attendance] Where[Attendance](System.Linq.IQueryable`1[FuncInEFIncludeExample.Attendance], System.Linq.Expressions.Expression`1[System.Func`2[FuncInEFIncludeExample.Attendance,System.Boolean]])' (Parameter 'arg1')
   at System.Dynamic.Utils.ExpressionUtils.ValidateOneArgument(MethodBase method, ExpressionType nodeKind, Expression arguments, ParameterInfo pi, String methodParamName, String argumentParamName, Int32 index)
   at System.Linq.Expressions.Expression.Call(Expression instance, MethodInfo method, Expression arg0, Expression arg1)
   at System.Linq.Expressions.Expression.Call(Expression instance, MethodInfo method, IEnumerable`1 arguments)
   at System.Linq.Expressions.Expression.Call(MethodInfo method, IEnumerable`1 arguments)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryableMethodNormalizingExpressionVisitor.TryConvertEnumerableToQueryable(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryableMethodNormalizingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Linq.Expressions.ExpressionVisitor.VisitLambda[T](Expression`1 node)
   at System.Linq.Expressions.Expression`1.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Linq.Expressions.ExpressionVisitor.VisitUnary(UnaryExpression node)
   at System.Linq.Expressions.UnaryExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at System.Dynamic.Utils.ExpressionVisitorUtils.VisitArguments(ExpressionVisitor visitor, IArgumentProvider nodes)
   at System.Linq.Expressions.ExpressionVisitor.VisitMethodCall(MethodCallExpression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryableMethodNormalizingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryTranslationPreprocessor.NormalizeQueryableMethod(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryTranslationPreprocessor.NormalizeQueryableMethod(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.QueryTranslationPreprocessor.Process(Expression query)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.IncludableQueryable`2.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at FuncInEFIncludeExample.Program.Main() in W:\Projects\FuncInEFInclude\FuncInEFIncludeExample\Program.cs:line 81
</code></pre>
<p>//** fails with</p>
<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Attendance&gt;()
    .Where(a =&gt; EF.Property&lt;Guid?&gt;(EntityShaperExpression: 
        FuncInEFIncludeExample.Student
        ValueBufferExpression: 
            ProjectionBindingExpression: EmptyProjectionMember
        IsNullable: False
    , &quot;Id&quot;) != null &amp;&amp; object.Equals(
        objA: (object)EF.Property&lt;Guid?&gt;(EntityShaperExpression: 
            FuncInEFIncludeExample.Student
            ValueBufferExpression: 
                ProjectionBindingExpression: EmptyProjectionMember
            IsNullable: False
        , &quot;Id&quot;), 
        objB: (object)EF.Property&lt;Guid?&gt;(a, &quot;StudentId&quot;)))
    .Where(a =&gt; Invoke(__func_x_0, a)
    )' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|15_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass15_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.TranslateSubquery(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.IncludeExpression.VisitChildren(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.VisitExtension(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitExtension(Expression extensionExpression)
   at System.Linq.Expressions.Expression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator()
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.IncludableQueryable`2.GetEnumerator()
   at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)
   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)
   at FuncInEFIncludeExample.Program.Main() in W:\Projects\FuncInEFInclude\FuncInEFIncludeExample\Program.cs:line 91
</code></pre>
<p>The rest are failing as //*, and the last one, //*****, as expected, does not even compile.</p>
<p>I tried further to play around with nested collections, making them IQueryable&lt;&gt;. Could not achieve what I want. I am especially confused by</p>
<pre><code>System.ArgumentException: Expression of type 'System.Func`2[FuncInEFIncludeExample.Attendance,System.Boolean]' cannot be used for parameter of type 'System.Linq.Expressions.Expression`1[System.Func`2[FuncInEFIncludeExample.Attendance,System.Boolean]]' of method 'System.Linq.IQueryable`1[FuncInEFIncludeExample.Attendance]
</code></pre>
<p>Is there an invalid cast in the middle of Visitor pattern implementation (looking at stacktrace)?</p>
<p>Hence is my question.
Has anybody tried to achieve the same in EF Core? May be any suggestions?</p>
<p>Thanks!</p>

## Answers
### Answer ID: 70389839
<p>As suggested, LINQKit is the answer so far.
Thanks.</p>

### Answer ID: 70383799
<p>If you want query translation, you have to deal only with <code>Expression</code>, just <code>Func</code> is not tranaslateble to the SQL. Good news, that you do not need <code>Z.EntityFramework</code>, bad news that EF Core still will not translate your query.</p>
<p>You neeed ligthweigh library <a href="https://github.com/scottksmith95/LINQKit" rel="nofollow noreferrer">LINQKit</a>. It needs just configuring DbContextOptions:</p>
<pre class="lang-cs prettyprint-override"><code>builder
    .UseSqlServer(connectionString)
    .WithExpressionExpanding(); // enabling LINQKit extension
</code></pre>
<p>Then you can use your expression via <code>Invoke</code> extension:</p>
<pre class="lang-cs prettyprint-override"><code>Expression&lt;Func&lt;Attendance, bool&gt;&gt; func_x = attendance =&gt; true;
Expression&lt;Func&lt;Attendance, bool&gt;&gt; func_y = attendance =&gt; attendance.Rank &lt; 3.0m;
Expression&lt;Func&lt;Attendance, bool&gt;&gt; expr = att =&gt; att.Rank &lt; 3.0m; 

using (var db = new UniversityDbContext(connString)) 
{
    var students_x = db
        .Students
        .Include(student =&gt; student.Attendances.Where(x =&gt; func_x.Invoke(x)))
        .ToList();
}
</code></pre>

