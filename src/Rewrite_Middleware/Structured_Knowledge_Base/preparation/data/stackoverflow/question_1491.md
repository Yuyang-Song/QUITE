# SQL Scan vs Seek when using OR in where criteria
[Link to question](https://stackoverflow.com/questions/78799866/sql-scan-vs-seek-when-using-or-in-where-criteria)
**Creation Date:** 1722027681
**Score:** 0
**Tags:** sql-server, t-sql, query-optimization
## Question Body
<p>Consider the following two queries from the AdventureWorks database. The where criteria is entirely on indexed columns. If you use OR criteria both tables get a full table scan on them. In the second scenario the criteria is split out over two queries that are unioned. In the second scenario both tables get index seeks. Can someone explain why SQL can't/won't optimize the first query to do an index seek?  Are there ways to tell SQL to do a seek without rewriting as a UNION? (I've tried index hints with no success)</p>
<pre><code>SELECT *
FROM [AdventureWorks2022].[Sales].[SalesOrderHeader] hdr
JOIN [AdventureWorks2022].[Sales].[SalesOrderDetail] dtl ON hdr.SalesOrderID = dtl.SalesOrderID
WHERE hdr.SalesOrderID = 43659 OR dtl.SalesOrderDetailID =  43659

----

SELECT *
FROM [AdventureWorks2022].[Sales].[SalesOrderHeader] hdr
JOIN [AdventureWorks2022].[Sales].[SalesOrderDetail] dtl ON hdr.SalesOrderID = dtl.SalesOrderID
WHERE hdr.SalesOrderID = 43659
 
UNION
 
SELECT *
FROM [AdventureWorks2022].[Sales].[SalesOrderHeader] hdr
JOIN [AdventureWorks2022].[Sales].[SalesOrderDetail] dtl ON hdr.SalesOrderID = dtl.SalesOrderID
WHERE dtl.SalesOrderDetailID =  43659
</code></pre>

## Answers
### Answer ID: 78808563
<p><a href="https://dba.stackexchange.com/a/289679/3690">This answer by Paul White</a> seems to explain it and confirms that SQL cannot come up with the <code>UNION</code> plan with the <code>OR</code> criteria.</p>
<blockquote>
<p>This transform <strong>only applies to a single table</strong>, and does not apply to
attribute-to-attribute comparisons.</p>
</blockquote>

