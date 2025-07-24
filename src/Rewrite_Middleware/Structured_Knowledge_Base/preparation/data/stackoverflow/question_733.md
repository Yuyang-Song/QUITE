# Unordered N records for each group of grouped results
[Link to question](https://stackoverflow.com/questions/39516737/unordered-n-records-for-each-group-of-grouped-results)
**Creation Date:** 1473959417
**Score:** 3
**Tags:** mysql, sql
## Question Body
<p>I have a table containing user records, and I want to take 5 records per <code>user_id</code>. I don't care about any sort of order. I could do this to get 1 record per user:</p>

<blockquote>
  <p>SELECT * FROM records GROUP BY user_id</p>
</blockquote>

<p>I could also do something with <a href="https://stackoverflow.com/a/30269273/326402">user variables</a> to take the top N records. However, my database is very large and a query with user variables isn't efficiently using the index on the <code>user_id</code> column because it has to sort within each group. I don't care about order at all, so I shouldn't have to touch records that aren't relevant. Since I only want 5 and each user has 200-400 records, this is a big performance hit.</p>

<p>Is there a way to write this query efficiently?</p>

<p>This question is <strong>not</strong> the same as asking how to get the top N records, because I don't care about ordering and I believe that removing that restriction should allow an efficient rewriting. If this is not the case, please explain why not. I have clarified this in the title.</p>

## Answers
### Answer ID: 39517443
<p>Try out with the below query.
The sub query will number the row based on the column mentioned in the <strong>Order By</strong> clause. In the outer query you can give the filter criteria.</p>

<pre><code>SET @rowNum = NULL, @rowVal = NULL;
SELECT * FROM (
    SELECT
        *, 
        @rowNum := IF(@rowVal = userid, @rowNum + 1, 1) AS Rno,
        @rowVal := userid AS Dummy
    FROM Yourtable
    ORDER BY [user_id] 
) AS t
 WHERE Rno &lt;= 5
</code></pre>

### Answer ID: 39517141
<p>You can resolve this using a view along with a Partition:</p>

<p>Create a view querying the core table ( add a RowId column counting how many records per user_id):</p>

<pre><code>SELECT *, ROW_NUMBER() OVER(PARTITION BY User_id) AS RowID
FROM Records 
</code></pre>

<p><strong>lets assume you call the view above ^ "Recordsvw</strong>"</p>

<p>It's simple, now of you need only 5 records per user_id query the view that you created above like this:</p>

<pre><code>SELECT *
FROM Recordsvw
WHERE ROwID &lt;= 5
</code></pre>

