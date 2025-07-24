# How to apply check on &#39;0&#39;?
[Link to question](https://stackoverflow.com/questions/49528814/how-to-apply-check-on-0)
**Creation Date:** 1522223199
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>I am creating a query where I am supposed to add column values and values is in one column at a time. Now I am using <code>ISNULL(Col1,Col2)</code> to check if any column contains value. Now suddenly there is some sort of change in the code and now instead of going <code>NULL</code> in the database column it is saving 0 so ISNULL is not working on those columns and picking up the <code>Col1</code> which is in the first place I suppose.</p>

<p>Is there anyway to handle this without rewriting the entire query or digging up more ?</p>

<p>Here is my query if anyone wants to look at.</p>

<pre><code>;WITH CTE AS (
SELECT 
ID, SUM(DrAmount) [DrAmount], SUM(CrAmount) [CrAmount]
FROM FICO.tbl_TransactionDetail
GROUP BY ID
)
SELECT ID, D.DrAmount, D.CrAmount, D.Amount, D.Amount-ISNULL(D.DrAmount,D.CrAmount) [Opening]
    FROM(
        SELECT *,
                SUM(ISNULL(DrAmount, 0)+ISNULL(CrAmount, 0)) OVER (ORDER BY ID 
                         ) as Amount
        FROM CTE
        )D
</code></pre>

## Answers
### Answer ID: 49529054
<p>As per comments, I have use <code>ISNULL(NULLIF(col1, 0), col2)</code> trick for this issue. Here is updated query -</p>

<pre><code>;WITH CTE AS (
  SELECT 
    ID,
    SUM(DrAmount) [DrAmount],
    SUM(CrAmount) [CrAmount]
  FROM FICO.tbl_TransactionDetail
  GROUP BY ID
)
SELECT
  ID,
  D.DrAmount,
  D.CrAmount,
  D.Amount,
  D.Amount-ISNULL(D.DrAmount,D.CrAmount) [Opening]
FROM(
        SELECT
          *,
          SUM(ISNULL(NULLIF(DrAmount, 0), 0)+ISNULL(NULLIF(CrAmount, 0), 0)) OVER (ORDER BY ID) as Amount
        FROM CTE
    )D
</code></pre>

