# Sql Multiple Where Clauses on Same field
[Link to question](https://stackoverflow.com/questions/5034238/sql-multiple-where-clauses-on-same-field)
**Creation Date:** 1297974541
**Score:** 0
**Tags:** sql, where-clause
## Question Body
<p>I have several queries in an MS Access database that I am rewriting in a SQL stored procedure. The queries have several filters applied to the same field.</p>

<pre><code>select *
from DT.SM_T_OCDetails
where 
    (Rest1 &lt;&gt; 'S' Or Rest1 Is Null)
    and (Rest2 &lt;&gt; 'S' Or Rest2 Is Null) 
    and (Rest3 &lt;&gt; 'S' Or Rest3 Is Null)
    and (Rest4 &lt;&gt; 'S' Or Rest4 Is Null)
</code></pre>

<p>Is there a better way to write the </p>

<pre><code>(Rest1 &lt;&gt; 'S' Or Rest1 Is Null)
</code></pre>

<p>part of the queries?  I looked at coalesce for it but unless I am doing it wrong, I don't think that works.  </p>

<p>Thanks</p>

## Answers
### Answer ID: 5034260
<p>Using coalesce:</p>

<pre><code>coalesce(Rest1,'NOT-S') &lt;&gt; 'S'
</code></pre>

<p>Though I actually think your original is clearer.</p>

