# ORACLE SQL rewritten query
[Link to question](https://stackoverflow.com/questions/58962717/oracle-sql-rewritten-query)
**Creation Date:** 1574281178
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<p>In an Oracle database, how can I see the SQL that is really executed?</p>
<p>Let's say I have a query that looks like this:</p>
<pre><code>WITH numsA
     AS (SELECT 1 num FROM DUAL
         UNION
         SELECT 2 FROM DUAL
         UNION
         SELECT 3 FROM DUAL)
SELECT *
  FROM numsA
       FULL OUTER JOIN (SELECT 3 num FROM DUAL
                        UNION
                        SELECT 4 FROM DUAL
                        UNION
                        SELECT 5 FROM DUAL) numsB
          ON numsA.num = numsB.num
</code></pre>
<p>I suppose that the SQL engine will rewrite this SQL into something different before executing it.
Can some tell me how can I see that rewritten query (with tkprof maybe)?</p>

## Answers
### Answer ID: 58968494
<p>As @Gordon already commented that query does not execute in the oracle. Oracle creates the execution plan and further processing is done using the best plan chosen by the optimizer.</p>

<p>If you are keen to see how the query is executed then you must go for the execution plan.</p>

<p>Many tools provide the feature to directly see the execution plan and if you want to see the execution plan by yourself then you can achieve it using the following technique(taking the simplest example with query <code>SELECT 1 FROM DUAL</code>):</p>

<pre><code>SQL&gt; explain plan for
  2  select 1 from dual;

Explained.

SQL&gt; select * from table(dbms_xplan.display);

PLAN_TABLE_OUTPUT
--------------------------------------------------------------------------------
Plan hash value: 1388734953

-----------------------------------------------------------------
| Id  | Operation        | Name | Rows  | Cost (%CPU)| Time     |
-----------------------------------------------------------------
|   0 | SELECT STATEMENT |      |     1 |     2   (0)| 00:00:01 |
|   1 |  FAST DUAL       |      |     1 |     2   (0)| 00:00:01 |
-----------------------------------------------------------------

8 rows selected.

SQL&gt;
</code></pre>

<p>To understand the explain plan you must have to go through all the details related to it.</p>

<p>I advise you to refer to Oracle documentation for <a href="https://docs.oracle.com/database/121/TGSQL/tgsql_interp.htm#TGSQL94618" rel="nofollow noreferrer">Reading Execution Plans</a></p>

<p>Cheers!!</p>

