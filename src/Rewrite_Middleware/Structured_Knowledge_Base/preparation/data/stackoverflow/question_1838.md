# LINQ throwing Query nested too deeply exception
[Link to question](https://stackoverflow.com/questions/9838717/linq-throwing-query-nested-too-deeply-exception)
**Creation Date:** 1332503585
**Score:** 3
**Tags:** linq, exception, subquery
## Question Body
<p>I have the following class and objects</p>

<pre><code>Product{int ProdId{get; set;}, string ProdDesc{get; set;}}

IQueryable&lt;Product&gt; products = ProductRepository.GetAllProducts();

List&lt;int&gt; filteredProdIds = new List&lt;int&gt;();
</code></pre>

<p>The <code>GetAllProducts()</code> method performs a couple of joins over some <strong>EF classes</strong> and gives back a <code>IQueryable&lt;Product&gt;</code> object. I already tested whether it gives back the expected values and it does.</p>

<p>From <code>products</code> I want to get all the records that have their <code>ProdId</code> in <code>filteredProdIds</code> (assume that <code>filteredProdIds</code> has already been filled with <code>Ids</code>):</p>

<pre><code>products = products.Where(p =&gt; filteredProdIds.Any(fp =&gt; fp.Equals(p.ProdId)));
</code></pre>

<p>Whn I launch my application, it throws an exception </p>

<p><em>Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries.</em></p>

<p>I tried to verify the query with <strong>LINQPad</strong>, by replacing the <code>GetAllProducts()</code> method with an equivalent <strong>database view</strong>, and it works. </p>

<p>What can be the cause of this exception?</p>

<p><strong>UPDATE</strong></p>

<p>filteredProductIds is filled by this method:</p>

<pre><code>IEnumerable&lt;int&gt; filteredProductIds = products.Select(p =&gt; p.partId).Distinct().ToList();
</code></pre>

<p>I found a way to avoid this exception but there must be a much cleaner solution:</p>

<pre><code>foreach (var filteredProdId in filteredProdIds)
{
   product.Union(product.Where(p =&gt; p.ProdId.Equals(filteredProdId)));
}
product.Distinct();
</code></pre>

## Answers
### Answer ID: 9838955
<p>There is a limit to how many items can be within <code>filteredProdIds</code>, since it is a List.</p>

<p>To test you can set <code>filteredProdIds</code> to:</p>

<pre><code>filteredProdIds = filteredProdIds.Take(1).ToList();
</code></pre>

### Answer ID: 9838989
<pre><code>var filteredProdIds = FilterIds().ToArray();
var products = ProductRepository.GetAllProducts().Where(p =&gt; filteredProdIds.Contains(p.ProdId));
</code></pre>

