# SQL Query with the Northwind database (Catch: no Inner Join)
[Link to question](https://stackoverflow.com/questions/28052735/sql-query-with-the-northwind-database-catch-no-inner-join)
**Creation Date:** 1421778980
**Score:** 1
**Tags:** sql, ms-access-2010
## Question Body
<p>First and foremost - it is a homework assignment, yet I am not asking for anyone to do it. Instead I need help with how to construct the query.</p>

<p>As part of an assignment, using the Northwind database via Microsoft Access, I have to construct this query:</p>

<blockquote>
  <p>The product ID, product name, and quantity ordered for all products ordered  on an order taken by an employee with last name Fuller.</p>
</blockquote>

<p>Now, when I construct the query in design mode, this is the code I get:</p>

<pre><code>SELECT Products.ProductID, Products.ProductName, [Order Details].Quantity
FROM Products INNER JOIN ((Employees INNER JOIN Orders ON Employees.EmployeeID = Orders.EmployeeID) INNER JOIN [Order Details] ON Orders.OrderID = [Order Details].OrderID) ON Products.ProductID = [Order Details].ProductID
WHERE (((Employees.LastName)="Fuller"));
</code></pre>

<p>As I mentioned earlier, we are not allowed to use Inner Join. After scouring the text/notes thus far I can't find how to go about it. (Very new to SQL)</p>

<p>Would I be rewriting the FROM statement? And if so, do the SELECT and WHERE statements change?</p>

<p><strong>UPDATE:</strong> Here is the code as I rewrote it:</p>

<pre><code>SELECT Orders.OrderID, Orders.CustomerID, Orders.ShipCity
FROM Products, Orders, [Order Details], Employees
WHERE
  Products.ProductID = [Order Details].ProductID
  AND Employees.EmployeeID = Orders.EmployeeID
  AND Ordes.OrderID = [Order Details].OrderID
  AND Employees.LastName = "Fuller";
</code></pre>

<p>I'm having a sort of syntax issue though. Since the Order Details must be enclosed in brackets, it wants to ask for parameter values for what I wrote in the WHERE statement.</p>

## Answers
### Answer ID: 28053829
<p>The requirement not to use <code>INNER JOIN</code> is a little peculiar and I cannot guarantee this is what was intended for your assignment.</p>

<p>One way to alternatively write a simplistic relationship between two tables is with an <code>IN ()</code> subquery, the general form being:</p>

<pre><code>SELECT *
FROM a_table
WHERE some_column IN (
  SELECT some_related_column
  FROM b_table
  WHERE some_condition
)
</code></pre>

<p>But since you must represent columns from more than one of your 4 tables in the <code>SELECT</code> list, that form isn't going to work for you.  Another way of not <em>explicitly</em> using an <code>INNER JOIN</code> is to use the older implicit joining syntax, in which multiple tables are listed in the <code>FROM</code> clause separated by commas, and their joining conditions placed in the <code>WHERE</code> clause instead of in <code>ON</code>.</p>

<p>The general form is:</p>

<pre><code>SELECT 
  a_table.col1,
  a_table.col2,
  b_table.col1
FROM
  a_table,
  b_table
WHERE
 a_table.some_column = b_table.some_related_column
 AND some_other_conditions
</code></pre>

<p>It being an assignment, I will leave it to you to work out the entire statement, but yours would take a form like </p>

<pre><code>SELECT
  Orders.OrderID,
  Orders.CustomerID
FROM 
  Products,
  Orders,
  [Order Details],
  Employees
WHERE
  Products.ProductID = [Order Details].ProductID 
  AND ... (the other table relationships)
  AND Employees.LastName = 'Fuller'
</code></pre>

<p>Although it is functionally identical to explicit <code>INNER JOIN</code>s, this is an older syntax, and is often discouraged nowadays. <a href="https://stackoverflow.com/questions/44917/explicit-vs-implicit-sql-joins">More discussion is available in this question</a></p>

