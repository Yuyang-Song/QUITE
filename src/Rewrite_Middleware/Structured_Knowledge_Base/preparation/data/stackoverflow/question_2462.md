# How to keep the materialized view updated?
[Link to question](https://stackoverflow.com/questions/35413243/how-to-keep-the-materialized-view-updated)
**Creation Date:** 1455550468
**Score:** 0
**Tags:** mysql, database, data-warehouse, relational-algebra, materialized-views
## Question Body
<p>I am working on TPCH benchmark database and queries, and I am trying to solve this question:
Assume the query:</p>

<pre><code>GB c custkey,sum(o totalprice)(σo shippriority=0 and c acctbal&gt;0(ORDER ./ CUST OMER))
</code></pre>

<p>defines a materialized view on the TPCH database.</p>

<p>Assume that insertions into ORDER are stored into
table ORDER-INSERTIONS by the ETL process. Show the update needed to keep the materialized
view in sync by rewriting the SQL query above into extended relational algebra and then expanding
the resulting expression over table</p>

<pre><code>ORDERnew = ORDER ∪ ORDER − INSERTIONS
</code></pre>

