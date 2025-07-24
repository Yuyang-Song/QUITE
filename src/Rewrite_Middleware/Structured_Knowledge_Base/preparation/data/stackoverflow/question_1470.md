# ASP.NET Core 6 C# Grouping Data Daily ,Monthly ,Yearly based on CreatedDate(DateTime) causing : The LINQ expression could not be translated
[Link to question](https://stackoverflow.com/questions/77310623/asp-net-core-6-c-grouping-data-daily-monthly-yearly-based-on-createddatedate)
**Creation Date:** 1697559147
**Score:** 2
**Tags:** c#, asp.net, linq, entity-framework-core, .net-6.0
## Question Body
<p>I have a method which get data from a SQL Server database and groups it daily, monthly and yearly.</p>
<p>We are dealing with a min of 3k records currently and the number increases daily based on sales.</p>
<p>I am trying to get the data and do the group by on database because doing GroupBy on server-memory may be good currently but later it will be very much less efficient but every time I try, I get this error:</p>
<blockquote>
<p>The LINQ expression 'DbSet()\r\n.LeftJoin(\r\ninner: DbSet(), \r\n        outerKeySelector: b =&gt; EF.Property&lt;int?&gt;(b, &quot;CreatedByBusinessCrewId&quot;), \r\n        innerKeySelector: b0 =&gt; EF.Property&lt;int?&gt;(b0, &quot;Id&quot;), \r\n        resultSelector: (o, i) =&gt; new TransparentIdentifier&lt;BusinessSale, BusinessCrew&gt;(\r\n            Outer = o, \r\n            Inner = i\r\n        ))\r\n    .Where(b =&gt; b.Outer.BusinessId == __BusinessId_0 &amp;&amp; b.Inner.BranchId == __BranchId_1)\r\n    .GroupBy(b =&gt; Invoke(__dateTruncateFunction_2, b.Outer.CreateDate.Value)\r\n    )' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>Here are my enums</p>
<pre><code>public enum BusinessSalesFilteredBy
{
    Logs = 0,
    Day = 1,
    Month = 2,
    Year = 3,

}
</code></pre>
<p>Note that I am using unit of work.</p>
<p>Here is my code:</p>
<pre><code>var baseQuery = _uow.BusinessSalesRepo.GetAll(sale =&gt; sale.BusinessId == BusinessId &amp;&amp; sale.CreatedByBusinessCrew.BranchId == BranchId);

salesCount = baseQuery.Count();
clientsCount = baseQuery.Select(s=&gt; s.ClientProfileId).Distinct().Count();
sumPurchases = baseQuery.Sum(s=&gt; s.PurchasedAmount ?? 0);

 Func&lt;DateTime, DateTime&gt; dateTruncateFunction;

    switch (filterBy)
    {
        case (int)BusinessSalesFilteredBy.Day:
            groupKeySelector = sale=&gt; sale.CreateDate.Value.Date;
            break;
        case (int)BusinessSalesFilteredBy.Month:
            groupKeySelector = sale=&gt; new DateTime(sale.CreateDate.Value.Year,   checkin.CreateDate.Value.Month, 1);
            break;
        case (int)BusinessSalesFilteredBy.Year:
            groupKeySelector = sale=&gt; new DateTime(sale.CreateDate.Value.Year, 1, 1);
            break;
        default:
            // Default to daily grouping
            groupKeySelector = sale=&gt; sale.CreateDate.Value.Date;
            break;
    }

    // Now, calculate the summary data with date truncation
var summaryQuery = baseQuery
.GroupBy(sale=&gt; dateTruncateFunction(sale.CreateDate.Value))
                        .Select(grouped =&gt; new
                        {
                            SalesOn = grouped.Key,
                            SalesCount = grouped.Count(),
                            ClientCount = grouped.Select(x =&gt;    x.ClientProfileId).Distinct().Count(),
                            SumPurchases = grouped.Sum(x =&gt; x.PurchasedAmount ?? 0)
                        });
var pagedSummary = await summaryQuery.ToListAsync();
</code></pre>
<p>Finally here is the <code>GetAll()</code> method:</p>
<pre><code>public IQueryable&lt;T&gt; GetAll(Expression&lt;Func&lt;T, bool&gt;&gt; predicate)
{
    return GetAll().Where(predicate);
}

public IQueryable&lt;T&gt; GetAll()
{
    return _context.Set&lt;T&gt;().AsNoTracking();
}
</code></pre>
<p>My question how I can perform the entire operation on the database side without bringing the data into memory hoping of the most efficient way.</p>
<p>And is there no built-in thing that can help in the DateTime translation in LINQ queries?</p>

## Answers
### Answer ID: 77310819
<p>You have to use <code>Expression&lt;Func&lt;,&gt;&gt;</code> to make things work on the server side. Added <code>DateGroupingKey</code>, not sure  how EF will treat <code>DateTime</code> as grouping key.</p>
<pre class="lang-cs prettyprint-override"><code>class DateGroupingKey
{
    public int Year [ get; set; ]
    public int Month [ get; set; ]
    public int Day [ get; set; ]
}
</code></pre>
<pre class="lang-cs prettyprint-override"><code>var baseQuery = _uow.BusinessSalesRepo
    .GetAll(sale =&gt; sale.BusinessId == BusinessId &amp;&amp; sale.CreatedByBusinessCrew.BranchId == BranchId);


Expression&lt;Func&lt;DateTime, DateGroupingKey&gt;&gt; groupKeySelector;

switch (filterBy)
{
    case (int)BusinessSalesFilteredBy.Month:
        groupKeySelector = sale =&gt; new DateGroupingKey { 
            Year = sale.CreateDate.Value.Year, Month = sale.CreateDate.Value.Month 
        }
        break;
    case (int)BusinessSalesFilteredBy.Year:
        groupKeySelector = sale =&gt; new DateGroupingKey { 
            Year = sale.CreateDate.Value.Year 
        }
       break;
    default:
        // Default to daily grouping
        groupKeySelector = sale =&gt; new DateGroupingKey { 
            Year = sale.CreateDate.Value.Year, Month = sale.CreateDate.Value.Month, Day = sale.CreateDate.Value.Day 
        }

      break;
}

ar summaryQuery = baseQuery
    .GroupBy(groupKeySelector)
    .Select(grouped =&gt; new
    {
        SalesOn = grouped.Key,
        SalesCount = grouped.Count(),
        ClientCount = grouped.Select(x =&gt; x.ClientProfileId).Distinct().Count(),
        SumPurchases = grouped.Sum(x =&gt; x.PurchasedAmount ?? 0)
    });
var pagedSummary = await summaryQuery.ToListAsync();
</code></pre>

