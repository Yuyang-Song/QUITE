# How to rewrite MySQL CTE query without using CTE due version error?
[Link to question](https://stackoverflow.com/questions/58698262/how-to-rewrite-mysql-cte-query-without-using-cte-due-version-error)
**Creation Date:** 1572887940
**Score:** 1
**Tags:** mysql, mysql-workbench, common-table-expression
## Question Body
<p>I am getting an error with MY CTE. I host the database n Amazon RDS. I have another sample database host on my computer (localhost). CTE works fine with my local computer. I think something wrong with Amazon RDS. Maybe it is not supporting CTE. Does anybody experience the same issue? Any idea how to fix this or How can I rewrite this query without CTE? Any help on this will be highly appreciated. </p>

<pre><code>    WITH StoreSku AS
(
    SELECT 
        S.StoreName
        ,  RTRIM(LTRIM(LEFT(S.StoreName, 4))) 'StoreNumber'
        , P.Sku
        , P.Description
    FROM simplymac_staging.LocationMasterList S
    CROSS JOIN simplymac_staging.`dbo.Sku` P
    WHERE S.Disabled = 0
),
Inventory AS
(
    SELECT 
        I.StoreName
        , RTRIM(LTRIM(LEFT(I.StoreName, 4))) 'StoreNumber'
        , I. ProductName
        , I.ProductIdentifier
        , I.UnitCost
        , SUM(I.Quantity) 'Quantity'
        , I.BinStatus
    FROM simplymac_staging.inventorylistinstores I
    GROUP BY 
          I.ProductIdentifier
        , I.ProductName
        , I.BinStatus
        , I.StoreName
        , I.UnitCost
)
SELECT 
      P.StoreName
    , P.Description
    , P.Sku
    , CASE WHEN I.BinStatus in ('String_InStock') THEN I.Quantity ELSE 0 END ' In Stock'
    , CASE WHEN I.BinStatus in ('String_TransferIn') THEN I.Quantity ELSE 0 END 'TransferIn'
    , CASE WHEN I.BinStatus in ('String_TransferOut') THEN I.Quantity ELSE 0 END 'TransferOut'
    , CASE WHEN I.BinStatus in ('String_OnOrder') THEN I.Quantity ELSE 0 END 'OnOrder'
FROM StoreSku P
LEFT JOIN  Inventory I ON I.ProductIdentifier = P.ID AND I.StoreNumber = P.StoreNumber
</code></pre>

<p>ERROR </p>

<blockquote>
  <p>Error Code: 1064. You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'Stores AS (  SELECT     S.StoreName    ,  RTRIM(LTRIM(LEFT(S.StoreName, 4))) 'St' at line 1</p>
</blockquote>

<p>Again, any help to rewrite my query without a CTE will really appreciated. Thank yuo so much </p>

## Answers
### Answer ID: 58698288
<p>As a simple solution: since both CTE are apparently unrelated one with the other, no recursion is invovled, and each CTE is selected from only once in the main query, then you can just turn them to inline tables, ie move them to the <code>FROM</code> clause, like so:</p>

<pre><code>SELECT 
      P.StoreName
    , P.Description
    , P.Sku
    , CASE WHEN I.BinStatus in ('String_InStock') THEN I.Quantity ELSE 0 END ' In Stock'
    , CASE WHEN I.BinStatus in ('String_TransferIn') THEN I.Quantity ELSE 0 END 'TransferIn'
    , CASE WHEN I.BinStatus in ('String_TransferOut') THEN I.Quantity ELSE 0 END 'TransferOut'
    , CASE WHEN I.BinStatus in ('String_OnOrder') THEN I.Quantity ELSE 0 END 'OnOrder'
FROM 
(
    SELECT 
        S.StoreName
        ,  RTRIM(LTRIM(LEFT(S.StoreName, 4))) 'StoreNumber'
        , P.Sku
        , P.Description
    FROM simplymac_staging.LocationMasterList S
    CROSS JOIN simplymac_staging.`dbo.Sku` P
    WHERE S.Disabled = 0
) P
LEFT JOIN (
(
    SELECT 
        I.StoreName
        , RTRIM(LTRIM(LEFT(I.StoreName, 4))) 'StoreNumber'
        , I. ProductName
        , I.ProductIdentifier
        , I.UnitCost
        , SUM(I.Quantity) 'Quantity'
        , I.BinStatus
    FROM simplymac_staging.inventorylistinstores I
    GROUP BY 
          I.ProductIdentifier
        , I.ProductName
        , I.BinStatus
        , I.StoreName
        , I.UnitCost
) I ON I.ProductIdentifier = P.ID AND I.StoreNumber = P.StoreNumber
</code></pre>

