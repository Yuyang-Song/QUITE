# Subquery Using IN mysql Error Code: 1054
[Link to question](https://stackoverflow.com/questions/46637937/subquery-using-in-mysql-error-code-1054)
**Creation Date:** 1507514992
**Score:** 1
**Tags:** mysql, sql
## Question Body
<p>I'm essentially trying to rewrite a query so that SUM(amount) is calculated as a subquery, with the database named "sakila":</p>

<pre><code>SELECT first_name, last_name, SUM(amount) AS totalSpent
FROM sakila.customer c JOIN
     sakila.payment p
     ON c.customer_id = p.customer_id
GROUP BY last_name, first_name;
</code></pre>

<p>What I have is:</p>

<p><code>SELECT first_name, last_name, SUM(amount) AS totalSpent
FROM sakila.customer c
WHERE c.customer_id IN (SELECT customer_id FROM sakila.payment p)
GROUP BY last_name, first_name;</code></p>

<p>However, when I try to run it, it says ERROR CODE 1054, Unknown column 'amount' in 'field list'</p>

<p><img src="https://i.sstatic.net/Z5108.png" alt="EER Diagram"></p>

## Answers
### Answer ID: 46638037
<p>An alternative is to use a correlated subquery:</p>

<pre><code>SELECT c.first_name, c.last_name,
       (SELECT SUM(p.amount)
        FROM sakila.payment p
        WHERE p.customer_id = c.customer_id
       ) AS totalSpent
FROM sakila.customer c;
</code></pre>

<p>This saves the aggregation in the outer query.  And it can take advantage of an index on <code>payment(customer_id, amount)</code> for performance.</p>

<p>Note that your query doesn't work because you can only refer to columns in tables (or views or subqueries) referenced in the <code>FROM</code> clause.</p>

### Answer ID: 46638023
<p>First of all, you encountered the <code>amount error</code> because you didn't specify which source it comes from so I checked what is your expected result and came up with this:</p>

<pre><code>SELECT c.first_name, c.last_name, SUM(p.amount) AS totalSpent
FROM sakila.customer c
    INNER JOIN payment p ON p.customer_id = c.customer_id
GROUP BY c.last_name, c.first_name;
</code></pre>

### Answer ID: 46638019
<p>Here is your current query, which I actually think is the way to go here:</p>

<pre><code>SELECT
    first_name,
    last_name,
    SUM(amount) AS totalSpent
FROM sakila.customer c
INNER JOIN sakila.payment p
    ON c.customer_id = p.customer_id
GROUP BY
    first_name,
    last_name;
</code></pre>

<p>This is a fairly lean query because you are doing a join with a simple aggregation.  If you wanted to compute the amount as a subquery, you could do so via a correlated subquery on the <code>payment</code> table:</p>

<pre><code>SELECT
    first_name,
    last_name,
    SELECT(SUM(amount) FROM sakila.payment p
           WHERE p.customer_id = c.customer_id) AS totalSpent
FROM sakila.customer c;
</code></pre>

<p>Note that this query has a much highest cost because the subquery in the <code>SELECT</code> statement is <em>correlated</em> to the outer query.  This means that MySQL would have to run a separate query for <em>each row</em> of the <code>customer</code> table.  Your first query is probably the way to go here, because it would allow for things like an index and other optimizations.</p>

