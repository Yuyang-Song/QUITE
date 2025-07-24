# Registered conversion for Entity Framework Core in C# is not called when querying with Contains? Any workaround?
[Link to question](https://stackoverflow.com/questions/62817278/registered-conversion-for-entity-framework-core-in-c-is-not-called-when-queryin)
**Creation Date:** 1594305187
**Score:** 0
**Tags:** c#, linq, entity-framework-core, microsoft.data.sqlite
## Question Body
<p>I am trying to figure out why the conversions defined for my <code>SqliteDbContext </code> below are not considered when a <code>Contains</code> is necessary in a request:</p>
<pre class="lang-cs prettyprint-override"><code>public static class FSharpOptionExtensions
{
    public static T DefaultFromOption&lt;T&gt;(this FSharpOption&lt;T&gt; option)
        where T : IEquatable&lt;T&gt; =&gt;
        (FSharpOption&lt;T&gt;.get_IsNone(option)
            ? default
            : option.Value)!;

    public static FSharpOption&lt;T&gt; ToOption&lt;T&gt;(this T source)
        where T : IEquatable&lt;T&gt; =&gt;
        source.Equals(default)
            ? FSharpOption&lt;T&gt;.None
            : FSharpOption&lt;T&gt;.Some(source);
}

public class SqliteDbContext : DbContext
{
    public DbSet&lt;SqliteRecord&gt;? Records { get; set; }

    public SqliteDbContext() // : base()
    {
    }

    public SqliteDbContext(DbContextOptions&lt;SqliteDbContext&gt; options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        var faker = new Faker();
        var recordCount = faker.Random.Int(500, 1000);
        var records = Enumerable
            .Range(1, recordCount)
            .Select(index =&gt; new SqliteRecord
            {
                Id = index,
                Integer = faker.Random.Long(),
                Real = faker.Random.Double(),
                NullableText = faker.Name.FullName().OrNull(faker, .2f),
                NonNullableText = faker.Commerce.Product(),
                FSharpOptionText = FSharpOption&lt;string&gt;.Some(faker.Vehicle.Manufacturer())
                    .OrDefault(faker, 0.5f, FSharpOption&lt;string&gt;.None)
            });

        modelBuilder
            .Entity&lt;SqliteRecord&gt;()
            .Property(x =&gt; x.FSharpOptionText)
            .IsRequired(false)
            .HasConversion(new ValueConverter&lt;FSharpOption&lt;string&gt;?, string&gt;(
                option =&gt; option!.DefaultFromOption(),
                value =&gt; value.ToOption()));

        modelBuilder
            .Entity&lt;SqliteRecord&gt;()
            .HasKey(x =&gt; x.Id);

        modelBuilder
            .Entity&lt;SqliteRecord&gt;()
            .ToTable(&quot;Records&quot;)
            .HasData(records);
    }
}
</code></pre>
<pre class="lang-cs prettyprint-override"><code>var records = await _dbContext.Records.Select(x =&gt; new
{
    Id = x.Id,
    Integer = x.Integer,
    Real = x.Real,
    NullableText = x.NullableText,
    NonNullableText = x.NonNullableText,
    FSharpOptionText = x.FSharpOptionText!.DefaultFromOption()
}).Where(s =&gt;
    s.NullableText!.ToLower().Contains(&quot;d&quot;) ||
    s.NonNullableText!.ToLower().Contains(&quot;d&quot;) ||
    s.FSharpOptionText.ToLower().Contains(&quot;d&quot;)
).ToListAsync();
</code></pre>
<p>I get this error:</p>
<blockquote>
<p>System.InvalidOperationException: The LINQ expression 'DbSet()<br />
.Where(s =&gt; s.NullableText.ToLower().Contains(&quot;d&quot;) || s.NonNullableText.ToLo
wer().Contains(&quot;d&quot;) || s.FSharpOptionText<br />
.DefaultFromOption().ToLower().Contains(&quot;d&quot;))' could not be translated.</p>
<p>Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumer
able(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=</a>
2101038 for more information.</p>
<p>at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVi
sitor.g__CheckTranslated|15_0(ShapedQueryExpression translated,
&lt;&gt;c__DisplayClass15_0&amp; )<br />
at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVi
sitor.VisitMethodCall(MethodCallExpression methodCallExpression)<br />
at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visi
tor)<br />
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVi
sitor.VisitMethodCall(MethodCallExpression methodCallExpression)
at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visi
tor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExe
cutor[TResult](Expression query)
at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expre
ssion query, Boolean async)
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCor
e[TResult](IDatabase database, Expression query, IModel model, Boolean async)
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayCla
ss12_0<code>1.&lt;ExecuteAsync&gt;b__0() at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQu eryCore[TFunc](Object cacheKey, Func</code>1 compiler)
at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQu
ery[TResult](Object cacheKey, Func<code>1 compiler) at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TR esult](Expression query, CancellationToken cancellationToken) at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAs ync[TResult](Expression expression, CancellationToken cancellationToken) at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable</code>1.GetAsyncEnu
merator(CancellationToken cancellationToken)
at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable<code>1.GetA syncEnumerator() at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ToListAsy nc[TSource](IQueryable</code>1 source, CancellationToken cancellationToken)</p>
</blockquote>
<p>It doesn't make much sense to me since <a href="https://learn.microsoft.com/en-us/ef/core/modeling/value-conversions" rel="nofollow noreferrer">the conversion is supposed to be applied</a>:</p>
<blockquote>
<p>Value converters allow property values to be converted when reading from or writing to the database. This conversion can be from one value to another of the same type (for example, encrypting strings) or from a value of one type to a value of another type (for example, converting enum values to and from strings in the database.)</p>
</blockquote>
<p>Unless &quot;reading&quot; doesn't apply when &quot;querying&quot; and if that's really the case, wondering if there is any workaround out there? Any mechanism to extend how the expression is parsed?</p>
<hr />
<p>Btw the query below works just fine:</p>
<pre class="lang-cs prettyprint-override"><code>var records = await _dbContext.Records.Select(x =&gt; new
{
    Id = x.Id,
    Integer = x.Integer,
    Real = x.Real,
    NullableText = x.NullableText,
    NonNullableText = x.NonNullableText,
    FSharpOptionText = x.FSharpOptionText!.DefaultFromOption()
}).Where(x =&gt; x.Id == 1).ToListAsync();
</code></pre>
<pre><code>info: Microsoft.EntityFrameworkCore.Infrastructure[10403]
      Entity Framework Core 5.0.0-preview.6.20312.4 initialized 'SqliteDbContext
' using provider 'Microsoft.EntityFrameworkCore.Sqlite' with options: None
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (2ms) [Parameters=[], CommandType='Text', CommandTimeou
t='30']
      SELECT &quot;r&quot;.&quot;Id&quot;, &quot;r&quot;.&quot;Integer&quot;, &quot;r&quot;.&quot;Real&quot;, &quot;r&quot;.&quot;NullableText&quot;, &quot;r&quot;.&quot;NonNu
llableText&quot;, &quot;r&quot;.&quot;FSharpOptionText&quot;
      FROM &quot;Records&quot; AS &quot;r&quot;
      WHERE &quot;r&quot;.&quot;Id&quot; = 1
</code></pre>

