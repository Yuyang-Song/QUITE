# Get the difference of two queries
[Link to question](https://stackoverflow.com/questions/77121865/get-the-difference-of-two-queries)
**Creation Date:** 1694954910
**Score:** -1
**Tags:** sql, sql-server
## Question Body
<p>I have this query in my SQL Server database which returns 11196:</p>
<pre><code>SELECT count(*)
FROM all14020612 AS a
</code></pre>
<p>If I rewrite the query and join it with another table it returns 11013 records:</p>
<pre><code>SELECT count(*)
FROM   all14020612 AS a
       INNER JOIN MoshaverinAmlaks AS m
               ON a.[شناسه صنفی] COLLATE SQL_Latin1_General_CP1256_CI_AS = m.SenfID
       INNER JOIN Users AS u
               ON m.Code = u.MoshaverinAmlakCode 

</code></pre>
<p>I want the 183 records (the difference between these two queries), how can I write it to get these 183 expected records?
I tried this query below but It gives me 380 records which is not correct :</p>
<pre><code>SELECT count(*)
FROM   all14020612 AS a
WHERE  NOT EXISTS (SELECT 1
                   FROM   MoshaverinAmlaks AS m
                          INNER JOIN Users AS u
                                  ON m.Code = u.MoshaverinAmlakCode
                   WHERE  m.SenfID = a.[شناسه صنفی] COLLATE SQL_Latin1_General_CP1256_CI_AS) 

</code></pre>
<p>see I don't want the count of the differences, I want all of the records</p>

## Answers
### Answer ID: 77122089
<p>One possible way would be to use the <code>EXCEPT</code> operator.</p>
<p>The <a href="https://learn.microsoft.com/en-us/sql/t-sql/language-elements/set-operators-except-and-intersect-transact-sql?view=sql-server-ver16" rel="nofollow noreferrer"><code>EXCEPT</code></a> operator is used to return all rows in the first SELECT statement that are not returned by the second SELECT statement.</p>
<pre><code>SELECT a.*
FROM all14020612 AS a

EXCEPT

SELECT a.*
FROM all14020612 AS a
inner join MoshaverinAmlaks AS m
    on a.[شناسه صنفی] COLLATE SQL_Latin1_General_CP1256_CI_AS = m.SenfID
    INNER JOIN Users AS u ON m.Code = u.MoshaverinAmlakCode
;
</code></pre>
<hr />
<p>Why the count of rows in the difference result set is not the same as the <code>count(*) - count(*)</code>.</p>
<p>Let the first query return 10 rows:</p>
<pre><code>1
2
3
4
5
6
7
8
9
10
</code></pre>
<p>The <code>COUNT(*)</code> returns 10.</p>
<p>Let the second query return 8 rows with duplicates:</p>
<pre><code>1
2
3
4
5
5
5
5
</code></pre>
<p>The <code>COUNT(*)</code> returns 8.</p>
<p>The difference (<code>EXCEPT</code>) returns 5 rows</p>
<pre><code>6
7
8
9
10
</code></pre>
<p>which is more than 10-8.</p>
<p>Does your table <code>all14020612</code> have a primary key?
You can check if your second query returns duplicates of that primary key. This can happen if there is more than one <code>User</code>, or more than one <code>MoshaverinAmlak</code> for a certain row in <code>all14020612</code>.</p>

### Answer ID: 77123065
<p>It looks like there are 380 records in <code>all14020612</code> unmatched by <code>MoshaverinAmlaks JOIN Users</code> but one or more of the remaining rows in <code>all14020612</code> join to more than one row when you do the join.</p>
<p>When you subtract the counts you are implicitly assuming that each row in <code>all14020612</code> joins to exactly one or zero rows but this clearly isn't the case from your results.</p>
<p>(<a href="https://dbfiddle.uk/V6Y53Rrl" rel="nofollow noreferrer">This Fiddle gives example data that generates your stated results</a>).</p>
<p>You can use the following to get the rows that match <code>0</code> or <code>&gt;1</code> rows to see how this all breaks down.</p>
<pre><code>SELECT *
FROM all14020612 AS a
CROSS APPLY 
(
SELECT COUNT(*)
FROM   MoshaverinAmlaks AS m
        INNER JOIN Users AS u
                ON m.Code = u.MoshaverinAmlakCode
WHERE  m.SenfID = a.[شناسه صنفی] COLLATE SQL_Latin1_General_CP1256_CI_AS
) ca(joined_row_count)
WHERE joined_row_count &lt;&gt; 1
</code></pre>

### Answer ID: 77122026
<p>You can use a left join rather than inner join.  Left joins return all of the records from the left table whereas inner joins only return records that exist in both left and right tables.</p>
<pre><code>SELECT *
FROM all14020612 AS a
    LEFT OUTER JOIN MoshaverinAmlaks AS m ON a.[شناسه صنفی] COLLATE SQL_Latin1_General_CP1256_CI_AS = m.SenfID
    LEFT OUTER JOIN Users AS u ON m.Code = u.MoshaverinAmlakCode
WHERE m.SenfID IS NULL OR u.MoshaverinAmlakCode IS NULL
</code></pre>

