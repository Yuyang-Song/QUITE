# Oracle Sql Query taking a day long to return results using dblink
[Link to question](https://stackoverflow.com/questions/4614107/oracle-sql-query-taking-a-day-long-to-return-results-using-dblink)
**Creation Date:** 1294311037
**Score:** 0
**Tags:** sql, oracle-database, query-optimization
## Question Body
<p>Guys i have the following oracle sql query that gives me the monthwise report between the dates.Basically for nov month i want sum of values between the dates 01nov to 30 nov.
The table that is being queried is residing in another database and accesssed using dblink. The DT columns is of NUMBER type (for ex 20101201).</p>

<pre><code>SELECT /*+ PARALLEL (A 8) */ /*+ DRIVING_STATE(A) */
 TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM')- 1,'MM'),'MONYYYY') "MONTH", 
   TYPE AS "TYPE", COLUMN, COUNT (DISTINCT A) AS "A_COUNT",
    COUNT (COLUMN) AS NO_OF_COLS, SUM (DURATION) AS "SUM_DURATION",
     SUM (COST) AS "COST"  FROM **A@LN_PROD A**  
      WHERE DT &gt;=  TO_NUMBER(TO_CHAR(add_months(SYSDATE,-1),'YYYYMM"01"'))
      AND  DT &lt; TO_NUMBER(TO_CHAR(SYSDATE,'YYYYMM"01"'))
       GROUP BY TYPE, COLUMN
</code></pre>

<p>The execution of the query is taking a day long and not completed. kindly suggest me , if their is any optimisation that can be suggested to my DBA on  the dblink, or any tuning that can be done on the query , or rewriting the same.</p>

<p><strong>UPDATES ON THE TABLE</strong></p>

<p>The table is partiontioned on the date column  and almost 1 billion records.</p>

<p>Below i have given the <strong>EXPLAIN PLAN</strong> from <strong>TOAD</strong></p>

<pre><code>**Plan**
SELECT STATEMENT REMOTE  ALL_ROWSCost: 1,208,299  Bytes: 34,760  Cardinality: 790                                               
    12 PX COORDINATOR                                           
        11 PX SEND QC (RANDOM) SYS.:TQ10002 Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                                        
            10 SORT GROUP BY  Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                                      
                9 PX RECEIVE  Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                                  
                    8 PX SEND HASH SYS.:TQ10001 Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                            
                        7 SORT GROUP BY  Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                       
                            6 PX RECEIVE  Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                      
                                5 PX SEND HASH SYS.:TQ10000 Cost: 1,208,299  Bytes: 34,760  Cardinality: 790                
                                    4 SORT GROUP BY  Cost: 1,208,299  Bytes: 34,760  Cardinality: 790           
                                        3 FILTER        
                                            2 PX BLOCK ITERATOR  Cost: 1,203,067  Bytes: 15,066,833,144  Cardinality: 342,428,026  Partition #: 11  Partitions accessed #1 - #5 
                                                1 TABLE ACCESS FULL TABLE CDRR.FRD_CDF_DATA_INTL_IN_P Cost: 1,203,067  Bytes: 15,066,833,144  Cardinality: 342,428,026  Partition #: 11  
</code></pre>

<p><strong>The following things i am going to do today ,any additional tips would be helpful.</strong></p>

<ol>
<li>I am going to gather the tablewise statistics for this table, which may give optimal 
execution plan.</li>
<li>Check whether an local index is created for the partition .</li>
<li>using BETWEEN instead of >= and &lt;.</li>
</ol>

## Answers
### Answer ID: 4614643
<p>Impossible to answer without knowing the table structure, constraints, indexes, data volume, resultset size, network speed, level of concurrency, execution plans etcetera.</p>

<p>Some things I would investigate:</p>

<p>If the table is partitioned, does statistics exist for the partition the query is hitting? A common problem is that statistics are gathered on an empty partition before data has been inserted. Then when you query it (before the statistics are refreshed) Oracle chooses an index scan, when in fact it should use an FTS on that partition.</p>

<p>Also related to statistics: Make sure that </p>

<pre><code>WHERE DT &gt;=TO_NUMBER(TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM')-1,'MM'),'YYYYMMDD')) 
  AND DT &lt; TO_NUMBER(TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM'),'MM'),'YYYYMMDD')) 
</code></pre>

<p>generates the same execution plan as:</p>

<pre><code>WHERE DT &gt;= 20101201
  AND DT &lt;  20110101
</code></pre>

<p><strong>Updated</strong>
What version of Oracle are you on? The reason I'm asking is that on Oracle 10g and later, there is another implementation of group by that should have been selected in this case (hashing rather than sorting). It looks like you are basically sorting the 342 million rows returned from the date filter (14 gigabytes). Do you have the RAM to back that up? Otherwise you will be doing a multipass sort, spilling to disk. This is likely what is happening. </p>

<p>According to the plan, about 790 rows will be returned. Is that in the right ballpark?
If so, you can rule out network issues :)</p>

<p>Also, I'm not entirely familiar with the format on that plan. Is the table sub partitioned? Otherwise I don't get the partition #11 reference.</p>

### Answer ID: 4614718
<p>As usual for this type of question, an explain plan would be useful. It would help us work out what is actually going on in the database. </p>

<p>Ideally you want to make sure the query is running on the remote database the sending the result set back, rather than sending the data across the link and running the query locally. This ensures that less data is sent across the link. The <code>DRIVING_SITE</code> hint can help with this, although Oracle is usually fairly smart about it so it might not help at all. </p>

<p>Oracle seems to have got better at running remote queries but there still can be problems. </p>

<p>Also, it might pay to simplify some of your date conversions. </p>

<p>For example, replace this:</p>

<pre><code>TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM')- 1,'MM'),'MONYYYY')
</code></pre>

<p>with this:</p>

<pre><code>TO_CHAR(add_months(TRUNC(SYSDATE,'MM'), -1),'MONYYYY')
</code></pre>

<p>It is probably slightly more efficient but also is easier to read.</p>

<p>Likewise replace this:</p>

<pre><code>WHERE DT &gt;=TO_NUMBER(TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM')-1,'MM'),'YYYYMMDD')) 
  AND  DT &lt; TO_NUMBER(TO_CHAR(TRUNC(TRUNC(SYSDATE,'MM'),'MM'),'YYYYMMDD')) 
</code></pre>

<p>with </p>

<pre><code>WHERE DT &gt;=TO_NUMBER(TO_CHAR(add_months(TRUNC(SYSDATE,'MM'), -1),'YYYYMMDD')) 
  AND  DT &lt; TO_NUMBER(TO_CHAR(TRUNC(SYSDATE,'MM'),'YYYYMMDD')) 
</code></pre>

<p>or even</p>

<pre><code>WHERE DT &gt;=TO_NUMBER(TO_CHAR(add_months(SYSDATE,-1),'YYYYMM"01"')) 
  AND  DT &lt; TO_NUMBER(TO_CHAR(SYSDATE,'YYYYMM"01"')) 
</code></pre>

### Answer ID: 4614288
<p>It may be because several issues:
1.Network speed because the database may be residing on different hardware.
However you can refer this link 
<a href="http://www.experts-exchange.com/Database/Oracle/Q_21799513.html" rel="nofollow">http://www.experts-exchange.com/Database/Oracle/Q_21799513.html</a>.
There is a similar issue.</p>

