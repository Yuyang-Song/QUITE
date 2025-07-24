# One line is ruining the efficiency of my query?
[Link to question](https://stackoverflow.com/questions/58013855/one-line-is-ruining-the-efficiency-of-my-query)
**Creation Date:** 1568905032
**Score:** 0
**Tags:** sql, sql-server
## Question Body
<p>I have a simple query that partitions a database by an item number and then calculates the totals for that items</p>

<p>Here is what it looks like.</p>

<pre><code>SELECT DISTINCT

    Master_Item
    ,Item_Number
    ,'--' Color_Code 
    ,Description
    ,'--' Color_Description
    ,SUM(Unit_Retail) OVER (PARTITION BY Item_Number) Sum_Unit_Retail
    ,AVG(Unit_Retail) OVER (PARTITION BY Item_Number) Avg_Unit_Retail

    ,SUM(Unit_MarkDown) OVER (PARTITION BY Item_Number) Sum_Unit_MarkDown
    ,AVG(Unit_MarkDown) OVER (PARTITION BY Item_Number) Avg_Unit_MarkDown
    ,AVG(Unit_MarkDown_Percent) OVER (PARTITION BY Item_Number) Avg_Unit_MarkDown_Percent

    ,SUM(Sell_Price) OVER (PARTITION BY Item_Number) Sum_Sell_Price
    ,AVG(Sell_Price) OVER (PARTITION BY Item_Number) Avg_Sell_Price

    ,SUM(Discount_Value) OVER (PARTITION BY Item_Number) Sum_Discount_Value
    ,AVG(Discount_Value) OVER (PARTITION BY Item_Number) Avg_Discount_Value
    ,AVG(Unit_Discount_Value_Percent) OVER (PARTITION BY Item_Number) Avg_Discount_Value_Percent

    ,SUM(Sale_Price) OVER (PARTITION BY Item_Number) Sum_Sale_Price
    ,AVG(Sale_Price) OVER (PARTITION BY Item_Number) Avg_Sale_Price

    ,SUM(Royalty_Cost) OVER (PARTITION BY Item_Number) Sum_Royalty_Cost
    ,AVG(Royalty_Cost) OVER (PARTITION BY Item_Number) Avg_Royalty_Cost
    ,AVG(Unit_Royalty_Cost_Percent) OVER (PARTITION BY Item_Number) Avg_Royalty_Cost_Percent

    ,SUM(Item_Cost) OVER (PARTITION BY Item_Number) Sum_Item_Cost
    ,AVG(Item_Cost) OVER (PARTITION BY Item_Number) Avg_Item_Cost
    ,AVG(Unit_Item_Cost_Percent) OVER (PARTITION BY Item_Number) Avg_Item_Cost_Percent

    ,SUM(Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight) OVER (PARTITION BY Item_Number) Sum_Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight
    ,AVG(Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight) OVER (PARTITION BY Item_Number) Avg_Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight
    ,AVG(Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight_Percent) OVER (PARTITION BY Item_Number) Avg_Order_Gross_Profit_Minus_Discounts_And_Royalty_And_Freight_Percent

    ,MAX(Quantity_Invoiced+Quantity_Allocated) OVER (PARTITION BY Item_Number) Max_Quantity

    ,SUM(Quantity_Invoiced+Quantity_Allocated) OVER (PARTITION BY Item_Number) Total_Units

    ,(DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number ASC) + DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number DESC) - 1) Total_Orders_Cont

    ,SUM(Quantity_Invoiced+Quantity_Allocated) OVER (PARTITION BY Item_Number) 
    / NULLIF((DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number ASC) + DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number DESC) - 1),0) Average_Order_Quantity

    ,SUM(Quantity_Returned) OVER (PARTITION BY Item_Number) Total_Units_Returned
    ,MAX(Quantity_Returned) OVER (PARTITION BY Item_Number) Max_Quantity_Returned
    ,SUM(Quantity_Returned) OVER (PARTITION BY Item_Number) 
    /NULLIF(SUM(Quantity_Invoiced+Quantity_Allocated) OVER (PARTITION BY Item_Number),0) Return_Percentage

    ,SUM(CASE WHEN F.Line_Status = 'CANCELLED' THEN Quantity_Ordered ELSE 0 END) OVER (PARTITION BY Item_Number) Cancelled_Count
    ,SUM(CASE WHEN F.Line_Status = 'CANCELLED' THEN Quantity_Ordered ELSE 0 END) OVER (PARTITION BY Item_Number) 
    / NULLIF(SUM(Quantity_Ordered) OVER (PARTITION BY Item_Number),0) Cancelled_Count_Percent

    ,SUM(CASE WHEN (Tags not like '%customerrequested_cancel%' and Tags not like '%ia_cancel%' and (FulfillmentState like 'partial%' or FinancialState like 'partial%')) THEN Short_Shipped ELSE 0 END) OVER (PARTITION BY Item_Number) Short_Shipped_Count
    ,SUM(CASE WHEN (Tags not like '%customerrequested_cancel%' and Tags not like '%ia_cancel%' and (FulfillmentState like 'partial%' or FinancialState like 'partial%')) THEN Short_Shipped ELSE 0 END) OVER (PARTITION BY Item_Number) 
    / NULLIF(SUM(Quantity_Ordered) OVER (PARTITION BY Item_Number),0) Short_Shipped_Count_Percent

FROM 
    FinalEcomTable F

WHERE
    1=1
    AND (F.Company_Code = '09' OR '09' IS NULL)  
    AND (F.Division_Code = '001' OR '001' IS NULL)
    AND COALESCE(F.Shopify_Ordered ,F.Date_Entered) BETWEEN '1/1/2018' AND DATEADD(dayofyear, 1, '9/1/2019')
</code></pre>

<p>This query takes one second to run.</p>

<p>However, as soon as I add these next lines</p>

<pre><code>    ,(DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number ASC) + DENSE_RANK() OVER (PARTITION BY Item_Number ORDER BY Customer_Purchase_Order_Number DESC) - 1) 
    / NULLIF(SUM(CASE WHEN F.Order_Status &lt;&gt; 'CANCELLED' AND F.Odet_Line_Number = 1 THEN 1 ELSE 0 END) OVER () ,0) Percent_Of_Orders_Cont
</code></pre>

<p>This query goes from taking 1 seconds to taking 15 seconds. </p>

<p>The Problem is the divisor line</p>

<pre><code>(SUM(CASE WHEN F.Order_Status &lt;&gt; 'CANCELLED' AND F.Odet_Line_Number = 1 THEN 1 ELSE 0 END) OVER ())
</code></pre>

<p>Because if I try to run that line separately, it takes a very long time. </p>

<p>Is there any way to rewrite this line to make it more efficient or optimized? Does anyone know why it is behaving like this? Is it because I am changing the partition by from Item_number to everything? </p>

<p>Here is the execution plan without the offending line:</p>

<p><a href="https://www.brentozar.com/pastetheplan/?id=H1dVjXbDS" rel="nofollow noreferrer">https://www.brentozar.com/pastetheplan/?id=H1dVjXbDS</a></p>

<p>And here it is with the offending line placed back in:</p>

<p><a href="https://www.brentozar.com/pastetheplan/?id=SJy7hXWPr" rel="nofollow noreferrer">https://www.brentozar.com/pastetheplan/?id=SJy7hXWPr</a></p>

