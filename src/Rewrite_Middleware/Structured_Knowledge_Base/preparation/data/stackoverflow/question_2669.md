# Conditional aggregation performance
[Link to question](https://stackoverflow.com/questions/45795898/conditional-aggregation-performance)
**Creation Date:** 1503314732
**Score:** 22
**Tags:** sql, sql-server, query-performance, conditional-aggregation
## Question Body
<p>Let us have the following data</p>

<pre><code> IF OBJECT_ID('dbo.LogTable', 'U') IS NOT NULL  DROP TABLE dbo.LogTable

 SELECT TOP 100000 DATEADD(day, ( ABS(CHECKSUM(NEWID())) % 65530 ), 0) datesent 
 INTO [LogTable]
 FROM    sys.sysobjects
 CROSS JOIN sys.all_columns
</code></pre>

<p>I want to count the number of rows, the number of last year rows and the number of last ten years rows. This can be achieved using conditional aggregation query or using subqueries as follows</p>

<pre><code>-- conditional aggregation query
SELECT
    COUNT(*) AS all_cnt,
    SUM(CASE WHEN datesent &gt; DATEADD(year,-1,GETDATE())
             THEN 1 ELSE 0 END) AS last_year_cnt,
    SUM(CASE WHEN datesent &gt; DATEADD(year,-10,GETDATE())
             THEN 1 ELSE 0 END) AS last_ten_year_cnt
FROM LogTable


-- subqueries
SELECT
(
    SELECT count(*) FROM LogTable 
) all_cnt, 
(
    SELECT count(*) FROM LogTable WHERE datesent &gt; DATEADD(year,-1,GETDATE())
) last_year_cnt,
(
    SELECT count(*) FROM LogTable WHERE datesent &gt; DATEADD(year,-10,GETDATE())
) last_ten_year_cnt
</code></pre>

<p>If you perform the queries and look on query plans then you see something like</p>

<p><a href="https://i.sstatic.net/lcrYB.png" rel="noreferrer"><img src="https://i.sstatic.net/lcrYB.png" alt="enter image description here"></a></p>

<p>Clearly, the first solution has much nicer query plan, cost estimation and even the SQL command looks more concise and fancy. However, if you measure the CPU time of the query using <code>SET STATISTICS TIME ON</code> I get the following results (I have measured several times with approximately the same results)</p>

<pre><code>(1 row(s) affected)

 SQL Server Execution Times:
   CPU time = 47 ms,  elapsed time = 41 ms.

(1 row(s) affected)

(1 row(s) affected)

 SQL Server Execution Times:
   CPU time = 31 ms,  elapsed time = 26 ms.
SQL Server parse and compile time: 
   CPU time = 0 ms, elapsed time = 0 ms.

 SQL Server Execution Times:
   CPU time = 0 ms,  elapsed time = 0 ms.
</code></pre>

<p>Therefore, the second solution has slightly better (or the same) performance than the solution using conditional aggregation. The difference becomes more evident if we create the index on <code>datesent</code> attribute.</p>

<pre><code>CREATE INDEX ix_logtable_datesent ON dbo.LogTable(DateSent)
</code></pre>

<p>Then the second solution starts to use <code>Index Seek</code> instead of <code>Table Scan</code> and its query CPU time performance drops to 16ms on my computer. </p>

<p>My questions are two: (1) why the conditional aggregation solution does not outperform the subquery solution at least in the case without index, (2) is it possible to create 'index' for the conditional aggregation solution (or rewrite the conditional aggregation query) in order to avoid scan, or is conditional aggregation generally unsuitable if we are concerned about performance?</p>

<p><strong>Sidenote:</strong> I can say, that this scenario is quite optimistic for conditional aggregation since we select the number of all rows which always leads to a solution using scan. If the number of all rows is not needed, then indexed solution with subqueries has no scan, whereas, the solution with conditional aggregation has to perform the scan anyway.</p>

<p><strong>EDIT</strong></p>

<p>Vladimir Baranov basically answered the first question (thank you very much). However, the second question remains. I can see on StackOverflow answers using conditional aggregation solutions quite offten and they attract a lot of attention being accepted as the most elegant and clear solution (and sometimes being proposed as the most efficient solution). Therefore, I will slightly generalize the question:</p>

<p><em>Could you give me an example, where conditional aggregation notably outperforms the subquery solution?</em> </p>

<p>For simplicity let us assume that physical accesses are not present (data are in Buffer cache) since the today database servers remain most of their data in the memory anyway.</p>

## Answers
### Answer ID: 61596314
<p>Here's my example where subqueries on large tables were extremely slow (around 40-50sec) and I was given the advice to rewrite the query with <code>FILTER</code> (Conditional Aggregation) which sped it up to 1sec. I was amazed.</p>

<p>Now I always use <code>FILTER</code> Conditional Aggregation because you only join on the large tables <strong>just once</strong>, and all the retrieval is done with <code>FILTER</code>. It's a bad idea to sub-select on large tables.</p>

<p>Thread: <a href="https://stackoverflow.com/questions/58532465/sql-performance-issues-with-inner-selects-in-postgres-for-tabulated-report">SQL Performance Issues with Inner Selects in Postgres for tabulated report</a></p>

<p>I needed a tabulated report, as follows,</p>

<p>Example (easy flat stuff first, then the complicated tabulated stuff):</p>

<pre><code>RecallID | RecallDate | Event |..| WalkAlone | WalkWithPartner |..| ExerciseAtGym
256      | 10-01-19   | Exrcs |..| NULL      | NULL            |..| yes
256      | 10-01-19   | Walk  |..| yes       | NULL            |..| NULL
256      | 10-01-19   | Eat   |..| NULL      | NULL            |..| NULL
257      | 10-01-19   | Exrcs |..| NULL      | NULL            |..| yes
</code></pre>

<p>My SQL had Inner Selects for the tabulated answer-based columns, and looked like this:</p>

<pre><code>select 
-- Easy flat stuff first
r.id as recallid, r.recall_date as recalldate, ... ,

-- Example of Tabulated Columns:
(select l.description from answers_t ans, activity_questions_t aq, lookup_t l 
where l.id=aq.answer_choice_id and aq.question_id=13 
and aq.id=ans.activity_question_id and aq.activity_id=27 and ans.event_id=e.id) 
     as transportationotherintensity,
(select l.description from answers_t ans, activity_questions_t aq, lookup_t l
where l.id=66 and l.id=aq.answer_choice_id and aq.question_id=14
and aq.id=ans.activity_question_id and ans.event_id=e.id) 
     as commutework,
(select l.description from answers_t ans, activity_questions_t aq, lookup_t l
where l.id=67 and l.id=aq.answer_choice_id and aq.question_id=14 and aq.id=ans.activity_question_id and ans.event_id=e.id) 
     as commuteschool,
(select l.description from answers_t ans, activity_questions_t aq, lookup_t l
where l.id=95 and l.id=aq.answer_choice_id and aq.question_id=14 and aq.id=ans.activity_question_id and ans.event_id=e.id) 
     as dropoffpickup,
</code></pre>

<p>The performance was horrible. Gordon Linoff recommended the <strong>one-time Join on the large table ANSWERS_T</strong> with <code>FILTER</code> as appropriate on all the tabulated Selects. That sped it up to 1 sec.</p>

<pre><code>select ans.event_id,
       max(l.description) filter (where aq.question_id = 13 and aq.activity_id = 27) as transportationotherintensity
       max(l.description) filter (where l.id = 66 and aq.question_id = 14 and aq.activity_id = 67) as commutework,
       . . .
from activity_questions_t aq join
     lookup_t l 
     on l.id = aq.answer_choice_id join
     answers_t ans
     on aq.id = ans.activity_question_id
group by ans.event_id
</code></pre>

### Answer ID: 45797189
<h2>Short summary</h2>

<ul>
<li>Performance of subqueries method depends on the data distribution. </li>
<li>Performance of conditional aggregation does not depend on the data distribution.</li>
</ul>

<p>Subqueries method can be faster or slower than conditional aggregation, it depends on the data distribution.</p>

<p>Naturally, if the table has a suitable index, then subqueries are likely to benefit from it, because index would allow to scan only the relevant part of the table instead of the full scan. Having a suitable index is unlikely to significantly benefit the Conditional aggregation method, because it will scan the full index anyway. The only benefit would be if the index is narrower than the table and engine would have to read fewer pages into memory.</p>

<p>Knowing this you can decide which method to choose.</p>

<hr>

<h2>First test</h2>

<p>I made a larger test table, with 5M rows. There were no indexes on the table.
I measured the IO and CPU stats using SQL Sentry Plan Explorer. I used SQL Server 2014 SP1-CU7 (12.0.4459.0) Express 64-bit for these tests.</p>

<p>Indeed, your original queries behaved as you described, i.e. subqueries were faster even though the reads were 3 times higher.</p>

<p>After few tries on a table without an index I rewrote your conditional aggregate and added variables to hold the value of <code>DATEADD</code> expressions.</p>

<p>Overall time became significantly faster.</p>

<p>Then I replaced <code>SUM</code> with <code>COUNT</code> and it became a little bit faster again.</p>

<p>After all, conditional aggregation became pretty much as fast as subqueries.</p>

<p><strong>Warm the cache</strong> (CPU=375)</p>

<pre><code>SELECT -- warm cache
    COUNT(*) AS all_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

    

<p><strong>Subqueries</strong> (CPU=1031)</p>

<pre><code>SELECT -- subqueries
(
    SELECT count(*) FROM LogTable 
) all_cnt, 
(
    SELECT count(*) FROM LogTable WHERE datesent &gt; DATEADD(year,-1,GETDATE())
) last_year_cnt,
(
    SELECT count(*) FROM LogTable WHERE datesent &gt; DATEADD(year,-10,GETDATE())
) last_ten_year_cnt
OPTION (RECOMPILE);
</code></pre>

    

<p><strong>Original conditional aggregation</strong> (CPU=1641)</p>

<pre><code>SELECT -- conditional original
    COUNT(*) AS all_cnt,
    SUM(CASE WHEN datesent &gt; DATEADD(year,-1,GETDATE())
             THEN 1 ELSE 0 END) AS last_year_cnt,
    SUM(CASE WHEN datesent &gt; DATEADD(year,-10,GETDATE())
             THEN 1 ELSE 0 END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

    

<p><strong>Conditional aggregation with variables</strong> (CPU=1078)</p>

<pre><code>DECLARE @VarYear1 datetime = DATEADD(year,-1,GETDATE());
DECLARE @VarYear10 datetime = DATEADD(year,-10,GETDATE());

SELECT -- conditional variables
    COUNT(*) AS all_cnt,
    SUM(CASE WHEN datesent &gt; @VarYear1
             THEN 1 ELSE 0 END) AS last_year_cnt,
    SUM(CASE WHEN datesent &gt; @VarYear10
             THEN 1 ELSE 0 END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

    

<p><strong>Conditional aggregation with variables and COUNT instead of SUM</strong> (CPU=1062)</p>

<pre><code>SELECT -- conditional variable, count, not sum
    COUNT(*) AS all_cnt,
    COUNT(CASE WHEN datesent &gt; @VarYear1
             THEN 1 ELSE NULL END) AS last_year_cnt,
    COUNT(CASE WHEN datesent &gt; @VarYear10
             THEN 1 ELSE NULL END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

<p><a href="https://i.sstatic.net/HsV6A.png" rel="noreferrer"><img src="https://i.sstatic.net/HsV6A.png" alt="times"></a></p>

<p>Based on these results my guess is that <code>CASE</code> invoked <code>DATEADD</code> for each row, while <code>WHERE</code> was smart enough to calculate it once. Plus <code>COUNT</code> is a tiny bit more efficient than <code>SUM</code>.</p>

<p>In the end, conditional aggregation is only slightly slower than subqueries (1062 vs 1031), maybe because <code>WHERE</code> is a bit more efficient than <code>CASE</code> in itself, and besides, <code>WHERE</code> filters out quite a few rows, so <code>COUNT</code> has to process less rows.</p>

<hr>

<p>In practice I would use conditional aggregation, because I think that number of reads is more important. If your table is small to fit and stay in the buffer pool, then any query will be fast for the end user. But, if the table is larger than available memory, then I expect that reading from disk would slow subqueries significantly.</p>

<hr>

<h2>Second test</h2>

<p>On the other hand, filtering the rows out as early as possible is also important.</p>

<p>Here is a slight variation of the test, which demonstrates it. Here I set the threshold to be GETDATE() + 100 years, to make sure that no rows satisfy the filter criteria.</p>

<p><strong>Warm the cache</strong> (CPU=344)</p>

<pre><code>SELECT -- warm cache
    COUNT(*) AS all_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

<p><strong>Subqueries</strong> (CPU=500)</p>

<pre><code>SELECT -- subqueries
(
    SELECT count(*) FROM LogTable 
) all_cnt, 
(
    SELECT count(*) FROM LogTable WHERE datesent &gt; DATEADD(year,100,GETDATE())
) last_year_cnt
OPTION (RECOMPILE);
</code></pre>

<p><strong>Original conditional aggregation</strong> (CPU=937)</p>

<pre><code>SELECT -- conditional original
    COUNT(*) AS all_cnt,
    SUM(CASE WHEN datesent &gt; DATEADD(year,100,GETDATE())
             THEN 1 ELSE 0 END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

<p><strong>Conditional aggregation with variables</strong> (CPU=750)</p>

<pre><code>DECLARE @VarYear100 datetime = DATEADD(year,100,GETDATE());

SELECT -- conditional variables
    COUNT(*) AS all_cnt,
    SUM(CASE WHEN datesent &gt; @VarYear100
             THEN 1 ELSE 0 END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

<p><strong>Conditional aggregation with variables and COUNT instead of SUM</strong> (CPU=750)</p>

<pre><code>SELECT -- conditional variable, count, not sum
    COUNT(*) AS all_cnt,
    COUNT(CASE WHEN datesent &gt; @VarYear100
             THEN 1 ELSE NULL END) AS last_ten_year_cnt
FROM LogTable
OPTION (RECOMPILE);
</code></pre>

<p><a href="https://i.sstatic.net/71j5L.png" rel="noreferrer"><img src="https://i.sstatic.net/71j5L.png" alt="times2"></a></p>

<p>Below is a plan with subqueries. You can see that 0 rows went into the Stream Aggregate in the second subquery, all of them were filtered out at the Table Scan step.</p>

<p><a href="https://i.sstatic.net/QBYyM.png" rel="noreferrer"><img src="https://i.sstatic.net/QBYyM.png" alt="plan_subqueries"></a></p>

<p>As a result, subqueries are again faster. </p>

<h2>Third test</h2>

<p>Here I changed the filtering criteria of the previous test: all <code>&gt;</code> were replaced with <code>&lt;</code>. As a result, the conditional <code>COUNT</code> counted all rows instead of none. Surprise, surprise! Conditional aggregation query took same 750 ms, while subqueries became 813 instead of 500.</p>

<p><a href="https://i.sstatic.net/O3ocH.png" rel="noreferrer"><img src="https://i.sstatic.net/O3ocH.png" alt="times3"></a></p>

<p>Here is the plan for subqueries:</p>

<p><a href="https://i.sstatic.net/E8zsc.png" rel="noreferrer"><img src="https://i.sstatic.net/E8zsc.png" alt="plan_subqueries3"></a></p>

<blockquote>
  <p>Could you give me an example, where conditional aggregation notably
  outperforms the subquery solution?</p>
</blockquote>

<p>Here it is. Performance of subqueries method depends on the data distribution. Performance of conditional aggregation does not depend on the data distribution. </p>

<p>Subqueries method can be faster or slower than conditional aggregation, it depends on the data distribution. </p>

<p>Knowing this you can decide which method to choose.</p>

<hr>

<h2>Bonus details</h2>

<p>If you hover the mouse over the <code>Table Scan</code> operator you can see the <code>Actual Data Size</code> in different variants.</p>

<ol>
<li>Simple <code>COUNT(*)</code>:</li>
</ol>

<p><a href="https://i.sstatic.net/w08Pp.png" rel="noreferrer"><img src="https://i.sstatic.net/w08Pp.png" alt="data size count"></a></p>

<ol start="2">
<li>Conditional aggregation:</li>
</ol>

<p><a href="https://i.sstatic.net/0qb1v.png" rel="noreferrer"><img src="https://i.sstatic.net/0qb1v.png" alt="data size conditional"></a></p>

<ol start="3">
<li>Subquery in test 2:</li>
</ol>

<p><a href="https://i.sstatic.net/C60Q1.png" rel="noreferrer"><img src="https://i.sstatic.net/C60Q1.png" alt="data size subquery test2"></a></p>

<ol start="4">
<li>Subquery in test 3:</li>
</ol>

<p><a href="https://i.sstatic.net/C3Nqy.png" rel="noreferrer"><img src="https://i.sstatic.net/C3Nqy.png" alt="data size subquery test3"></a></p>

<p>Now it becomes clear that the difference in performance is likely caused by the difference in the amount of data that flows through the plan. </p>

<p>In case of simple <code>COUNT(*)</code> there is no <code>Output list</code> (no column values are needed) and data size is smallest (43MB).</p>

<p>In case of conditional aggregation this amount doesn't change between tests 2 and 3, it is always 72MB. <code>Output list</code> has one column <code>datesent</code>.</p>

<p>In case of subqueries, this amount <strong>does</strong> change depending on the data distribution.</p>

