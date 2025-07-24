# Query runs quickly in Oracle SQL Developer, but slowly in SSRS 2008 R2
[Link to question](https://stackoverflow.com/questions/4788987/query-runs-quickly-in-oracle-sql-developer-but-slowly-in-ssrs-2008-r2)
**Creation Date:** 1295917431
**Score:** 11
**Tags:** sql-server, oracle-database, ssrs-2008, oracle11g, execution-time
## Question Body
<p>It's that simple: a query that runs in just a few seconds in SQL Developer connecting to Oracle 11g takes 15-25 minutes in SSRS 2008 R2. I haven't tried other versions of SSRS. So far I'm doing all the report execution from VS 2008.</p>

<p>I'm using the OLE DB Provider "OraOLEDB.Oracle.1" which in the past has seemed to give me better results than using the Oracle provider.</p>

<p><strong>Here's what I've been able to determine so far:</strong></p>

<p>• The delay is during the DataSet execution phase and has nothing to do with the result set or rendering time. (Proving by selecting the same rowset directly from a table I inserted it to.)</p>

<p>• SSRS itself is not hung up. It is truly waiting for Oracle which is where the delay is (proven by terminating the DB session from the Oracle side, which resulted in a prompt error in SSRS about the session being killed).</p>

<p>• I have tried direct queries with parameters in the form :Parameter. Very early versions of my query that were more simple worked okay for direct querying, but it seemed like past a certain complexity, the query would start taking forever from SSRS.</p>

<p>• I then switched to executing an SP that inserts the query results to a table or global temp table. This helped for a little while, getting me farther than direct querying, but again, it almost seems like increased query complexity or length eventually broke this method, too. Note: running a table-populating SP works because with option "use single transaction" checked in the DataSource options, DataSets are then run in the order of their appearance in the rdl file. DataSets that return no Fields are still run, as long as all their parameters are satisfied.</p>

<p>• I just tried a table-returning function and this still made no improvement, even though direct calls with literal parameters in SQL Developer return in 1-5 seconds.</p>

<p>• The database in question does not have statistics. It is part of a product created by a vendor and we have not had the time or management buy-in to create/update statistics. I played with the DYNAMIC_SAMPLING hint to calculate statistics on the fly and got a better execution plan: without statistics the cost-based optimizer had been poorly using a LOOP join instead of a HASH join, causing similar many-minute execution times. Thus I put in query hints to force join order and also to cause it to use the strategic hash join, bringing the execution time back down to just seconds. I did not go back and try direct querying in SSRS using these execution hints.</p>

<p>• I got some help from our Oracle DBA who set up a trace (or whatever the Oracle equivalent is) and he was able to see things being run, but he hasn't found anything useful so far. Unfortunately his time is limited and we haven't been able to really dig in to find out what's being executed server-side. I don't have the experience to do this quickly or the time to study up on how to do this myself. Suggestions on what to do to determine what's going on would be appreciated.</p>

<p><strong>My only hypotheses are:</strong></p>

<p>• The query is somehow getting a bad execution plan. E.g., improperly using a LOOP join instead of a HASH join when there are tens of thousands of "left" or outer-loop rows rather than just a few hundred.</p>

<p>• SSRS could be submitting the parameters as nvarchar(4000) or something instead of something reasonable, and as Oracle SP &amp; function parameters don't have length specifications but get their execution lengths from the query call, then some process such as parameter sniffing is messing up the execution plan as in the previous point.</p>

<p>• The query is somehow being rewritten by SSRS/the provider. I AM using a multi-valued parameter, but not as is: the parameter is being submitted as expression Join(Parameters!MultiValuedParameter.Value, ",") so it shouldn't need any rewriting. Just a simple binding and submitting. I don't see how this could be true in the SP and the function calls, but gosh, what else could it be?</p>

<p>I realize it is a very complicated and lengthy query, but it does exactly what I need. It runs in 1-5 seconds depending on how much data is asked for. Some of the reasons for the complexity are:</p>

<ul>
<li>Properly handling the comma-separated cost center list parameter</li>
<li>Allowing the weekly breakdown to be optional and if included, ensuring all the weeks in a month are shown even if there is no data for them.</li>
<li>Showing "No Invoices" when appropriate.</li>
<li>Allowing a variable number of summary months.</li>
<li>Having an optional YTD total.</li>
<li>Including previous/historical comparison data means I can't simply use <em>this</em> month's vendors, I have to show all the vendors that will be in any historical column.</li>
</ul>

<p>Anyway, so here's the query, SP version (though I don't think it will be much help).</p>

<pre><code>create or replace
PROCEDURE VendorInvoiceSummary (
   FromDate IN date,
   ToDate IN date,
   CostCenterList IN varchar2,
   IncludeWeekly IN varchar2,
   ComparisonMonths IN number,
   IncludeYTD IN varchar2
)
AS
BEGIN

INSERT INTO InvoiceSummary (Mo, CostCenter, Vendor, VendorName, Section, TimeUnit, Amt)
SELECT
   Mo,
   CostCenter,
   Vendor,
   VendorName,
   Section,
   TimeUnit,
   Amt
FROM (
   WITH CostCenters AS (
      SELECT Substr(REGEXP_SUBSTR(CostCenterList, '[^,]+', 1, LEVEL) || '               ', 1, 15) CostCenter
      FROM DUAL
      CONNECT BY LEVEL &lt;= Length(CostCenterList) - Length(Replace(CostCenterList, ',', '')) + 1
   ), Invoices AS (
      SELECT  /*+ORDERED USE_HASH(D)*/
         TRUNC(I.Invoice_Dte, 'YYYY') Yr,
         TRUNC(I.Invoice_Dte, 'MM') Mo,
         D.Dis_Acct_Unit CostCenter,
         I.Vendor,
         V.Vendor_VName,
         CASE
            WHEN I.Invoice_Dte &gt;= FromDate AND I.Invoice_Dte &lt; ToDate
            THEN (TRUNC(I.Invoice_Dte, 'W') - TRUNC(I.Invoice_Dte, 'MM')) / 7 + 1
            ELSE 0
         END WkNum,
         Sum(D.To_Base_Amt) To_Base_Amt
      FROM
         ICCompany C
         INNER JOIN APInvoice I
            ON C.Company = I.Company
         INNER JOIN APDistrib D
            ON C.Company = D.Company
            AND I.Invoice = D.Invoice
            AND I.Vendor = D.Vendor
            AND I.Suffix = D.Suffix
         INNER JOIN CostCenters CC
            ON D.Dis_Acct_Unit = CC.CostCenter
         INNER JOIN APVenMast V ON I.Vendor = V.Vendor
      WHERE
         D.Cancel_Seq = 0
         AND I.Cancel_Seq = 0
         AND I.Invoice_Dte &gt;= Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY'))
         AND I.Invoice_Dte &lt; ToDate
         AND V.Vendor_Group = '1   ' -- index help
      GROUP BY
         TRUNC(I.Invoice_Dte, 'YYYY'),
         TRUNC(I.Invoice_Dte, 'MM'),
         D.Dis_Acct_Unit,
         I.Vendor,
         V.Vendor_VName,
         CASE
            WHEN I.Invoice_Dte &gt;= FromDate AND I.Invoice_Dte &lt; ToDate
            THEN (TRUNC(I.Invoice_Dte, 'W') - TRUNC(I.Invoice_Dte, 'MM')) / 7 + 1
            ELSE 0
         END
   ), Months AS (
      SELECT ADD_MONTHS(Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY')), LEVEL - 1) Mo
      FROM DUAL
      CONNECT BY LEVEL &lt;= MONTHS_BETWEEN(ToDate, Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY')))
   ), Sections AS (
      SELECT 1 Section, 1 StartUnit, 5 EndUnit FROM DUAL
      UNION ALL SELECT 2, 0, ComparisonMonths FROM DUAL
      UNION ALL SELECT 3, 1, 1 FROM DUAL WHERE IncludeYTD = 'Y'
   ), Vals AS (
      SELECT LEVEL - 1 TimeUnit
      FROM DUAL
      CONNECT BY LEVEL &lt;= (SELECT Max(EndUnit) FROM Sections) + 1
   ), TimeUnits AS (
      SELECT S.Section, V.TimeUnit
      FROM
         Sections S
         INNER JOIN Vals V
            ON V.TimeUnit BETWEEN S.StartUnit AND S.EndUnit
   ), Names AS (
      SELECT DISTINCT
         M.Mo,
         Coalesce(I.Vendor, '0') Vendor,
         Coalesce(I.Vendor_VName, 'No Paid Invoices') Vendor_VName,
         Coalesce(I.CostCenter, ' ') CostCenter
      FROM
         Months M
         LEFT JOIN Invoices I
            ON Least(ADD_MONTHS(M.Mo, -ComparisonMonths), TRUNC(M.Mo, 'YYYY')) &lt; I.Mo
            AND M.Mo &gt;= I.Mo
      WHERE
         M.Mo &gt;= FromDate
         AND M.Mo &lt; ToDate
   )
   SELECT
      N.Mo,
      N.CostCenter,
      N.Vendor,
      N.Vendor_VName VendorName,
      T.Section,
      T.TimeUnit,
      Sum(I.To_Base_Amt) Amt
   FROM
      Names N
      CROSS JOIN TimeUnits T
      LEFT JOIN Invoices I
         ON N.CostCenter = I.CostCenter
         AND N.Vendor = I.Vendor
         AND (
            (
               T.Section = 1 -- Weeks for current month
               AND N.Mo = I.Mo
               AND T.TimeUnit = I.WkNum
            ) OR (
               T.Section = 2 -- Summary months
               AND ADD_MONTHS(N.Mo, -T.TimeUnit) = I.Mo
            ) OR (
               T.Section = 3 -- YTD
               AND I.Mo BETWEEN TRUNC(N.Mo, 'YYYY') AND N.Mo
            )
         )
   WHERE
      N.Mo &gt;= FromDate
      AND N.Mo &lt; ToDate
      AND NOT ( -- Only 4 weeks when a month is less than 28 days long
         T.Section = 2
         AND T.TimeUnit = 5
         AND TRUNC(N.Mo + 28, 'MM') &lt;&gt; N.Mo
         AND I.CostCenter IS NULL
      ) AND (
         T.Section &lt;&gt; 1
         OR IncludeWeekly = 'Y'
      )
   GROUP BY
      N.Mo,
      N.CostCenter,
      N.Vendor,
      N.Vendor_VName,
      T.Section,
      T.TimeUnit
) X;
COMMIT;
END;
</code></pre>

<p><strong>UPDATE</strong></p>

<p>Even after learning all about Oracle execution plans and hints (to translate my SQL Server knowledge), I still could not get the query to run quickly in SSRS until I made it run in two steps, first to put the real table results into a <code>GLOBAL TEMPORARY TABLE</code> and then second to extract the data from that. <code>DYNAMIC_SAMPLING</code> gave me a good execution plan, which I then copied using join and access hints. Here's the final SP (it couldn't be a function because in Oracle you can't do DML in a function when that function is called inside of a SELECT statement):</p>

<p>Sometimes I swear it was ignoring my join hints such as <code>swap_join_inputs</code> and <code>no_swap_join_inputs</code> but from my reading apparently Oracle only ignores hints when they can't actually be used or you're doing something wrong. Fortunately, the tables swapped appropriately (as in the case of <code>USE_NL(CC)</code> it reliably puts the CC table as the swapped, left input, even though it's joined last).</p>

<pre><code>CREATE OR REPLACE
PROCEDURE VendorInvoicesSummary (
   FromDate IN date,
   ToDate IN date,
   CostCenterList IN varchar2,
   IncludeWeekly IN varchar2,
   ComparisonMonths IN number,
   IncludeYTD IN varchar2
)
AS
BEGIN

INSERT INTO InvoiceTemp (Yr, Mo, CostCenter, Vendor, WkNum, Amt) -- A global temporary table
SELECT /*+LEADING(C I D CC) USE_HASH(I D) USE_NL(CC)*/
   TRUNC(I.Invoice_Dte, 'YYYY') Yr,
   TRUNC(I.Invoice_Dte, 'MM') Mo,
   D.Dis_Acct_Unit CostCenter,
   I.Vendor,
   CASE
      WHEN I.Invoice_Dte &gt;= FromDate AND I.Invoice_Dte &lt; ToDate
      THEN (TRUNC(I.Invoice_Dte, 'W') - TRUNC(I.Invoice_Dte, 'MM')) / 7 + 1
      ELSE 0
   END WkNum,
   Sum(D.To_Base_Amt) To_Base_Amt
FROM
   ICCompany C
   INNER JOIN APInvoice I
      ON C.Company = I.Company
   INNER JOIN APDistrib D
      ON C.Company = D.Company
      AND I.Invoice = D.Invoice
      AND I.Vendor = D.Vendor
      AND I.Suffix = D.Suffix
   INNER JOIN (
      SELECT Substr(REGEXP_SUBSTR(CostCenterList, '[^,]+', 1, LEVEL) || '               ', 1, 15) CostCenter
      FROM DUAL
      CONNECT BY LEVEL &lt;= Length(CostCenterList) - Length(Replace(CostCenterList, ',', '')) + 1
   ) CC ON D.Dis_Acct_Unit = CC.CostCenter
WHERE
   D.Cancel_Seq = 0
   AND I.Cancel_Seq = 0
   AND I.Invoice_Dte &gt;= Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY'))
   AND I.Invoice_Dte &lt; ToDate
GROUP BY
   TRUNC(I.Invoice_Dte, 'YYYY'),
   TRUNC(I.Invoice_Dte, 'MM'),
   D.Dis_Acct_Unit,
   I.Vendor,
   CASE
      WHEN I.Invoice_Dte &gt;= FromDate AND I.Invoice_Dte &lt; ToDate
      THEN (TRUNC(I.Invoice_Dte, 'W') - TRUNC(I.Invoice_Dte, 'MM')) / 7 + 1
      ELSE 0
   END;

INSERT INTO InvoiceSummary (Mo, CostCenter, Vendor, VendorName, Section, TimeUnit, Amt)
SELECT
   Mo,
   CostCenter,
   Vendor,
   VendorName,
   Section,
   TimeUnit,
   Amt
FROM (
   WITH Months AS (
      SELECT ADD_MONTHS(Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY')), LEVEL - 1) Mo
      FROM DUAL
      CONNECT BY LEVEL &lt;= MONTHS_BETWEEN(ToDate, Least(ADD_MONTHS(FromDate, -ComparisonMonths), TRUNC(FromDate, 'YYYY')))
   ), Sections AS (
      SELECT 1 Section, 1 StartUnit, 5 EndUnit FROM DUAL
      UNION ALL SELECT 2, 0, ComparisonMonths FROM DUAL
      UNION ALL SELECT 3, 1, 1 FROM DUAL WHERE IncludeYTD = 'Y'
   ), Vals AS (
      SELECT LEVEL - 1 TimeUnit
      FROM DUAL
      CONNECT BY LEVEL &lt;= (SELECT Max(EndUnit) FROM Sections) + 1
   ), TimeUnits AS (
      SELECT S.Section, V.TimeUnit
      FROM
         Sections S
         INNER JOIN Vals V
            ON V.TimeUnit BETWEEN S.StartUnit AND S.EndUnit
   ), Names AS (
      SELECT DISTINCT
         M.Mo,
         Coalesce(I.Vendor, '0') Vendor,
         Coalesce(I.CostCenter, ' ') CostCenter
      FROM
         Months M
         LEFT JOIN InvoiceTemp I
            ON Least(ADD_MONTHS(M.Mo, -ComparisonMonths), TRUNC(M.Mo, 'YYYY')) &lt;= I.Mo
            AND I.Mo &lt;= M.Mo
      WHERE
         M.Mo &gt;= FromDate
         AND M.Mo &lt; ToDate
   )
   SELECT
      N.Mo,
      N.CostCenter,
      N.Vendor,
      Coalesce(V.Vendor_VName, 'No Paid Invoices') VendorName,
      T.Section,
      T.TimeUnit,
      Sum(I.Amt) Amt
   FROM
      Names N
      INNER JOIN APVenMast V ON N.Vendor = V.Vendor
      CROSS JOIN TimeUnits T
      LEFT JOIN InvoiceTemp I
         ON N.CostCenter = I.CostCenter
         AND N.Vendor = I.Vendor
         AND (
            (
               T.Section = 1 -- Weeks for current month
               AND N.Mo = I.Mo
               AND T.TimeUnit = I.WkNum
            ) OR (
               T.Section = 2 -- Summary months
               AND ADD_MONTHS(N.Mo, -T.TimeUnit) = I.Mo
            ) OR (
               T.Section = 3 -- YTD
               AND I.Mo BETWEEN TRUNC(N.Mo, 'YYYY') AND N.Mo
            )
         )
   WHERE
      N.Mo &gt;= FromDate
      AND N.Mo &lt; ToDate
      AND V.Vendor_Group = '1   '
      AND NOT ( -- Only 4 weeks when a month is less than 28 days long
         T.Section = 2
         AND T.TimeUnit = 5
         AND TRUNC(N.Mo + 28, 'MM') &lt;&gt; N.Mo
         AND I.CostCenter IS NULL
      ) AND (
         T.Section &lt;&gt; 1
         OR IncludeWeekly = 'Y'
      )
   GROUP BY
      N.Mo,
      N.CostCenter,
      N.Vendor,
      V.Vendor_VName,
      T.Section,
      T.TimeUnit
) X;

COMMIT;
END;
</code></pre>

<p>This has been a long, painful ride, but if there's one thing I've learned it's that working in a database without properly updated statistics (which I'm going to look into getting our DBA to add even though the vendor doesn't care about them) can be a real disaster for someone who wants to get things done in a reasonable amount of time.</p>

## Answers
### Answer ID: 78959773
<p>For anyone else encountering this issue with SSRS and an Oracle database this may be the golden bullet you are looking for.</p>
<p>We had the same issue with SSRS and an Oracle Database. The query through SQL developer would run very quickly(seconds) but very slowly within SSRS(Minutes). We stumbled across an Oracle guide which had a golden bullet fix for this issue on pages 16 and 17. After making the change it and restarting SSRS it exponentially improved the reports performance.</p>
<p>Typically, BI and ETL applications retrieve large data amounts from a source database for further
processing. To speed up Oracle data retrieval via SSIS or SSRS, the ODP.NET FetchSize can be
increased from its default 128K value (131,072 bytes) to as large as int.MaxValue. The FetchSize
determines the amount of data ODP.NET fetches into its internal cache upon each database round
trip. It’s possible to improve performance by an order of magnitude by significantly increasing
FetchSize when retrieving large result sets.</p>
<p><a href="https://www.oracle.com/a/otn/docs/database/connecting-ssrs-to-oracle-adb.pdf" rel="nofollow noreferrer">connecting-ssrs-to-oracle-adb</a></p>

### Answer ID: 18005204
<p>I know this is old but we had a similar problem and had to set the nsl_sort to binary instead of binary_ci.  People could try setting the session to binary: alter session set nls_sort=binary</p>

### Answer ID: 4789281
<p>Posting the query may help.</p>

<p>Your DBA should be able to identify the session in a view called v$session, and the columns EVENT and WAIT_CLASS should give an indication of what is happening on the Oracle end.</p>

<p>He would also be able to identify the SQL (SQL_ID from v$session) and use that in a SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(sql_id)) to determine the plan.</p>

<p>If it is a development/test instance, see if he will grant you permissions to do that yourself if he (or she) is busy.</p>

