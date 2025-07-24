# Filter a DbSet by the content of an IList using LINQ
[Link to question](https://stackoverflow.com/questions/60775161/filter-a-dbset-by-the-content-of-an-ilist-using-linq)
**Creation Date:** 1584710918
**Score:** 2
**Tags:** c#, linq, asp.net-core, razor-pages
## Question Body
<p>I have 2 ILists Suppliers and VwSrmAhmSuppliers. They are both queried from a database. I first fill Suppliers. Then, when I'm querying VwSrmAhmSuppliers, I want to filter the results based on what I've already pulled in Suppliers.</p>

<pre><code>public IList&lt;Supplier&gt; Suppliers { get;set; }
public IList&lt;Models.ExternalData.VwSrmAhmSupplier&gt; VwSrmAhmSuppliers { get; set; }

public async Task OnGetAsync(Boolean? All)
{
   //don't show all records unless explicity asked to!
   if (All == true)
   {
      Suppliers = await _context.Supplier
         .Include(s =&gt; s.Status)
         .Include(c =&gt; c.Category)
         .Include(c =&gt; c.Comments)
         .OrderByDescending(c =&gt; c.CreateDate)
         .ToListAsync();

      //these do not work
      //VwSrmAhmSuppliers = await _externalcontext.VwSrmAhmSuppliers.Where(d =&gt; Suppliers.Any(s=&gt;s.SupplierNo == d.AhmSupplierNo)).ToListAsync();
      //VwSrmAhmSuppliers = await _externalcontext.VwSrmAhmSuppliers.Where(v =&gt; Suppliers.Any(s=&gt; s.SupplierNo.Equals(v.AhmSupplierNo))).ToListAsync();

      //This does work, it gets all suppliers but it's too many
      //VwSrmAhmSuppliers = await _externalcontext.VwSrmAhmSuppliers.ToListAsync();


      VwSrmAhmSuppliers = await _externalcontext.VwSrmAhmSuppliers
         .Where(v =&gt; Suppliers
            .Any(s =&gt; s.SupplierNo == v.AhmSupplierNo))
         .ToListAsync();
   }
}
</code></pre>

<p>The error generated is:</p>

<blockquote>
  <p>InvalidOperationException: The LINQ expression
  'DbSet .Where(v => __Suppliers_0 .Any(s =>
  s.SupplierNo == v.AhmSupplierNo))' could not be translated. Either
  rewrite the query in a form that can be translated, or switch to
  client evaluation explicitly by inserting a call to either
  AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See
  <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>

<p>And it is not clear to me.</p>

## Answers
### Answer ID: 60775288
<p>You need to project out an in-memory collection of simple reference types first (<code>int</code>, <code>string</code> etc.), rather than a list of type <code>Supplier</code>, then use that for your <code>Any</code> or <code>Contains</code> condition, e.g:</p>

<pre><code>Suppliers = await _context.Supplier
         .Include(s =&gt; s.Status)
         .Include(c =&gt; c.Category)
         .Include(c =&gt; c.Comments)
         .OrderByDescending(c =&gt; c.CreateDate)
         .ToListAsync();

//Project out the required references
var supplierNos = Suppliers.Select(s =&gt; s.SupplierNo).ToList();

//Use the simple reference type collection in your query
VwSrmAhmSuppliers = await _externalcontext.VwSrmAhmSuppliers
    .Where(d =&gt; supplierNos.Any(s=&gt; s == d.AhmSupplierNo)).ToListAsync();

</code></pre>

