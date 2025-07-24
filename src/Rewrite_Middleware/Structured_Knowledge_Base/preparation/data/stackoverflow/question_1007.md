# Rewriting database query in Codeigniter&#39;s query builder
[Link to question](https://stackoverflow.com/questions/54419130/rewriting-database-query-in-codeigniters-query-builder)
**Creation Date:** 1548758257
**Score:** 0
**Tags:** php, codeigniter
## Question Body
<p>I'm trying to rewrite existing database query in Codeigniter' query builder, how do I solve WHERE EXISTS(I think that's where's the problem)?</p>

<p>This is original query I want to rewrite:</p>

<pre><code>$query = $this-&gt;db-&gt;query('SELECT p_customer.*' .
        ' FROM p_customer' .
        ' WHERE EXISTS (' .
        'SELECT null' .
        ' FROM p_customer_group_rel' .
        ' WHERE p_customer_group_rel.customer_group_id=' . $e_id.
        ' AND p_customer_group_rel.customer_id = p_customer.id' .
        ')' .
        ' AND p_customer.deleted IS NULL' .
        ' AND p_customer.id &gt; 0' .
        ' ORDER BY p_customer.full_name'
    );
</code></pre>

<p>This is what I got so far:</p>

<pre><code>$query = $this-&gt;db
        -&gt;select('p_customer.*')
        -&gt;from('p_customer')
        -&gt;where('EXISTS(SELECT null FROM p_customer_group_rel WHERE 
p_customer_group_rel.customer_group_id= ' . $e_id . ' AND 
p_customer_group_rel.customer_id = p_customer.id)')
        -&gt;where('p_customer.deleted is NULL')
        -&gt;where('p_customer.id &gt; 0')
        -&gt;order_by('p_customer.full_name');
        -&gt;get();
</code></pre>

<p>The result I get from first query is array of object.
This is what I get from my query:</p>

<pre><code>SELECT p_customer.* FROM p_customer WHERE EXISTS( SELECT null FROM p_customer_group_rel WHERE p_customer_group_rel.customer_group_id= $e_id ) AND p_customer_group.port_id = p_port.id
</code></pre>

<p>which is not what I want, any help? :)</p>

## Answers
### Answer ID: 54422363
<p>Maybe it's not best solution, but I did the following and it works:</p>

<pre><code>$sub_q = 'SELECT null FROM p_customer_group_rel WHERE p_customer_group_rel.customer_group_id=' . $e_id . ' AND p_customer_group_rel.customer_id = p_customer.id';
$query = $this-&gt;db -&gt;select('p_customer.*') -&gt;from('p_customer') -&gt;where('EXISTS(' . $sub_q . ')') -&gt;where('p_customer.id &gt;', 0) -&gt;where('p_customer.deleted', NULL) -&gt;order_by('p_customer.full_name') -&gt;get();
</code></pre>

