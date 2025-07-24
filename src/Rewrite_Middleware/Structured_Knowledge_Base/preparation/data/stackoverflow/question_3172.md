# How can I replace the $filter of a DataServiceQuery?
[Link to question](https://stackoverflow.com/questions/69934121/how-can-i-replace-the-filter-of-a-dataservicequery)
**Creation Date:** 1636660276
**Score:** 0
**Tags:** c#, wcf-data-services
## Question Body
<p>Lets say I have a query like this :</p>
<pre><code>DataServiceQuery&lt;Order&gt; selectedOrders = context.Orders
    .AddQueryOption(&quot;$filter&quot;, &quot;Freight gt 30&quot;)
    .AddQueryOption(&quot;$orderby&quot;, &quot;OrderID desc&quot;);
</code></pre>
<p>I would like to append something like this using an <code>IQueryable&lt;Order&gt;</code></p>
<pre><code>.Where(o =&gt; o.OrderID &gt; 10)
</code></pre>
<p>Is there a way this can be accomplished easily?</p>
<p>In my actual real-world scenario, both the existing Select/Expands and the <code>.Where</code> that is getting appended can be rather complex and I do not wish to attempt rewriting them with <code>.AddQueryOption</code> or Expressions. There are also a lot of them (it's for all the reports in our system), and the actual filter being added using <code>AddQueryOption</code> will be using a dynamic property name although the logic behind it should be the same.</p>
<p>I found I can cast the <code>IQueryable</code> to a <code>DataServiceQuery</code> as well and extract the <code>$filter</code> portion, but don't know how to alter/append it.</p>
<pre><code>IQueryable&lt;Order&gt; orders = context.Orders
    .Where(o =&gt; o.OrderID &gt; 10);

var dataServiceQuery = (DataServiceQuery&lt;Order&gt;)orders;
var filter = System.Web.HttpUtility.ParseQueryString(dataServiceQuery.RequestUri.Query)[&quot;$filter&quot;];

// How do I change the filter to append &quot; and Freight gt 30&quot;?
</code></pre>
<p>I feel this should be something easy, but I'm still fairly to working with <code>DataServiceQuery</code> and my google skills are failing me.</p>

