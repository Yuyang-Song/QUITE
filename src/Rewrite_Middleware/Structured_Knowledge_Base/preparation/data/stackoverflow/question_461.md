# Rewriting the HAVING clause and COUNT function
[Link to question](https://stackoverflow.com/questions/27240184/rewriting-the-having-clause-and-count-function)
**Creation Date:** 1417482262
**Score:** 1
**Tags:** sql, sqlite, count, url-rewriting, having
## Question Body
<p>I'm trying to conceptually understand how to rewrite the HAVING clause and COUNT function.</p>

<p>I was asked "Find the names of all reviewers who have contributed three or more ratings. (As an extra challenge, try writing the query without HAVING or without COUNT.)" in relation this this simple database: <a href="http://sqlfiddle.com/#!5/35779/2/0" rel="nofollow">http://sqlfiddle.com/#!5/35779/2/0</a></p>

<p>The query with HAVING and COUNT is easy. Without, I'm having difficulty.</p>

<p>Help would be very much appreciated. Thank you.</p>

## Answers
### Answer ID: 27240403
<p>One option would be to use <code>SUM(1)</code> in place of <code>COUNT</code> in a subquery, and using <code>WHERE</code> instead of <code>HAVING</code>:</p>

<pre><code>SELECT b.name
FROM (SELECT rID,SUM(1) Sum1
      FROM rating
      GROUP BY rID
      )a
JOIN reviewer b
  ON a.rID = b.rID
WHERE Sum1 &gt;= 3
</code></pre>

<p>Demo: <a href="http://sqlfiddle.com/#!7/7ab3a/1/0" rel="nofollow">SQL Fiddle</a></p>

<p>Update: Some explanation of <code>SUM(1)</code>:
Adding a constant to a <code>SELECT</code> statement will result in that value being repeated for every row returned, for example:</p>

<pre><code>SELECT rID
      ,1 as Col1
FROM rating
</code></pre>

<p>Returns:</p>

<pre><code>| rID | Col1 |
|-----|------|
| 201 |    1 |
| 201 |    1 |
| 202 |    1 |
| 203 |    1 |
| 203 |    1 |
......
</code></pre>

<p><code>SUM(1)</code> is applying a constant <code>1</code> to every row and aggregating it.</p>

