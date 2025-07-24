# Column aliases in where clause giving invalid column name error
[Link to question](https://stackoverflow.com/questions/26368922/column-aliases-in-where-clause-giving-invalid-column-name-error)
**Creation Date:** 1413315352
**Score:** 2
**Tags:** sql, sql-server, sql-server-2005
## Question Body
<p>This is a simple question that I'm hung up on. I want to know if I can create a column alias and then use it in my <code>WHERE</code> clause, i.e.:</p>

<pre><code>SELECT TRACTOR, CONVERT(VARCHAR, ORDER) AS NUMBER
FROM TABLE
WHERE NUMBER = '4'
</code></pre>

<p>Keep in mind this is just an example of what I'm trying to do. The query I'm running is a bit more complex, but just the basic idea of how to create a variable and then use it in a clause. </p>

<p>My question is about the aliased columns in the where clause. I have a query that looks for an invoice number in one database and matches it the first 7 digits of a field in another database. The query worked fine when we only had 6 digits but now that we have 7, I'm getting an error and I'm trying to rewrite the query in a different manner.</p>

## Answers
### Answer ID: 26369262
<p>Re-using aliased columns is a great use case for <code>CROSS APPLY</code>:</p>

<pre><code>SELECT t.TRACTOR, CxA.Num
FROM TABLE t
CROSS APPLY
  (SELECT CONVERT(VARCHAR(10), ORDER)) CxA(Num)
WHERE CxA.Num = '4'
</code></pre>

<p>Anything in a <code>CROSS APPLY</code> can be referenced in the <code>SELECT</code>, <code>WHERE</code>, <code>ORDER BY</code>, etc with some limitations (normally if you have aggregation in the <code>CROSS APPLY</code> expression).</p>

### Answer ID: 26368986
<p>Take a look at: <a href="http://sqlmag.com/t-sql/working-variables-t-sql-part-1" rel="nofollow noreferrer">http://sqlmag.com/t-sql/working-variables-t-sql-part-1</a></p>

<p>The basic syntax of variables would be like so:</p>

<pre><code>declare @id int
select @id = 1

select *
from myTable
where id = @id
</code></pre>

<p>EDIT: in case you're actually asking about column aliases in your where clause, and not sql variables, take a look at this SO question: <a href="https://stackoverflow.com/questions/8370114/referring-to-a-column-alias-in-a-where-clause">Referring to a Column Alias in a WHERE Clause</a></p>

<p>EDITx2:</p>

<p>for your specific case (assuming asking about column aliases) you could do the following:</p>

<pre><code>SELECT *
FROM (
    SELECT TRACTOR, CONVERT(VARCHAR(100), ORDER) AS NUMBER
    FROM TABLE
) someTableAlias
WHERE NUMBER = '4'
</code></pre>

<p>Though you may want to rethink your column names... i <em>think</em> number and order are both reserved words, and should be avoided where possible.  you can get around these for the most part by using [order] and [number] I believe, but still best to avoid reserved words as columns/tables/whatevers.</p>

