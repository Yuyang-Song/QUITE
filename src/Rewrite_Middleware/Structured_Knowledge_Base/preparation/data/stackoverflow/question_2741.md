# Convert SQL to Laravel Eloquent Statement
[Link to question](https://stackoverflow.com/questions/50066008/convert-sql-to-laravel-eloquent-statement)
**Creation Date:** 1524844043
**Score:** 1
**Tags:** laravel, eloquent
## Question Body
<p>I've been working on a few tables where through a rather complex relationship (that I'm trying to clean up, but I still need reports made from the data through my Laravel).</p>

<p>At the moment, I can pull the data using the following SQL query to my MySQL database:</p>

<pre><code>SELECT
customers.id,
customers.customer_name,
SUM(shipments.balance) AS shipmentBalance

FROM customers

LEFT JOIN shipments 
ON customers.id = shipments.bill_to  
AND balance &gt; (SELECT IFNULL(SUM(payments_distributions.amount),0)                
    FROM payments_distributions               
    WHERE payments_distributions.shipment_id = pro_number)
GROUP BY customers.id, customers.customer_name
ORDER BY shipmentBalance DESC
LIMIT 5;
</code></pre>

<p>I'm just not sure how to rewrite it properly into the whereRaw or DB::raw statements that Laravel Eloquent requires, as my previous attempts have failed.</p>

<h2>Update</h2>

<p>Here is the closest solution I have tried:</p>

<pre><code>DB::table('customers')
        -&gt;select('customers', DB::raw('SUM(shipments.balance) AS shipmentBalance'))
        -&gt;leftJoin(
                 DB::raw('
                        (select shipments 
                        ON customers.id = shipments.bill_to
                        AND balance &gt; (SELECT IFNULL(SUM(payments_distributions.amount),0) 
                            FROM payments_distributions 
                            WHERE payments_distributions.shipment_id = pro_number)'))
        -&gt;groupBy('customers.id')
        -&gt;orderByRaw('shipmentBalance DESC')
        -&gt;limit(5)
        -&gt;get();
</code></pre>

<h2>Update 2</h2>

<p>Edit for Dom:</p>

<p>Using everything as it stands with your answer, I get the following response:</p>

<pre><code>SQLSTATE[42S22]: Column not found: 1054 Unknown column '' in 'on clause' (SQL: select customers.id, customers.customer_name,SUM(s.balance) AS shipmentBalance from `customers` left join `shipments` as `s` on `customers`.`id` = `s`.`bill_to` and s.balance &gt; (SELECT IFNULL(SUM(payments_distributions.amount),0) FROM payments_distributions WHERE payments_distributions.shipment_id = s.pro_number) = `` group by `customers`.`id`, `customers`.`customer_name` order by SUM(s.balance) DESC limit 5)
</code></pre>

<p>But if I remove this section, it brings up the page and the customers (though in the wrong order as I have removed one of the necessary components:</p>

<pre><code>$join-&gt;on(DB::raw('s.balance &gt; 
            (SELECT IFNULL(SUM(payments_distributions.amount),0)                
            FROM payments_distributions               
            WHERE payments_distributions.shipment_id = s.pro_number)
                                            ')); 
</code></pre>

<p>Is there anything I can provide you with to get this specific statement to work with your entire answer?</p>

## Answers
### Answer ID: 50069221
<p>Use this:</p>

<pre class="lang-php prettyprint-override"><code>DB::table('customers')
    -&gt;select('customers.id', 'customers.customer_name', DB::raw('SUM(shipments.balance) AS shipmentBalance'))
    -&gt;leftJoin('shipments', function($join) {
        $join-&gt;on('customers.id', 'shipments.bill_to')
            -&gt;where('balance', '&gt;', function($query) {
                $query-&gt;selectRaw('IFNULL(SUM(payments_distributions.amount),0)')
                    -&gt;from('payments_distributions')
                    -&gt;where('payments_distributions.shipment_id', DB::raw('pro_number'));
            });
    })
    -&gt;groupBy('customers.id', 'customers.customer_name')
    -&gt;orderByDesc('shipmentBalance')
    -&gt;limit(5)
    -&gt;get();
</code></pre>

### Answer ID: 50068571
<p>Without the Models containing relationships or being able to test on this specific project, this is the most eloquent way I can think of performing your task.  </p>

<p>The benefit of starting with the Customer model is you will have a <a href="https://laravel.com/docs/5.6/collections" rel="nofollow noreferrer">laravel collection</a> and can <a href="https://laravel.com/docs/5.6/pagination" rel="nofollow noreferrer">paginate</a> as needed.  Also review the <a href="https://laravel.com/docs/5.6/eloquent" rel="nofollow noreferrer">eloquent docs</a>, they help you understand all the different options.  Hope his helps.  </p>

<p>P.S.  Start by using your model in your controller or wherever you are placing this query with:</p>

<pre><code>use App\Customer
</code></pre>

<p><strong>The query</strong></p>

<pre><code>$theQuery = Customer::select(DB::raw('customers.id, customers.customer_name,SUM(s.balance) AS shipmentBalance'))
        -&gt;leftJoin('shipments as s', function($join)
        {
            $join-&gt;on('customers.id', '=', 's.bill_to');
            $join-&gt;on(DB::raw('s.balance &gt; 
                                (SELECT IFNULL(SUM(payments_distributions.amount),0)                
                                    FROM payments_distributions               
                                    WHERE payments_distributions.shipment_id = s.pro_number)
                            '));    
        })
        -&gt;groupBy('customers.id', 'customers.customer_name')
        -&gt;orderByRaw('SUM(s.balance) DESC')
        -&gt;limit(5)
        -&gt;get();
</code></pre>

