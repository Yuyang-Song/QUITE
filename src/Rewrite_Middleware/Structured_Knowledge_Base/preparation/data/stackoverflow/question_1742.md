# Make Oracle 9i use indexes
[Link to question](https://stackoverflow.com/questions/6056308/make-oracle-9i-use-indexes)
**Creation Date:** 1305796322
**Score:** 2
**Tags:** performance, oracle-database, oracle9i
## Question Body
<p>I'm having a performance issue when deploying an app developed on 10g XE in a client's 9i server. The same query produces completely different query plans depending on the server:</p>

<pre><code>SELECT DISTINCT FOO.FOO_ID               AS C0,
    GEE.GEE_CODE                         AS C1,
    TO_CHAR(FOO.SOME_DATE, 'DD/MM/YYYY') AS C2,
    TMP_FOO.SORT_ORDER                   AS SORT_ORDER_
FROM TMP_FOO
INNER JOIN FOO ON TMP_FOO.FOO_ID=FOO.FOO_ID
LEFT JOIN BAR ON FOO.FOO_ID=BAR.FOO_ID
LEFT JOIN GEE ON FOO.GEE_ID=GEE.GEE_ID
ORDER BY SORT_ORDER_;
</code></pre>

<p>Oracle Database 10g Express Edition Release 10.2.0.1.0 - Production:</p>

<pre><code>-------------------------------------------------------------------------------------------
| Id  | Operation                       | Name    | Rows  | Bytes | Cost (%CPU)| Time     |
-------------------------------------------------------------------------------------------
|   0 | SELECT STATEMENT                |         |     1 |    67 |    10  (30)| 00:00:01 |
|   1 |  SORT UNIQUE                    |         |     1 |    67 |     9  (23)| 00:00:01 |
|   2 |   NESTED LOOPS OUTER            |         |     1 |    67 |     8  (13)| 00:00:01 |
|*  3 |    HASH JOIN OUTER              |         |     1 |    48 |     7  (15)| 00:00:01 |
|   4 |     NESTED LOOPS                |         |     1 |    44 |     3   (0)| 00:00:01 |
|   5 |      TABLE ACCESS FULL          | TMP_FOO |     1 |    26 |     2   (0)| 00:00:01 |
|   6 |      TABLE ACCESS BY INDEX ROWID| FOO     |     1 |    18 |     1   (0)| 00:00:01 |
|*  7 |       INDEX UNIQUE SCAN         | FOO_PK  |     1 |       |     0   (0)| 00:00:01 |
|   8 |     TABLE ACCESS FULL           | BAR     |     1 |     4 |     3   (0)| 00:00:01 |
|   9 |    TABLE ACCESS BY INDEX ROWID  | GEE     |     1 |    19 |     1   (0)| 00:00:01 |
|* 10 |     INDEX UNIQUE SCAN           | GEE_PK  |     1 |       |     0   (0)| 00:00:01 |
-------------------------------------------------------------------------------------------
</code></pre>

<p>Oracle9i Release 9.2.0.1.0 - 64bit Production:</p>

<pre><code>----------------------------------------------------------------------------
| Id  | Operation               |  Name    | Rows  | Bytes |TempSpc| Cost  |
----------------------------------------------------------------------------
|   0 | SELECT STATEMENT        |          |    98M|  6546M|       |  3382K|
|   1 |  SORT UNIQUE            |          |    98M|  6546M|    14G|  1692K|
|*  2 |   HASH JOIN OUTER       |          |    98M|  6546M|   137M|  2874 |
|   3 |    VIEW                 |          |  2401K|   109M|       |   677 |
|*  4 |     HASH JOIN OUTER     |          |  2401K|   169M|    40M|   677 |
|   5 |      VIEW               |          |   587K|    34M|       |    24 |
|*  6 |       HASH JOIN         |          |   587K|    34M|       |    24 |
|   7 |        TABLE ACCESS FULL| TMP_FOO  |  8168 |   207K|       |    10 |
|   8 |        TABLE ACCESS FULL| FOO      |  7188 |   245K|       |     9 |
|   9 |      TABLE ACCESS FULL  | BAR      |   409 |  5317 |       |     1 |
|  10 |    TABLE ACCESS FULL    | GEE      |  4084 | 89848 |       |     5 |
----------------------------------------------------------------------------
</code></pre>

<p>As far as I can tell, indexes exist and are correct. What are my options to make Oracle 9i use them?</p>

<p><strong>Update #1:</strong> <code>TMP_FOO</code> is a temporary table and it has no rows in this test. <code>FOO</code> is a regular table with 13,035 rows in my local XE; not sure why the query plan shows <strong>1</strong>, perhaps it's realising that an INNER JOIN against an empty table won't require a full table scan :-?</p>

<p><strong>Update #2:</strong> I've spent a couple of weeks trying <em>everything</em> and <em>nothing</em> provided a real enhancement: query rewriting, optimizer hints, changes in DB design, getting rid of temp tables... Finally, I got a copy of the same 9.2.0.1.0 unpatched Oracle version the customer has (with obvious architecture difference), installed it at my site and... surprise! In my 9i, all execution plans come instantly and queries take from 1 to 10 seconds to complete.</p>

<p>At this point, I'm almost convinced that the customer has a serious misconfiguration issue.</p>

## Answers
### Answer ID: 6691731
<p>The customer had changed a default setting in order to support a very old third-party legacy application: the static parameter <code>OPTIMIZER_FEATURES_ENABLE</code> had been changed from the default value in 9i (<code>9.2.0</code>) to <code>8.1.7</code>.</p>

<p>I made the same change in a local copy of 9i and I got the same problems: explain plans that take hours to be calculated and so on.</p>

<p><em>(Knowing this, I've asked a <a href="https://serverfault.com/questions/280224/alternative-for-optimizer-features-enable">related question at ServerFault</a>, but I believe this solves the original question.)</em></p>

### Answer ID: 6057309
<p>In general it is hard to tune queries when the target version is older and a different edition. You have no chance of tuning a query without realistic volumes of data, or at least <em>realistic statistics</em>.  </p>

<p>If you have a good relationship with your client you could ask them to export their statistics using <a href="http://download.oracle.com/docs/cd/B10500_01/appdev.920/a96612/d_stats2.htm#1003982" rel="nofollow">DBMS_STATS.EXPORT_SCHEMA_STATS()</a>.  Then you can import the stats using the matching IMPORT_SCHEMA_STATS procedure.</p>

<p>Otherwise you'll have to fake the numbers yourself using the DBMS_STATS.SET_TABLE_STATISTICS() procedure.  <a href="http://decipherinfosys.wordpress.com/2007/07/31/dbms_statsset_table_stats/" rel="nofollow" title="Systems Engineering and RDBMS">Find out more</a>.</p>

### Answer ID: 6056419
<p>it looks like either you don't have data on your 10g express database, or your statistics are not collected properly. In either case it looks to Oracle like there aren't many rows, and therefore an index-range scan is appropriate.</p>

<p>In your 9i database, the statistics look like they are collected properly and Oracle sees a 4-table join with lots of rows and <em>without a where clause</em>. In that case since you haven't supplied an hint, Oracle builds an explain plan with the default ALL_ROWS optimizer behaviour: Oracle will find the plan that is the most performant to return <strong>all</strong> rows to the last. In that case the HASH JOIN with full table scans is brutally efficient, it will return big sets of rows faster that with an index NESTED LOOP join.</p>

<p>Maybe you want to use an index because you are only interested in the first few rows of the query. In that case use the hint <code>/*+ FIRST_ROWS*/</code> that will help Oracle understand that you are more interested in the first row response time than overall total query time.</p>

<p>Maybe you want to use an index because you think this would result in a faster total query time. You can force an explain plan through the use of hints like <a href="http://download.oracle.com/docs/cd/B19306_01/server.102/b14200/sql_elements006.htm#SQLRF50701" rel="nofollow"><code>USE_NL</code></a> and <a href="http://download.oracle.com/docs/cd/B19306_01/server.102/b14200/sql_elements006.htm#BABBABGJ" rel="nofollow"><code>USE_HASH</code></a> but most of the time you will see that if the statistics are up-to-date the optimizer will have picked the most efficient plan.</p>

<hr>

<p><strong>Update</strong>: I saw your update about TMP_FOO being a temporary table having no row. The problem with temporary table is that they have no stats so my above answer doesn't apply perfectly to temporary tables. Since the temp table has no stats, Oracle has to make a guess (here it chooses quite arbitrarly 8168 rows) which results in an inefficient plan.</p>

<p>This would be a case where it could be appropriate to use hints. You have several options:</p>

<ul>
<li>A mix of <a href="http://download.oracle.com/docs/cd/E11882_01/server.112/e17118/sql_elements006.htm#SQLRF50705" rel="nofollow">LEADING</a>, USE_NL and USE_HASH hints can force a specific plan (LEADING to set the order of the joins and USE* to set the join method).</li>
<li>You could use the undocumented CARDINALITY hint to give additional information to the optimizer as described in an <a href="http://asktom.oracle.com/pls/asktom/f?p=100:11:0%3a%3a%3a%3aP11_QUESTION_ID:3779680732446#15740265481549" rel="nofollow">AskTom article</a>. While the hint is undocumented, it is arguably <a href="http://asktom.oracle.com/pls/apex/f?p=100:11:0%3a%3aNO%3a%3aP11_QUESTION_ID:2233040800346569775" rel="nofollow">safe to use</a>. Note: on 10g+ the DYNAMIC_SAMPLING could be the documented alternative.</li>
<li>You can also set the statistics on the temporary table beforehand with the <a href="http://download.oracle.com/docs/cd/B19306_01/appdev.102/b14258/d_stats.htm#i997763" rel="nofollow">DBMS_STATS.set_table_stats</a> procedure. This last option would be quite radical since it would potentially modify the plan of all queries against this temp table.</li>
</ul>

### Answer ID: 6056648
<p>You could add the following hints which would "force" Oracle to use your indexes (if possible):</p>

<pre><code>Select /*+ index (FOO FOO_PK) */
       /*+ index (GEE GEE_PK) */
From ...
</code></pre>

<p>Or try to use the FIRST_ROWS hint to indicate you're not going to fetch all these estimated 98 Million rows... Otherwise I doubt the indexes would make a huge difference because you have no Where clause so Oracle would have to read these tables anyways. </p>

### Answer ID: 6056425
<p>It could be that 9i is doing it exactly right.  According to the stats posted, the Oracle 9i database believes it is dealing with a statement returning 98 million rows, whereas the 10G database thinks it will return 1 row.  It could be that both are correct, i.e the amount of data in the 2 databases is very very different.  Or it could be that you need to gather stats in either or both databases to get a more accurate query plan.</p>

