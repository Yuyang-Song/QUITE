# sql Top 1 vs System.Linq firstordefault
[Link to question](https://stackoverflow.com/questions/15639547/sql-top-1-vs-system-linq-firstordefault)
**Creation Date:** 1364307963
**Score:** 2
**Tags:** c#, sql, linq
## Question Body
<p>I am rewriting an SProc in c#. the problem is that in SProc there is a query like this:</p>

<pre><code>select top 1 *
from ClientDebt
where ClinetID = 11234
order by Balance desc
</code></pre>

<p>For example :I have a client with 3 debts, all of them have same balance. the debt ids are : 1,2,3  </p>

<p>c# equivalent of that query is :</p>

<pre><code>debts.OrderByDescending(d =&gt; d.Balance)
     .FirstOrDefault()
</code></pre>

<p>debts represent clients 3 debts</p>

<p>the interesting part is that sql return debt with Id 2 but c# code returns Id 1.
The Id 1 make sense for me But in order to keep code functionality the same I need to change the c# code to return middle one.</p>

<p>I do not sure what is the logic behind sql top 1 where several rows match the query.</p>

<p>The query will select one debt and update the database. I would like the linq to return the same result with sql</p>

<p>Thanks</p>

## Answers
### Answer ID: 75944965
<p>Try Take(1) before firstordefault.</p>

### Answer ID: 15639982
<p>You can start SQL Profiler, execute stored procedure, review result, and then catch query which application send through linq, and again review result. </p>

<p>Also, you can easily view execution plan of you procedure, and try it to optimize, but with linq query, you cannot easily do this.</p>

### Answer ID: 15639704
<pre><code>debts.OrderByDescending(d =&gt; d.Balance).ThenByDescending(d =&gt; d.Id)
     .FirstOrDefault()
</code></pre>

### Answer ID: 15639652
<p>AFAIK, IN SQL if you select rows without ORDER BY, it orders the resultset based on the primary key.
With Order BY CLAUSE [field], implicitly next order is [primarykey].</p>

