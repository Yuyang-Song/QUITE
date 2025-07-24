# how to use the result of a groupby query into another query?
[Link to question](https://stackoverflow.com/questions/70446599/how-to-use-the-result-of-a-groupby-query-into-another-query)
**Creation Date:** 1640164155
**Score:** 0
**Tags:** c#, entity-framework, linq
## Question Body
<p>I have a fairly simple problem, I think. I want to use the result of a LINQ query with some kind of groupby in another query, but I cannot figure this out.
I have a database with a Company table, an Office table, a Department table and an OrderDetails table. Companies have offices, offices have departments. Orders are registered by department, but I need them by office (per date).</p>
<p>These are my models:</p>
<pre><code>public class Company
{
    public string Name { get; set; }
    public int Id { get; set; }
    public IEnumerable&lt;Office&gt; offices { get; set; }
}

public class Office
{
    public string Name { get; set; }
    public int NumberOfEmployees { get; set; }
    public IEnumerable&lt;Order&gt; ordersPerDate { get; set; }
}

public class Order
{
    public int OfficeId;
    public DateTime Date { get; set; }
    public Size Size { get; set; }         
    public IEnumerable&lt;OrderDetail&gt; Details { get; set; }
}
</code></pre>
<p>I want to make a collection of companies. Every company has a lists of offices and in that list I want another list with all orders on the same Date that belong to that office.
So first I create a collection of orders per date, per office:</p>
<pre><code>//Orders are registred by department, but I need them by office (per date)
var orderDetails = _context.TblOrderDetails
                 .Join(_context.TblDepartments, p =&gt; p.TblDepartmentId, department =&gt; department.Id, (p, department) =&gt; new { p, department })
                 .Join(_context.TblOffices, department2 =&gt; department2.department.TblOfficeId, office =&gt; office.Id, (department2, office) =&gt; new { department2, office })
                 .GroupBy(x =&gt; new { x.office.Id, x.department2.p.OrderDate.Date })
                 .Select(output =&gt; new Order
                 {
                     OfficeId = output.Key.Id,
                     Date = output.Key.Date,
                     Size = new Size
                     {
                         Unknown = output.Sum(s =&gt; s.department2.p.QuantityTotal1),
                         Large = output.Sum(s =&gt; s.department2.p.QuantityTotal2),
                         Medium = output.Sum(s =&gt; s.department2.p.QuantityTotal3),
                         Small = output.Sum(s =&gt; s.department2.p.QuantityTotal4),
                         Other = output.Sum(s =&gt; s.department2.p.QuantityTotal5)
                     },
                     Details = new List&lt;OrderDetail&gt;()
                 }).ToList();
</code></pre>
<p>Now I want to use these <code>orderDetails</code> in another query and I cannot figure out how I have to do this. So far I've came up with 3 &quot;solutions&quot;, but they all fail.</p>
<pre><code>var companyData = _context.TblCompanies
    .Include(&quot;TblOffices&quot;)
    .Where(x =&gt; x.TblOffices.Any(x =&gt; x.Description.Length &gt; 0))
    .Select(company =&gt; new Company
    {
        Name = company.CompanyName,
        Id = company.Id, 
        //list of offices
        offices = company.TblOffices
        .Select(office =&gt; new Office
        {
            Name = office.Description,
            NumberOfEmployees = 30,

            //solution 1: error: Processing of the LINQ expression [..]  by 'NavigationExpandingExpressionVisitor' failed. This may indicate either a bug or a limitation in EF Core
            //ordersPerDate = _context.TblOffices
            //                .Where(off =&gt; off.Id == office.Id)
            //                .Join(orderDetails, of =&gt; of.Id, od =&gt; od.OfficeId, (of, od) =&gt; new Order 
            //                { 
            //                OfficeId = od.OfficeId,
            //                Date = od.Date,
            //                Size = new Size(),  // to be filled in
            //                Details = new List&lt;OrderDetail&gt;() // to be filled in                                    
            //                }).ToList()

            //solution 2: error: Object reference not set to an instance of an object
            //ordersPerDate = orderDetails.ToList().Where(od =&gt; od.OfficeId == office.Id).Select(output =&gt; new Order
            //{
            //OfficeId = output.OfficeId,
            //Date = output.Date,
            //Size = new Size(),  // to be filled in
            //Details = new List&lt;OrderDetail&gt;() // to be filled in 
            //}).ToList()

            //solution 3:  System.Private.CoreLib: Exception while executing function: Test. System.Linq.Expressions: When called from 'VisitLambda', rewriting a node of type 'System.Linq.Expressions.ParameterExpression' must return a non-null value of the same type. Alternatively, override 'VisitLambda' and change it to not visit children of this type.
            ordersPerDate = ( orderDetails.Where(od =&gt; od.OfficeId == office.Id) == null ) ? new List&lt;Order&gt; () : orderDetails.Where(od =&gt; od.OfficeId == office.Id).ToList()

            //maybe use an empty list and fill it later (but how?)
            //ordersPerDate = new List&lt;Order&gt;()
        
        }).ToList()
    }).ToList();

</code></pre>
<p>How can I solve this problem?</p>
<p><strong>edit</strong></p>
<p>fixed it by creating an empty orderlist in the companyData projection:</p>
<pre><code>ordersPerDate = new List&lt;Order&gt;()
</code></pre>
<p>and do this after the LINQ query:</p>
<pre><code>foreach (var company in companyData)
{
    foreach (var c in company.offices)
        c.ordersPerDate = orderDetails.Where(x =&gt; x.OfficeId == c.Id).ToList();                
}
</code></pre>
<p>But I would like to know if this is possible in the same query.</p>
<p><strong>edit2</strong></p>
<p>I'm working with EF Core 3. When I use this line in the &quot;var companyData&quot; query to add the orders:</p>
<pre><code> ordersPerDate = orderDetails.Where(od =&gt; od.OfficeId == office.Id).ToList()
</code></pre>
<p>I get this error: &quot;<em>System.Private.CoreLib: Exception while executing function: Test. Core Microsoft SqlClient Data Provider: Column 'TblPurchaseOrderDetails.ID' is invalid in the select list because it is not contained in either an aggregate function or the GROUP BY clause.</em>&quot;</p>
<p>When I switch to EF Core 5 the errormessage changes to: &quot;<em>System.InvalidOperationException: 'Unable to translate collection subquery in projection since it uses 'Distinct' or 'Group By' operations and doesn't project key columns of all of
it's tables which are required to generate results on client side. Missing column: t.Id. Either add column(s) to the projection or rewrite query to not use 'GroupBy'/'Distinct' operation.</em>'&quot;</p>

