# Rewriting Queries and data layers
[Link to question](https://stackoverflow.com/questions/40693815/rewriting-queries-and-data-layers)
**Creation Date:** 1479564438
**Score:** 0
**Tags:** database, vitess
## Question Body
<p>I was going through the following question in quora :</p>

<p><a href="https://www.quora.com/How-was-YouTube-programmed-in-Python" rel="nofollow noreferrer">https://www.quora.com/How-was-YouTube-programmed-in-Python</a></p>

<p>The first answer here mentioned about a software named "Vitess " . It mentioned that vitess rewrites queries and so provides optimization . 
What exactly does it mean to rewrite queries for optimization of database transactions . I have read about few software having their own customized RDBMS systems and layering of data for making database operations faster .</p>

<p>How exactly can rewriting queries make the operations faster ?
With the fear of broadening of the scope of this question , I would request some insights on layering of data and materials where I can start from to know more about data layering and rewriting of queries.</p>

## Answers
### Answer ID: 40696110
<p>I work on <a href="http://vitess.io" rel="nofollow noreferrer">vitess</a>.</p>

<p>If an optimization was universally viable, then the database engine would itself do it.</p>

<p>The types of optimizations that Vitess performs are trade-offs that are viable for today's applications. For example:</p>

<ul>
<li>For OLTP workloads, Vitess adds a limit clause to your query. If the number of rows exceeds certain amount, it returns an error.</li>
<li>If a query is taking too long to complete, it's most likely causing harm to other queries. So, we kill such queries in order to keep the system going.</li>
<li>We rewrite DMLs to be primary key based. This way, the replicas don't have to redo the original work. This is applicable if you're using statement based replication.</li>
<li>If two identical queries hit the system, send only one and share the results.</li>
</ul>

<p>These are just some highlights. We've added many more such tuning options based on problems and outages we've seen at YouTube.</p>

