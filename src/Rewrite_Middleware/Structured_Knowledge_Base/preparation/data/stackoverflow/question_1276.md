# Union of multiple Database queries with same parameters
[Link to question](https://stackoverflow.com/questions/67816114/union-of-multiple-database-queries-with-same-parameters)
**Creation Date:** 1622699946
**Score:** 2
**Tags:** sql, hana
## Question Body
<p>I am having this code and its running as expected. However I am trying to find a better way to rewrite the following query as it can be seen that the dates and account codes are repeated all the time.</p>
<p>The data is being extracted from 3 Databases i.e. Db1, Db2 and Db3.
The tables of each Database are similar. Even the AcctCodes to be extracted are similar.</p>
<p>So,I am wondering if the following code can be rewritten in few lines.</p>
<p>Since, the AcctCodes are similar, so adding an empty row with database name as Headers between each query helps me to identify them.</p>
<blockquote>
<p>Select 'Outlet1','0','0' from Dummy</p>
</blockquote>
<p>So if there is a better version of the following code, please let me know. Thanks.</p>
<pre><code>Select 'Outlet1','0','0' from Dummy

UNION ALL

SELECT 
    T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db1.Table1 T0  
        INNER JOIN Db1.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db1.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001','105008001','105009001','105104001','105105001','105106001',
        '105107001','105108001','105109001','106001001','107009001','109018001','109022001','201001001','201002001'
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;

UNION ALL

Select 'Outlet2','0','0' from Dummy

UNION ALL

SELECT 
    T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db2.Table1 T0  
        INNER JOIN Db2.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db2.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001','105008001','105009001','105104001','105105001','105106001',
        '105107001','105108001','105109001','106001001','107009001','109018001','109022001','201001001','201002001'
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;

UNION ALL

Select 'Outlet3','0','0' from Dummy

UNION ALL

SELECT 
    T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db3.Table1 T0  
        INNER JOIN Db3.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db3.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001','105008001','105009001','105104001','105105001','105106001',
        '105107001','105108001','105109001','106001001','107009001','109018001','109022001','201001001','201002001'
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;
</code></pre>
<p>I have reframed my code now and now it looks something like this.</p>
<pre><code>SELECT 
    'Databse1' as DataSource,T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db1.Table1 T0  
        INNER JOIN Db1.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db1.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001','105008001'
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;

UNION ALL

SELECT 
    'Database2' As DataSource,T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db2.Table1 T0  
        INNER JOIN Db2.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db2.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001' ,'105008001' 
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;

UNION ALL

SELECT 
    'Database3' As DataDource,T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db3.Table1 T0  
        INNER JOIN Db3.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db3.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
    WHERE 
        T1.&quot;AcctCode&quot; in
        (
        '105004001','105005001','105006001','105007001', '105008001'
        )      
        AND '01.01.0001' &lt;= '01.07.2020'  
        AND '31.03.2021' &gt;= T0.&quot;RefDate&quot;  
    GROUP BY T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;
</code></pre>
<p>So, my question is if it's possible to mention the AcctCode globally i.e. AcctCode would be same for all and all the sub queries will be using the same AcctCode...</p>

## Answers
### Answer ID: 67818734
<p>Implementing this &quot;merge results from n different DBs&quot; is rather common.
Most of the times, this is done by means of a data warehouse.</p>
<p>HANA allows creating <em>virtual tables</em> that represent tables or views in <strong>remote systems</strong> - which is the basis for an integration scenario very popular with HANA sales folks: &quot;<em>...simply integrate all your DBs in HANA... no data warehouse and heavy data lifting required...</em>&quot;</p>
<p>I assume this is one of those scenarios.</p>
<p>So, what options are there to only have to specify the selection parameters once?</p>
<p>A simple approach would be to use <strong>query parameters</strong>.
This can be done either via <strong>user defined table functions</strong> or <strong>parameterized views</strong> (yes, also via calculation views and parameters, but I will skip this here).</p>
<p>So, with this one could write something like this:</p>
<pre><code>CREATE VIEW CombinedOutletBalances 
                (startReferencePeriod NVARCHAR(10),
                 endReferencePeriod  NVARCHAR(10))
    as
    
    WITH selAcctCodes as 
       (SELECT '105004001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL 
        SELECT '105005001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105006001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105007001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105008001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105009001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105104001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105105001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105106001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105107001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105108001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '105109001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '106001001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '107009001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '109018001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '109022001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '201001001' as &quot;AcctCode&quot; FROM DUMMY UNION ALL  
        SELECT '201002001' as &quot;AcctCode&quot; FROM DUMMY) 
       
    SELECT 
        'Outlet1' AS &quot;DataSource&quot;, T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
    FROM Db1.Table1 T0  
        INNER JOIN Db1.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
        INNER JOIN Db1.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
        INNER JOIN selAcctCodes sac ON T1.&quot;AcctCode&quot; = sac.&quot;AcctCode&quot;
    WHERE 
             '01.01.0001' &lt;= :startReferencePeriod
        AND :endReferencePeriod &gt;= T0.&quot;RefDate&quot;   
    GROUP BY 
            T1.&quot;AcctCode&quot;, T1.&quot;AcctName&quot;
 UNION ALL  
    SELECT 
         'Outlet2' AS &quot;DataSource&quot;, T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
        FROM Db2.Table1 T0  
            INNER JOIN Db2.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
            INNER JOIN Db2.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
            INNER JOIN selAcctCodes sac ON T1.&quot;AcctCode&quot; = sac.&quot;AcctCode&quot;
    WHERE 
             '01.01.0001' &lt;= :startReferencePeriod
        AND :endReferencePeriod &gt;= T0.&quot;RefDate&quot;   
    GROUP BY 
            T1.&quot;AcctCode&quot;, T1.&quot;AcctName&quot;
 UNION ALL
    SELECT 
        'Outlet3' AS &quot;DataSource&quot;, T1.&quot;AcctCode&quot;,T1.&quot;AcctName&quot;, SUM(T0.&quot;Debit&quot;) - SUM(T0.&quot;Credit&quot;) as TotalBal
        FROM Db3.Table1 T0  
            INNER JOIN Db3.Table2 T1 ON T0.&quot;Account&quot; = T1.&quot;AcctCode&quot; 
            INNER JOIN Db3.Table3 T2 ON T0.&quot;TransId&quot; = T2.&quot;TransId&quot;
            INNER JOIN selAcctCodes sac ON T1.&quot;AcctCode&quot; = sac.&quot;AcctCode&quot;
        WHERE 
                '01.01.0001' &lt;= :startReferencePeriod
            AND :endReferencePeriod &gt;= T0.&quot;RefDate&quot;  
        GROUP BY 
            T1.&quot;AcctCode&quot;, T1.&quot;AcctName&quot;;
</code></pre>
<p>This reduces the repetition to the minimum of what can be done in pure HANA SQL.</p>
<p>If the selection for the <code>AcctCode</code> should be more flexible then the next best option would be to fill a temporary table with the selected codes and join that instead of the common table expression.</p>
<p>Note that I pulled the <code>DataSource</code> into the actual data queries, that way the result set can still be handled in further queries and reporting tools without screwing up the result data (e.g. with the &quot;rows in-between&quot; approach you wouldn't be able to correctly calculate the average any more).</p>
<p>Also note, that this may not be very well-performing, if the different source table really are on remote databases. You may want to test this extensively.</p>

