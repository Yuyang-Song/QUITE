# Linq to Sql with the And operator on the same field
[Link to question](https://stackoverflow.com/questions/2418308/linq-to-sql-with-the-and-operator-on-the-same-field)
**Creation Date:** 1268236436
**Score:** 4
**Tags:** sql, linq
## Question Body
<p>I have the following linq query (applied to the Northwind database)</p>

<pre><code>(from od in OrderDetails
where od.ProductID == 11 || od.ProductID == 42
select od.OrderID).Distinct()
</code></pre>

<p>Which gives me a list of Order Ids (67 items) where the order includes either product 11 or 42. How can I rewrite the query to give me a list of Order Ids where the order <strong>includes both product 11 and 42</strong>? The resulting list should only feature one order (orderid = 10248)</p>

<p>Obviously the following query does not return any orders.</p>

<pre><code>(from od in OrderDetails
    where od.ProductID == 11 &amp;&amp; od.ProductID == 42
    select od.OrderID).Distinct()
</code></pre>

<p>Here is a sql query that does the job but what is the best (or most efficient) way of writing it in linq?</p>

<pre><code>    SELECT DISTINCT OrderID
    FROM         [Order Details]
    WHERE     (OrderID IN
                              (SELECT     OrderID
                                FROM          [Order Details] AS OD1
                                WHERE      (ProductID = 11))) AND (OrderID IN
                              (SELECT     OrderID
                                FROM          [Order Details] AS OD2
                                WHERE      (ProductID = 42)))
</code></pre>

<p>[edit]</p>

<p>Thanks to klausbyskov for his solution. From that i was able to build an expression (using PredicateBuilder) that can take a dynamic list of product ids, use them in the where clause and return a list of orders. Here it is if anyone is interested.</p>

<pre><code>public static Expression&lt;Func&lt;Order, bool&gt;&gt; WhereProductIdListEqualsAnd( int[] productIds )
{
    var condition = PredicateBuilder.True&lt;Order&gt;();

    foreach ( var id in productIds )
    {
        condition = condition.And( o =&gt; o.OrderDetails.Any( od =&gt; od.ProductId == id ) );
    }

    return condition;
}
</code></pre>

## Answers
### Answer ID: 2418464
<p>Start the query on the order relation instead:</p>

<pre><code>var result = Orders.Where(o =&gt; o.OrderDetails.Any(od =&gt; od.ProductId == 11) 
                            &amp;&amp; o.OrderDetails.Any(od =&gt; od.ProductId == 42));
</code></pre>

### Answer ID: 2418374
<p>You could simplify this into one query of course, but this would work:</p>

<pre><code>var o1 = OrderDetails.Where( od =&gt; od.ProductID == 11).Select( od =&gt; od.OrderID );
var o2 = OrderDetails.Where( od =&gt; od.ProductID == 42).Select( od =&gt; od.OrderID );
var intersection = o1.Intersect(o2);
</code></pre>

<p>Another (possibly more efficient) way of doing it would be via a join:</p>

<pre><code>(from o1 in OrderDetails
join o2 in OrderDetails on o1.OrderID equals o2.OrderID
where o1.ProductID == 11 and o2.ProductID == 42
select o1.OrderID).Distinct()
</code></pre>

