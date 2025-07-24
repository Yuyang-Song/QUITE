# PostgreSQL 9.6 nested INSERT/RETURN statements have unacceptably poor CTE performance
[Link to question](https://stackoverflow.com/questions/77772880/postgresql-9-6-nested-insert-return-statements-have-unacceptably-poor-cte-perfor)
**Creation Date:** 1704627206
**Score:** 1
**Tags:** sql, database, postgresql-9.6
## Question Body
<p>I have a large table (&gt; 50M rows) that I'm trying to convert into a new table format.  As part of this, the row ids returned from the first insert need to be used in a second insert into a second table.</p>
<p>I am using a CTE that looks something like this:</p>
<pre><code>WITH inserted_data AS (
    INSERT INTO table1 (column1, column2, column3, column4)
    SELECT value1, value2, value3, value4
    FROM original_table
    RETURNING rowid, column4
)
INSERT INTO table2 (table1_id, column4)
SELECT rowid, column4
FROM inserted_data;
</code></pre>
<p>The problem is, this is unacceptably slow.  For only 4800 rows it takes 21 seconds, while for 9600 rows it takes around 50 seconds.  At this rate I expect it would take around 3 days for 50 million records.  I have a time constraint of around 2 hours.</p>
<p>If I perform just the first insert (no CTE), the query is 100x times faster, around 200 milliseconds and 500 milliseconds for 4800 and 9600 rows.  I know that the time for the second insert would also be negligible.  At this rate the query would finish in the allotted time.</p>
<p>The question is, how can I rewrite the query to perform at the rate the individual queries could complete in.  Shuffling all the data out of the database into an external program would be a hassle and error prone as well as require extra resources.  If I do something like write a function with a loop then I'm not inserting in one go and i expect poor performance there as well.   I don't think using a temporary table will help, because the issue seems to be with the mere existence of the CTE.</p>
<p>I tried this:</p>
<pre><code>INSERT INTO table2 (table1_id, column4)
SELECT rowid, column4
FROM (
    WITH inserted_data AS (
        INSERT INTO table1 (column1, column2, column3, column4)
        SELECT value1, value2, value3, value4
        FROM original_table
        RETURNING rowid, column4
    )
)
</code></pre>
<p>But this gives me:</p>
<pre><code>syntax error at or near &quot;INTO&quot;
</code></pre>

## Answers
### Answer ID: 77772969
<p>How about separating the inserts in two statements?  The second <code>insert</code> could look like:</p>
<pre><code>INSERT INTO table2
       (table1_id, column4)
SELECT t1.rowid
,      ot.column4
FROM   original_table ot
JOIN   table1 t1 
ON     t1.column1 = ot.value1
       AND t1.column2 = ot.value2
       AND t1.column3 = ot.value3
       AND t1.column4 = ot.value4
</code></pre>
<p>For each row in <code>original_table</code>, the join conditions looks for the row inserted into <code>table1</code>.</p>

