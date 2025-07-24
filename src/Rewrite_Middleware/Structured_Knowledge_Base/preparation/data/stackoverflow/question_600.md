# speed of SQL queries with variables
[Link to question](https://stackoverflow.com/questions/33239587/speed-of-sql-queries-with-variables)
**Creation Date:** 1445351824
**Score:** 0
**Tags:** sql, native-sql
## Question Body
<p>I am new to SQL and trying to query a large database so speed is an issue. I have been using a query (with line <strong>1</strong>) of the form shown below which has been working fine, but when I modify it (to switch line <strong>1</strong> for line <strong>2</strong>) to use a constant to make a cut rather than a value derived within the query itself then the query is significantly slower (running time of <strong>1</strong> is ~1sec and <strong>2</strong> is a few minutes). I would have actually expected it to be much quicker.
Can someone explain why this is happening or suggest how I might rewrite this query better?</p>

<p>Thanks</p>

<h2>Query</h2>

<pre><code>with local_sample as 

( SELECT b.mass, ...various other columns selected... 

FROM table1 TAB, table2 b 

WHERE ...a few clauses... )


SELECT min(prog.num), LTAB.mass, ...various other columns...

from local_sample LTAB, table2 prog

WHERE ...a few clauses... 

[**1**] and prog.mass &gt; LTAB.mass/2.0

[**2**] and prog.mass &gt; 31.62

group by ...columns...
</code></pre>

## Answers
### Answer ID: 33242514
<p>Information in the question is kind of scarce, so at a guess, it's an implicit conversion issue. My hunch is LTAB.mass is the same data type as prog.mass, so no conversion is necessary, but whatever that data type is doesn't play nicely with decimal.</p>

<p>Numbers in sql come in many flavors, and most of the time we don't have to think about it because the conversions are very fast and happen in the background. Occasionally though, you'll come across number types formats that don't play well with others (float for instance) and it can become a performance pain point.</p>

<p>So here is a way to test if that's the issue run the below query (assuming Microsoft SQL Server is your RDBMS):</p>

<pre><code>select SQL_VARIANT_PROPERTY(Mass,'BaseType') AS 'Base Type'
From table2
</code></pre>

<p>If my hunch is correct it will return float as the base type. If that's the case and the implicit conversion is the issue then the below should work in a similar manner to query 1:</p>

<pre><code>with local_sample as 
( SELECT b.mass, ...various other columns selected... 
FROM table1 TAB, table2 b 
WHERE ...a few clauses... )

Declare @Mass float = 31.62

SELECT min(prog.num), LTAB.mass, ...various other columns...
from local_sample LTAB, table2 prog
WHERE ...a few clauses... 
and prog.mass &gt; @Mass
group by ...columns...
</code></pre>

<p>Anyway let me know if that doesn't work for you.</p>

