# Entity Framework Core `HasConversion` property configuration not used when querying data with postgresql
[Link to question](https://stackoverflow.com/questions/59741856/entity-framework-core-hasconversion-property-configuration-not-used-when-query)
**Creation Date:** 1579036385
**Score:** 5
**Tags:** c#, linq, .net-core, entity-framework-core, npgsql
## Question Body
<p>I am using Entity Framework with Postgre through Npgsql, part of my configuration for the <code>Cashout</code> type which maps to the <code>Cashouts</code> table involves:</p>

<pre class="lang-cs prettyprint-override"><code>public void Configure(EntityTypeBuilder&lt;Cashout&gt; builder)
{
    builder.ToTable("Cashouts");
    builder.ConfigureGuidEntity();

    builder.Property(c =&gt; c.RecipientAccountId).IsRequired();
    builder.Property(c =&gt; c.State).IsRequired().HasConversion(
    v =&gt; v!.Name, 
    v =&gt; Enumeration.FromDisplayName&lt;CashoutState&gt;(v));

    builder.HasIndex(e =&gt; e.State);
    builder.HasIndex(e =&gt; e.RecipientAccountId);

    builder.UseXminAsConcurrencyToken();
}
</code></pre>

<p>The <code>Cashout</code> type is defined as below:</p>

<pre class="lang-cs prettyprint-override"><code>public class Cashout : GuidEntity
{
    public int RecipientAccountId { get; set; }
    public string? RecipientAccountName { get; set; }
    public decimal Amount { get;  set; }
    public string? Comment { get; set; }
    public CashoutState? State { get; set; } = CashoutState.Pending;
    public string? Reason { get; set; }

    public Cashout()
    {
    }

    public Cashout(Guid id)
        : base(id)
    {
    }
}
</code></pre>

<p>and inherits from the <code>GuidEntity</code> type:</p>

<pre class="lang-cs prettyprint-override"><code>public abstract class GuidEntity : Entity&lt;Guid&gt;
{
    protected GuidEntity()
    {
        Id = Guid.Empty;
    }
    protected GuidEntity(Guid id)
    {
        Id = id;
    }

    public DateTimeOffset CreatedOn { get; private set; } = DateTimeOffset.UtcNow;
    public DateTimeOffset? UpdatedOn { get; private set; }
}
</code></pre>

<p>which itself inherits from <code>Entity</code>:</p>

<pre class="lang-cs prettyprint-override"><code>public abstract class Entity&lt;TKey&gt; : IEntity&lt;TKey&gt;, IEquatable&lt;Entity&lt;TKey&gt;&gt;
        where TKey: struct
{
    private readonly Lazy&lt;int&gt; _requestedHashCode;
    private readonly Lazy&lt;int&gt; _requestedTransientHashCode;

    public virtual TKey Id { get; protected set; }

    protected Entity()
    {
        _requestedHashCode = new Lazy&lt;int&gt;(() =&gt; Id.GetHashCode() ^ 31);
        _requestedTransientHashCode = new Lazy&lt;int&gt;(() =&gt; Guid.NewGuid().GetHashCode());
    }

    public bool IsTransient() =&gt;
        EqualityComparer&lt;TKey&gt;.Default.Equals(Id, default);

    public override bool Equals(object obj) =&gt;
        Equals((obj as Entity&lt;TKey&gt;)!);

    public bool Equals(Entity&lt;TKey&gt; other)
    {
        if (other == null)
        {
            return false;
        }

        if (ReferenceEquals(this, other))
        {
            return true;
        }

        if (other.IsTransient() || this.IsTransient())
        {
            return false;
        }

        return EqualityComparer&lt;TKey&gt;.Default.Equals(other.Id, Id);
    }

    public override int GetHashCode() =&gt; IsTransient() ?
        _requestedTransientHashCode.Value :
        _requestedHashCode.Value;
}
</code></pre>

<p>The type of the <code>State</code> property is the <code>CashoutState</code>:</p>

<pre class="lang-cs prettyprint-override"><code>public abstract class CashoutState : Enumeration
{
    public static CashoutState Transferred = new TransferredCashoutState();
    public static CashoutState TransferFailed = new TransferFailedCashoutState();

    public static CashoutState Withdrawn = new WithdrawnCashoutState();
    public static CashoutState WithdrawalFailed = new WithdrawalFailedCashoutState();

    public static CashoutState Pending = new PendingCashoutState();
    public static CashoutState Cancelled = new CancelledCashoutState();

    protected CashoutState(int id, string name)
        : base(id, name) { }

    private class TransferredCashoutState : CashoutState
    {
        public TransferredCashoutState()
            : base(1, nameof(Transferred)) { }
    }

    private class WithdrawnCashoutState : CashoutState
    {
        public WithdrawnCashoutState()
            : base(2, nameof(Withdrawn)) { }
    }

    private class WithdrawalFailedCashoutState : CashoutState
    {
        public WithdrawalFailedCashoutState()
            : base(3, nameof(WithdrawalFailed)) { }
    }

    private class TransferFailedCashoutState : CashoutState
    {
        public TransferFailedCashoutState()
            : base(4, nameof(TransferFailed)) { }
    }

    private class PendingCashoutState : CashoutState
    {
        public PendingCashoutState()
            : base(5, nameof(Pending)) { }
    }

    private class CancelledCashoutState : CashoutState
    {
        public CancelledCashoutState()
            : base(6, nameof(Cancelled)) { }
    }
}
</code></pre>

<p>and then there is yet another bit of inheritance with the <code>Enumeration</code> type:</p>

<pre class="lang-cs prettyprint-override"><code>    public abstract class Enumeration : IComparable
    {
        public string Name { get; private set; }

        public int Id { get; private set; }

        protected Enumeration(int id, string name)
        {
            Id = id;
            Name = name;
        }

        public override string ToString() =&gt; Name;

        public static IEnumerable&lt;T&gt; GetAll&lt;T&gt;() where T : Enumeration =&gt;
            typeof(T)
                .GetFields(BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly)
                .Select(f =&gt; f.GetValue(null)).Cast&lt;T&gt;();

        public override bool Equals(object obj)
        {
            if (!(obj is Enumeration otherValue))
                return false;

            var typeMatches = GetType() == obj.GetType();
            var valueMatches = Id.Equals(otherValue.Id);

            return typeMatches &amp;&amp; valueMatches;
        }

        public override int GetHashCode() =&gt; 
            Id.GetHashCode();

        public static int AbsoluteDifference(Enumeration firstValue, Enumeration secondValue) =&gt;
            Math.Abs(firstValue.Id - secondValue.Id);

        public static T FromValue&lt;T&gt;(int value) where T : Enumeration =&gt;
            Parse&lt;T, int&gt;(value, "value", item =&gt; item.Id == value);

        public static T FromDisplayName&lt;T&gt;(string displayName) where T : Enumeration =&gt;
            Parse&lt;T, string&gt;(displayName, "display name", item =&gt;
                string.Equals(item.Name, displayName, StringComparison.InvariantCultureIgnoreCase));

        private static T Parse&lt;T, TValue&gt;(TValue value, string description, Func&lt;T, bool&gt; predicate) where T : Enumeration =&gt;
            GetAll&lt;T&gt;().FirstOrDefault(predicate) ?? 
            throw new InvalidOperationException($"'{value}' is not a valid {description} in {typeof(T)}");

        public int CompareTo(object obj) =&gt; 
            Id.CompareTo(((Enumeration)obj).Id);
    }
</code></pre>

<p>The configuration works for persisting data:</p>

<pre class="lang-cs prettyprint-override"><code>var cashout = new Cashout
{
    Amount = command.Amount,
    RecipientAccountId = command.RecipientAccountId,
    Comment = command.Comment,
    State = CashoutState.Pending
};  

dbContext.Cashouts.Add(cashout);
dbContext.SaveChanges();
</code></pre>

<p>but when it comes to querying data based on that state, it fails miserably, I tried respectively:</p>

<h1>Querying given a specific state</h1>

<pre class="lang-cs prettyprint-override"><code>var cancelledByState = await _dbContext.Cashouts.Where(x =&gt; x.State == CashoutState.Cancelled).FirstAsync();
</code></pre>

<p>throws: </p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Cashout&gt;
    .Where(c =&gt; c.State.Name == __Cancelled_Name_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to
either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, Expression expression, CancellationToken cancella
tionToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.FirstAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
</code></pre>

<h1>Querying given a specific state name</h1>

<pre class="lang-cs prettyprint-override"><code>var cancelledByStateName = await _dbContext.Cashouts.Where(x =&gt; x.State.Name == CashoutState.Cancelled.Name).FirstAsync();
</code></pre>

<p>throws:</p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Cashout&gt;
    .Where(c =&gt; c.State.Name == __Cancelled_Name_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to
either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, Expression expression, CancellationToken cancella
tionToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.FirstAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
</code></pre>

<h1>Querying given a specific state id</h1>

<pre class="lang-cs prettyprint-override"><code>var cancelledByStateId = await _dbContext.Cashouts.Where(x =&gt; x.State.Id == CashoutState.Cancelled.Id).FirstAsync();
</code></pre>

<p>throws:</p>

<pre><code>System.InvalidOperationException: The LINQ expression 'DbSet&lt;Cashout&gt;
    .Where(c =&gt; c.State.Id == __Cancelled_Id_0)' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to eith
er AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, Expression expression, CancellationToken cancella
tionToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.ExecuteAsync[TSource,TResult](MethodInfo operatorMethodInfo, IQueryable`1 source, CancellationToken cancellationToken)
   at Microsoft.EntityFrameworkCore.EntityFrameworkQueryableExtensions.FirstAsync[TSource](IQueryable`1 source, CancellationToken cancellationToken)
</code></pre>

<p>I would like to find a way to query the <code>DbSet&lt;Cashout&gt;</code> using the state property.</p>

<p>Note 1: it seems that it works like a charm when using the In-memory mode and failed like above whenever the context is bound to an actual postgresql database server.</p>

<p>Note 2: I also created 2 issues on GitHub:</p>

<ul>
<li><a href="https://github.com/dotnet/efcore/issues/19589" rel="nofollow noreferrer">https://github.com/dotnet/efcore/issues/19589</a></li>
<li><a href="https://github.com/npgsql/efcore.pg/issues/1199" rel="nofollow noreferrer">https://github.com/npgsql/efcore.pg/issues/1199</a></li>
</ul>

## Answers
### Answer ID: 78530231
<p>I hope that you already had solved your problem, but after several hours of research i discovered how to fix the LINQ query when use HasConversion. Basicaly you need to do a cast with a primitive type with a implicit operator in you object that you want to convert, see <a href="https://khalidabuhakmeh.com/entity-framework-core-conversions-for-logical-domain-types" rel="nofollow noreferrer">this post</a> for more details.</p>
<p>Now in EF Core 8 have <a href="https://devblogs.microsoft.com/dotnet/announcing-ef8-rc1/" rel="nofollow noreferrer">Complex Types</a> if you need an type more complex.</p>

