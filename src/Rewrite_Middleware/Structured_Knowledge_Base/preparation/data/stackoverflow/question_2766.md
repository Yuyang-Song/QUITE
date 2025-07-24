# How to get the list of objects that have just been inserted into the table in the entity framework
[Link to question](https://stackoverflow.com/questions/51761407/how-to-get-the-list-of-objects-that-have-just-been-inserted-into-the-table-in-th)
**Creation Date:** 1533800575
**Score:** 0
**Tags:** c#, performance, entity-framework
## Question Body
<blockquote>
  <p>The best way to get object list has just been inserted into the
  database?</p>
</blockquote>

<p>I have the code to add a new object list to the database, I want to retrieve the list of objects without having to select again from the database.</p>

<p>I expect something like <code>insert</code> in the SQL Server trigger.</p>

<p>Here is my code snippet.</p>

<pre><code>        List&lt;string&gt; productNames = new List&lt;string&gt;();

        foreach (var name in productNames)
        {
            var product = new Product {Name = name, Color = "something", Body="something body" };
            DbContext.Products.Add(product);
        }

        DbContext.SaveChanges();

        var result = ListProductsInserted; // I want to get list product
</code></pre>

<blockquote>
  <p>I do not want to rewrite the query to retrieve data from the database
  again.</p>
</blockquote>

<p>Is there a better way?</p>

## Answers
### Answer ID: 51761450
<p>If I understaood your question properly, Use code below</p>

<pre><code>List&lt;string&gt; productNames = new List&lt;string&gt;();
List&lt;Product&gt; holdProducts = new List&lt;Product&gt;();
foreach (var name in productNames)
{
    var product = new Product {Name = name, Color = "something", Body="something body" };
    DbContext.Products.Add(product);
    holdProducts.Add(product);
}
DbContext.SaveChanges();
var result = holdProducts; 
</code></pre>

### Answer ID: 51761545
<p>The easiest way for you would be <a href="https://msdn.microsoft.com/en-us/library/system.data.entity.infrastructure.dbentityentry.reload(v=vs.113).aspx#M:System.Data.Entity.Infrastructure.DbEntityEntry.Reload" rel="nofollow noreferrer">DbEntityEntry.Reload()</a></p>

<p>you can use it like this:</p>

<pre><code>yourContext.Entry(yourEntity).Reload();
</code></pre>

