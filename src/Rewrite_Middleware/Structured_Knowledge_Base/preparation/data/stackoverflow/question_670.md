# How to order query by column not in alphabetical order
[Link to question](https://stackoverflow.com/questions/36604493/how-to-order-query-by-column-not-in-alphabetical-order)
**Creation Date:** 1460565260
**Score:** 1
**Tags:** php, mysql, phalcon
## Question Body
<p>I'm using the Phalcon's QueryBuilder to build a query, returning full model objects.  I need to order the query by a "semester" column, in chronological order.  The problem is the contents of the column are "F","W","G","S", which is the order I need the values to be sorted in.  So all rows with "F" come first, then "W", etc.</p>

<p>First I tried to order with the MySQL FIELD() function, but I was getting parse exceptions, so I don't think PDO supports it.  I was unable to find any documentation one way or the other.</p>

<p>Then, I tried using the <code>-&gt;columns()</code> method of the QueryBuilder, but that renamed all my columns, and caused the return type to not be model objects.</p>

<p>Dropping QueryBuilder and using just raw SQL queries is not an option I'm going to consider - I have a complex framework built up around QueryBuilder and it would take too much work to rewrite.</p>

<p>My final attempt will be simply to change how "semester" is stored in the database, with "F" being 0, "W" being 1, etc.  I'd rather not change the data if I can get this to work in code.</p>

<p>Any ideas?</p>

## Answers
### Answer ID: 36604851
<p>You could try this string with the orderBy function :</p>

<pre><code>"CASE
 WHEN Semester = 'F' THEN 0
 WHEN Semester = 'W' THEN 1
 WHEN Semester = 'G' THEN 2
 ELSE 3
 END"
</code></pre>

### Answer ID: 36604692
<p>You could try joining with a user-defined select like this</p>

<pre><code>SELECT *
FROM yourtable
INNER JOIN
(SELECT 'F' as code,0 as sequence
 UNION
 SELECT 'W' as code,1 as sequence
 UNION
 SELECT 'G' as code,2 as sequence
 UNION
 SELECT 'S' as code,3 as sequence)
as T ON T.code = yourtable.column
ORDER BY T.sequence ASC
</code></pre>

<p>or you could use the FIND_IN_SET() function to define your order like this</p>

<pre><code>SELECT
  *,
  FIND_IN_SET(code,'F,W,G,S') as sequence
FROM semester
ORDER BY sequence ASC
</code></pre>

