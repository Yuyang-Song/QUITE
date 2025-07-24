# SQL multiple results in one cell
[Link to question](https://stackoverflow.com/questions/31969146/sql-multiple-results-in-one-cell)
**Creation Date:** 1439392284
**Score:** 0
**Tags:** sql, sql-server, t-sql, sql-server-2008-r2
## Question Body
<p>I have a database in which an invoice can be linked to multiple orders. I'd like to have multiple results from the order table put in one cell, but (And that's the problem) I need to have the orders filtered the same way as they are from the main query, without rewriting them in the subquery. I doubt it is possible, but the idea is actually to rely as much as possible on the main query, mainly because the columns are created automatically and independently of the conditions.</p>

<p>The query:</p>

<pre><code>SELECT [Invoice].INV_ID AS 'Invoice ID',
       INV_TIT AS 'Invoice title', 
       (SELECT CAST((SELECT ORD_TIT + ' | ' FROM ORD WHERE ORD_ID IN ([Order].ORD_ID) FOR XML PATH('')) AS VARCHAR(MAX))) AS 'Order list'
FROM INV [Invoice]
JOIN INV_ORD [InvoiceOrder] ON [Invoice].INV_ID = [InvoiceOrder].INV_ID 
INNER JOIN ORD [Order] ON [InvoiceOrder].ORD_ID = [Order].ORD_ID
WHERE [Invoice].INV_ID IN (29517, 30951, 42048)
  AND [Invoice].INV_ISDEL = 0
  AND [Order].ORD_DAT = GETDATE()
</code></pre>

<p>The result:</p>

<pre><code>╔════════════╦════════════════╦═══════════════════╗
║ Invoice ID ║ Invoice title  ║ Order list        ║
╠════════════╬════════════════╬═══════════════════╣
║ 1          ║ Cinema tickets ║ 1 cinema ticket   ║
║ 1          ║ Cinema tickets ║ 2 cinema tickets  ║
║ 2          ║ Groceries      ║ 1 toothbrush      ║
║ 2          ║ Groceries      ║ 5 shampoo bottles ║
╚════════════╩════════════════╩═══════════════════╝
</code></pre>

<p>The desired result:</p>

<pre><code>╔════════════╦════════════════╦════════════════════════════════════╗
║ Invoice ID ║ Invoice title  ║ Order list                         ║
╠════════════╬════════════════╬════════════════════════════════════╣
║ 1          ║ Cinema tickets ║ 1 cinema ticket | 2 cinema tickets ║
║ 2          ║ Groceries      ║ 1 toothbrush | 5 shampoo bottles   ║
╚════════════╩════════════════╩════════════════════════════════════╝
</code></pre>

## Answers
### Answer ID: 31980081
<p>try:</p>

<pre><code>create table #tmp (Id int,value1 varchar(max),value2 varchar(max))

insert into #tmp values
(1,'Cinema tickets','1 cinema ticket'),
(1,'Cinema tickets','2 cinema tickets'),
(2,'Groceries','1 toothbrush '),
(2,'Groceries','5 shampoo bottles')


SELECT Id,value1,STUFF(
             (SELECT '|' + value2 
              FROM #tmp where Id=t.Id
              FOR XML PATH (''))
             , 1, 1, '') from #tmp t group by Id,value1
</code></pre>

