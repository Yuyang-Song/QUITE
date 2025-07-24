# What is better option? IN operator or EXISTS
[Link to question](https://stackoverflow.com/questions/45235429/what-is-better-option-in-operator-or-exists)
**Creation Date:** 1500633272
**Score:** 0
**Tags:** mysql, sql, operators
## Question Body
<p>What is better option? Using IN operator or EXISTS operator? In term of performance and server load. Is there any supporting factors for IN and/or EXISTS operator in database (like index, constraint or something)? </p>

<p>Here is sample queries using IN and EXISTS</p>

<pre><code>SELECT * FROM Customers WHERE Customer_ID IN (SELECT Cust_ID FROM Sales);
</code></pre>

<p>AND</p>

<pre><code>SELECT Customer_ID FROM Customers WHERE EXISTS (SELECT Cust_ID FROM Sales);
</code></pre>

<p>If the two queries were different, what is better way to count or list Customer? Or if query is more complex in like below. </p>

<pre><code>SELECT sub_id FROM subscription 
WHERE start_date = CURDATE()
AND end_date &gt; CURDATE()
AND sub_id NOT IN (SELECT DISTINCT sub_id FROM subscription 
WHERE start_date &lt; CURDATE());
</code></pre>

<p>Is it possible to replace NOT IN operator with NOT EXISTS? In this case, rewriting above query with NOT EXISTS is better or something? </p>

## Answers
### Answer ID: 45235539
<p>You could use them for the same, but <code>exists</code> keyword is generaly used when you are checking if conditional statements.</p>

<p><code>In</code> keyword, is generaly used with a list comparation.</p>

<p>Also, as jarlh says, you can replace <code>in</code> using <code>join</code>.</p>

### Answer ID: 45235469
<p>The two queries do different things.  You probably intend a correlated subquery for <code>EXISTS</code>:</p>

<pre><code>SELECT Customer_ID c
FROM Customers c
WHERE EXISTS (SELECT 1 FROM Sales s WHERE s.Cust_ID = c.Customer_Id);
</code></pre>

<p>Both methods are fine for expressing your logic.  I tend to prefer <code>EXISTS</code> for two reasons:</p>

<ul>
<li><code>NOT EXISTS</code> is generally a better choice than <code>NOT IN</code> because of the way it handles <code>NULL</code>.  This does not apply to <code>EXISTS</code>/<code>IN</code>, but it spills over.</li>
<li><code>EXISTS</code> is generally no worse than <code>IN</code> from a performance perspective. </li>
</ul>

