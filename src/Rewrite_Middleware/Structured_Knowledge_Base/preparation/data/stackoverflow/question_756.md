# SQL Joins and exclusions
[Link to question](https://stackoverflow.com/questions/4084039/sql-joins-and-exclusions)
**Creation Date:** 1288755558
**Score:** 3
**Tags:** sql, sql-server, performance, t-sql
## Question Body
<p>Assuming a query as such in T-SQL.</p>

<pre><code>   SELECT *  
     FROM Stock S    
LEFT JOIN StockBarcode SB ON SB.StockID = S.StockID
                         AND SB.ShopID = @ShopID 
                         AND SB.Inactive = 0    
LEFT JOIN StockBarcode SB1 ON SB1.StockID = S.StockID
                          AND SB1.ShopID = 0 
                          AND SB1.Inactive = 0    
    WHERE S.StockID = @StockID
</code></pre>

<p>My understanding is that I could rewrite the query as such</p>

<pre><code>   SELECT * 
     FROM Stock S    
LEFT JOIN StockBarcode SB ON S.StockID = SB.StockID 
                         AND SB.ShopID = @ShopID    
LEFT JOIN StockBarcode SB1 ON S.StockID = SB1.StockID 
                          AND SB1.ShopID = 0     
    WHERE S.StockID = @StockID 
      AND ISNULL(SB.Inactive, 0) = 0 
      AND ISNULL(SB1.Inactive, 0) = 0
</code></pre>

<p>...and the results would be the same. (Please correct me if I am wrong)
Which is the optimal query and why? Would the case be different if I was using another database engine such as MySql?</p>

<p>Thanks in advance to any answers :-)</p>

<p><strong>EDIT:</strong>
For clarification here is the entire query as it stands at the moment if that will help. </p>

<pre><code>SELECT 
    SSCLRU.SupplierCode,  
    S.[Description],
    S.TaxRate AS GSTRate,
    ISNULL(ISNULL(SB.PackPrice, SB1.PackPrice), S.RRP) AS Price,
    ISNULL(SB.PackSize, SB1.PackSize) AS Quantity,
    ISNULL(SB.SalePrice, SB1.SalePrice) AS SalePrice,
    ISNULL(SB.SaleDateFrom, SB1.SaleDateFrom) AS SalePriceStartDate,
    ISNULL(SB.SaleDateTo, SB1.SaleDateTo) AS SalePriceEndDate
FROM Stock S

LEFT JOIN StockSupplierCodePreferredLastReceivedUnique SSCLRU ON
S.StockID = SSCLRU.StockID

LEFT JOIN StockBarcode SB ON
S.StockID = SB.StockID AND
SB.ShopID = @ShopID AND
SB.Inactive = 0

LEFT JOIN StockBarcode SB1 ON
S.StockID = SB1.StockID AND
SB1.ShopID = 0 AND
SB1.Inactive = 0

WHERE S.StockID = @StockID 
</code></pre>

## Answers
### Answer ID: 4087641
<p>They are not <em>quite</em> the same, unless StockBarcode.Inactive is not nullable.</p>

<p>If StockBarcode.Inactive <em>is</em> nullable, then the first query will not return any details for StockBarcodes where Inactive is null (since they fail the join condition), while the second query will include them if they match the  other join conditions - they will match the <code>where</code> condition.</p>

### Answer ID: 4084456
<p>The 1st one is clearer because you don't have to worry about non-matching rows in the WHERE</p>

<p>However, I'd probably use this construct to fully separate join and filter conditions</p>

<pre><code>FROM
   Stock S
   LEFT JOIN
   StockSupplierCodePreferredLastReceivedUnique SSCLRU ON S.StockID = SSCLRU.StockID

   LEFT JOIN
   (
    SELECT StockID, ...
    FROM StockBarcode
    WHERE ShopID = @ShopID AND Inactive = 0
   ) SB ON S.StockID = SB.StockID

   LEFT JOIN
   (
    SELECT StockID, ...
    FROM StockBarcode
    WHERE ShopID = 0 AND Inactive = 0
   ) SB1 ON S.StockID = SB1.StockID
WHERE
   S.StockID = @StockID 
</code></pre>

<p>The derived tables could be pushed into a CTE (or 2 ) as well.</p>

### Answer ID: 4084221
<blockquote>
  <p>Which is the optimal query and why?</p>
</blockquote>

<p>Look at the query plan.</p>

<p>But I bet the 1st should be more performant, since <code>SB.Inactive = 0</code> condition can be covered by index.</p>

<blockquote>
  <p>Would the case be different if I was using another database engine such as MySql?</p>
</blockquote>

<p>Sure, the execution plan and performance is strictly dependent on vendor.</p>

