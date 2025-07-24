# SQL ignore condition clause if the value is null or empty
[Link to question](https://stackoverflow.com/questions/52948391/sql-ignore-condition-clause-if-the-value-is-null-or-empty)
**Creation Date:** 1540295540
**Score:** 0
**Tags:** sql
## Question Body
<p>I have the following query</p>

<pre><code>SELECT id, namn, postA, postB postN FROM k.dbo.PF WHERE
        namn LIKE @name + '%' AND
        postA LIKE @address + '%' AND
        postB LIKE @coAddress + '%' AND
        postN LIKE @zip + '%' AND
        k.dbo.status = 0
</code></pre>

<p>This query works as long as I have the correct values in all the fields. But in this case, the care of address (postB column) can sometimes be null in the database. But when I provide the parameter @coAddress with a null value, the query doesn't return anything. How can I rewrite this query so that it will skip the <strong>AND</strong> clause completely if the coAddress parameter is null?</p>

## Answers
### Answer ID: 52948496
<p>Try:-</p>

<pre><code>SELECT id, namn, postA, postB postN FROM k.dbo.PF WHERE
        namn LIKE @name + '%' AND
        postA LIKE @address + '%' AND
        (@coAddress is NULL or postB LIKE @coAddress + '%') AND
        postN LIKE @zip + '%' AND
        k.dbo.status = 0
</code></pre>

<p>Any expression involving a NULL value will always return false except for "IS NULL".</p>

### Answer ID: 52948427
<p>Use <code>OR</code>:</p>

<pre><code>SELECT id, namn, postA, postB postN
FROM k.dbo.PF
WHERE (@name is null OR namn LIKE @name + '%') AND
      (@address is null OR postA LIKE @address + '%') AND
      (@coAddress is null OR postB LIKE @coAddress + '%') AND
      (@zip is null OR postN LIKE @zip + '%') AND
      k.dbo.status = 0;
</code></pre>

