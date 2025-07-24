# sql slow postgresql dbeaver
[Link to question](https://stackoverflow.com/questions/75460489/sql-slow-postgresql-dbeaver)
**Creation Date:** 1676467717
**Score:** 0
**Tags:** sql, postgresql
## Question Body
<p>I am using DBeaver to query a PostgreSQL database.
I have this query, it simply selects the highest id per Enterprise_Nbr.  The query works but is really slow.  Is there any way I can rewrite the query to improve performance.</p>
<p>I am using the querytool DBeaver because I don't have direct access to PostgreSQL.  The ultimate goal is to link the PostgreSQL with PowerBi.</p>
<pre><code>select * 
from public.address 
where &quot;ID&quot;  in (select max(&quot;ID&quot;) 
  from public.address a 
  group by &quot;Enterprise_Nbr&quot;)
</code></pre>

## Answers
### Answer ID: 75460611
<p>Queries for <a href="/questions/tagged/greatest-n-per-group" class="post-tag" title="show questions tagged &#39;greatest-n-per-group&#39;" aria-label="show questions tagged &#39;greatest-n-per-group&#39;" rel="tag" aria-labelledby="greatest-n-per-group-container">greatest-n-per-group</a> problems are typically faster if done using Postgres' proprietary <code>distinct on ()</code> operator</p>
<pre><code>select distinct on (&quot;Enterprise_Nbr&quot;) *
from public.address
order by &quot;Enterprise_Nbr&quot;, &quot;ID&quot; desc;
</code></pre>

