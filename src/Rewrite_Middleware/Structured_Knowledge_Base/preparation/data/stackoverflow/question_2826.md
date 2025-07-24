# EXISTS vs IN; implementation detail that gives rise to (claimed) performance difference
[Link to question](https://stackoverflow.com/questions/54229601/exists-vs-in-implementation-detail-that-gives-rise-to-claimed-performance-dif)
**Creation Date:** 1547703250
**Score:** 0
**Tags:** sql, query-optimization
## Question Body
<p>In <a href="https://stackoverflow.com/questions/24929/difference-between-exists-and-in-in-sql">Difference between EXISTS and IN in SQL?</a> it's clear that lots of people think "exists is faster if the subquery returns many rows, in is faster if it returns a few rows" but I'd like to know a bit more detail about the actual implementation of each of these keywords and how it could give rise to a difference in performance based on result set size </p>

<p>Lots of people were claiming that EXISTS is simply looking for a true or false (as though IN isn't??) and gives up as soon as a true is found, whereas IN will "scan the entire set" - really? If I were writing a dbms and using a naive loop to establish the truth of <code>3 IN (1,2,3,4,5)</code> I'm pretty sure I'd code it up such that if I found 3 after a checking 1 and 2, I wouldn't check 4 and 5 to see if they were also 3</p>

<p>I've a strong suspicion that, for the most part, IN, EXISTS and even JOIN are implemented identically/the query optimisers of modern DBs rewrite/approach these different keywords in the same way anyway - is there a modern database out there that does still exhibit an appreciable performance difference with EXISTS vs IN and what is the actual implementation detail that causes the difference?</p>

<p>Side note; in that question, some references to Oracle 8/SQL Server 2000 were made and the strategies they adopted, and I can see how a performance difference would arise with them, but I don't think these can be classed as modern databases unless the latest iterations of these products still implement these keywords the same as they did 20 years ago...</p>

## Answers
### Answer ID: 54236107
<p>Although this is too broad, there are multiple semantic differences among the three approaches:</p>

<ul>
<li><code>JOIN</code> can result in multiple rows when there are multiple matches.</li>
<li><code>NOT IN</code> filters out all rows if <em>any</em> value is <code>NULL</code>.</li>
<li><code>EXISTS</code> works in all databases regardless of conditions, including conditions on multiple columns.  <code>IN</code> (historically and in many databases) only works on one column.</li>
</ul>

<p>Although there are cases where the three overlap, they are not equivalent.</p>

