# Using values from rows within a group in subuery critera
[Link to question](https://stackoverflow.com/questions/26002995/using-values-from-rows-within-a-group-in-subuery-critera)
**Creation Date:** 1411499823
**Score:** 2
**Tags:** sql, oracle-database, group-by, subquery
## Question Body
<p>Let's assume I have the following tables in an Oracle database:</p>

<ul>
<li><code>TBL_A</code> with the columns <code>ID</code>, <code>C_1</code>, <code>C_2</code>, <code>C_3</code>, ..., <code>C_20</code> (primary key: <code>ID</code>)</li>
<li><code>TBL_B</code> with the columns <code>ID</code>, <code>A_ID</code>, <code>C_1</code>, <code>C_2</code>, <code>C_3</code>, ..., <code>C_20</code> (foreign key <code>A_ID</code> references <code>TBL_A.ID</code>)</li>
<li><code>TBL_C</code>, <code>TBL_D</code> etc. with the same generic layout as <code>TBL_B</code></li>
</ul>

<p>Now, I am trying to build a report based on grouping rows from <code>TBL_A</code> and at the same time e.g. aggregating different data (sums, counts, min/max/avg values, etc.) from the additional tables (<code>TBL_B</code>, <code>TBL_C</code>, etc.), in which some additional criteria is met.</p>

<p>My problem probably boils down to how (if it's possible at all) to connect data from <code>TBL_x</code> in a subquery, if the primary query is based on a select from <code>TBL_A</code> using a <code>GROUP BY</code> clause, e.g. like this:</p>

<pre><code>select a.c_1,
count(a.id) as cnt, -- number of matches in TBL_A for this group
(select count(*) from tbl_b b where b.a_id = a.id and b.c_1 = 2) as b_cnt,
(select sum(c_5) from tbl_c c where c.a_id = a.id and c.c_3 = 3) as c_sum
from tbl_a a
where ...
group by a.c_1;
</code></pre>

<p>Even if Oracle won't execute this code (ORA-00979, a.id is not a GROUP BY expression), I hope the purpose of the query should be obvious. In this case, I need a four column result set with:</p>

<ol>
<li>All distinct values of <code>TBL_A.C_1</code>.</li>
<li>The number of rows in <code>TBL_A</code> within this group.</li>
<li>The number of rows in <code>TBL_B</code> where <code>C_1 = 2</code> and <code>A_ID</code> refers to any of the rows in <code>TBL_A</code> contained in this group.</li>
<li>The sum of <code>C_5</code> of the rows in <code>TBL_B</code> where <code>C_3 = 3</code> and <code>A_ID</code> refers to any of the rows in <code>TBL_A</code> contained in this group.</li>
</ol>

<p>I know I could rewrite the subqueries, so that the group-by columns are repeated in the where clause, e.g. like this for just one of the columns:</p>

<pre><code>select a.c_1,
(select count(*) from tbl_b b, tbl_a a2 
    where a2.c_1 = a.c_1 and b.a_id = a2.id and b.c_1 = 2) as b_cnt_2
from tbl_a a
where ...
group by a.c_1;
</code></pre>

<p>But in this case, I would both have to repeat all group by columns and the outer where clause in all subqueries and since in reality the where clause is rather long and I have both quite a few columns in the group by clause, as well as many subqueries referring to different tables with different relations to <code>TBL_A</code>, the SQL statement will probably end up as a complete mess.</p>

<p>Is it really not possible in Oracle to use values from individual rows within a group in subqueries like I tried in the first example (both <code>b.a_id = a.id</code> as well as <code>b.a_id in a.id</code> fails)? I also considered doing some tricks with <code>listagg</code>, but Oracle seem not to accept any aggregating functions in the subquery clause (ORA-00934 group function is not allowed here). I would understand the limitation in the outer where clause, but not why this is not allowed in the subquery where clause.</p>

<p>I have tried to implement the query by joining the additional tables (<code>TBL_B</code>, <code>TBL_C</code>, etc) with outer joins instead of writing subqueries, but this will expand the result (creating several combinations of all involved tables) before grouping, so that the same row is considered more than once by the aggregation functions. E.g. having two rows in <code>TBL_B</code> referring to one row in <code>TBL_A</code>, <code>count(a.id)</code> would count the same row in <code>TBL_A</code> twice.</p>

<p>Anyone with an idea how to proceed?</p>

## Answers
### Answer ID: 26003364
<p>If I understand what you're trying to do correctly you can get the aggregate for each a.id in a derived table, join those aggregates to table a and then aggregate again using <code>sum</code></p>

<pre><code>select 
    a.c_1
    count(a.id),
    coalesce(sum(b_count),0) b_cnt,
    coalesce(sum(c_sum),0) c_sum
from tbl_a a
left join (
    select a_id, count(*) b_count from tbl_b
    where c_1 = 2
    group by a_id
) b on b.a_id = a.id
left join (
    select a_id, sum(c_5) c_sum from tbl_c
    where c_3 = 3
    group by a_id
) c on c.a_id = a.id
where ...
group by a.c_1
</code></pre>

### Answer ID: 26003094
<p>Probably the simplest way is to use a subquery or CTE:</p>

<pre><code>with a as (
      select a.c_1, a.id,
             count(a.id) as cnt, -- number of matches in TBL_A for this group
             (select count(*) from tbl_b b where b.a_id = a.id and b.c_1 = 2) as b_cnt,
             (select sum(c_5) from tbl_c c where c.a_id = a.id and c.c_3 = 3) as c_sum
      from tbl_a a
      where ...
      group by a.id
     )
select a.c_1,
       sum(cnt) as cnt,
       sum(b_cnt) as b_cnt,
       sum(c_sum) as c_sum
from a
group by a.c_1;
</code></pre>

<p>This will work fine for most aggregation functions.  If you have an <code>avg()</code>, then do the sum and count separately, and divide the totals for the average.  If you have a <code>count(distinct)</code> then this will not work.  Your question has neither of these.</p>

