# What should I do to be able to test a custom translated function in Sqlite in-memory database?
[Link to question](https://stackoverflow.com/questions/66136119/what-should-i-do-to-be-able-to-test-a-custom-translated-function-in-sqlite-in-me)
**Creation Date:** 1612957053
**Score:** 1
**Tags:** sql-server, sqlite, .net-core, entity-framework-core, in-memory-database
## Question Body
<p>In my team's project, we use sql-server as database and sqlite as integration test's database.</p>
<p>I really want to use  <code>DayOfWeek</code> to group things.
So I created a translation In <code>DBContext</code> class like so</p>
<pre class="lang-cs prettyprint-override"><code>...
public int? DayOfWeek(DateTimeOffset date) =&gt; throw new Exception();
...
protected override void OnModelCreating(ModelBuilder builder)
{
    var DayOfWeekMethodInfo = typeof(DBContext).GetMethod(nameof(DBContext.DayOfWeek));
    if (Database.IsSqlServer())
    {
         builder
             .HasDbFunction(DayOfWeekMethodInfo)
             .HasTranslation(args =&gt; SqlFunctionExpression.Create(&quot;DATEPART&quot;, new[]
             {
                 new SqlFragmentExpression(&quot;weekday&quot;), 
                    args.ToArray()[0]
             }, typeof(int?), null));
    else
    {
         builder
            .HasDbFunction(DayOfWeekMethodInfo)
            .HasTranslation(args =&gt; SqlFunctionExpression.Create(&quot;strftime&quot;, new[]
            {
                new SqlFragmentExpression(&quot;'%w'&quot;),
                    args.ToArray()[0]
            }, typeof(int?), null));
     }
}
</code></pre>
<p>In use:</p>
<pre class="lang-cs prettyprint-override"><code>public IQueryable&lt;TransactionCount&gt; SomeRandomFunction()
{
    return from t in QueryAllTransaction()
           group t by new 
           {
                dayOfWeek = dbConText.DayOfWeek(t.transactionDate)
           }
           into g
           select new TransactionCount
           {
                dayOfWeek = g.Key.dayOfWeek,
                count = g.Count()
           };
}
</code></pre>
<p>When debuging (sql-server), the code is working fine. But in the test, it thrown error</p>
<blockquote>
<p>System.InvalidOperationException : The LINQ expression
'DbSet could not be translated. Either rewrite the query
in a form that can be translated, or switch to client evaluation
explicitly by inserting a call to either AsEnumerable(),
AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>
<p>What should I do to be able to test the function in Sqlite in-memory database?</p>

