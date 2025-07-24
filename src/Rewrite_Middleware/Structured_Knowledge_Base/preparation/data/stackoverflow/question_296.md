# In Oracle VPD / RLS, how are malicious user predicates prevented from leaking info?
[Link to question](https://stackoverflow.com/questions/19786499/in-oracle-vpd-rls-how-are-malicious-user-predicates-prevented-from-leaking-in)
**Creation Date:** 1383646510
**Score:** 5
**Tags:** oracle-database, security, row-level-security
## Question Body
<p>I've been reading the docs for Oracle VPD (Virtual Private Database, a.k.a. fine-grained security, the basis of label-based security), and there's something I'm having a hard time grasping. How does VPD prevent a user from leaking information using a malicious function in the <code>WHERE</code> clause?</p>

<p>Say you have a VPD policy that generates a static predicate like <code>cust_no = SYS_CONTEXT('order_entry', 'cust_num');</code> (like in <a href="http://docs.oracle.com/cd/B28359_01/network.111/b28531/vpd.htm" rel="noreferrer">the Oracle VPD tutorial</a>). </p>

<p>That results in queries being rewritten, so:</p>

<pre><code>SELECT * FROM orders;
</code></pre>

<p>becomes:</p>

<pre><code>SELECT * FROM orders 
  WHERE cust_no = SYS_CONTEXT('order_entry', 'cust_num');
</code></pre>

<p>Fine so far as it goes. But what if the user writes:</p>

<pre><code>SELECT * FROM orders WHERE my_malicious_function(secret_column);
</code></pre>

<p>? Where <code>my_malicious_function</code> inserts each value it sees into another table owned by the malicious user's control, so they can then see the secret data by selecting that table.</p>

<p>The VPD rewriter will produce, according to the docs, something like:</p>

<pre><code>SELECT * FROM orders 
  WHERE cust_no = SYS_CONTEXT('order_entry', 'cust_num')
    AND my_malicious_function(secret_column);
</code></pre>

<p>but Oracle is free to re-order sub-clauses in <code>WHERE</code>. What stops it from just running <code>my_malicious_function</code> first, if it thinks that'll be the cheaper or more selective predicate? (Unlikely when the security condition is a <code>SYS_CONTEXT</code> lookup, but very likely if the condition is a subquery against another table, or is a UDF its self).</p>

<p>I've read the documentation and I'm not seeing where it specifies any ordering guarantee on execution of VPD predicates vs user-supplied predicates. Is there such a guarantee, or any other mechanism to protect against malicious predicate functions?</p>

<p>(I'm also curious about whether a malicious predicate function in a VPD policy could cause a privileged user to run user-supplied code they did not intend by generating a predicate that refers to the malicious function, but that's somewhat separate.)</p>

## Answers
### Answer ID: 19803395
<p>The "malicious function" is run after the VPD policy is applied, so it cannot see the hidden data.</p>

<p>So, in your example, the following query:</p>

<pre><code>SELECT * FROM orders WHERE my_malicious_function(secret_column);
</code></pre>

<p>Gets rewritten to:</p>

<pre><code>SELECT * FROM (
  SELECT * FROM orders orders
  WHERE cust_no = SYS_CONTEXT('order_entry', 'cust_num')
)
WHERE my_malicious_function(secret_column);
</code></pre>

<p>Therefore, the function is only executed for rows that satisfy the VPD predicate.</p>

<p>Refer: <a href="http://docs.oracle.com/cd/E11882_01/appdev.112/e40758/d_rls.htm#i1005326" rel="nofollow">http://docs.oracle.com/cd/E11882_01/appdev.112/e40758/d_rls.htm#i1005326</a></p>

<blockquote>
  <p>When a table alias is required (for example, parent object is a type
  table) in the predicate, the name of the table or view itself must be
  used as the name of the alias. The server constructs the transient
  view as something like</p>
  
  <p><code>select c1, c2, ... from tab tab where &lt;predicate&gt;</code></p>
</blockquote>

