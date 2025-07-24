# LINQKit + EF Core: Where clause as method error
[Link to question](https://stackoverflow.com/questions/61147833/linqkit-ef-core-where-clause-as-method-error)
**Creation Date:** 1586548920
**Score:** 0
**Tags:** c#, entity-framework, linqkit
## Question Body
<p>I am using LINQKit.Core 1.1.17 and I would like to use my method in Expression Func. My problem is that I am getting error:</p>
<blockquote>
<p>The LINQ expression 'DbSet .Where(v =&gt; TestService.Distance(
x1: __current_X_0,
y1: __current_Y_1,
x2: v.X,
y2: v.Y) &lt; __8__locals1_maxDistance_2)' could not be translated. Either rewrite the query in a form that can be translated, or switch
to client evaluation explicitly by inserting a call to either
AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See
<a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>Here is my code.</p>
<p>Expression:</p>
<pre><code>Expression&lt;Func&lt;Test, bool&gt;&gt; exp = v =&gt; Distance(current.X, current.Y, v.X, v.Y) &lt; maxDistance;
</code></pre>
<p>Distance method:</p>
<pre><code>    private double Distance(int x1, int y1, int x2, int y2)
    {
        var x = Math.Abs(x1 - x2);
        var y = Math.Abs(y1 - y2);

        return Math.Sqrt(x ^ 2 + y ^ 2);
    }
</code></pre>
<p>Is it possible to accomplish that using LINQKit? Are there better ways to query database in that way?</p>

## Answers
### Answer ID: 66650693
<p>You can define this method as marked by <code>ExpandableAttribute</code></p>
<pre class="lang-cs prettyprint-override"><code>public static class HelperFunctions
{
    [Expandable(nameof(DistanceImpl))]
    public static double Distance(int x1, int y1, int x2, int y2)
    {
        var x = Math.Abs(x1 - x2);
        var y = Math.Abs(y1 - y2);

        return Math.Sqrt(x ^ 2 + y ^ 2);
    }

    private static Expression&lt;Func&lt;int, int, int, int, double&gt;&gt; DistanceImpl()
    {
        rerutn (x1, y1, x2, y2) =&gt;
            Math.Sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
    }
}
</code></pre>
<p>Then you can use this function in filters:</p>
<pre class="lang-cs prettyprint-override"><code>var query = query
   .AsExpandable()
   .Where(q =&gt; HelperFunctions.Distance(q.x1, q.y1, q.x2, q.y2) &lt; maxDistance);
</code></pre>
<p>LINQKit will inject lambda body defined in <code>DistanceImpl</code> and make EF LINQ translator happy.</p>

