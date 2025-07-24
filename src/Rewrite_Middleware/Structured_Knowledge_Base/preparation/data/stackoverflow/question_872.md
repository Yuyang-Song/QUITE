# Oracle 11 query runs fast on first 2 executions, slower on subsequent, no plan change
[Link to question](https://stackoverflow.com/questions/47780877/oracle-11-query-runs-fast-on-first-2-executions-slower-on-subsequent-no-plan-c)
**Creation Date:** 1513109897
**Score:** 7
**Tags:** oracle-database, oracle11g, recursive-query
## Question Body
<p>Oracle Database 11g Release 11.2.0.4.0 - 64bit Production</p>

<p>Solved: was caused by cardinality feedback. I thought I had tested this earlier and eliminated it, but clearly got it wrong.</p>

<p>Added this to query:</p>

<pre><code>select --+ opt_param('_optimizer_use_feedback' 'false')
</code></pre>

<p>Now consistently fast.</p>

<hr>

<p>I have this odd case where a query seems to run reasonably quickly on the first 2 executions, and then much slower on subsequent executions. I am using sqlplus with "set autotrace on" to get query plans, and for each run the plans are identical (same row estimates etc). The autotrace stats at the end show that more data is read in the subsequent executions.</p>

<p>If I change the query syntactically (just adding or removing comments will do), so that it is presumably new to the SQL cache, then it runs quickly twice, and then slowly again. If I change it back to a version of the query I have used before (thus in the cache) then it is always slow.</p>

<p>I don't think it is related to <a href="http://orcasoracle.squarespace.com/oracle-rdbms/2012/12/18/when-a-query-runs-slower-on-second-execution-a-possible-side.html" rel="nofollow noreferrer">cardinality feedback</a> because:</p>

<ul>
<li>I have tried disabling this feature with no effect</li>
<li>the plans for all executions are identical</li>
</ul>

<p>So where do I look next? What tools can I used to narrow down why this is happening?</p>

<p>This is the query I am testing with:</p>

<pre class="lang-sql prettyprint-override"><code>set timing on
set autotrace on

select distinct
      cc2.circuit_id as circuit_id
    , cc2.circuit_component_id as component_circuit_id
from bsdb.bs_instance si
join bsdb.bs_location_schedule ls
    on ls.bs_instance_id = si.id
    and coalesce(ls.terminated_date, sysdate) &gt;= sysdate
join npc.npc_customer_service cs
    on cs.bs_location_schedule_id = ls.id
    and cs.circuit_status_id in (1, 2, 6)
join tdb.loc_site_code lsc
    on lsc.id = ls.site_code_id
left outer join scdb.brand br
    on br.id = si.brand_id
join tdb.organisation o
    on o.org_code = coalesce(br.brand_org_code, si.client_org_code)
    and o.org_code = 2421
join npc.npc_customer_service_circuit csc
    on csc.customer_service_id = cs.customer_service_id
    and coalesce(csc.end_date, sysdate) &gt;= sysdate
join npc.npc_circuit_component cc
    on cc.circuit_id = csc.circuit_id
    and coalesce(cc.end_date, sysdate) &gt;= sysdate
join npc.npc_circuit_hierarchy ch
    on ch.sub_circuit_id = cc.circuit_component_id
join npc.npc_circuit_component cc2
    on cc2.circuit_id = ch.master_circuit_id
    and coalesce(cc2.end_date, sysdate) &gt;= sysdate
;
</code></pre>

<p>If I remove the outer join to scdb.brand (not required in this specific case but is in general for this query) then the performance is fast and consistent across multiple runs.</p>

<p>autotrace output including plan, fast run:</p>

<pre><code>109 rows selected.

Elapsed: 00:00:00.51

Execution Plan

Plan hash value: 2956052167

--------------------------------------------------------------------------------------------------------------------
| Id  | Operation                           | Name                         | Rows  | Bytes | Cost (%CPU)| Time     |
--------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT                    |                              |   173 | 18857 |  2069   (6)| 00:00:07 |
|   1 |  HASH UNIQUE                        |                              |   173 | 18857 |  2069   (6)| 00:00:07 |
|*  2 |   FILTER                            |                              |       |       |            |          |
|*  3 |    HASH JOIN OUTER                  |                              |   173 | 18857 |  2068   (6)| 00:00:07 |
|*  4 |     HASH JOIN                       |                              |   173 | 17473 |  2063   (6)| 00:00:07 |
|*  5 |      HASH JOIN                      |                              |   173 | 15397 |  2000   (6)| 00:00:07 |
|   6 |       NESTED LOOPS                  |                              |   244 | 18056 |  1297   (2)| 00:00:05 |
|   7 |        NESTED LOOPS                 |                              |   249 | 18056 |  1297   (2)| 00:00:05 |
|   8 |         NESTED LOOPS                |                              |   249 | 15438 |   799   (3)| 00:00:03 |
|*  9 |          HASH JOIN                  |                              |   205 |  9635 |   183   (9)| 00:00:01 |
|* 10 |           HASH JOIN                 |                              |   280 |  8960 |   110   (5)| 00:00:01 |
|* 11 |            TABLE ACCESS FULL        | BS_LOCATION_SCHEDULE         |   695 | 12510 |    44   (7)| 00:00:01 |
|  12 |            NESTED LOOPS             |                              |  3452 | 48328 |    66   (4)| 00:00:01 |
|* 13 |             INDEX UNIQUE SCAN       | ORGANISATION__PK             |     1 |     4 |     1   (0)| 00:00:01 |
|* 14 |             TABLE ACCESS FULL       | NPC_CUSTOMER_SERVICE         |  3452 | 34520 |    65   (4)| 00:00:01 |
|* 15 |           TABLE ACCESS FULL         | NPC_CUSTOMER_SERVICE_CIRCUIT |  2531 | 37965 |    72  (13)| 00:00:01 |
|* 16 |          TABLE ACCESS BY INDEX ROWID| NPC_CIRCUIT_COMPONENT        |     1 |    15 |     3   (0)| 00:00:01 |
|* 17 |           INDEX RANGE SCAN          | NPC_CIRCUIT_COMPONENT_I01    |     9 |       |     2   (0)| 00:00:01 |
|* 18 |         INDEX UNIQUE SCAN           | NPC_CIRCUIT_HIERARCHY_I02    |     1 |       |     1   (0)| 00:00:01 |
|  19 |        TABLE ACCESS BY INDEX ROWID  | NPC_CIRCUIT_HIERARCHY        |     1 |    12 |     2   (0)| 00:00:01 |
|* 20 |       TABLE ACCESS FULL             | NPC_CIRCUIT_COMPONENT        | 23529 |   344K|   702  (13)| 00:00:03 |
|  21 |      TABLE ACCESS FULL              | BS_INSTANCE                  | 13483 |   158K|    63   (2)| 00:00:01 |
|  22 |     TABLE ACCESS FULL               | BRAND                        |  1246 |  9968 |     5   (0)| 00:00:01 |
--------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - filter(COALESCE("BR"."BRAND_ORG_CODE","SI"."CLIENT_ORG_CODE")=2421)
   3 - access("BR"."ID"(+)="SI"."BRAND_ID")
   4 - access("LS"."BS_INSTANCE_ID"="SI"."ID")
   5 - access("CC2"."CIRCUIT_ID"="CH"."MASTER_CIRCUIT_ID")
   9 - access("CSC"."CUSTOMER_SERVICE_ID"="CS"."CUSTOMER_SERVICE_ID")
  10 - access("CS"."BS_LOCATION_SCHEDULE_ID"="LS"."ID")
  11 - filter(COALESCE("LS"."TERMINATED_DATE",SYSDATE@!)&gt;=SYSDATE@! AND "LS"."SITE_CODE_ID" IS NOT NULL)
  13 - access("O"."ORG_CODE"=2421)
  14 - filter("CS"."BS_LOCATION_SCHEDULE_ID" IS NOT NULL AND ("CS"."CIRCUIT_STATUS_ID"=1 OR
              "CS"."CIRCUIT_STATUS_ID"=2 OR "CS"."CIRCUIT_STATUS_ID"=6))
  15 - filter(COALESCE("CSC"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)
  16 - filter(COALESCE("CC"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)
  17 - access("CC"."CIRCUIT_ID"="CSC"."CIRCUIT_ID")
  18 - access("CH"."SUB_CIRCUIT_ID"="CC"."CIRCUIT_COMPONENT_ID")
  20 - filter(COALESCE("CC2"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)


Statistics

         29  recursive calls
          0  db block gets
      45368  consistent gets
          0  physical reads
          0  redo size
       3423  bytes sent via SQL*Net to client
        576  bytes received via SQL*Net from client
          9  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
        109  rows processed
</code></pre>

<p>autotrace output including plan, slow run:</p>

<pre><code>109 rows selected.

Elapsed: 00:00:02.67

Execution Plan

Plan hash value: 2956052167

--------------------------------------------------------------------------------------------------------------------
| Id  | Operation                           | Name                         | Rows  | Bytes | Cost (%CPU)| Time     |
--------------------------------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT                    |                              |   173 | 18857 |  2069   (6)| 00:00:07 |
|   1 |  HASH UNIQUE                        |                              |   173 | 18857 |  2069   (6)| 00:00:07 |
|*  2 |   FILTER                            |                              |       |       |            |          |
|*  3 |    HASH JOIN OUTER                  |                              |   173 | 18857 |  2068   (6)| 00:00:07 |
|*  4 |     HASH JOIN                       |                              |   173 | 17473 |  2063   (6)| 00:00:07 |
|*  5 |      HASH JOIN                      |                              |   173 | 15397 |  2000   (6)| 00:00:07 |
|   6 |       NESTED LOOPS                  |                              |   244 | 18056 |  1297   (2)| 00:00:05 |
|   7 |        NESTED LOOPS                 |                              |   249 | 18056 |  1297   (2)| 00:00:05 |
|   8 |         NESTED LOOPS                |                              |   249 | 15438 |   799   (3)| 00:00:03 |
|*  9 |          HASH JOIN                  |                              |   205 |  9635 |   183   (9)| 00:00:01 |
|* 10 |           HASH JOIN                 |                              |   280 |  8960 |   110   (5)| 00:00:01 |
|* 11 |            TABLE ACCESS FULL        | BS_LOCATION_SCHEDULE         |   695 | 12510 |    44   (7)| 00:00:01 |
|  12 |            NESTED LOOPS             |                              |  3452 | 48328 |    66   (4)| 00:00:01 |
|* 13 |             INDEX UNIQUE SCAN       | ORGANISATION__PK             |     1 |     4 |     1   (0)| 00:00:01 |
|* 14 |             TABLE ACCESS FULL       | NPC_CUSTOMER_SERVICE         |  3452 | 34520 |    65   (4)| 00:00:01 |
|* 15 |           TABLE ACCESS FULL         | NPC_CUSTOMER_SERVICE_CIRCUIT |  2531 | 37965 |    72  (13)| 00:00:01 |
|* 16 |          TABLE ACCESS BY INDEX ROWID| NPC_CIRCUIT_COMPONENT        |     1 |    15 |     3   (0)| 00:00:01 |
|* 17 |           INDEX RANGE SCAN          | NPC_CIRCUIT_COMPONENT_I01    |     9 |       |     2   (0)| 00:00:01 |
|* 18 |         INDEX UNIQUE SCAN           | NPC_CIRCUIT_HIERARCHY_I02    |     1 |       |     1   (0)| 00:00:01 |
|  19 |        TABLE ACCESS BY INDEX ROWID  | NPC_CIRCUIT_HIERARCHY        |     1 |    12 |     2   (0)| 00:00:01 |
|* 20 |       TABLE ACCESS FULL             | NPC_CIRCUIT_COMPONENT        | 23529 |   344K|   702  (13)| 00:00:03 |
|  21 |      TABLE ACCESS FULL              | BS_INSTANCE                  | 13483 |   158K|    63   (2)| 00:00:01 |
|  22 |     TABLE ACCESS FULL               | BRAND                        |  1246 |  9968 |     5   (0)| 00:00:01 |
--------------------------------------------------------------------------------------------------------------------

Predicate Information (identified by operation id):
---------------------------------------------------

   2 - filter(COALESCE("BR"."BRAND_ORG_CODE","SI"."CLIENT_ORG_CODE")=2421)
   3 - access("BR"."ID"(+)="SI"."BRAND_ID")
   4 - access("LS"."BS_INSTANCE_ID"="SI"."ID")
   5 - access("CC2"."CIRCUIT_ID"="CH"."MASTER_CIRCUIT_ID")
   9 - access("CSC"."CUSTOMER_SERVICE_ID"="CS"."CUSTOMER_SERVICE_ID")
  10 - access("CS"."BS_LOCATION_SCHEDULE_ID"="LS"."ID")
  11 - filter(COALESCE("LS"."TERMINATED_DATE",SYSDATE@!)&gt;=SYSDATE@! AND "LS"."SITE_CODE_ID" IS NOT NULL)
  13 - access("O"."ORG_CODE"=2421)
  14 - filter("CS"."BS_LOCATION_SCHEDULE_ID" IS NOT NULL AND ("CS"."CIRCUIT_STATUS_ID"=1 OR
              "CS"."CIRCUIT_STATUS_ID"=2 OR "CS"."CIRCUIT_STATUS_ID"=6))
  15 - filter(COALESCE("CSC"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)
  16 - filter(COALESCE("CC"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)
  17 - access("CC"."CIRCUIT_ID"="CSC"."CIRCUIT_ID")
  18 - access("CH"."SUB_CIRCUIT_ID"="CC"."CIRCUIT_COMPONENT_ID")
  20 - filter(COALESCE("CC2"."END_DATE",SYSDATE@!)&gt;=SYSDATE@!)


Statistics

          0  recursive calls
          0  db block gets
      82317  consistent gets
          0  physical reads
          0  redo size
       3423  bytes sent via SQL*Net to client
        577  bytes received via SQL*Net from client
          9  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
        109  rows processed
</code></pre>

<p>tkprof output, fast run:</p>

<pre><code>call     count       cpu    elapsed       disk      query    current        rows
------- ------  -------- ---------- ---------- ---------- ----------  ----------
Parse        1      0.05       0.05          0          0          0           0
Execute      1      0.00       0.00          0          0          0           0
Fetch        9      0.59       0.59          0      65896          0         109
------- ------  -------- ---------- ---------- ---------- ----------  ----------
total       11      0.64       0.64          0      65896          0         109

Misses in library cache during parse: 1
Optimizer mode: ALL_ROWS
Parsing user id: 631  
Number of plan statistics captured: 1

Rows (1st) Rows (avg) Rows (max)  Row Source Operation
---------- ---------- ----------  ---------------------------------------------------
       109        109        109  HASH UNIQUE (cr=65896 pr=0 pw=0 time=596536 us cost=2069 size=18857 card=173)
       192        192        192   FILTER  (cr=65896 pr=0 pw=0 time=629952 us)
     25244      25244      25244    HASH JOIN OUTER (cr=65896 pr=0 pw=0 time=595042 us cost=2068 size=18857 card=173)
     25244      25244      25244     HASH JOIN  (cr=65874 pr=0 pw=0 time=579863 us cost=2063 size=17473 card=173)
     25244      25244      25244      HASH JOIN  (cr=65501 pr=0 pw=0 time=408409 us cost=2000 size=15397 card=173)
     12247      12247      12247       NESTED LOOPS  (cr=61723 pr=0 pw=0 time=338753 us cost=1297 size=18056 card=244)
     12247      12247      12247        NESTED LOOPS  (cr=49476 pr=0 pw=0 time=276466 us cost=1297 size=18056 card=249)
     16700      16700      16700         NESTED LOOPS  (cr=24758 pr=0 pw=0 time=232395 us cost=799 size=15438 card=249)
     12630      12630      12630          HASH JOIN  (cr=995 pr=0 pw=0 time=59090 us cost=183 size=9635 card=205)
      5558       5558       5558           HASH JOIN  (cr=622 pr=0 pw=0 time=36847 us cost=110 size=8960 card=280)
      8984       8984       8984            TABLE ACCESS FULL BS_LOCATION_SCHEDULE (cr=247 pr=0 pw=0 time=6835 us cost=44 size=12510 card=695)
      5653       5653       5653            NESTED LOOPS  (cr=375 pr=0 pw=0 time=7076 us cost=66 size=48328 card=3452)
         1          1          1             INDEX UNIQUE SCAN ORGANISATION__PK (cr=2 pr=0 pw=0 time=38 us cost=1 size=4 card=1)(object id 98786)
      5653       5653       5653             TABLE ACCESS FULL NPC_CUSTOMER_SERVICE (cr=373 pr=0 pw=0 time=5278 us cost=65 size=34520 card=3452)
     32022      32022      32022           TABLE ACCESS FULL NPC_CUSTOMER_SERVICE_CIRCUIT (cr=373 pr=0 pw=0 time=25562 us cost=72 size=37965 card=2531)
     16700      16700      16700          TABLE ACCESS BY INDEX ROWID NPC_CIRCUIT_COMPONENT (cr=23763 pr=0 pw=0 time=131644 us cost=3 size=15 card=1)
     17448      17448      17448           INDEX RANGE SCAN NPC_CIRCUIT_COMPONENT_I01 (cr=17401 pr=0 pw=0 time=61607 us cost=2 size=0 card=9)(object id 4306712)
     12247      12247      12247         INDEX UNIQUE SCAN NPC_CIRCUIT_HIERARCHY_I02 (cr=24718 pr=0 pw=0 time=78582 us cost=1 size=0 card=1)(object id 4306727)
     12247      12247      12247        TABLE ACCESS BY INDEX ROWID NPC_CIRCUIT_HIERARCHY (cr=12247 pr=0 pw=0 time=51413 us cost=2 size=12 card=1)
    324238     324238     324238       TABLE ACCESS FULL NPC_CIRCUIT_COMPONENT (cr=3778 pr=0 pw=0 time=161012 us cost=702 size=352935 card=23529)
     13529      13529      13529      TABLE ACCESS FULL BS_INSTANCE (cr=373 pr=0 pw=0 time=5917 us cost=63 size=161796 card=13483)
      1271       1271       1271     TABLE ACCESS FULL BRAND (cr=22 pr=0 pw=0 time=542 us cost=5 size=9968 card=1246)

********************************************************************************
</code></pre>

<p>tkprof output, slow run:</p>

<pre><code>call     count       cpu    elapsed       disk      query    current        rows
------- ------  -------- ---------- ---------- ---------- ----------  ----------
Parse        1      0.00       0.00          0          0          0           0
Execute      1      0.00       0.00          0          0          0           0
Fetch        9      5.66       5.66          0      82317          0         109
------- ------  -------- ---------- ---------- ---------- ----------  ----------
total       11      5.66       5.66          0      82317          0         109

Misses in library cache during parse: 0
Optimizer mode: ALL_ROWS
Parsing user id: 631  
Number of plan statistics captured: 1

Rows (1st) Rows (avg) Rows (max)  Row Source Operation
---------- ---------- ----------  ---------------------------------------------------
       109        109        109  HASH UNIQUE (cr=82317 pr=0 pw=0 time=5667122 us cost=16766 size=16723107 card=153423)
       192        192        192   FILTER  (cr=82317 pr=0 pw=0 time=5865780 us)
     25244      25244      25244    HASH JOIN RIGHT OUTER (cr=82317 pr=0 pw=0 time=5595368 us cost=13509 size=16723107 card=153423)
      1271       1271       1271     TABLE ACCESS FULL BRAND (cr=22 pr=0 pw=0 time=315 us cost=5 size=9968 card=1246)
     25244      25244      25244     HASH JOIN  (cr=82295 pr=0 pw=0 time=5582567 us cost=13501 size=15495723 card=153423)
     13529      13529      13529      TABLE ACCESS FULL BS_INSTANCE (cr=373 pr=0 pw=0 time=6801 us cost=63 size=161796 card=13483)
     25244      25244      25244      HASH JOIN  (cr=81922 pr=0 pw=0 time=5561289 us cost=13435 size=13654647 card=153423)
      8984       8984       8984       TABLE ACCESS FULL BS_LOCATION_SCHEDULE (cr=247 pr=0 pw=0 time=5118 us cost=44 size=161712 card=8984)
     25388      25388      25388       HASH JOIN  (cr=81675 pr=0 pw=0 time=5568466 us cost=13388 size=10893033 card=153423)
     12343      12343      12343        HASH JOIN  (cr=77897 pr=0 pw=0 time=7626696 us cost=12679 size=1423744 card=25424)
     16798      16798      16798         HASH JOIN  (cr=4526 pr=0 pw=0 time=217551 us cost=848 size=1139336 card=25894)
     12751      12751      12751          HASH JOIN  (cr=748 pr=0 pw=0 time=21460 us cost=139 size=124439 card=4291)
      5653       5653       5653           NESTED LOOPS  (cr=375 pr=0 pw=0 time=4514 us cost=66 size=48328 card=3452)
         1          1          1            INDEX UNIQUE SCAN ORGANISATION__PK (cr=2 pr=0 pw=0 time=22 us cost=1 size=4 card=1)(object id 98786)
      5653       5653       5653            TABLE ACCESS FULL NPC_CUSTOMER_SERVICE (cr=373 pr=0 pw=0 time=3612 us cost=65 size=34520 card=3452)
     32022      32022      32022           TABLE ACCESS FULL NPC_CUSTOMER_SERVICE_CIRCUIT (cr=373 pr=0 pw=0 time=13825 us cost=72 size=480330 card=32022)
    324238     324238     324238          TABLE ACCESS FULL NPC_CIRCUIT_COMPONENT (cr=3778 pr=0 pw=0 time=112639 us cost=703 size=4863570 card=324238)
  24918733   24918733   24918733         INDEX FAST FULL SCAN NPC_CIRCUIT_HIERARCHY_U01 (cr=73371 pr=0 pw=0 time=3349816 us cost=11418 size=292240992 card=24353416)(object id 4306730)
    324238     324238     324238        TABLE ACCESS FULL NPC_CIRCUIT_COMPONENT (cr=3778 pr=0 pw=0 time=95358 us cost=703 size=4863570 card=324238)

********************************************************************************
</code></pre>

<p>So the slow query is actually using a different plan, but this plan is not the same as the one shown by autotrace. Would still love to know why it changes after two runs.</p>

<p>I'm thinking I'll try rewriting the query to eliminate the outer join, by splitting it into two separate queries joined by a union.</p>

<p>Edit 1: added query</p>

<p>Edit 2: added autotrace output</p>

<p>Edit 3: removed with(), dual, 1=1 from test query</p>

<p>Edit 4: added tkprof output</p>

<p>Edit 5: turns out it was cardinality feedback</p>

## Answers
### Answer ID: 63435444
<p>[adding edit as answer, as requested by Jon Heller]</p>
<p>This was caused by cardinality feedback. I thought I had tested this earlier and eliminated it, but clearly got it wrong.</p>
<p>Added this to query:</p>
<pre><code>select --+ opt_param('_optimizer_use_feedback' 'false')
</code></pre>
<p>Now consistently fast.</p>

### Answer ID: 55228727
<p>Try running SQL Tunning advisor for the Query,And check all recommendations.</p>

### Answer ID: 47897357
<p>Your query has a number of problems as written:</p>

<ul>
<li>You make <em>very</em> heavy use of <code>COALESCE</code> instead of just checking for <code>NULL</code> explicitly. This could negatively impact the use of indexes. Notice that these filters correspond to full table scans in the plan.</li>
<li>You have a <code>LEFT JOIN</code> followed by several inner <code>JOIN</code>s. It's not clear what your intention is (at least not without staring at it for 15 minutes). Should rows where the <code>LEFT JOIN</code> finds no match still be included with <code>NULL</code> for all <code>JOIN</code>ed table columns, be left out of the result set if there's no match in the following <code>JOIN</code>ed tables, or something else?</li>
<li>You actually don't even need to <code>JOIN</code> some tables. You're filtering to a specific <code>org_code</code> and you never use the columns from <code>tdb.organisation</code>, so that join accomplishes nothing. <code>tdb.loc_site_code</code> is not referenced anywhere, so the join is just a simple filter to valid data values in that column at most. If the relating column is a DB enforced foreign key, then it's redundant.</li>
<li>Your static filters are in your <code>JOIN</code> conditions instead of in the <code>WHERE</code> clause. This makes it more difficult to read and understand.</li>
</ul>

<p>I'd advise rewriting the query completely and see how that performs. Try this:</p>

<pre><code>select distinct
    cc2.circuit_id as circuit_id,
    cc2.circuit_component_id as component_circuit_id
from bsdb.bs_instance si
join bsdb.bs_location_schedule ls on ls.bs_instance_id = si.id
join npc.npc_customer_service cs on cs.bs_location_schedule_id = ls.id
join npc.npc_customer_service_circuit csc on csc.customer_service_id = cs.customer_service_id
join npc.npc_circuit_component cc on cc.circuit_id = csc.circuit_id
join npc.npc_circuit_hierarchy ch on ch.sub_circuit_id = cc.circuit_component_id
join npc.npc_circuit_component cc2 on cc2.circuit_id = ch.master_circuit_id
-- join tdb.loc_site_code lsc on lsc.id = ls.site_code_id -- Uncomment if ls.site_code_id isn't a foreign key
left outer join scdb.brand br on br.id = si.brand_id
where
    coalesce(br.brand_org_code, si.client_org_code) = 2421
    and cs.circuit_status_id in (1, 2, 6)
    and (ls.terminated_date IS NULL OR ls.terminated_date &gt;= sysdate)
    and (csc.end_date IS NULL OR csc.end_date &gt;= sysdate)
    and (cc.end_date IS NULL OR cc.end_date &gt;= sysdate)
    and (cc2.end_date IS NULL OR cc2.end_date &gt;= sysdate)
    -- and ls.site_code_id IS NOT NULL -- Uncomment if site_code_id is a nullable foreign key
;
</code></pre>

<p><em>Much</em> easier to make sense of:</p>

<ul>
<li>Static filters all in the <code>WHERE</code> clause. (Note that this doesn't negatively impact performance. The DB is smart enough to figure out that it can do static filters before the <code>JOIN</code>s.)</li>
<li>Date columns have separate <code>NULL</code> checks, instead of using <code>COALESCE</code> that might prevent the planner from using indexes.</li>
<li><code>JOIN</code>s are exclusively on simple table ID columns.</li>
<li>The <code>JOIN</code>s progress in a clear, straightforward, easy to follow order. Most of them reference an ID column in the table directly above it.</li>
<li><code>LEFT JOIN</code> located at the end of the query, making it clear which tables' columns can be all <code>NULL</code> or not.</li>
<li>No joins to extraneous tables. All of them are used either for result columns or filtering.</li>
</ul>

<p>If the organization code is a very selective filter (filters out a lot of rows), try replacing <code>coalesce(br.brand_org_code, si.client_org_code) = 2421</code> with</p>

<pre><code>((br.brand_org_code IS NULL and si.client_org_code = 2421) or br.brand_org_code = 2421)
</code></pre>

<p>Take careful note of the parentheses. The planner might have a better chance of realizing it can use indexes on this.</p>

<p>If you really <em>do</em> need <code>tdb.organisation</code> for some reason and just aren't referencing those columns in this particular query, turn the above into a subquery and join to it <em>after</em> all the other filtering and transformation:</p>

<pre><code>select distinct
    circuit_id,
    component_circuit_id
from (
    select
        cc2.circuit_id as circuit_id,
        cc2.circuit_component_id as component_circuit_id,
        coalesce(br.brand_org_code, si.client_org_code) as org_code
    from bsdb.bs_instance si
    join bsdb.bs_location_schedule ls on ls.bs_instance_id = si.id
    join npc.npc_customer_service cs on cs.bs_location_schedule_id = ls.id
    join npc.npc_customer_service_circuit csc on csc.customer_service_id = cs.customer_service_id
    join npc.npc_circuit_component cc on cc.circuit_id = csc.circuit_id
    join npc.npc_circuit_hierarchy ch on ch.sub_circuit_id = cc.circuit_component_id
    join npc.npc_circuit_component cc2 on cc2.circuit_id = ch.master_circuit_id
    -- join tdb.loc_site_code lsc on lsc.id = ls.site_code_id -- Uncomment if ls.site_code_id isn't a foreign key
    left outer join scdb.brand br on br.id = si.brand_id
    where
        coalesce(br.brand_org_code, si.client_org_code) = 2421
        and cs.circuit_status_id in (1, 2, 6)
        and (ls.terminated_date IS NULL OR ls.terminated_date &gt;= sysdate)
        and (csc.end_date IS NULL OR csc.end_date &gt;= sysdate)
        and (cc.end_date IS NULL OR cc.end_date &gt;= sysdate)
        and (cc2.end_date IS NULL OR cc2.end_date &gt;= sysdate)
        -- and ls.site_code_id IS NOT NULL -- Uncomment if site_code_id is a nullable foreign key
) active_circuit_components
join tdb.organisation org on org.org_code = active_circuit_components.org_code
;
</code></pre>

<p>I'd also recommend coming up with meaningful aliases. With this number of aliases and how similar they all look at a glance, it's hard to keep track of which table is which. Some examples:</p>

<ul>
<li><code>si</code>: <code>bs_instance</code></li>
<li><code>ls</code>: <code>loc_sched</code></li>
<li><code>cs</code>: <code>cust_serv</code></li>
<li><code>csc</code>: <code>cust_serv_circuit</code></li>
</ul>

<p>They're more verbose, but they'll make it <em>vastly</em> easier to make semantic sense of the query when you or another developer comes back to it. I know such short aliases are common practice, but for large queries, it really matters whether you have to look back at the list of tables just to check whether a column is coming from the table you think it is.</p>

### Answer ID: 47854959
<p>I'll take a stab at this. </p>

<p>Using the information you've provided I have the following observations:</p>

<p>1 - You can use Index Hints</p>

<p>When the SQL is slow it is not accessing the following tables in the same way:
 - npc_circuit_component
 - npc_circuit_hierarchy</p>

<p>The NPC_CIRCUIT_COMPONENT_I01 and NPC_CIRCUIT_HIERARCHY_I02 indexes are not being used when accessing these tables. Both these are also shown in your explain plan.</p>

<p>A solution here (without modifying your query) is to use Index Hints to force the use of this indexes all the time.</p>

<pre><code>/*+ index(ch npc_circuit_hierarch_i02) */
/*+ index(cc npc_circuit_component_i01) */
</code></pre>

<p>2 - Rebuild Indexes or Gather Stats</p>

<p>If you haven't done so already, stats may need to be gathered or rebuild the above indexes so they are updated before using the hint.</p>

<p>3 - The Query Itself</p>

<p>The need for a hint usually implies that there may be an issue with how the query is written. Whilst I can't quite get a grasp of what is in the database tables without completely understanding the data model this section could possibly be written better:</p>

<pre><code>bsdb.bs_instance si
left outer join scdb.brand br
    on br.id = si.brand_id
join tdb.organisation o
    on o.org_code = coalesce(br.brand_org_code, si.client_org_code)
    and o.org_code = 2421
</code></pre>

<p>The org code is hardcoded here and may make the use of the organisation table redundant. You mentioned that the LEFT OUTER JOIN when removed will make it run faster. You can rewrite it with a WHERE:</p>

<pre><code>WHERE CASE WHEN si.brand_id IS NULL THEN 
       si.client_org_code
      ELSE
        SELECT br.brand_org_code FROM brand br
         WHERE br.id = si.brand_id
      END = 2421 -- Ord Code
</code></pre>

<p>This is just going off the top of my head, but this avoids having to use the left outer join and also removes the use of coalesce which will make any index on the brand_org_code or client_org_code columns redundant.</p>

<p>Anyway...not sure if this will help. Hope it does. Good Luck!</p>

<p>Please correct my understanding if anything here is incorrect.</p>

