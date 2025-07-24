# Is it possible to flatten a parent-child hierarchy table to a flat/wide table using recursive CTE (Snowflake SQL)?
[Link to question](https://stackoverflow.com/questions/78388506/is-it-possible-to-flatten-a-parent-child-hierarchy-table-to-a-flat-wide-table-us)
**Creation Date:** 1714111277
**Score:** 0
**Tags:** sql, snowflake-cloud-data-platform, jinja2, common-table-expression, recursive-cte
## Question Body
<p>I have a dumb/bad solution to my problem, but I have read the Snowflake docs on recursive CTEs (<a href="https://docs.snowflake.com/en/sql-reference/constructs/with" rel="nofollow noreferrer">https://docs.snowflake.com/en/sql-reference/constructs/with</a> and <a href="https://docs.snowflake.com/en/user-guide/queries-cte" rel="nofollow noreferrer">https://docs.snowflake.com/en/user-guide/queries-cte</a>) and wanted to see if I could create a more readable/efficient solution using recursive CTEs. However, I am unable to get the result that I want. Have I misunderstood what is possible using recursive CTEs or is there a mistake in my code?</p>
<p>I have a Snowflake database and a table that looks like this:</p>
<p><strong>parentmember_table</strong></p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th>MemberId</th>
<th>ParentMemberId</th>
<th>MemberLevel</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>6</td>
<td>1</td>
<td>2</td>
</tr>
<tr>
<td>1007407</td>
<td>6</td>
<td>3</td>
</tr>
<tr>
<td>1010551</td>
<td>1007407</td>
<td>4</td>
</tr>
</tbody>
</table></div>
<p>My goal is to &quot;flatten&quot; this table into the following table format:</p>
<p><strong>flat_table</strong></p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th>Level1</th>
<th>Leve2</th>
<th>Level3</th>
<th>Level4</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>6</td>
<td>1007407</td>
<td>1010551</td>
</tr>
</tbody>
</table></div>
<p>(I have removed all the columns, from both tables, that I think are irrelevant to the question.)</p>
<p>Here is the dumb solution which gets me what I want (I can rewrite this using dbt/Jinja to avoid copy pasting every table):</p>
<pre><code>use database MY_DATABASE;

create temporary table parentmember_table (memberid integer, parentmemberid integer, memberlevel integer);

INSERT INTO parentchild VALUES
  (1,       1,       1), -- root is where memberid = parentmemberid
  (6,       1,       2),
  (1007407, 6,       3),
  (1010551, 1007407, 4)
;


create or replace temporary table t0 as
select  parentmemberid as Level1
        , null as Level2
        , null as Level3
        , null as Level4
        , memberid
        , memberlevel
from    parentchild
where   parentmemberid = memberid
;


create or replace temporary table t1 as
select  a.Level1
        , case  when (b.memberlevel = 2) then b.memberid
                else coalesce(a.Level2, null)
                end as Level2
        
        , case  when (b.memberlevel = 3) then b.memberid
                else coalesce(a.Level3, null)
                end as Level3
        
        , case  when (b.memberlevel = 4) then b.memberid
                else coalesce(a.Level4, null)
                end as Level4
        
        , b.memberid as memberid
        , b.memberlevel as memberlevel
from    t0 as a
        , parentchild as b
where   b.parentmemberid = a.memberid
        and b.parentmemberid &lt;&gt; b.memberid
;


create or replace temporary table t2 as
select  a.Level1
        , case  when (b.memberlevel = 2) then b.memberid
                else coalesce(a.Level2, null)
                end as Level2
        
        , case  when (b.memberlevel = 3) then b.memberid
                else coalesce(a.Level3, null)
                end as Level3
        
        , case  when (b.memberlevel = 4) then b.memberid
                else coalesce(a.Level4, null)
                end as Level4
        
        , b.memberid as memberid
        , b.memberlevel as memberlevel
from    t1 as a
        , parentchild as b
where   b.parentmemberid = a.memberid
        and b.parentmemberid &lt;&gt; b.memberid
;

create or replace temporary table flat_table as
select  a.Level1
        , case  when (b.memberlevel = 2) then b.memberid
                else coalesce(a.Level2, null)
                end as Level2
        
        , case  when (b.memberlevel = 3) then b.memberid
                else coalesce(a.Level3, null)
                end as Level3
        
        , case  when (b.memberlevel = 4) then b.memberid
                else coalesce(a.Level4, null)
                end as Level4
        
        , b.memberid as memberid
        , b.memberlevel as memberlevel
from    t2 as a
        , parentchild as b
where   b.parentmemberid = a.memberid
        and b.parentmemberid &lt;&gt; b.memberid
;
</code></pre>
<p>Here is my attempt using recursive CTEs:</p>
<pre><code>create or replace temporary table recursive_cte_table as (
WITH RECURSIVE t (
        Level1
        , Level2
        , Level3
        , Level4
        , MemberId
        , MemberLevel
        ) AS (

        --&lt;anchor_clause&gt;
        select  MemberId as Level1
                , null as Level2
                , null as Level3
                , null as Level4
                , MemberId
                , MemberLevel
        from    parentchild
        where   ParentMemberID = MemberID

        UNION ALL

        --&lt;recursive_clause&gt;
        select  a.Level1
                , case  when (b.MemberLevel = 2) then b.MemberId
                        end as Level2
                , case  when (b.MemberLevel = 3) then b.MemberId
                        end as Level3
                , case  when (b.MemberLevel = 4) then b.MemberId
                        end as Level4
                , b.MemberId as MemberId
                , b.MemberLevel as MemberLevel
        from    t as a
                , parentchild as b
        where   b.ParentMemberId = a.MemberId
                and b.ParentMemberId &lt;&gt; b.MemberId
)

SELECT * FROM t
);
</code></pre>
<p>This gives me 4 rows instead of 1 row, with NULL in most columns:</p>
<p><strong>recursive_cte_table</strong></p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th>Level1</th>
<th>Leve2</th>
<th>Level3</th>
<th>Level4</th>
<th>MemberId</th>
<th>MemberLevel</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>null</td>
<td>null</td>
<td>null</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>1</td>
<td>6</td>
<td>null</td>
<td>null</td>
<td>6</td>
<td>2</td>
</tr>
<tr>
<td>1</td>
<td>null</td>
<td>1007407</td>
<td>null</td>
<td>1007407</td>
<td>3</td>
</tr>
<tr>
<td>1</td>
<td>null</td>
<td>null</td>
<td>1010551</td>
<td>1010551</td>
<td>4</td>
</tr>
</tbody>
</table></div>
<p>Is there a mistake in my code which can be fixed to make <strong>recursive_cte_table</strong> the same as <strong>flat_table</strong>? Or have I misunderstood what is possible using recursive CTEs?</p>
<p>EDIT: fixed table formatting.</p>

