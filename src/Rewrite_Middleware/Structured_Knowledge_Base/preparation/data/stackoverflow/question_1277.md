# Convert Expression&lt;Func&lt;T, bool&gt;&gt; to another Predicate Expression Expression&lt;Func&lt;U, bool&gt;&gt;
[Link to question](https://stackoverflow.com/questions/67884451/convert-expressionfunct-bool-to-another-predicate-expression-expressionfun)
**Creation Date:** 1623142436
**Score:** 1
**Tags:** linq, c#-4.0, entity-framework-core, expression-trees, ef-core-5.0
## Question Body
<p>I want to convert One predicate Expression(<strong>Expression&lt;Func&lt;Item, bool&gt;&gt;</strong>) to another Predicate Expression (<strong>Expression&lt;Func&lt;ItemEntity, bool&gt;&gt;</strong>) but after converting I am not able to query through LINQ.
I Already try <a href="https://stackoverflow.com/questions/43387196/convert-expressionfunct-u-to-expressionfuncobject-object">this</a> and <a href="https://stackoverflow.com/questions/65035260/convert-expressionfunct1-bool-to-expressionfunct2-bool/65035636#65035636">this</a> approach but nothing work properly
can anyone tells me how to do it properly, My approach for this problems.</p>
<pre><code>using System;
using System.Linq;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Threading.Tasks;
using System.Reflection;

public class ItemEntity {
    public int ItemId {set;get;}
    public int ItemParentId {set;get;}
    public int ItemName {set;get;}
}

public class Item {
   public int Id{ set;get;}
   public int ParentId{set;get;}
   public int Name {set;get;}
}

public class Program
{
    
    public static Item Convert(ItemEntity itemChild)
    {
        return new Item()
        {
            Id = itemChild.ItemId,
            ParentId = itemChild.ItemParentId,
            Name = itemChild.ItemName
        };
    }
    
    public async Task&lt;IList&lt;ItemEntity&gt;&gt; SelectAsync(Expression&lt;Func&lt;ItemEntity, bool&gt;&gt; predicate)
    {
        // using Microsoft.EntityFrameworkCore;
        // private readonly DbContext _context; // Injected globally by using Service.AddScoped&lt;ItemContext&gt;();
        // return await _context.Set&lt;ItemEntity&gt;().AsNoTracking().Where(predicate).ToListAsync();
        return await Task.Run(() =&gt; new List&lt;ItemEntity&gt;()); // actually return the result with matching predicate
    }
    public async Task&lt;List&lt;Item&gt;&gt; GetItems(Expression&lt;Func&lt;Item, bool&gt;&gt; expression)
    {
        
            MethodInfo convertMethod = ((Func&lt;ItemEntity, Item&gt;)Convert).Method;
            
            var p = Expression.Parameter(typeof(ItemEntity));
            var converted = Expression.Lambda&lt;Func&lt;ItemEntity, bool&gt;&gt;(
                Expression.Invoke(expression, Expression.Convert(p, typeof(Item), convertMethod)), p);
            
            IList&lt;ItemEntity&gt; res = await SelectAsync(converted);
            var t = res.Select(x =&gt; Convert(x)).ToList();
            return t;
    }
    
    public static void Main()
    {
        Program pr = new Program();
        Func&lt;Expression&lt;Func&lt;Item, bool&gt;&gt;, Task&lt;List&lt;Item&gt;&gt;&gt; getItem = pr.GetItems;
        var res = getItem.Invoke(x =&gt; x.Id.Equals(1));
        Console.WriteLine(&quot;Hello World&quot;);
    }
}
</code></pre>
<p>but I am getting error</p>
<blockquote>
<p>The LINQ expression 'DbSet()\r\n    .Where(i =&gt; ((Item)i).Id.Equals(__Id_0))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>I don't able to understand it properly, as per my understanding I am using ToList() for client evaluation, but and also provide method to convert ItemEntity to Item.</p>
<p>I any other way to create fresh Expression Tree based on ItemEntity and then query on DBSet?
Any Help is appreciated</p>
<p>version used:</p>
<ul>
<li>dot-net 5.0</li>
<li>Microsoft.EntityFrameworkCore 5.0.6</li>
<li>EntityFramework 6.4.4</li>
<li>Database SQL Server</li>
</ul>

## Answers
### Answer ID: 67900656
<p>Try the following approach. Main idea to use filter exactly on the projected DTO before materialization.</p>
<pre class="lang-cs prettyprint-override"><code>using System;
using System.Collections.Generic;
using System.Linq.Expressions;
using System.Threading.Tasks;

public class ItemEntity
{
    public int ItemId { set; get; }
    public int ItemParentId { set; get; }
    public int ItemName { set; get; }
}

public class Item
{
    public int Id { set; get; }
    public int ParentId { set; get; }
    public int Name { set; get; }
}

public class Program
{
    public static Expression&lt;Func&lt;ItemEntity, Item&gt;&gt; ToItem()
    {
        return itemChild =&gt; new Item
        {
            Id = itemChild.ItemId,
            ParentId = itemChild.ItemParentId,
            Name = itemChild.ItemName
        };
    }

    public Task&lt;IList&lt;Item&gt;&gt; SelectAsync(Expression&lt;Func&lt;Item, bool&gt;&gt; predicate)
    {
        return _context.Set&lt;ItemEntity&gt;()
            .AsNoTracking()
            .Select(ToItem())
            .Where(predicate)
            .ToListAsync();

        //return Task.Run(() =&gt; new List&lt;ItemEntity&gt;().AsQueryable().Select(ToItem()).Where(predicate).ToList());
    }

    public async Task&lt;IList&lt;Item&gt;&gt; GetItems(Expression&lt;Func&lt;Item, bool&gt;&gt; expression)
    {
        var res = await SelectAsync(expression);
        return res;
    }

    public static void Main()
    {
        var pr = new Program();
        var res = pr.GetItems(x =&gt; x.Id == 1);
        Console.WriteLine(&quot;Hello World&quot;);
    }
}
</code></pre>

