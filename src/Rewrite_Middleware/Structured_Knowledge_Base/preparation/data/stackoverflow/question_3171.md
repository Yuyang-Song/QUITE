# Where is client evaluation needed?
[Link to question](https://stackoverflow.com/questions/69880186/where-is-client-evaluation-needed)
**Creation Date:** 1636358137
**Score:** 0
**Tags:** entity-framework
## Question Body
<p>I have a query which works fine in Linq to Objects in this <a href="https://dotnetfiddle.net/k19Z9f" rel="nofollow noreferrer">fiddle</a>:</p>
<pre><code>var list = from order in orders
             join detail in details
             on order.id equals detail.order into od
             select new { order = order, details = od };
</code></pre>
<p>I tried applying the same query when the data is in a database (note I am mapping Linq to Sql manually):</p>
<pre><code>public class dbContext: DbContext {
   public DbSet&lt;Order&gt; Orders { get; set; }
   public DbSet&lt;Detail&gt; Details { get; set; }
   protected override void OnConfiguring(DbContextOptionsBuilder oB) {
     oB.UseSqlServer(&quot;...connection string...&quot;);
   }
}

using (var db = new dbContext() {
  var list = from order in db.Orders
               join detail in db.Details
               on order.id equals detail.order into orderDetails
               select new { order = order, details = orderDetails };
}
</code></pre>
<p>The above gives:</p>
<blockquote>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I tried <code>details = orderDetails.ToList()</code> in the last line but the same error is there. Where should I add the manual client evaluation?</p>
<hr />
<p>Some background information: the following database query (without the <code>into</code>) works fine:</p>
<pre><code>var list = from order in db.Orders
            join detail in db.Details
            on order.id equals detail.order
           select new { order = order, detail = detail };
</code></pre>

## Answers
### Answer ID: 69884125
<p>Instead of a join you should declare <a href="https://learn.microsoft.com/en-us/ef/core/modeling/relationships?tabs=fluent-api%2Cfluent-api-simple-key%2Csimple-key" rel="nofollow noreferrer">Navigation Properties</a> and use something like:</p>
<pre><code>var query = from order in db.Orders
  select new { order = order, details = order.OrderDetails };

var list = query.ToList();
</code></pre>
<p>or simply</p>
<pre><code>var list = db.Orders.Include(o =&gt; o.OrderDetails).ToList();
</code></pre>

