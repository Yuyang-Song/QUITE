# OpenAccess SDK SQL Engine / ODBC compatible way to query only top row from a joined table with a 1-to-many relationship
[Link to question](https://stackoverflow.com/questions/32340304/openaccess-sdk-sql-engine-odbc-compatible-way-to-query-only-top-row-from-a-joi)
**Creation Date:** 1441139191
**Score:** 0
**Tags:** sql-server, sql-server-2008, t-sql, odbc
## Question Body
<p>I'm using a 3rd party ODBC driver for a proprietary application.  </p>

<p>I can run both of the following queries against the database using the proprietary application's other tools, but I need to find a way to rewrite this so that it will work against the ODBC driver.  On the back-end, the application uses SQL Server 2008.</p>

<p>I'm looking for another way to tackle the same problem that hopefully the ODBC driver will be able to understand.</p>

<p>Failed attempt 1 using CROSS APPLY:</p>

<pre><code>SELECT 
    po.Order_No
  , pol.Line_No
  , por.Release_No
  , por.Due_Date
  , por.Quantity
  , por.Quantity_Shipped
  , polp.Effective_Date
  , polp.Price_Change_Reason_Key
FROM Sales_v_PO_e po
INNER JOIN Sales_v_PO_Line_e pol
  ON pol.PO_Key = po.PO_Key
  AND pol.PCN = po.PCN
INNER JOIN Sales_v_Release_e por
  ON por.PO_Line_Key = pol.PO_Line_Key
  AND por.PCN = pol.PCN
CROSS APPLY 
      (
        SELECT TOP 1 Effective_Date, Price_Change_Reason_Key
        FROM Sales_v_Price_e
        WHERE PO_Line_Key = pol.PO_Line_Key
          AND PCN = pol.PCN  
          AND Active = 1
          AND Effective_Date &lt;= por.Due_Date
        ORDER BY Effective_Date DESC, Add_Date DESC
      ) polp
WHERE polp.Effective_Date &lt;= GETDATE()
</code></pre>

<p>This throws the following error:</p>

<blockquote>
  <p>OLE DB provider "MSDASQL" for linked server "MyServer" returned
  message "[Application][ODBC ODBC Report Data Source driver][OpenAccess
  SDK SQL Engine]Syntax error in SQL statement. syntax error line 19 at
  or after token CROSS.[10179]".</p>
</blockquote>

<p>Failed attempt 2 using JOIN:</p>

<pre><code>SELECT 
    po.Order_No
  , pol.Line_No
  , por.Release_No
  , por.Due_Date
  , por.Quantity
  , por.Quantity_Shipped
  , polp.Effective_Date
  , polp.Price_Change_Reason_Key
FROM Sales_v_PO_e po
INNER JOIN Sales_v_PO_Line_e pol
  ON pol.PO_Key = po.PO_Key
  AND pol.PCN = po.PCN
INNER JOIN Sales_v_Release_e por
  ON por.PO_Line_Key = pol.PO_Line_Key
  AND por.PCN = pol.PCN
INNER JOIN  Sales_v_Price_e polp
  ON polp.Price_Key = 
      (
        SELECT TOP 1 Price_Key
        FROM Sales_v_Price_e
        WHERE PO_Line_Key = pol.PO_Line_Key
          AND PCN = pol.PCN  
          AND Active = 1
          AND Effective_Date &lt;= por.Due_Date
        ORDER BY Effective_Date DESC, Add_Date DESC
      )
WHERE polp.Effective_Date &lt;= GETDATE()
</code></pre>

<p>This throws the error:</p>

<blockquote>
  <p>OLE DB provider "MSDASQL" for linked server "MyServer" returned message "[Application][ODBC ODBC Report Data Source driver][OpenAccess SDK SQL Engine]Syntax error in SQL statement. syntax error line 35 at or after token ORDER.[10179]".</p>
</blockquote>

<p>UPDATE:</p>

<p>Here is a 3rd attempt that worked in the SQL environment but failed with the ODBC driver.  This attempt leverages the incrementing integer key to get the last added record.</p>

<pre><code>SELECT 
    po.Order_No
  , pol.Line_No
  , por.Release_No
  , por.Due_Date
  , por.Quantity
  , por.Quantity_Shipped
  , polp.Effective_Date
  , polp.Price_Change_Reason_Key
FROM Sales_v_PO_e po
INNER JOIN Sales_v_PO_Line_e pol
  ON pol.PO_Key = po.PO_Key
  AND pol.PCN = po.PCN
INNER JOIN Sales_v_Release_e por
  ON por.PO_Line_Key = pol.PO_Line_Key
  AND por.PCN = pol.PCN
INNER JOIN Sales_v_Price_e polp
  ON polp.Price_Key =
      (
        SELECT MAX(Price_Key)
        FROM Sales_v_Price_e
        WHERE PO_Line_Key = por.PO_Line_Key
          AND PCN = por.PCN  
          AND Active = 1
          AND Effective_Date &lt;= por.Due_Date
      ) 
WHERE polp.Effective_Date &lt;= GETDATE()
</code></pre>

<p>Throws the error</p>

<blockquote>
  <p>OLE DB provider "MSDASQL" for linked server "MyServer" returned message "[Application][ODBC ODBC Report Data Source driver][OpenAccess SDK SQL Engine]Column:PO_Line_Key not found.[10125]".</p>
</blockquote>

## Answers
### Answer ID: 32341984
<p>It looks like the <a href="http://media.datadirect.com/download/docs/openaccess/alloa/wwhelp/wwhimpl/js/html/wwhelp.htm#href=sqlref/limitations.8.01.html" rel="nofollow">OpenAccess SDK SQL Engine does not support</a> <code>CROSS APPLY</code> joins or sub-queries with <code>TOP</code> in them.  It does appear to allow the <code>ROW_NUMBER</code> function so maybe this would work:</p>

<pre><code>SELECT 
    Order_No
  , Line_No
  , Release_No
  , Due_Date
  , Quantity
  , Quantity_Shipped
  , Effective_Date
  , Price_Change_Reason_Key
FROM 
    (select po.Order_No
      , pol.Line_No
      , por.Release_No
      , por.Due_Date
      , por.Quantity
      , por.Quantity_Shipped
      , polp.Effective_Date
      , polp.Price_Change_Reason_Key
      , ROW_NUMBER() OVER 
          (PARTITION BY po.Order_No, pol.Line_No, por.Release_No
           ORDER BY Effective_Date DESC, Add_Date DESC) RowNum
    FROM Sales_v_PO_e po
    INNER JOIN Sales_v_PO_Line_e pol
      ON pol.PO_Key = po.PO_Key
      AND pol.PCN = po.PCN
    INNER JOIN Sales_v_Release_e por
      ON por.PO_Line_Key = pol.PO_Line_Key
      AND por.PCN = pol.PCN
    INNER JOIN  Sales_v_Price_e polp
      ON PO_Line_Key = pol.PO_Line_Key
      AND PCN = pol.PCN  
      AND Active = 1
      AND Effective_Date &lt;= por.Due_Date
    ) o
WHERE RowNum=1
    and o.Effective_Date &lt;= GETDATE()
</code></pre>

