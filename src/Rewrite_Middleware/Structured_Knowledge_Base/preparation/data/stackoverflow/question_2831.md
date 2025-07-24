# ORA-01652: Unable to extend temp space
[Link to question](https://stackoverflow.com/questions/54501733/ora-01652-unable-to-extend-temp-space)
**Creation Date:** 1549187760
**Score:** 0
**Tags:** oracle-database, ora-01652
## Question Body
<p>I have a procedure and a particular query in the procedure is generating about 50GB of temp space causing below exception after few executions.:  </p>

<p>SQL state [72000]; error code [1652]; ORA-01652: unable to extend temp segment by 128 in tablespace TEMP</p>

<p>DBAs are pointing to the below query in the stored procedure that needs to be rewritten. The tables used in the query below are smaller than 0.1 GB but the query generates 50GB of temp space!</p>

<pre><code>SELECT tab1.ORDID ID1, tab2.ORDID ID2
FROM (
    SELECT 
    OT.ORDID,
    CONNECT_BY_ROOT OT.UNIQ_ORIG_KEY ORIG_UID
    FROM order_tab OT, status_tab ST
    WHERE OT.otype IN ('A','B') 
    AND OT.order_uid IS NULL 
    AND OT.BATCH_ID = ST.BATCH_ID 
    AND ST.CT_DATE = :A1 
    AND ST.BSTATUS = 1 
    CONNECT BY PRIOR OT.UNIQ_KEY = OT.UNIQ_ORIG_KEY 
      ) tab1 , order_tab tab2
WHERE tab2.ORD_VERID = 1 
AND tab1.ORIG_UID = tab2.UNIQ_KEY 
ORDER BY ID1;
</code></pre>

<p>Could someone please help in rewriting the query efficiently so that temp space utilization is reduced. Database used Oracle 12c.</p>

