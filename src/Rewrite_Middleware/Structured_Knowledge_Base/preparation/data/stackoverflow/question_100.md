# Is there something wrong with joins that don&#39;t use the JOIN keyword in SQL or MySQL?
[Link to question](https://stackoverflow.com/questions/128965/is-there-something-wrong-with-joins-that-dont-use-the-join-keyword-in-sql-or-my)
**Creation Date:** 1222281372
**Score:** 46
**Tags:** sql, mysql, join
## Question Body
<p>When I started writing database queries I didn't know the JOIN keyword yet and naturally I just extended what I already knew and wrote queries like this:</p>
<pre><code>SELECT a.someRow, b.someRow 
FROM tableA AS a, tableB AS b 
WHERE a.ID=b.ID AND b.ID= $someVar
</code></pre>
<p>Now that I know that this is the same as an INNER JOIN I find all these queries in my code and ask myself if I should rewrite them. Is there something smelly about them or are they just fine?</p>
<hr />
<p><strong>My answer summary</strong>: There is nothing wrong with this query BUT using the keywords will most probably make the code more readable/maintainable.</p>
<p><strong>My conclusion</strong>: I will not change my old queries but I will correct my writing style and use the keywords in the future.</p>

## Answers
### Answer ID: 69911033
<p><strong>And what about performances ???</strong></p>
<p>As a matter of fact, performances is a very important problem in RDBMS.</p>
<p>So the question is <em>what is the most performant... Using JOIN or having joined table in the WHERE clause ?</em></p>
<p>Because optimizer (or planer as they said in PG...) ordinary does a good job, the two execution plans are the same, so the performances while excuting the query will be the same...</p>
<p><strong>But devil are hidden in some details....</strong></p>
<p>All optimizers have a limited time or a limited amount of work to find the best plan... And when the limit is reached, the result is the best plan among all computed plans, and not the better of all possible plans !</p>
<p>Now the question is <em>do I loose time when I use WHERE clause instead of JOINs for joining tables ?</em></p>
<p>And the answer is <strong>YES</strong> !</p>
<p>YES, because the relational engine use relational algebrae that knows only JOIN operator, not pseudo joins made in the WHERE clause. So the first thing that the optimizer do (in fact the parser or the algrebriser) is to rewrite the query... and this loose some chances to have the best of all plans !</p>
<p>I have seen this problem twice, in my long RDBMS career (40 years...)</p>

### Answer ID: 558908
<p>Another thing to consider in the old join syntax is that is is very easy to get a cartesion join by accident since there is no on clause. If the Distinct keyword is in the query and it uses the old style joins, convert it to an ANSI standard join and see if you still need the distinct. If you are fixing accidental cartesion joins this way, you can improve performance tremendously by rewriting to specify the join and the join fields.</p>

### Answer ID: 129443
<p>The one problem that can arise is when you try to mix the old "comma-style" join with SQL-92 joins in the same query, for example if you need one inner join and another outer join.</p>

<pre><code>SELECT *
FROM table1 AS a, table2 AS b
 LEFT OUTER JOIN table3 AS c ON a.column1 = c.column1
WHERE a.column2 = b.column2;
</code></pre>

<p>The problem is that recent SQL standards say that the JOIN is evaluated before the comma-join.  So the reference to "a" in the ON clause gives an error, because the correlation name hasn't been defined yet as that ON clause is being evaluated.  This is a very confusing error to get.</p>

<p>The solution is to not mix the two styles of joins.  You can continue to use comma-style in your old code, but if you write a new query, convert all the joins to SQL-92 style.</p>

<pre><code>SELECT *
FROM table1 AS a
 INNER JOIN table2 AS b ON a.column2 = b.column2
 LEFT OUTER JOIN table3 AS c ON a.column1 = c.column1;
</code></pre>

### Answer ID: 129424
<p>In general: </p>

<p>Use the JOIN keyword to link (ie. "join") primary keys and foreign keys.</p>

<p>Use the WHERE clause to limit your result set to only the records you are interested in. </p>

### Answer ID: 129410
<p>Filtering joins solely using <code>WHERE</code> can be extremely inefficient in some common scenarios.  For example:</p>

<pre><code>SELECT * FROM people p, companies c 
    WHERE p.companyID = c.id AND p.firstName = 'Daniel'
</code></pre>

<p>Most databases will execute this query quite literally, first taking the <a href="http://en.wikipedia.org/wiki/Cartesian_product" rel="noreferrer">Cartesian product</a> of the <code>people</code> and <code>companies</code> tables and <em>then</em> filtering by those which have matching <code>companyID</code> and <code>id</code> fields.  While the fully-unconstrained product does not exist anywhere but in memory and then only for a moment, its calculation does take some time.</p>

<p>A better approach is to group the constraints with the <code>JOIN</code>s where relevant.  This is not only subjectively easier to read but also far more efficient.  Thusly:</p>

<pre><code>SELECT * FROM people p JOIN companies c ON p.companyID = c.id
    WHERE p.firstName = 'Daniel'
</code></pre>

<p>It's a little longer, but the database is able to look at the <code>ON</code> clause and use it to compute the fully-constrained <code>JOIN</code> directly, rather than starting with <em>everything</em> and then limiting down.  This is faster to compute (especially with large data sets and/or many-table joins) and requires less memory.</p>

<p>I change every query I see which uses the "comma <code>JOIN</code>" syntax.  In my opinion, the only purpose for its existence is conciseness.  Considering the performance impact, I don't think this is a compelling reason.</p>

### Answer ID: 129134
<p>It also depends on whether you are just doing inner joins this way or outer joins as well.  For instance, the MS SQL Server syntax for outer joins in the WHERE clause (=* and *=) can give different results than the OUTER JOIN syntax and is no longer supported (<a href="http://msdn.microsoft.com/en-us/library/ms178653(SQL.90).aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/ms178653(SQL.90).aspx</a>) in SQL Server 2005.</p>

### Answer ID: 129076
<p>In SQL Server there are always query plans to check, a text output can be made as follows:</p>

<pre><code>SET SHOWPLAN_ALL ON
GO

DECLARE @TABLE_A TABLE
(
    ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Data VARCHAR(10) NOT NULL
)
INSERT INTO @TABLE_A
SELECT 'ABC' UNION 
SELECT 'DEF' UNION
SELECT 'GHI' UNION
SELECT 'JKL' 

DECLARE @TABLE_B TABLE
(
    ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    Data VARCHAR(10) NOT NULL
)
INSERT INTO @TABLE_B
SELECT 'ABC' UNION 
SELECT 'DEF' UNION
SELECT 'GHI' UNION
SELECT 'JKL' 

SELECT A.Data, B.Data
FROM
    @TABLE_A AS A, @TABLE_B AS B
WHERE
    A.ID = B.ID

SELECT A.Data, B.Data
FROM
    @TABLE_A AS A
    INNER JOIN @TABLE_B AS B ON A.ID = B.ID
</code></pre>

<p>Now I'll omit the plan for the table variable creates, the plan for both queries is identical though:</p>

<pre><code> SELECT A.Data, B.Data  FROM   @TABLE_A AS A, @TABLE_B AS B  WHERE   A.ID = B.ID
  |--Nested Loops(Inner Join, OUTER REFERENCES:([A].[ID]))
       |--Clustered Index Scan(OBJECT:(@TABLE_A AS [A]))
       |--Clustered Index Seek(OBJECT:(@TABLE_B AS [B]), SEEK:([B].[ID]=@TABLE_A.[ID] as [A].[ID]) ORDERED FORWARD)
 SELECT A.Data, B.Data  FROM   @TABLE_A AS A   INNER JOIN @TABLE_B AS B ON A.ID = B.ID
  |--Nested Loops(Inner Join, OUTER REFERENCES:([A].[ID]))
       |--Clustered Index Scan(OBJECT:(@TABLE_A AS [A]))
       |--Clustered Index Seek(OBJECT:(@TABLE_B AS [B]), SEEK:([B].[ID]=@TABLE_A.[ID] as [A].[ID]) ORDERED FORWARD)
</code></pre>

<p>So, short answer - No need to rewrite, unless you spend a long time trying to read them each time you maintain them?</p>

### Answer ID: 128995
<p>Nothing is wrong with the syntax in your example.  The 'INNER JOIN' syntax is generally termed 'ANSI' syntax, and came after the style illustrated in your example.  It exists to clarify the type/direction/constituents of the join, but is not generally functionally different than what you have.</p>

<p>Support for 'ANSI' joins is per-database platform, but it's more or less universal these days.</p>

<p>As a side note, one addition with the 'ANSI' syntax was the 'FULL OUTER JOIN' or 'FULL JOIN'.</p>

<p>Hope this helps.</p>

### Answer ID: 129006
<p>The more verbose <code>INNER JOIN, LEFT OUTER JOIN, RIGHT OUTER JOIN, FULL OUTER JOIN</code> are from the ANSI SQL/92 syntax for joining.  For me, this verbosity makes the join more clear to the developer/DBA of what the intent is with the join.</p>

### Answer ID: 129005
<p>It's more of a syntax choice.  I prefer grouping my join conditions with my joins, hence I use the INNER JOIN syntax</p>

<pre><code>SELECT a.someRow, b.someRow
FROM tableA AS a
INNER JOIN tableB AS b
  ON a.ID = b.ID
WHERE b.ID = ?
</code></pre>

<p>(? being a placeholder)</p>

### Answer ID: 129000
<p>I avoid implicit joins; when the query is really large, they make the code hard to decipher</p>

<p>With explicit joins, and good formatting, the code is more readable and understandable without need for comments.</p>

