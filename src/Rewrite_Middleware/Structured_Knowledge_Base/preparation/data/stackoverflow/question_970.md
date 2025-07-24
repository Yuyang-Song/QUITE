# SQL- Creating an Inner JOIN for Two Columns inside Same Table
[Link to question](https://stackoverflow.com/questions/52450362/sql-creating-an-inner-join-for-two-columns-inside-same-table)
**Creation Date:** 1537559793
**Score:** 0
**Tags:** sql, oracle-sqldeveloper
## Question Body
<p>I am attempting to work out a practice problem from my book. 
The problem goes like this: </p>

<p>Find all the vendors who have invoices that have not been paid yet. 
(Hint: the invoice_total will be different than the payment_total).</p>

<p>Rewrite the above query in a total of 3 ways: 
Using equijoins, using INNER JOIN and using NATURAL JOIN.</p>

<p>I completed the first step by doing, </p>

<pre><code>SELECT DISTINCT VENDOR_ID
FROM INVOICES
WHERE Invoice_Total != payment_total;
</code></pre>

<p>However, when I try to do the inner joins, I keep getting errors. 
Both Invoice_Total and Payment_Total are columns inside of the same "INVOICES" table. </p>

<p>How would I be able to show the discrepancies whilst pulling the vendor ID's?</p>

<p><a href="https://i.sstatic.net/4oOz7.jpg" rel="nofollow noreferrer">This is a picture of the practice database that I am working with.</a></p>

## Answers
### Answer ID: 52450894
<p>It seems silly to inner join a table to itself to solve this particular problem (there are plenty of good reasons to self-join, but this isn't one of them), but I suppose from a "practice problem" standpoint it's reasonable.  </p>

<p>I would think here it would be best to pre-aggregate the <code>invoices</code> before the join to cut down on the processing time (unless there is an index in place to help the join):</p>

<pre><code>SELECT t1.vendor_id
FROM (SELECT vendor_id, sum(invoice_total) sum_invoice_total FROM INVOICES GROUP BY vendor_id) t1
    INNER JOIN (SELECT vendor_id, sum(payment_total) sum_payment_total FROM INVOICES GROUP BY vendor_id) t2
        ON t1.vendor_id = t2.vendor_id
WHERE
    t1.sum_invoice_total != t2.sum_payment_total
</code></pre>

<p>There is a chance this could break down though if it's possible for a vendor to overpay for an invoice. Consider:</p>

<pre><code>+------------+-----------+---------------+---------------+
| invoice_id | vendor_id | invoice_total | payment_total |
+------------+-----------+---------------+---------------+
|          1 | a         |            10 |            20 |
|          2 | a         |            10 |             0 |
+------------+-----------+---------------+---------------+
</code></pre>

<p>Without pre-aggregating (again this makes no sense, but it will work):</p>

<pre><code>SELECT DISTINCT t1.vendor_id
FROM invoices t1
    INNER JOIN invoices t2
        ON t1.invoice_id = t2.invoice_id
WHERE
    t1.invoice_total != t2.payment_total
</code></pre>

<p>This is nearly identical to your original query, but adds in a superfluous inner join. I'm just guessing at your primary key as <code>invoice_id</code> here. Edit as needed.</p>

