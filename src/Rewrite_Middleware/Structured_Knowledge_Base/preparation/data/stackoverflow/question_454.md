# FOR XML PATH - how to implement grouping?
[Link to question](https://stackoverflow.com/questions/26994022/for-xml-path-how-to-implement-grouping)
**Creation Date:** 1416312583
**Score:** 0
**Tags:** sql-server, xml, t-sql
## Question Body
<p>I have a T-SQL code which creates XML files out of database table. The tables contain order responses info. Each record represents a line of the response. For each response there are many lines. </p>

<p>The query returns one result for many records in the table. I want to rewrite the query to return one result set for each order response (not each line). The XML file should look like that:</p>

<pre><code>&lt;Line&gt;
  &lt;Line-Item&gt;xxxxxx&lt;/Line-Item&gt;
  &lt;Line-Item&gt;yyyyyy&lt;/Line-Item&gt;
&lt;/Line&gt;
</code></pre>

<p>Currently the code looks like that:</p>

<pre><code>Select '231' as "OrderResponse-Header/OrderResponseType",
   'Const' as "OrderResponse-Header/OrderResponseNumber", 
   coalesce(convert(varchar(10), GETDATE(), 20), '') as "OrderResponse-Header/OrderResponseDate",
   coalesce(T.OrderNumber, '') as "OrderResponse-Header/OrderNumber",
   coalesce(convert(varchar(10), GETDATE(), 20), '') as "OrderResponse-Header/OrderDate",
   '0' as "OrderResponse-Header/DocumentFunctionCode",

    '' as "DetailsOfTransport/TermsOfDelivery",
    '' as "OrderResponse-Parties/Buyer/ILN",
    '' as "OrderResponse-Parties/Buyer/PartyName",
    '' as "OrderResponse-Parties/Buyer/StreetAndNumber",
    '' as "OrderResponse-Parties/Buyer/CityName",
    '' as "OrderResponse-Parties/Buyer/PostCode",
    '' as "OrderResponse-Parties/Buyer/Country",

    '' as "OrderResponse-Parties/Seller/ILN",
    '' as "OrderResponse-Parties/Seller/PartyName",
    '' as "OrderResponse-Parties/Seller/StreetAndNumber",
    '' as "OrderResponse-Parties/Seller/CityName",
    '' as "OrderResponse-Parties/Seller/PostCode",
    '' as "OrderResponse-Parties/Seller/Country",

    '' as "OrderResponse-Parties/DeliveryPoint/ILN",

    '' as "OrderResponse-Parties/ShipFrom/ILN",

    coalesce(T.LineNumber, '') as "OrderResponse-Lines/Line/Line-Item/LineNumber",
    coalesce(T.BuyerItemCode, '') as "OrderResponse-Lines/Line/Line-Item/BuyerItemCode",
    '' as "OrderResponse-Lines/Line/Line-Item/ItemDescription",
    '' as "OrderResponse-Lines/Line/Line-Item/ItemStatus",
    '' as "OrderResponse-Lines/Line/Line-Item/ItemType",
    '0' as "OrderResponse-Lines/Line/Line-Item/OrderedQuantity",
    coalesce(T.QuantityToBeDelivered, '') as "OrderResponse-Lines/Line/Line-Item/QuantityToBeDelivered",
    '0' as "OrderResponse-Lines/Line/Line-Item/QuantityDifference",
    '' as "OrderResponse-Lines/Line/Line-Item/UnitOfMeasure",
    '0' as "OrderResponse-Lines/Line/Line-Item/OrderedUnitNetPrice",
    '0' as "OrderResponse-Lines/Line/Line-Item/Discount",
    coalesce(convert(varchar(10), T.ExpectedDeliveryDate, 20), '') as "OrderResponse-Lines/Line/Line-Item/ExpectedDeliveryDate",
    '0' as "OrderResponse-Summary/TotalLines"
from Import.OrderResponses as T
where T.OrderNumber = 'Gr342'
for xml path(''), root('Document-OrderResponse'), type
</code></pre>

<p>EDIT:
Here is the example of a result from 2 order response lines: The Line and Line-Item nodes are completely separate (in 2 different blocks, but they should be in the same one. </p>

<p>I tried creating abother table for lines and join it to the Order Response table but it didnt help.</p>

<pre><code>  &lt;Document-OrderResponse&gt;
  &lt;OrderResponse-Header&gt;
    &lt;OrderResponseType&gt;231&lt;/OrderResponseType&gt;
    &lt;OrderResponseNumber&gt;Const&lt;/OrderResponseNumber&gt;
    &lt;OrderResponseDate&gt;2014-11-19&lt;/OrderResponseDate&gt;
    &lt;OrderNumber&gt;Gr342&lt;/OrderNumber&gt;
    &lt;OrderDate&gt;2014-11-19&lt;/OrderDate&gt;
    &lt;DocumentFunctionCode&gt;0&lt;/DocumentFunctionCode&gt;
  &lt;/OrderResponse-Header&gt;
  &lt;DetailsOfTransport&gt;
    &lt;TermsOfDelivery&gt;&lt;/TermsOfDelivery&gt;
  &lt;/DetailsOfTransport&gt;
  &lt;OrderResponse-Parties&gt;
    &lt;Buyer&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
      &lt;PartyName&gt;&lt;/PartyName&gt;
      &lt;StreetAndNumber&gt;&lt;/StreetAndNumber&gt;
      &lt;CityName&gt;&lt;/CityName&gt;
      &lt;PostCode&gt;&lt;/PostCode&gt;
      &lt;Country&gt;&lt;/Country&gt;
    &lt;/Buyer&gt;
    &lt;Seller&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
      &lt;PartyName&gt;&lt;/PartyName&gt;
      &lt;StreetAndNumber&gt;&lt;/StreetAndNumber&gt;
      &lt;CityName&gt;&lt;/CityName&gt;
      &lt;PostCode&gt;&lt;/PostCode&gt;
      &lt;Country&gt;&lt;/Country&gt;
    &lt;/Seller&gt;
    &lt;DeliveryPoint&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
    &lt;/DeliveryPoint&gt;
    &lt;ShipFrom&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
    &lt;/ShipFrom&gt;
  &lt;/OrderResponse-Parties&gt;
  &lt;OrderResponse-Lines&gt;
    &lt;Line&gt;
      &lt;Line-Item&gt;
        &lt;LineNumber&gt;3&lt;/LineNumber&gt;
        &lt;BuyerItemCode&gt;gesgrere&lt;/BuyerItemCode&gt;
        &lt;ItemDescription&gt;&lt;/ItemDescription&gt;
        &lt;ItemStatus&gt;&lt;/ItemStatus&gt;
        &lt;ItemType&gt;&lt;/ItemType&gt;
        &lt;OrderedQuantity&gt;0&lt;/OrderedQuantity&gt;
        &lt;QuantityToBeDelivered&gt;55&lt;/QuantityToBeDelivered&gt;
        &lt;QuantityDifference&gt;0&lt;/QuantityDifference&gt;
        &lt;UnitOfMeasure&gt;&lt;/UnitOfMeasure&gt;
        &lt;OrderedUnitNetPrice&gt;0&lt;/OrderedUnitNetPrice&gt;
        &lt;Discount&gt;0&lt;/Discount&gt;
        &lt;ExpectedDeliveryDate&gt;2014-02-12&lt;/ExpectedDeliveryDate&gt;
      &lt;/Line-Item&gt;
    &lt;/Line&gt;
  &lt;/OrderResponse-Lines&gt;
  &lt;OrderResponse-Summary&gt;
    &lt;TotalLines&gt;0&lt;/TotalLines&gt;
  &lt;/OrderResponse-Summary&gt;
  &lt;OrderResponse-Header&gt;
    &lt;OrderResponseType&gt;231&lt;/OrderResponseType&gt;
    &lt;OrderResponseNumber&gt;Const&lt;/OrderResponseNumber&gt;
    &lt;OrderResponseDate&gt;2014-11-19&lt;/OrderResponseDate&gt;
    &lt;OrderNumber&gt;Gr342&lt;/OrderNumber&gt;
    &lt;OrderDate&gt;2014-11-19&lt;/OrderDate&gt;
    &lt;DocumentFunctionCode&gt;0&lt;/DocumentFunctionCode&gt;
  &lt;/OrderResponse-Header&gt;
  &lt;DetailsOfTransport&gt;
    &lt;TermsOfDelivery&gt;&lt;/TermsOfDelivery&gt;
  &lt;/DetailsOfTransport&gt;
  &lt;OrderResponse-Parties&gt;
    &lt;Buyer&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
      &lt;PartyName&gt;&lt;/PartyName&gt;
      &lt;StreetAndNumber&gt;&lt;/StreetAndNumber&gt;
      &lt;CityName&gt;&lt;/CityName&gt;
      &lt;PostCode&gt;&lt;/PostCode&gt;
      &lt;Country&gt;&lt;/Country&gt;
    &lt;/Buyer&gt;
    &lt;Seller&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
      &lt;PartyName&gt;&lt;/PartyName&gt;
      &lt;StreetAndNumber&gt;&lt;/StreetAndNumber&gt;
      &lt;CityName&gt;&lt;/CityName&gt;
      &lt;PostCode&gt;&lt;/PostCode&gt;
      &lt;Country&gt;&lt;/Country&gt;
    &lt;/Seller&gt;
    &lt;DeliveryPoint&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
    &lt;/DeliveryPoint&gt;
    &lt;ShipFrom&gt;
      &lt;ILN&gt;&lt;/ILN&gt;
    &lt;/ShipFrom&gt;
  &lt;/OrderResponse-Parties&gt;
  &lt;OrderResponse-Lines&gt;
    &lt;Line&gt;
      &lt;Line-Item&gt;
        &lt;LineNumber&gt;3&lt;/LineNumber&gt;
        &lt;BuyerItemCode&gt;gesgrere&lt;/BuyerItemCode&gt;
        &lt;ItemDescription&gt;&lt;/ItemDescription&gt;
        &lt;ItemStatus&gt;&lt;/ItemStatus&gt;
        &lt;ItemType&gt;&lt;/ItemType&gt;
        &lt;OrderedQuantity&gt;0&lt;/OrderedQuantity&gt;
        &lt;QuantityToBeDelivered&gt;55&lt;/QuantityToBeDelivered&gt;
        &lt;QuantityDifference&gt;0&lt;/QuantityDifference&gt;
        &lt;UnitOfMeasure&gt;&lt;/UnitOfMeasure&gt;
        &lt;OrderedUnitNetPrice&gt;0&lt;/OrderedUnitNetPrice&gt;
        &lt;Discount&gt;0&lt;/Discount&gt;
        &lt;ExpectedDeliveryDate&gt;2014-02-12&lt;/ExpectedDeliveryDate&gt;
      &lt;/Line-Item&gt;
    &lt;/Line&gt;
  &lt;/OrderResponse-Lines&gt;
  &lt;OrderResponse-Summary&gt;
    &lt;TotalLines&gt;0&lt;/TotalLines&gt;
  &lt;/OrderResponse-Summary&gt;
&lt;/Document-OrderResponse&gt;
</code></pre>

## Answers
### Answer ID: 27012012
<p>The code:</p>

<pre><code>select '' as "OrderResponse-Lines/Line/Line-Item/ItemDescription",
    '' as "OrderResponse-Lines/Line/Line-Item/ItemStatus",
    '' as "OrderResponse-Lines/Line/Line-Item/ItemType"
for xml path(''), root('Document-OrderResponse'), type;
</code></pre>

<p>results in:</p>

<pre><code>&lt;Document-OrderResponse&gt;
  &lt;OrderResponse-Lines&gt;
    &lt;Line&gt;
      &lt;Line-Item&gt;
        &lt;ItemDescription&gt;&lt;/ItemDescription&gt;
        &lt;ItemStatus&gt;&lt;/ItemStatus&gt;
        &lt;ItemType&gt;&lt;/ItemType&gt;
      &lt;/Line-Item&gt;
    &lt;/Line&gt;
  &lt;/OrderResponse-Lines&gt;
&lt;/Document-OrderResponse&gt;
</code></pre>

<p>A single <code>/Line</code> and <code>/Line-Item</code> nodes are created, as you can see. My <code>@@version</code>:</p>

<blockquote>
  <p>Microsoft SQL Server 2012 - 11.0.5058.0 (X64)     May 14 2014 18:34:29 
    Copyright (c) Microsoft Corporation     Developer Edition (64-bit) on
  Windows NT 6.1  (Build 7601: Service Pack 1)</p>
</blockquote>

<p>EDIT: Ah, I see. Looks like you have duplicated rows in your table. What is the result of:</p>

<p><code>select count(*) from Import.OrderResponses where T.OrderNumber = 'Gr342';</code></p>

### Answer ID: 27012021
<pre><code>SELECT
   '231' AS "OrderResponse-Header/OrderResponseType",
   'Const' AS "OrderResponse-Header/OrderResponseNumber", 
   COALESCE(CONVERT(VARCHAR(10), GETDATE(), 20), '') AS "OrderResponse-Header/OrderResponseDate",
   COALESCE(T.OrderNumber, '') AS "OrderResponse-Header/OrderNumber",
   COALESCE(CONVERT(VARCHAR(10), GETDATE(), 20), '') AS "OrderResponse-Header/OrderDate",
   '0' AS "OrderResponse-Header/DocumentFunctionCode",

   /* ... */

   (
      SELECT
         COALESCE(T1.LineNumber, '') AS "LineNumber",
         COALESCE(T1.BuyerItemCode, '') AS "BuyerItemCode",
         '' AS "ItemDescription",
         '' AS "ItemStatus",
         '' AS "ItemType",
         '0' AS "OrderedQuantity",
         COALESCE(T1.QuantityToBeDelivered, '') AS "QuantityToBeDelivered",
         '0' AS "QuantityDifference",
         '' AS "UnitOfMeasure",
         '0' AS "OrderedUnitNetPrice",
         '0' AS "Discount",
         COALESCE(CONVERT(VARCHAR(10), T1.ExpectedDeliveryDate, 20), '') AS "ExpectedDeliveryDate"
      FROM Import.OrderResponses AS T1
      WHERE T1.OrderNumber = T.OrderNumber
      FOR XML PATH('Line-Item'), ROOT('Line'), TYPE
   ) AS "OrderResponse-Lines",
   '0' AS "OrderResponse-Summary/TotalLines"
FROM Import.OrderResponses AS T
WHERE T.OrderNumber = 'Gr342'
GROUP BY T.OrderNumber
FOR XML PATH(''), ROOT('Document-OrderResponse'), TYPE
</code></pre>

<p>I am not sure if you want the <code>&lt;Line&gt;</code> element or the <code>&lt;Line-Item&gt;</code> element repeated. I chose the <code>&lt;Line-Item&gt;</code> element, but it should be easy to change by manipulating the <code>FOR XML</code> arguments.</p>

