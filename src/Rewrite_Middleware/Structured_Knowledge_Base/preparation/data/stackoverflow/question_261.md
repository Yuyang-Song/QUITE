# Materialized View fast refresh taking a long time
[Link to question](https://stackoverflow.com/questions/1833489/materialized-view-fast-refresh-taking-a-long-time)
**Creation Date:** 1259766522
**Score:** 2
**Tags:** oracle-database
## Question Body
<p>I have a large table that is replicated from Oracle 10.2.0.4 to and Oracle 9i database using MView replication over the network.  The master table is about 50GB, 160M rows and there are about 2 - 3M new or updates rows per day.</p>

<p>The master table has a materialized view log created using rowid.</p>

<p>The full refresh of the view works and takes about 5 hours, which we can live with.</p>

<p>However the fast refresh is struggling to keep up.  Oracle seems to require two queries against the mlog and master table to do the refresh, the first looks like this:</p>

<pre><code>SELECT          /*+ */
   DISTINCT "A1"."M_ROW$$"
       FROM "GENEVA_ADMIN"."MLOG$_BILLSUMMARY" "A1"
      WHERE "A1"."M_ROW$$" &lt;&gt; ALL (SELECT "A2".ROWID
                                     FROM "GENEVA_ADMIN"."BILLSUMMARY" "A2"
                                    WHERE "A2".ROWID = "A1"."M_ROW$$")
        AND "A1"."SNAPTIME$$" &gt; :1
        AND "A1"."DMLTYPE$$" &lt;&gt; 'I'
</code></pre>

<p>The current plan is:</p>

<pre><code>---------------------------------------------------------------
| Id  | Operation                     | Name                  |
---------------------------------------------------------------
|   0 | SELECT STATEMENT              |                       |
|   1 |  HASH UNIQUE                  |                       |
|   2 |   FILTER                      |                       |
|   3 |    TABLE ACCESS BY INDEX ROWID| MLOG$_BILLSUMMARY     |
|   4 |     INDEX RANGE SCAN          | MLOG$_BILLSUMMARY_AK1 |
|   5 |    TABLE ACCESS BY USER ROWID | BILLSUMMARY           |
</code></pre>

<p>When there are 3M rows changed, this query literally runs forever - its basically useless.  However, if I rewrite it slightly and tell it to full scan the master table and mlog table, it completes in 20 minutes.</p>

<p>The problem is that the above query is coming out of the inners of Oracle and I cannot change it.  The problem is really the FILTER operation on line 2 - if I could get it to full scan both tables and hash join / anti-join, I am confident I can get it to complete quick enough, but no receipe of hints I offer will get this query to stop using the FILTER operation - maybe its not even valid.  I can use hints to get it to full scan both the tables, but the FILTER operation remains, and I understand it execute long 5 for each row returned by line 3, which will be 2- 3M rows.</p>

<p>Has anyone got any ideas on how to trick this query into the plan I want without changing the actual query, or better, any ways of getting replication to take a more sensible plan for my tablesizes?</p>

<p>Thanks,</p>

<p>Stephen. </p>

## Answers
### Answer ID: 1834197
<p>How do the estimated cardinalities look for the refresh query in comparison to the actual cardinalities? Maybe the MLOG$ table statistics are incorrect.</p>

<p>It might be better to have no statistics on the table and lock them in order to invoke dynamic sampling, which ought to give a reasonable estimation based on the multiple predicates in the query.</p>

### Answer ID: 1833641
<p>As you wrote the queries are part of an internal Oracle mechanism so your tuning options are limited. The fast-refresh algorithm seems to behave differently in the more recent versions, check <a href="http://www.adellera.it/blog/2009/11/03/11gr2-materialized-view-logs-changes/" rel="nofollow noreferrer">Alberto Dell’Era’s analysis</a>. </p>

<p>You could also look into <a href="http://download.oracle.com/docs/cd/B19306_01/server.102/b14211/sql_tune.htm#PFGRF02605" rel="nofollow noreferrer">SQL profiles</a> (10g feature). With the package <a href="http://download-uk.oracle.com/docs/cd/B19306_01/appdev.102/b14258/d_sqltun.htm#i1009409" rel="nofollow noreferrer"><code>DBMS_SQLTUNE</code></a> this should allow you to tune individual SQL statements.</p>

