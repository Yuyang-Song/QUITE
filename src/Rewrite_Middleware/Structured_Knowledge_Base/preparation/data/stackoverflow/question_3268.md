# LINQ avoid OUTER APPLY Oracle 11g
[Link to question](https://stackoverflow.com/questions/74415752/linq-avoid-outer-apply-oracle-11g)
**Creation Date:** 1668279767
**Score:** 0
**Tags:** c#, oracle-database, linq, devart, dotconnect
## Question Body
<p>When running the LINQ Query below against Oracle 11g instance, it will throw an OUTER APPLY not supported error.</p>
<pre class="lang-cs prettyprint-override"><code>var shipmentDetails = (
    from r in _db.XXF_SHIPMENT_DETAILs 
    where r.SHIP_TO == tradingPartnerId &amp;&amp; r.PICKUP_DATE &gt;= pickUpDate 
    select r)
    .GroupBy(x =&gt; x.HEADERID)
    .Select(x =&gt; x.FirstOrDefault());
</code></pre>
<blockquote>
<p>&quot;OUTER APPLY is not supported by Oracle Database 11g and lower. Oracle
12c or higher is required to run this LINQ statement correctly. If you
need to run this statement with Oracle Database 11g or lower, rewrite
it so that it can be converted to SQL, supported by the version of
Oracle you use.&quot;</p>
</blockquote>

## Answers
### Answer ID: 74416132
<p>You can use the following query which will get latest record from the group:</p>
<pre class="lang-cs prettyprint-override"><code>var filtered = db.XXF_SHIPMENT_DETAILs 
    .Where(r =&gt; r.SHIP_TO == tradingPartnerId &amp;&amp; r.PICKUP_DATE &gt;= pickUpDate);

var grouped = fltered
    .GroupBy(r =&gt; r.HEADERID)
    .Select(g =&gt; new
    {
        HEADERID = g.Key,
        LastId = g.Max(x =&gt; x.Id)
    });

var shipmentDetails = 
    from s in filtered
    join g in grouped on s.LastId equals g.Id
    select s;
</code></pre>
<p>Still not the best as raw SQL and window functions, but should give much better performance than processing data on the client side.</p>

### Answer ID: 74415753
<p>The solution is to use simple statements to achieve the results you are after. Referencing the query above, we...</p>
<p>First, get all the shipments. Use the <code>.ToList()</code> to force query execution</p>
<pre><code>var shipmentDetails = (from r in _db.XXF_SHIPMENT_DETAILs where r.SHIP_TO == tradingPartnerId &amp;&amp; r.PICKUP_DATE &gt;= pickUpDate select r).ToList();
</code></pre>
<p>Now <code>.GroupBy()</code> and <code>.Select()</code> to filter - but this will be done in memory and not at the server level therefore avoiding the unsupported OUTER APPLY</p>
<pre><code>var uniqueShipmentsWithDistinctHeaderIds = shipmentDetails.GroupBy(x =&gt; x.HEADERID).Select(x =&gt; x.FirstOrDefault());
</code></pre>

