# Oracle Query with Cross join - Performance problem
[Link to question](https://stackoverflow.com/questions/68179872/oracle-query-with-cross-join-performance-problem)
**Creation Date:** 1624974008
**Score:** 1
**Tags:** sql, query-optimization, oracle12c, cross-join, cbo
## Question Body
<p>I hope anyone can help me to see whether I can improve a bit more this query:</p>
<p>Environment:</p>
<ul>
<li>Oracle Database 12cR2</li>
<li>Linux Red Hat 7</li>
<li>VM with 8 CPU and 32GB RAM</li>
<li>Statistics are up to date calculated with AUTO SAMPLE and method FOR ALL COLUMNS SIZE AUTO</li>
<li>Optimizer parameters are the default ones for 12.2</li>
</ul>
<p>The original query belongs to a third party software. It is using <code>cross join</code> which is creating HASH JOINS, as expected. The original query and plan statistics are:</p>
<pre><code>$ sqlplus /@USERWALLET @original.sql

SQL*Plus: Release 12.2.0.1.0 Production on Tue Jun 29 13:19:47 2021

Copyright (c) 1982, 2016, Oracle.  All rights reserved.


Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL&gt; var processingDate number;
SQL&gt; exec :processingDate := 20210621;

PL/SQL procedure successfully completed.

Elapsed: 00:00:00.00
SQL&gt; -- without index
SQL&gt; select distinct 1 as col_0_0_ from ALFATS.FloatingRateRollover floatingra0_
  2  cross join ALFATS.FloatingRateDetail floatingra1_
  3  cross join ALFATS.FloatingRateInterestCalendar floatingra2_
  4  cross join ALFATS.Schedule schedule3_
  5  where floatingra0_.agreementNumber=floatingra1_.agreementNumber and
  6  floatingra0_.scheduleNumber=floatingra1_.scheduleNumber and
  7  floatingra0_.id=floatingra2_.floatingRateRolloverId and
  8  floatingra0_.agreementNumber=schedule3_.agreementNumber and
  9  floatingra0_.scheduleNumber=schedule3_.scheduleNumber and
 10  floatingra0_.terminationNumber=schedule3_.terminationNumber and
 11  floatingra0_.adjustmentProcessedIndicator='N' and
 12  floatingra2_.processingDate&lt;=:processingDate  and
 13  floatingra1_.variableRateType='U' and
 14  floatingra0_.terminationNumber=0 and
 15  schedule3_.scheduleStatus&lt;&gt;'PRE' and
 16  not (exists (select 1 from ALFATS.TransactionFailure transactio4_
 17  where floatingra0_.agreementNumber=transactio4_.agreementNumber and
 18  floatingra0_.scheduleNumber=transactio4_.scheduleNumber and
 19  floatingra0_.terminationNumber=transactio4_.terminationNumber))
 20  ;

  COL_0_0_
----------
         1

1 row selected.

Elapsed: 00:00:23.70

Execution Plan
----------------------------------------------------------
Plan hash value: 3077170061

-----------------------------------------------------------------------------------------------------------------
| Id  | Operation                | Name                         | Rows  | Bytes |TempSpc| Cost (%CPU)| Time     |
-----------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT         |                              |   106K|    15M|       |   236K  (1)| 00:00:10 |
|   1 |  SORT UNIQUE NOSORT      |                              |   106K|    15M|       |   236K  (1)| 00:00:10 |
|*  2 |   HASH JOIN RIGHT ANTI   |                              |   106K|    15M|       |   232K  (1)| 00:00:10 |
|*  3 |    INDEX FAST FULL SCAN  | TRANSACTIONFAILURE_NK        |    39 |  1170 |       |     3   (0)| 00:00:01 |
|*  4 |    HASH JOIN SEMI        |                              |   106K|    12M|    10M|   232K  (1)| 00:00:10 |
|*  5 |     HASH JOIN RIGHT SEMI |                              |   110K|  9207K|  4608K|   230K  (1)| 00:00:10 |
|*  6 |      INDEX FAST FULL SCAN| FLOATINGRATEDETAIL_1         |   109K|  3319K|       |   724   (1)| 00:00:01 |
|*  7 |      HASH JOIN           |                              |   284K|    14M|  6944K|   228K  (1)| 00:00:09 |
|*  8 |       TABLE ACCESS FULL  | FLOATINGRATEINTERESTCALENDAR |   284K|  3608K|       | 20338   (1)| 00:00:01 |
|*  9 |       TABLE ACCESS FULL  | FLOATINGRATEROLLOVER         |    29M|  1153M|       |   133K  (1)| 00:00:06 |
|* 10 |     INDEX FAST FULL SCAN | SCHEDULE_L1                  |   274K|     9M|       |   852   (1)| 00:00:01 |
-----------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;SCHEDULENUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;TERMINATIONNUMBER&quot;)
   3 - filter(&quot;TRANSACTIO4_&quot;.&quot;TERMINATIONNUMBER&quot;=0)
   4 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;SCHEDULENUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;TERMINATIONNUMBER&quot;)
   5 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;FLOATINGRA1_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;FLOATINGRA1_&quot;.&quot;SCHEDULENUMBER&quot;)
   6 - filter(&quot;FLOATINGRA1_&quot;.&quot;VARIABLERATETYPE&quot;=U'U')
   7 - access(&quot;FLOATINGRA0_&quot;.&quot;ID&quot;=&quot;FLOATINGRA2_&quot;.&quot;FLOATINGRATEROLLOVERID&quot;)
   8 - filter(&quot;FLOATINGRA2_&quot;.&quot;PROCESSINGDATE&quot;&lt;=TO_NUMBER(:PROCESSINGDATE))
   9 - filter(&quot;FLOATINGRA0_&quot;.&quot;ADJUSTMENTPROCESSEDINDICATOR&quot;=U'N' AND
              &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=0)
  10 - filter(&quot;SCHEDULE3_&quot;.&quot;TERMINATIONNUMBER&quot;=0 AND &quot;SCHEDULE3_&quot;.&quot;SCHEDULESTATUS&quot;&lt;&gt;U'PRE')


Statistics
----------------------------------------------------------
          4  recursive calls
          0  db block gets
     569374  consistent gets
     488274  physical reads
        484  redo size
        542  bytes sent via SQL*Net to client
        607  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed
</code></pre>
<p>After reviewing the plan, I tried to avoid those TABLE FULL SCAN by creating the following two indexes:</p>
<pre><code>SQL&gt; CREATE INDEX alfats.FloatingRateRollover_PRF1 
     ON alfats.FloatingRateRollover (adjustmentProcessedIndicator, agreementNumber, scheduleNumber, terminationNumber, id) 
     INVISIBLE 
     COMPUTE STATISTICS;

Index created.

Elapsed: 00:01:58.14

SQL&gt; CREATE INDEX alfats.FloatingRateInterestCalendar_PRF2 
     ON alfats.FloatingRateInterestCalendar (floatingRateRolloverId, processingDate) 
     INVISIBLE 
     COMPUTE STATISTICS;

Index created.

Elapsed: 00:00:06.60
</code></pre>
<p>After this, the query improves, it is accessing by <code>INDEX FAST FULL SCAN</code> in all the tables involved but still is taking time</p>
<pre><code>$ sqlplus /@USERWALLET @original_with_indexes.sql

SQL*Plus: Release 12.2.0.1.0 Production on Tue Jun 29 13:24:27 2021

Copyright (c) 1982, 2016, Oracle.  All rights reserved.
    
Connected to:
Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production

SQL&gt; var processingDate number;
SQL&gt; exec :processingDate := 20210621;

PL/SQL procedure successfully completed.

Elapsed: 00:00:00.00
SQL&gt; alter session set optimizer_use_invisible_indexes=true;

Session altered.

Elapsed: 00:00:00.00
SQL&gt; select distinct 1 as col_0_0_ from ALFATS.FloatingRateRollover floatingra0_
  2  cross join ALFATS.FloatingRateDetail floatingra1_
  3  cross join ALFATS.FloatingRateInterestCalendar floatingra2_
  4  cross join ALFATS.Schedule schedule3_
  5  where floatingra0_.agreementNumber=floatingra1_.agreementNumber and
  6  floatingra0_.scheduleNumber=floatingra1_.scheduleNumber and
  7  floatingra0_.id=floatingra2_.floatingRateRolloverId and
  8  floatingra0_.agreementNumber=schedule3_.agreementNumber and
  9  floatingra0_.scheduleNumber=schedule3_.scheduleNumber and
 10  floatingra0_.terminationNumber=schedule3_.terminationNumber and
 11  floatingra0_.adjustmentProcessedIndicator='N' and
 12  floatingra2_.processingDate&lt;=:processingDate  and
 13  floatingra1_.variableRateType='U' and
 14  floatingra0_.terminationNumber=0 and
 15  schedule3_.scheduleStatus&lt;&gt;'PRE' and
 16  not (exists (select 1 from ALFATS.TransactionFailure transactio4_
 17  where floatingra0_.agreementNumber=transactio4_.agreementNumber and
 18  floatingra0_.scheduleNumber=transactio4_.scheduleNumber and
 19  floatingra0_.terminationNumber=transactio4_.terminationNumber))
 20  ;

  COL_0_0_
----------
         1

1 row selected.

Elapsed: 00:00:10.95

Execution Plan
----------------------------------------------------------
Plan hash value: 1805021994

-----------------------------------------------------------------------------------------------------------------------
| Id  | Operation                 | Name                              | Rows  | Bytes |TempSpc| Cost (%CPU)| Time     |
-----------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT          |                                   |   106K|    15M|       |   149K  (1)| 00:00:06 |
|   1 |  SORT UNIQUE NOSORT       |                                   |   106K|    15M|       |   149K  (1)| 00:00:06 |
|*  2 |   HASH JOIN RIGHT ANTI    |                                   |   106K|    15M|       |   145K  (1)| 00:00:06 |
|*  3 |    INDEX FAST FULL SCAN   | TRANSACTIONFAILURE_NK             |    39 |  1170 |       |     3   (0)| 00:00:01 |
|*  4 |    HASH JOIN SEMI         |                                   |   106K|    12M|    10M|   145K  (1)| 00:00:06 |
|*  5 |     HASH JOIN RIGHT SEMI  |                                   |   110K|  9207K|  4608K|   143K  (1)| 00:00:06 |
|*  6 |      INDEX FAST FULL SCAN | FLOATINGRATEDETAIL_1              |   109K|  3319K|       |   724   (1)| 00:00:01 |
|*  7 |      HASH JOIN            |                                   |   284K|    14M|  6944K|   141K  (1)| 00:00:06 |
|*  8 |       INDEX FAST FULL SCAN| FLOATINGRATEINTERESTCALENDAR_PRF2 |   284K|  3608K|       |  5050   (2)| 00:00:01 |
|*  9 |       INDEX FAST FULL SCAN| FLOATINGRATEROLLOVER_PRF1         |    29M|  1153M|       | 62326   (1)| 00:00:03 |
|* 10 |     INDEX FAST FULL SCAN  | SCHEDULE_L1                       |   274K|     9M|       |   852   (1)| 00:00:01 |
-----------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;SCHEDULENUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;TRANSACTIO4_&quot;.&quot;TERMINATIONNUMBER&quot;)
   3 - filter(&quot;TRANSACTIO4_&quot;.&quot;TERMINATIONNUMBER&quot;=0)
   4 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;SCHEDULENUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;SCHEDULE3_&quot;.&quot;TERMINATIONNUMBER&quot;)
   5 - access(&quot;FLOATINGRA0_&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;FLOATINGRA1_&quot;.&quot;AGREEMENTNUMBER&quot; AND
              &quot;FLOATINGRA0_&quot;.&quot;SCHEDULENUMBER&quot;=&quot;FLOATINGRA1_&quot;.&quot;SCHEDULENUMBER&quot;)
   6 - filter(&quot;FLOATINGRA1_&quot;.&quot;VARIABLERATETYPE&quot;=U'U')
   7 - access(&quot;FLOATINGRA0_&quot;.&quot;ID&quot;=&quot;FLOATINGRA2_&quot;.&quot;FLOATINGRATEROLLOVERID&quot;)
   8 - filter(&quot;FLOATINGRA2_&quot;.&quot;PROCESSINGDATE&quot;&lt;=TO_NUMBER(:PROCESSINGDATE))
   9 - filter(&quot;FLOATINGRA0_&quot;.&quot;ADJUSTMENTPROCESSEDINDICATOR&quot;=U'N' AND &quot;FLOATINGRA0_&quot;.&quot;TERMINATIONNUMBER&quot;=0)
  10 - filter(&quot;SCHEDULE3_&quot;.&quot;TERMINATIONNUMBER&quot;=0 AND &quot;SCHEDULE3_&quot;.&quot;SCHEDULESTATUS&quot;&lt;&gt;U'PRE')


Statistics
----------------------------------------------------------
          0  recursive calls
          0  db block gets
     257732  consistent gets
          0  physical reads
       6224  redo size
        542  bytes sent via SQL*Net to client
        607  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed
</code></pre>
<p>My last attempt has been trying to rewrite the query by converting some of those <code>cross joins</code> into <code>inner joins</code> ( where I could ). I get a better time but the plan looks the same. I ran several times the test with different levels of loading in the server, still I got better time in the query below, even though the plan looks identical.</p>
<pre><code>SQL&gt; select distinct 1 as col_0_0_ from
  2  ALFATS.FloatingRateRollover t0
  3  inner join ALFATS.FloatingRateDetail t1
  4  on ( t0.agreementNumber=t1.agreementNumber
  5       and
  6       t0.scheduleNumber=t1.scheduleNumber
  7       and
  8       t0.adjustmentProcessedIndicator='N'
  9       and
 10       t0.terminationNumber=0
 11       and
 12       t1.variableRateType='U'
 13   )
 14  inner join ALFATS.Schedule t3
 15  on (
 16  t0.agreementNumber=t3.agreementNumber
 17  and
 18  t0.scheduleNumber=t3.scheduleNumber
 19  and
 20  t0.terminationNumber=t3.terminationNumber
 21  and
 22  t3.scheduleStatus&lt;&gt;'PRE'
 23  )
 24  inner join ALFATS.FloatingRateInterestCalendar t2
 25  on (
 26  t0.id = t2.floatingRateRolloverId
 27  and
 28  t2.processingDate&lt;=:processingDate
 29  ) where
 30  not (exists (select 1 from ALFATS.TransactionFailure t4
 31               where t0.agreementNumber=t4.agreementNumber and
 32               t0.scheduleNumber=t4.scheduleNumber and
 33               t0.terminationNumber=t4.terminationNumber)
 34  )
 35  ;

1 row selected.

Elapsed: 00:00:07.93

Execution Plan
----------------------------------------------------------
Plan hash value: 1805021994

-----------------------------------------------------------------------------------------------------------------------
| Id  | Operation                 | Name                              | Rows  | Bytes |TempSpc| Cost (%CPU)| Time     |
-----------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT          |                                   |   106K|    15M|       |   149K  (1)| 00:00:06 |
|   1 |  SORT UNIQUE NOSORT       |                                   |   106K|    15M|       |   149K  (1)| 00:00:06 |
|*  2 |   HASH JOIN RIGHT ANTI    |                                   |   106K|    15M|       |   145K  (1)| 00:00:06 |
|*  3 |    INDEX FAST FULL SCAN   | TRANSACTIONFAILURE_NK             |    39 |  1170 |       |     3   (0)| 00:00:01 |
|*  4 |    HASH JOIN SEMI         |                                   |   106K|    12M|    10M|   145K  (1)| 00:00:06 |
|*  5 |     HASH JOIN RIGHT SEMI  |                                   |   110K|  9207K|  4608K|   143K  (1)| 00:00:06 |
|*  6 |      INDEX FAST FULL SCAN | FLOATINGRATEDETAIL_1              |   109K|  3319K|       |   724   (1)| 00:00:01 |
|*  7 |      HASH JOIN            |                                   |   284K|    14M|  6944K|   141K  (1)| 00:00:06 |
|*  8 |       INDEX FAST FULL SCAN| FLOATINGRATEINTERESTCALENDAR_PRF2 |   284K|  3608K|       |  5050   (2)| 00:00:01 |
|*  9 |       INDEX FAST FULL SCAN| FLOATINGRATEROLLOVER_PRF1         |    29M|  1153M|       | 62326   (1)| 00:00:03 |
|* 10 |     INDEX FAST FULL SCAN  | SCHEDULE_L1                       |   274K|     9M|       |   852   (1)| 00:00:01 |
-----------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - access(&quot;T0&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;T4&quot;.&quot;AGREEMENTNUMBER&quot; AND &quot;T0&quot;.&quot;SCHEDULENUMBER&quot;=&quot;T4&quot;.&quot;SCHEDULENUMBER&quot;
              AND &quot;T0&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;T4&quot;.&quot;TERMINATIONNUMBER&quot;)
   3 - filter(&quot;T4&quot;.&quot;TERMINATIONNUMBER&quot;=0)
   4 - access(&quot;T0&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;T3&quot;.&quot;AGREEMENTNUMBER&quot; AND &quot;T0&quot;.&quot;SCHEDULENUMBER&quot;=&quot;T3&quot;.&quot;SCHEDULENUMBER&quot;
              AND &quot;T0&quot;.&quot;TERMINATIONNUMBER&quot;=&quot;T3&quot;.&quot;TERMINATIONNUMBER&quot;)
   5 - access(&quot;T0&quot;.&quot;AGREEMENTNUMBER&quot;=&quot;T1&quot;.&quot;AGREEMENTNUMBER&quot; AND &quot;T0&quot;.&quot;SCHEDULENUMBER&quot;=&quot;T1&quot;.&quot;SCHEDULENUMBER&quot;)
   6 - filter(&quot;T1&quot;.&quot;VARIABLERATETYPE&quot;=U'U')
   7 - access(&quot;T0&quot;.&quot;ID&quot;=&quot;T2&quot;.&quot;FLOATINGRATEROLLOVERID&quot;)
   8 - filter(&quot;T2&quot;.&quot;PROCESSINGDATE&quot;&lt;=TO_NUMBER(:PROCESSINGDATE))
   9 - filter(&quot;T0&quot;.&quot;ADJUSTMENTPROCESSEDINDICATOR&quot;=U'N' AND &quot;T0&quot;.&quot;TERMINATIONNUMBER&quot;=0)
  10 - filter(&quot;T3&quot;.&quot;TERMINATIONNUMBER&quot;=0 AND &quot;T3&quot;.&quot;SCHEDULESTATUS&quot;&lt;&gt;U'PRE')


Statistics
----------------------------------------------------------
          0  recursive calls
          0  db block gets
     257573  consistent gets
          0  physical reads
       1288  redo size
        542  bytes sent via SQL*Net to client
        608  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed
</code></pre>
<p><strong>UPDATE</strong></p>
<p>As requested, here the details for SQL MONITOR for the original query</p>
<pre><code>Global Stats
=================================================
| Elapsed |   Cpu   |  Other   | Fetch | Buffer |
| Time(s) | Time(s) | Waits(s) | Calls |  Gets  |
=================================================
|      11 |      11 |     0.05 |     2 |   266K |
=================================================

SQL Plan Monitoring Details (Plan Hash Value=768763834)
=======================================================================================================================================================================
| Id |          Operation          |               Name                |  Rows   | Cost  |   Time    | Start  | Execs |   Rows   |  Mem  | Activity | Activity Detail |
|    |                             |                                   | (Estim) |       | Active(s) | Active |       | (Actual) | (Max) |   (%)    |   (# samples)   |
=======================================================================================================================================================================
|  0 | SELECT STATEMENT            |                                   |         |       |         6 |     +6 |     1 |        1 |     . |          |                 |
|  1 |   SORT UNIQUE NOSORT        |                                   |    869K |  192K |         6 |     +6 |     1 |        1 |     . |          |                 |
|  2 |    HASH JOIN RIGHT ANTI     |                                   |    869K |  163K |         6 |     +6 |     1 |       61 |   1MB |          |                 |
|  3 |     INDEX FAST FULL SCAN    | TRANSACTIONFAILURE_NK             |      42 |     4 |         1 |     +6 |     1 |       42 |     . |          |                 |
|  4 |     HASH JOIN RIGHT SEMI    |                                   |    869K |  163K |         6 |     +6 |     1 |       70 |  22MB |          |                 |
|  5 |      INDEX FAST FULL SCAN   | SCHEDULE_L1                       |    276K |   856 |         1 |     +6 |     1 |     279K |     . |          |                 |
|  6 |      HASH JOIN RIGHT SEMI   |                                   |    901K |  157K |         6 |     +6 |     1 |       70 |  10MB |          |                 |
|  7 |       INDEX FAST FULL SCAN  | FLOATINGRATEDETAIL_1              |    110K |   728 |         1 |     +6 |     1 |     110K |     . |          |                 |
|  8 |       HASH JOIN             |                                   |      2M |  149K |        11 |     +1 |     1 |       70 | 108MB |          |                 |
|  9 |        INDEX FAST FULL SCAN | FLOATINGRATEINTERESTCALENDAR_PRF2 |      2M |  5039 |         1 |     +6 |     1 |       2M |     . |          |                 |
| 10 |        INDEX FAST FULL SCAN | FLOATINGRATEROLLOVER_PRF1         |     30M | 66438 |         9 |     +3 |     1 |      30M |     . |          |                 |
=======================================================================================================================================================================
</code></pre>
<p>And monitor report of the query changed by me with JOIN / ON syntax</p>
<pre><code>Global Stats
=================================================
| Elapsed |   Cpu   |  Other   | Fetch | Buffer |
| Time(s) | Time(s) | Waits(s) | Calls |  Gets  |
=================================================
|      9  |      9  |     0.01 |     2 |   266K |
=================================================

SQL Plan Monitoring Details (Plan Hash Value=768763834)
=======================================================================================================================================================================
| Id |          Operation          |               Name                |  Rows   | Cost  |   Time    | Start  | Execs |   Rows   |  Mem  | Activity | Activity Detail |
|    |                             |                                   | (Estim) |       | Active(s) | Active |       | (Actual) | (Max) |   (%)    |   (# samples)   |
=======================================================================================================================================================================
|  0 | SELECT STATEMENT            |                                   |         |       |         5 |     +6 |     1 |        1 |     . |          |                 |
|  1 |   SORT UNIQUE NOSORT        |                                   |    869K |  192K |         5 |     +6 |     1 |        1 |     . |          |                 |
|  2 |    HASH JOIN RIGHT ANTI     |                                   |    869K |  163K |         5 |     +6 |     1 |       61 |   1MB |          |                 |
|  3 |     INDEX FAST FULL SCAN    | TRANSACTIONFAILURE_NK             |      42 |     4 |         7 |     +0 |     1 |       42 |     . |          |                 |
|  4 |     HASH JOIN RIGHT SEMI    |                                   |    869K |  163K |         5 |     +6 |     1 |       70 |  22MB |          |                 |
|  5 |      INDEX FAST FULL SCAN   | SCHEDULE_L1                       |    276K |   856 |         1 |     +6 |     1 |     279K |     . |          |                 |
|  6 |      HASH JOIN RIGHT SEMI   |                                   |    901K |  157K |         5 |     +6 |     1 |       70 |  10MB |          |                 |
|  7 |       INDEX FAST FULL SCAN  | FLOATINGRATEDETAIL_1              |    110K |   728 |         1 |     +6 |     1 |     110K |     . |          |                 |
|  8 |       HASH JOIN             |                                   |      2M |  149K |         9 |     +2 |     1 |       70 | 108MB |          |                 |
|  9 |        INDEX FAST FULL SCAN | FLOATINGRATEINTERESTCALENDAR_PRF2 |      2M |  5039 |         6 |     +1 |     1 |       2M |     . |          |                 |
| 10 |        INDEX FAST FULL SCAN | FLOATINGRATEROLLOVER_PRF1         |     30M | 66438 |         8 |     +3 |     1 |      30M |     . |          |                 |
=======================================================================================================================================================================
</code></pre>
<p>As you can see by the monitor, both queries are using the same PLAN HASH VALUE, so the CBO is using the same plan for both of them as interpreting they are indeed the same query. Still, I got better times always with the query with JOIN / ON syntax, which honestly I don't understand why.</p>
<p>My question is whether there is a simpler way to improve this query keeping in consideration the volumes. It would be great to understand why the query with JOIN / ON syntax behaves better in performance when the plan and cost ( including access path and predicate information ) are identical.</p>
<p>Thanks in advance.</p>

