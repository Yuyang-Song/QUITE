# sum(DATALENGTH) returning an &quot;Arithmetic overflow&quot; error
[Link to question](https://stackoverflow.com/questions/31118678/sumdatalength-returning-an-arithmetic-overflow-error)
**Creation Date:** 1435589091
**Score:** 3
**Tags:** sql-server, function, t-sql, sum
## Question Body
<p>I am new to SQL Server so please accept my apologies if my question seems too easy. I tried finding a solution, but so far I couldn't see anything that I could use in my query. </p>

<p>I am trying to find length of the biggest columns in a table and I'm using the following query.</p>

<pre><code>SELECT
    SUM(DATALENGTH([INSDetails])) as [INSDetails]
FROM 
    dbo.Contractors
</code></pre>

<p>The table <code>Contractors</code> is slightly over 8GB and has over 30mln rows. <code>INSDetails</code> column is <code>varchar(2048)</code></p>

<p>The query above works perfectly well for all the other columns of all the other tables in my database, but when I run it on <code>Contractors</code> table it returns an error </p>

<blockquote>
  <p>Msg 8115, Level 16, State 2, Line 26<br>
  Arithmetic overflow error converting expression to data type int.</p>
</blockquote>

<p>I understand that this error message appears when you try to convert a value of a certain datatype to another datatype, but that value is too large for the second datatype.</p>

<p>Could you please help me to rewrite the query or suggest alternative approach to get the output? </p>

<p>I read that someone suggested using CAST AS big int to solve this issue, but I'm not sure how it can be incorporated in my query. </p>

<p>Any suggestions will be appreciated. Thank you in advance.</p>

## Answers
### Answer ID: 31118868
<pre><code>select sum(cast(datalength([INSDetails]) as bigint))
</code></pre>

