# Using GroupBy to pick rows in Entity Framework
[Link to question](https://stackoverflow.com/questions/71456006/using-groupby-to-pick-rows-in-entity-framework)
**Creation Date:** 1647168795
**Score:** 0
**Tags:** c#, linq, entity-framework-core, ef-core-5.0
## Question Body
<p>I'm trying to get a list of all unique combinations of make and model and also include the most recent time stamp and the corresponding color from the following table:</p>
<pre><code>+-------+---------+-------------------------+--------+
| Make  | Model   |        Last Seen        | Color  |
+-------+---------+-------------------------+--------+
| Volvo | XC90    | 2022-03-11 13:30:31.623 | Blue   |
| Volvo | XC90    | 2022-03-11 14:30:31.623 | Green  |
| BMW   | M3      | 2022-03-11 15:30:31.623 | Orange |
| Ford  | Mustang | 2022-03-11 16:30:31.623 | Red    |
+-------+---------+-------------------------+--------+
</code></pre>
<p>In this case since there are two rows with the make Volvo and Model XC90, I want to pick the row with the latest timestamp and return the following:</p>
<pre><code>+-------+---------+-------------------------+--------+
| Make  | Model   |        Last Seen        | Color  |
+-------+---------+-------------------------+--------+  
| Volvo | XC90    | 2022-03-11 14:30:31.623 | Green  |
| BMW   | M3      | 2022-03-11 15:30:31.623 | Orange |
| Ford  | Mustang | 2022-03-11 16:30:31.623 | Red    |
+-------+---------+-------------------------+--------+
</code></pre>
<p>I have tried different combinations of <code>GroupBy</code> and select but without success. Here is an example of what I'm trying to do which I think is very close, but it's throwing an exception</p>
<pre><code>using Microsoft.EntityFrameworkCore;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace TestEntityFramework
{
    class Program
    {
        public class Car
        {
            public Guid Id { get; set; }
            public string Make { get; set; }
            public string Model { get; set; }
            public DateTime Time { get; set; }
            public string Color { get; set; }
        }

        public class CarContext : DbContext
        {
            public CarContext(DbContextOptions&lt;CarContext&gt; options) : base(options)
            {
            }

            public DbSet&lt;Car&gt; Cars { get; set; }
        }

        static async Task Main(string[] args)
        {
            DbContextOptions&lt;CarContext&gt; _options = new DbContextOptionsBuilder&lt;CarContext&gt;()
                    .UseInMemoryDatabase(&quot;CarsDataBase&quot;)
                    .Options;

            Car car1 = new Car() { Id = Guid.NewGuid(), Make = &quot;Volvo&quot;, Model = &quot;VC90&quot;, Time = DateTime.Now, Color = &quot;Blue&quot; };
            Car car2 = new Car() { Id = Guid.NewGuid(), Make = &quot;Volvo&quot;, Model = &quot;VC90&quot;, Time = DateTime.Now, Color = &quot;Green&quot; };
            Car car3 = new Car() { Id = Guid.NewGuid(), Make = &quot;BMW&quot;, Model = &quot;M3&quot;, Time = DateTime.Now, Color = &quot;Red&quot; };
            Car car4 = new Car() { Id = Guid.NewGuid(), Make = &quot;Ford&quot;, Model = &quot;Mustang&quot;, Time = DateTime.Now, Color = &quot;Orange&quot; };

            using (var context = new CarContext(_options))
            {
                await context.Cars.AddAsync(car1);
                await context.Cars.AddAsync(car2);
                await context.Cars.AddAsync(car3);
                await context.Cars.AddAsync(car4);

                await context.SaveChangesAsync();
            }

            using (var context = new CarContext(_options))
            {
                var cars = context.Cars.GroupBy(o =&gt; new { o.Make, o.Model })
                    .Select(n =&gt; n.OrderByDescending(c =&gt; c.Time).First())
                    .ToList();
            }
        }
     }
}
</code></pre>
<p>I get this error:</p>
<pre><code>System.InvalidOperationException   HResult=0x80131509   Message=The LINQ expression 'GroupByShaperExpression: KeySelector: new { 
    Make = ExpressionExtensions.ValueBufferTryReadValue&lt;string&gt;(
        valueBuffer: grouping.Key, 
        index: 0, 
        property: Property: Car.Make (string)), 
    Model = ExpressionExtensions.ValueBufferTryReadValue&lt;string&gt;(
        valueBuffer: grouping.Key, 
        index: 1, 
        property: Property: Car.Model (string))  },  ElementSelector:EntityShaperExpression: 
    EntityType: Car
    ValueBufferExpression: 
        ProjectionBindingExpression: EmptyProjectionMember
    IsNullable: False

    .OrderByDescending(c =&gt; c.Time)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.  Source=Microsoft.EntityFrameworkCore.InMemory   StackTrace:    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryExpressionTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)    at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)    at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryExpressionTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)    at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)    at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryExpressionTranslatingExpressionVisitor.TranslateInternal(Expression expression)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryExpressionTranslatingExpressionVisitor.Translate(Expression expression)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryProjectionBindingExpressionVisitor.Visit(Expression expression)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryProjectionBindingExpressionVisitor.Translate(InMemoryQueryExpression queryExpression, Expression expression)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)    at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)    at Microsoft.EntityFrameworkCore.InMemory.Query.Internal.InMemoryQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)    at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)    at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)    at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)    at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)    at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)    at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0() at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)    at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)    at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)    at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetEnumerator() at System.Collections.Generic.List`1..ctor(IEnumerable`1 collection)   at System.Linq.Enumerable.ToList[TSource](IEnumerable`1 source)    at TestEntityFramework.Program.&lt;Main&gt;d__2.MoveNext() in C:\Apps\TestEntityFramework\Program.cs:line 52
</code></pre>

## Answers
### Answer ID: 71466365
<p>EF Core 6 should handle your query. For EF Core 5, use the following emulation which is close what EF Core 6 do internally:</p>
<pre class="lang-cs prettyprint-override"><code>using (var context = new CarContext(_options))
{
    var query = context.Cars;

    var carQuery = 
        from d in query.Select(o =&gt; new { o.Make, o.Model }).Distinct()
        from car in query
            .Where(car =&gt; car.Make == d.Make &amp;&amp; car.Model == d.Model)
            .OrderByDescending(car =&gt; car.Time)
            .Take(1)
        select car;

    var cars = carQuery.ToList();
}
</code></pre>

