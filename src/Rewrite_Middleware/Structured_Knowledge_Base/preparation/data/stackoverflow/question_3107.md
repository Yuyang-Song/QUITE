# Query with `groupjoin` cannot be translated although it&#39;s documened as being supported
[Link to question](https://stackoverflow.com/questions/66844615/query-with-groupjoin-cannot-be-translated-although-its-documened-as-being-sup)
**Creation Date:** 1616955001
**Score:** 16
**Tags:** c#, entity-framework-core
## Question Body
<p>I don't understand why this doesn't translate. It seems to be exactly the use case described <a href="https://learn.microsoft.com/en-us/ef/core/querying/complex-query-operators#groupjoin" rel="noreferrer">here</a>.</p>
<p>The LINQ expression</p>
<pre><code>DbSet&lt;A&gt;()
    .GroupJoin(
        inner: DbSet&lt;B&gt;(),
        outerKeySelector: a =&gt; a.AId,
        innerKeySelector: b =&gt; b.AId,
        resultSelector: (a, bs) =&gt; new {
            a = a,
            bs = bs
         })
</code></pre>
<p>produces the error:</p>
<blockquote>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>The LINQ code producing the exception is</p>
<pre class="lang-cs prettyprint-override"><code>from a in ctx.As
    join b in ctx.Bs on a.aId equals b.aId into bs
    select new {A = a, Bs = bs.ToList()};
</code></pre>
<p>Edit: maybe I misunderstood the doc and this is an example of something that does NOT translate.</p>
<blockquote>
<p>Executing a query like the following example generates a result of Blog &amp; IEnumerable. Since databases (especially relational databases) don't have a way to represent a collection of client-side objects, GroupJoin doesn't translate to the server in many cases. It requires you to get all of the data from the server to do GroupJoin without a special selector (first query below). But if the selector is limiting data being selected then fetching all of the data from the server may cause performance issues (second query below). That's why EF Core doesn't translate GroupJoin.</p>
</blockquote>
<p>But then my question becomes instead : <strong>how do I achieve the result I'm looking for without requiring navigational properties ?</strong></p>

## Answers
### Answer ID: 78335437
<p>I encountered the same issue and tried various approaches such as introducing variables, using joins, and different LINQ query syntax, but none of them resolved the issue. Surprisingly, I had successfully used the same group-join LINQ syntax in the past with .NET Framework 4.6, so encountering this problem was unexpected.</p>
<p>To address this issue, I found two potential solutions:</p>
<ol>
<li><p>Sub-query: Although I'm uncertain whether it will be interpreted as a sub-query, you could try structuring the query in a way that resembles a sub-query.</p>
</li>
<li><p><strong>Upgrade to .NET 7</strong> and use EF 7.x: Transitioning to .NET 7 and utilizing EF 7.x could potentially resolve the issue. It's worth noting that according to @ivan-stoev, there might be challenges with early versions of EF 7, but in my experience, using the latest version worked effectively. While Microsoft documentation suggests that EF7 can be used with .NET 6, I had to upgrade other references in our project as well.</p>
</li>
</ol>
<hr />
<h2>My Code Sample 1 [Sub Query]:</h2>
<pre class="lang-cs prettyprint-override"><code>var query =
            from nationalCodeWhiteList in _nationalCodeWhiteListRepository.GetIQueryableAsNoTracking()
            join circulation in _circulationRepository.GetIQueryableAsNoTracking()
                on nationalCodeWhiteList.CrclRow equals circulation.CrclRow
            join announceCar in _announceCarRepository.GetIQueryableAsNoTracking()
                on circulation.AnnounceCarID equals announceCar.Id
            join car in _carRepository.GetIQueryableAsNoTracking()
                on announceCar.CarRow equals car.CarRow
            join onlineShopping in _onlineShoppingRepository.GetIQueryableAsNoTracking()
                on nationalCodeWhiteList.CrclRow equals onlineShopping.CrclRow
            join branch in _branchRepository.GetIQueryableAsNoTracking()
                on new { BranchNo = onlineShopping.BrncNo }
                equals new { BranchNo = branch.BranchCode == null ? (decimal?)null : Convert.ToDecimal(branch.BranchCode) }
                into branches
            from branch in branches.DefaultIfEmpty()

            // ==== NO JOIN IN HERE ====

            join customer in _customerRepository.GetIQueryableAsNoTracking()
                on onlineShopping.IDMember equals customer.Id

            where customer.MeliCode == currentUserNationalCode

            orderby nationalCodeWhiteList.CDate

            select new GetAllCustomerWhiteListRecordsResponseDto_Item_Api
            {
                CDate = nationalCodeWhiteList.CDate,
                CarTitle = car.Title,
                CirculationTitle = circulation.Title,
                RegisteringDate = onlineShopping.CDate,
                BranchNumber = onlineShopping.BrncNo,
                BranchTitle = branch.BrncName,
    
                // ==== SUB-QUERY IN HERE ====

                IsPaidSuccessfully = (from payment in _paymentRepository.GetIQueryableAsNoTracking(null)
                    where payment.HostID == onlineShopping.Id
                    select payment)
                    .Any(w =&gt; w.TransactionCode != null &amp;&amp; w.Status == &quot;00&quot;)
            };
</code></pre>
<hr />
<h2>My Code Sample 2 [Group Join] (EF Core 7^, EF Classic - Framework 4.5^)</h2>
<pre class="lang-cs prettyprint-override"><code>var query =
            from nationalCodeWhiteList in _nationalCodeWhiteListRepository.GetIQueryableAsNoTracking()
            join circulation in _circulationRepository.GetIQueryableAsNoTracking()
                on nationalCodeWhiteList.CrclRow equals circulation.CrclRow
            join announceCar in _announceCarRepository.GetIQueryableAsNoTracking()
                on circulation.AnnounceCarID equals announceCar.Id
            join car in _carRepository.GetIQueryableAsNoTracking()
                on announceCar.CarRow equals car.CarRow
            join onlineShopping in _onlineShoppingRepository.GetIQueryableAsNoTracking()
                on nationalCodeWhiteList.CrclRow equals onlineShopping.CrclRow
            join branch in _branchRepository.GetIQueryableAsNoTracking()
                on new { BranchNo = onlineShopping.BrncNo }
                equals new { BranchNo = branch.BranchCode == null ? (decimal?)null : Convert.ToDecimal(branch.BranchCode) }
                into branches
            from branch in branches.DefaultIfEmpty()

            // ==== GROUP-JOIN IN HERE ====
            
            join payment in _paymentRepository.GetIQueryableAsNoTracking() // 1 to N
                on onlineShopping.Id equals payment.HostID
                into payments
            
            join customer in _customerRepository.GetIQueryableAsNoTracking()
                on onlineShopping.IDMember equals customer.Id

            where customer.MeliCode == currentUserNationalCode

            orderby nationalCodeWhiteList.CDate

            select new GetAllCustomerWhiteListRecordsResponseDto_Item_Api
            {
                CDate = nationalCodeWhiteList.CDate,
                CarTitle = car.Title,
                CirculationTitle = circulation.Title,
                RegisteringDate = onlineShopping.CDate,
                BranchNumber = onlineShopping.BrncNo,
                BranchTitle = branch.BrncName,

                // ==== NO SUB-QUERY IN HERE ====

                IsPaidSuccessfully = payments.Any(w =&gt; w.TransactionCode != null &amp;&amp; w.Status == &quot;00&quot;)
            };
</code></pre>

### Answer ID: 66845729
<p>This functionality has been implemented as of EF Core 7. Not exactly what we wanted (leads to <code>OUTER APPLY</code> in SQL rather than <code>LEFT JOIN</code> as with manual correlated subquery shown below, or collection navigation property), but at least is translated.</p>
<hr />
<p>The explanation in the linked documentation just follows the EF Core team vision and  is ridiculous, because of course it can easily be translated - I had a long discussion with the team here <a href="https://github.com/dotnet/efcore/issues/17068" rel="noreferrer">Query with GroupBy or GroupJoin throws exception #17068</a> and continue here <a href="https://github.com/dotnet/efcore/issues/19930" rel="noreferrer">Query: Support GroupJoin when it is final query operator #19930</a>, trying to convince them why it should be supported, with no luck regardless of the arguments.</p>
<p>The whole point is (and that's the current workaround) it can be processed like if it was correlated subquery (<code>SelectMany</code>), which is translated and processed properly (even though the query result shape has no SQL equivalent.</p>
<p>Anyway, the current status is &quot;Needs Design&quot; (whatever that means), and the workaround is to replace the join with correlated subquery (which is what EF Core is using internally when &quot;expanding&quot; collection navigation properties during the query translation).</p>
<p>In your case, replace</p>
<pre><code>join b in ctx.Bs on a.aId equals b.aId into bs
</code></pre>
<p>with</p>
<pre><code>let bs = ctx.Bs.Where(b =&gt; a.aId == b.aId)
</code></pre>
<hr />
<p>However, I highly recommend adding and using navigation properties. Not sure why you &quot;can't use&quot; them, in LINQ to Entities which do not project entities they serve just metadata for relationships, thus produce automatically the necessary joins. By not defining them you just put on yourself unneeded limitations (additionally to EF Core limitations/bugs). In general EF Core works better and support more things when using navigation properties instead of manual joins.</p>

### Answer ID: 75367742
<p>EF Core will not allow you to do a <code>GroupJoin</code> without following up with a <code>SelectMany</code> in order to flatten the list. The <code>GroupJoin</code> has no equivalent implementation in SQL, however the <code>GroupJoin</code>/<code>SelectMany</code> is equivalent to an inner-join or left-join (depending on if you use <code>DefaultIfEmpty</code>) so it works fine:</p>
<pre><code>context.Users.GroupJoin(
        context.UserRoles,
        u =&gt; u.UserId,
        r =&gt; r.UserId,
        (user, roles) =&gt; new { user, roles })

    //Will not work without this line
    .SelectMany(x =&gt; x.roles.DefaultIfEmpty(), (x, r) =&gt; new { x.user, role = r })
    .ToList();
</code></pre>
<p>If you actually want your results to be grouped (as opposed to trying to do a left-join) you have a few options:</p>
<ol>
<li><p>You can materialize the results of a left join, then group the results in-memory (the code below uses my <code>LeftJoin</code> function shown in <a href="https://stackoverflow.com/questions/3404975/left-outer-join-in-linq/73503586#73503586">LEFT OUTER JOIN in LINQ</a>):</p>
<pre><code>context.Users.LeftJoin(
            context.UserRoles,
            u =&gt; u.UserId,
            r =&gt; r.UserId,
            (user, roles) =&gt; new { user, roles })
        .ToList()
        .GroupBy(x =&gt; x.user, (u, x) =&gt; new
        {
            User = u,
            Roles = x.Select(z =&gt; z.role).Where(r =&gt; r != null).ToList()
        })
        .ToList();
</code></pre>
</li>
<li><p>You can use a sub-query. Note that EF is smart enough to use a left-join when it generates the SQL:</p>
<pre><code>context.Users.Select(u =&gt; new
    {
        User = u,
        Roles = context.UserRoles.Where(r =&gt; r.UserId == u.UserId).ToList()
    })
    .ToList();
</code></pre>
</li>
</ol>
<hr />
<p>If you prefer the <code>GroupJoin</code> syntax, but don't want to have to keep calling all the other functions to flatten, materialize, then re-group the results, you can use my <code>JoinMany()</code> extension method. This method uses the sub-query approach but wraps it in a generic method that looks very similar to the <code>GroupJoin</code> function:</p>
<pre><code>    context.Users.JoinMany(
            context.UserRoles,
            (u, r) =&gt; u.UserId == r.UserId,
            (user, roles) =&gt; new { user, roles })
        .ToList();
</code></pre>
<p>Supporting code:</p>
<pre><code>public static class QueryableExtensions
{
    public static IQueryable&lt;TResult&gt; LeftJoin&lt;TOuter, TInner, TKey, TResult&gt;(
           this IQueryable&lt;TOuter&gt; outer,
           IEnumerable&lt;TInner&gt; inner, Expression&lt;Func&lt;TOuter, TKey&gt;&gt; outerKeySelector,
           Expression&lt;Func&lt;TInner, TKey&gt;&gt; innerKeySelector,
           Expression&lt;Func&lt;TOuter, TInner, TResult&gt;&gt; resultSelector)
    {
        return outer
            .GroupJoin(inner, outerKeySelector, innerKeySelector, (o, i) =&gt; new { o, i })
            .SelectMany(o =&gt; o.i.DefaultIfEmpty(), (x, i) =&gt; new { x.o, i })
            .ApplySelector(x =&gt; x.o, x =&gt; x.i, resultSelector);
    }

    public static IQueryable&lt;TResult&gt; JoinMany&lt;TOuter, TInner, TResult&gt;(
        this IQueryable&lt;TOuter&gt; outers, IQueryable&lt;TInner&gt; inners,
        Expression&lt;Func&lt;TOuter, TInner, bool&gt;&gt; condition,
        Expression&lt;Func&lt;TOuter, IEnumerable&lt;TInner&gt;, TResult&gt;&gt; resultSelector)
    {
        //Use a placeholder &quot;p =&gt; true&quot; expression for the sub-query
        Expression&lt;Func&lt;TOuter, JoinResult&lt;TOuter, IEnumerable&lt;TInner&gt;&gt;&gt;&gt; joinSelector = o =&gt;
            new JoinResult&lt;TOuter, IEnumerable&lt;TInner&gt;&gt; { Outer = o, Inner = inners.Where(p =&gt; true) };

        //Create the where-clause that will be used for the sub-query
        var whereClause = Expression.Lambda&lt;Func&lt;TInner, bool&gt;&gt;(
                        condition.Body.ReplaceParameter(condition.Parameters[0], joinSelector.Parameters[0]),
                        condition.Parameters[1]);

        //Replace the placeholder expression with our new where clause
        joinSelector = Expression.Lambda&lt;Func&lt;TOuter, JoinResult&lt;TOuter, IEnumerable&lt;TInner&gt;&gt;&gt;&gt;(
            joinSelector.Body.VisitExpression(node =&gt;
                (node is LambdaExpression le &amp;&amp; le.Parameters.Count == 1 &amp;&amp; le.Parameters[0].Type == typeof(TInner)
                    &amp;&amp; le.Body is ConstantExpression ce &amp;&amp; ce.Value is bool b &amp;&amp; b)
                    ? whereClause : null),
            joinSelector.Parameters[0]);

        return outers.Select(joinSelector).ApplySelector(x =&gt; x.Outer, x =&gt; x.Inner, resultSelector);
    }

    private static IQueryable&lt;TResult&gt; ApplySelector&lt;TSource, TOuter, TInner, TResult&gt;(
        this IQueryable&lt;TSource&gt; source,
        Expression&lt;Func&lt;TSource, TOuter&gt;&gt; outerProperty,
        Expression&lt;Func&lt;TSource, TInner&gt;&gt; innerProperty,
        Expression&lt;Func&lt;TOuter, TInner, TResult&gt;&gt; resultSelector)
    {
        var p = Expression.Parameter(typeof(TSource), $&quot;param_{Guid.NewGuid()}&quot;.Replace(&quot;-&quot;, string.Empty));
        Expression body = resultSelector?.Body
            .ReplaceParameter(resultSelector.Parameters[0], outerProperty.Body.ReplaceParameter(outerProperty.Parameters[0], p))
            .ReplaceParameter(resultSelector.Parameters[1], innerProperty.Body.ReplaceParameter(innerProperty.Parameters[0], p));
        var selector = Expression.Lambda&lt;Func&lt;TSource, TResult&gt;&gt;(body, p);
        return source.Select(selector);
    }

    public class JoinResult&lt;TOuter, TInner&gt;
    {
        public TOuter Outer { get; set; }
        public TInner Inner { get; set; }
    }
}


public static class ExpressionExtensions
{
    public static Expression ReplaceParameter(this Expression source, ParameterExpression toReplace, Expression newExpression)
        =&gt; new ReplaceParameterExpressionVisitor(toReplace, newExpression).Visit(source);

    public static Expression VisitExpression(this Expression source, Func&lt;Expression, Expression&gt; onVisit)
        =&gt; new DelegateExpressionVisitor (onVisit).Visit(source);
}

public class DelegateExpressionVisitor : ExpressionVisitor
{
    Func&lt;Expression, Expression&gt; OnVisit { get; }

    public DelegateExpressionVisitor(Func&lt;Expression, Expression&gt; onVisit)
    {
        this.OnVisit = onVisit;
    }

    public override Expression Visit(Expression node)
    {
        return OnVisit(node) ?? base.Visit(node);
    }
}

public class ReplaceParameterExpressionVisitor : ExpressionVisitor
{
    public ParameterExpression ToReplace { get; }
    public Expression ReplacementExpression { get; }

    public ReplaceParameterExpressionVisitor(ParameterExpression toReplace, Expression replacement)
    {
        this.ToReplace = toReplace;
        this.ReplacementExpression = replacement;
    }

    protected override Expression VisitParameter(ParameterExpression node)
        =&gt; (node == ToReplace) ? ReplacementExpression : base.VisitParameter(node);
}
</code></pre>

### Answer ID: 66845654
<p>Try this query, it should work with EF Core:</p>
<pre class="lang-cs prettyprint-override"><code>var query =
    from a in ctx.As
    select new {A = a, Bs = ctx.Bs.Where(b =&gt; b.Id == a.aId).ToList()};
</code></pre>

### Answer ID: 66844819
<p>Probably the <code>.ToList()</code> cannot be translated. Use include instead</p>
<pre><code>var result = ctx.As
    .Include(a =&gt; a.Bs)
    .ToList();
</code></pre>
<p>Where you must have a navigation property for the Bs in the A class:</p>
<pre class="lang-cs prettyprint-override"><code>public class A
{
    public int aId { get; set; }
    public List&lt;B&gt; Bs { get; set; }
}
</code></pre>
<p>See:</p>
<ul>
<li><a href="https://learn.microsoft.com/en-us/ef/core/querying/related-data/eager" rel="nofollow noreferrer">Eager Loading of Related Data</a></li>
<li><a href="https://learn.microsoft.com/en-us/ef/core/modeling/relationships?tabs=fluent-api%2Cfluent-api-simple-key%2Csimple-key" rel="nofollow noreferrer">Relationships - EF Core</a></li>
</ul>

