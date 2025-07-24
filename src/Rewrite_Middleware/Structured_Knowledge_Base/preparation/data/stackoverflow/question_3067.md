# C# Sql Raw Query to Entity Framework query
[Link to question](https://stackoverflow.com/questions/64910164/c-sql-raw-query-to-entity-framework-query)
**Creation Date:** 1605783100
**Score:** 0
**Tags:** c#, sql, entity-framework-core
## Question Body
<p>I have a group data in my database like that:</p>
<pre><code>Code   ModificationDate
--------------------------
 A     2020/01/02
 A     2020/01/01
 B     2020/01/03
 B     2020/01/01
 C     2020/01/04
 C     2020/01/01
</code></pre>
<p>And I want to get the value with the most recent <code>ModificationDate</code> from each group of codes.</p>
<p>I tried some linq queries, but I always get the same error</p>
<blockquote>
<p>Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable'</p>
</blockquote>
<p>To workaround it, I wrote this code:</p>
<pre><code>var query = _context.Customers.FromSqlRaw(@&quot;
            SELECT t.* FROM(
                  SELECT[Code], MAX([ModificationDate]) as [ModificationDate]
                  FROM[Customers]
                  GROUP BY[Code]
            ) c
            INNER JOIN[Customers] t
            ON t.[Code] = c.[Code] AND t.[ModificationDate] = c.[ModificationDate]&quot;);
</code></pre>
<p>It works fine, but I want to translate it to a linq query that doesn't trigger the mentioned error.</p>
<p>I don't want to use <code>AsEnumerable</code> or <code>ToList</code> because I have a lot of data and load it into memory is going to be slow.</p>

## Answers
### Answer ID: 64965905
<p>Finally i'm using this:</p>
<pre><code>IQueryable&lt;Customer&gt; query =
           from c in _context.Customers.GroupBy(a =&gt; a.Code).Select(a =&gt; a.Max(a =&gt; a.ModificationDate))
           from s in _context.Customers
           where c == s.ModificationDate
           select s;
</code></pre>
<p>This works fine</p>

### Answer ID: 64911187
<p>This exception occurs frequently with <code>GroupBy</code> in EF core 3/5. In your case there is way to make EF happy by following this query pattern (based on the Chinook sample database, not knowing your class model):</p>
<pre class="lang-cs prettyprint-override"><code>from c in Customers
from i in c.Invoices.OrderByDescending(i =&gt; i.InvoiceDate).Take(1)
select new 
{
    c.LastName,
    i.BillingAddress
}
</code></pre>
<p>This is even the preferred query pattern, even failing sufficient <code>GroupBy</code> support, because (at least in Sql Server, maybe other providers too), EF translates <code>Take</code> into the efficient <code>ROW_NUMBER() OVER(PARTITION BY ...)</code> construct in SQL. The LINQ query above is translated to this SQL statement in EF-core 3.1.10:</p>
<pre><code>SELECT [c].[LastName], [t0].[BillingAddress]
FROM [Customer] AS [c]
INNER JOIN (
    SELECT [t].[InvoiceId], [t].[BillingAddress], [t].[BillingCity], [t].[BillingCountry], [t].[BillingPostalCode], [t].[BillingState], [t].[CustomerId], [t].[InvoiceDate], [t].[Total]
    FROM (
        SELECT [i].[InvoiceId], [i].[BillingAddress], [i].[BillingCity], [i].[BillingCountry], [i].[BillingPostalCode], [i].[BillingState], [i].[CustomerId], [i].[InvoiceDate], [i].[Total]
    , ROW_NUMBER() OVER(PARTITION BY [i].[CustomerId] ORDER BY [i].[InvoiceDate] DESC) AS [row]
        FROM [Invoice] AS [i]
    ) AS [t]
    WHERE [t].[row] &lt;= 1
) AS [t0] ON [c].[CustomerId] = [t0].[CustomerId]
</code></pre>
<p>It's a bit disappointing, though, that EF doesn't reduce the fields in the subquery according to the properties requested in the LINQ query. That could be achieved by a query like this:</p>
<pre class="lang-cs prettyprint-override"><code>from c in Customers
from i in c.Invoices.OrderByDescending(i =&gt; i.InvoiceDate)
    .Select(i =&gt; new { i.BillingAddress, i.BillingCity })
    .Take(1)
select new 
{
    c.LastName,
    i.BillingAddress,
    i.BillingCity
}
</code></pre>
<p>...unfortunately causing some code repetition.</p>

