# Break out part of linq-to-sql expression to a separate function
[Link to question](https://stackoverflow.com/questions/7945685/break-out-part-of-linq-to-sql-expression-to-a-separate-function)
**Creation Date:** 1319987288
**Score:** 2
**Tags:** c#, .net, linq-to-sql
## Question Body
<p>I have two entity classes:</p>

<pre><code>public class Invoice
{
  public int ID { get; set;}
  public int Amount { get { return InvoiceLines.Sum(il =&gt; il.Amount); }}
  public EntitySet&lt;InvoiceLines&gt; InvoiceLines {get;set;};
}

public class InvoiceLine
{
  public Invoice Invoice {get;set;}
  public int InvoiceID {get;set;}
  public int Amount {get;set;}
  public string SomeHugeString {get;set;}
}
</code></pre>

<p>(The real classes are sqlmetal generated, I shortened it down here to get to the point).</p>

<p>Querying for all amounts:</p>

<pre><code>var amounts = from i in invoice select i.Amount;
</code></pre>

<p>This will cause all invoicelines to be lazy loaded with one database call per invoice. I can solve it with data load options, but that would cause the entire InvoiceLine objects to be read, including <code>SomeHugeString</code>.</p>

<p>Repeating the amount calculation in the query will get a good SQL translation:</p>

<pre><code>var amounts = from i in invoice select i.InvoiceLines.Sum(il =&gt; il.Amount);
</code></pre>

<p>I sould like to have linq-to-sql somehow get part of the expression tree from a function/property. Is there a way to rewrite <code>Invoice.Amount</code> so that the first amounts query will give the same SQL translation as the second one?</p>

## Answers
### Answer ID: 7947593
<p>I'd suggest you set the 'SomeHugeString' property to be lazy loaded. This way you can load <code>InvoiceLine</code> without getting that huge string, which means you can use <code>DataLoadOptions.LoadWith()</code>:</p>

<p><img src="https://i.sstatic.net/1dMTS.png" alt="Set a single property to be delay loaded by right clicking it, selecting properties and then setting the Delay Loaded property to True"></p>

### Answer ID: 7947533
<p>You can create your own functions using <code>IQueryable</code> interface.</p>

<p>I've used standard NorthWind DB:</p>

<pre><code>public static class LinqExtensions
{
    public static IQueryable&lt;int&gt; CalculateAmounts(this IQueryable&lt;Order&gt; order)
    {
        return from o in order select o.Order_Details.Sum(i =&gt; i.Quantity);
    }
}

var amounts = (from o in context.Orders select o).CalculateAmounts();
</code></pre>

<p>This code generates such SQL:</p>

<pre><code>SELECT [t2].[value]
FROM [dbo].[Orders] AS [t0]
OUTER APPLY (
    SELECT SUM(CONVERT(Int,[t1].[Quantity])) AS [value]
    FROM [dbo].[Order Details] AS [t1]
    WHERE [t1].[OrderID] = [t0].[OrderID]
    ) AS [t2]
</code></pre>

### Answer ID: 7946021
<p>You can do something similar using <code>AsExpandable()</code> from <a href="http://www.albahari.com/nutshell/linqkit.aspx" rel="nofollow">LINQKit</a>:</p>

<pre><code>Expression&lt;Func&lt;Invoice, int&gt;&gt; getAmount =
    i =&gt; i.InvoiceLines.Sum(il =&gt; il.Amount);

var amounts = from i in invoice.AsExpandable() select getAmount.Invoke(i);
</code></pre>

