# How to add a WHERE statement correctly to a complex MySQL query?
[Link to question](https://stackoverflow.com/questions/24344052/how-to-add-a-where-statement-correctly-to-a-complex-mysql-query)
**Creation Date:** 1403371514
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I have a quite complex query to get some data from the database, sort them and rank them accordingly.</p>

<p>Here is the SQL fiddle for it: <a href="http://sqlfiddle.com/#!2/148ff4/14" rel="nofollow" title="SQL Fiddle">SQL Fiddle</a></p>

<p>Now what I want to do is, to add a <code>WHERE</code> statement to this query, so only limited users will be selected (3 users above and 3 users below, the id = 8).</p>

<pre><code>WHERE sort BETWEEN @userpos - 3 AND @userpos + 3
</code></pre>

<p>So it should look something like this, but with the first example:</p>

<p><a href="http://sqlfiddle.com/#!2/ce034b/10" rel="nofollow" title="SQL Fiddle">SQL Fiddle</a></p>

<p>I have already tried to implement this WHERE statement to this query, but I couldn't figure it out where should I add, as I've always received error (that the column cannot be found).</p>

<p>Any suggestion and / or solution for my problem? Should I rewrite the whole query for this?</p>

## Answers
### Answer ID: 24344324
<p>If I understand correctly, you can do this with a subquery:</p>

<pre><code>SET @userid = 8

SELECT *
FROM (SELECT @pos := @pos + 1 AS sort, points, r.userid, s.active
      FROM rank r JOIN
           settings s
           USING (userid) CROSS JOIN
           (SELECT @pos := 0) p
      WHERE s.active = 1
      ORDER BY points DESC
    ) list 
WHERE userid = @userid;
</code></pre>

<p>Note that this eliminates a layer of subqueries that you have.  Otherwise, it is quite similar to your query.</p>

<p>EDIT:</p>

<p>The above was based more on the SQL Fiddle than on the question.  (Oops.)</p>

<p>To get three rows before and after a given row is possible and just a small tweak, using a trick.  The trick is to define another variable with the user pos and then use that variable in the outer query:</p>

<pre><code>SELECT *
FROM (SELECT @pos := @pos + 1 AS sort, points, r.userid, s.active,
             if(userid = @userid, @userpos := @pos, 0)
      FROM rank r JOIN
           settings s
           USING (userid) CROSS JOIN
           (SELECT @pos := 0, @userpos := 0) p
      WHERE s.active = 1
      ORDER BY points DESC
    ) list 
WHERE `sort` between @userpos - 3 and @userpos + 3;
</code></pre>

<p>Note:  MySQL does not guarantee the order of evaluation for variables in the select.  The following is a bit safer in terms of order of execution:</p>

<pre><code>SELECT *
FROM (SELECT (case when (@pos := @pos + 1) is NULL then NULL
                   when (case when (userid = @userid) then @userpos := @pos else 1 end) is null
                   then NULL
                   else @pos
              end) AS sort, points, r.userid, s.active,
             if(userid = @userid, @userpos := @pos)
      FROM rank r JOIN
           settings s
           USING (userid) CROSS JOIN
           (SELECT @pos := 0, @userpos := 0) p
      WHERE s.active = 1
      ORDER BY points DESC
    ) list 
WHERE `sort` between @userpos - 3 and @userpos + 3;
</code></pre>

<p>The weird <code>case</code> statements are to ensure statement executions.  The <code>is null</code> is to ensure that the <code>when</code> clauses fail, so the assignments are made sequentially.</p>

