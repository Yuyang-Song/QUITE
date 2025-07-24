# Undoing a CTE (Common Table Expression)
[Link to question](https://stackoverflow.com/questions/50937740/undoing-a-cte-common-table-expression)
**Creation Date:** 1529447166
**Score:** 0
**Tags:** mysql, mariadb, common-table-expression
## Question Body
<p>Another developer wrote a query against this for a MariaDB (MySQL Version 10.x) and not the MySQL database is should have been written for (MySQL Version 5.6). They are no longer available to have them rewrite it for MySQL 5.6.</p>

<p>Can someone assist with reverse engineering this thing?</p>

<pre><code>WITH temptable (column1, column2, column3) 
     AS (SELECT t3.column1, 
                t3.column2, 
                CASE 
                  WHEN t3.column3 = 1 
                       AND t2.column3 = 1 THEN 2 
                  ELSE COALESCE(t2.column3, 0) 
                END AS column3 
         FROM   table1 t1 
                JOIN table2 t2 
                  ON t1.column5 = t2.column5 
                     AND t1.column6 = t2.column6 
                JOIN table3 t3 
                  ON t3.column1 = t2.column1 
         WHERE  t1.column4 = :var1 
                AND t1.column6 = :var2 
                AND t3.column7 = 0)
SELECT column2, 
       column3 
FROM   temptable 
UNION 
SELECT t3.column2, 
       t3.column3 
FROM   table3 t3 
WHERE  t3.column7 = -1 
UNION 
SELECT t3.column2, 
       0 AS column3 
FROM   table3 t3 
       LEFT JOIN temptable temp 
              ON temp.column2 = t3.column2 
WHERE  temp.action IS NULL 
       AND t3.column7 = 0;
</code></pre>

<p><em>The tables and columns have been changed to protect the innocent.</em> </p>

## Answers
### Answer ID: 50938011
<p>The "easy button" fix is to take the definition of the CTE and use it as an inline view, in place of references to <code>temptable</code> in the outer query. (This isn't necessarily the best fix, or the best way to write the query.)</p>

<hr>

<p>Chop out the beginning of the query, this part, </p>

<pre><code>WITH temptable 
( column1
, column2
, column3
) 
AS
( SELECT t3.column1
       , t3.column2
       , CASE
           WHEN t3.column3 = 1 AND t2.column3 = 1 THEN 2
           ELSE COALESCE(t2.column3, 0)
         END AS column3 
    FROM table1 t1
    JOIN table2 t2
      ON t1.column5   = t2.column5
     AND t1.column6   = t2.column6
    JOIN table3 t3
      ON t3.column1   = t2.column1
   WHERE t1.column4   = :var1
     AND t1.column6   = :var2 
     AND t3.column7   = 0
)
</code></pre>

<p>leaving just this:</p>

<pre><code>SELECT a.column2
     , a.column3 
  FROM temptable a

 UNION 

SELECT b.column2
     , b.column3 
  FROM table3 b
 WHERE b.column7 = -1

 UNION 

SELECT p.column2
     , 0 AS column3
  FROM table3 p
  LEFT
  JOIN temptable q
    ON q.column2 = p.column2
 WHERE q.action IS NULL
   AND p.column7 = 0
</code></pre>

<p>(As noted in a comment on the question, the reference to <code>action</code> is invalid, because there's no column named <code>action</code> from <code>temptable</code>.)</p>

<p>Then replace the references to the CTE <code>temptable</code> with the inline view definition.</p>

<p>In the query, this would be aliaas <code>a</code> and <code>q</code>.</p>

<p>Like this:</p>

<pre><code>SELECT a.column2
     , a.column3 
  FROM -- temptable
       ( 
         SELECT t3.column1
              , t3.column2
              , CASE
                  WHEN t3.column3 = 1 AND t2.column3 = 1 THEN 2
                  ELSE COALESCE(t2.column3, 0)
                END AS column3 
           FROM table1 t1
           JOIN table2 t2
             ON t1.column5   = t2.column5
            AND t1.column6   = t2.column6
           JOIN table3 t3
             ON t3.column1   = t2.column1
          WHERE t1.column4   = :var1
            AND t1.column6   = :var2 
            AND t3.column7   = 0
       ) a

 UNION

SELECT b.column2
     , b.column3 
  FROM table3 b
 WHERE b.column7 = -1

 UNION 

SELECT p.column2
     , 0 AS column3
  FROM table3 p
  LEFT
  JOIN -- temptable 
       (
         SELECT t3.column1
              , t3.column2
              , CASE
                  WHEN t3.column3 = 1 AND t2.column3 = 1 THEN 2
                  ELSE COALESCE(t2.column3, 0)
                END AS column3 
           FROM table1 t1
           JOIN table2 t2
             ON t1.column5   = t2.column5
            AND t1.column6   = t2.column6
           JOIN table3 t3
             ON t3.column1   = t2.column1
          WHERE t1.column4   = :var1
            AND t1.column6   = :var2 
            AND t3.column7   = 0
       ) q
    ON q.column2 = p.column2
 WHERE q.action IS NULL
   AND p.column7 = 0
</code></pre>

<p><strong>EDIT</strong></p>

<p>Oh, also... the references to <code>:var1</code> and <code>:var2</code> placeholders in the second occurrence of the inline view definition will probably need to be changed to be unique ... <code>:var1b</code> and <code>:var2b</code>  (at least, this is the case with named placeholders using PDO, they have to be unique)</p>

<p>Copies of the values provided for for <code>:var1</code> and <code>:var2</code> will need to be provided for the new bind placeholders.</p>

<p><strong>FOLLOWUP</strong></p>

<p>Q: This query is ... hit a lot. You mention an "easy fix" but at what expense?</p>

<p>A: In the "easy button" fix, the two inline views <code>a</code> and <code>q</code> (replacement for references to the CTE) are being materialized separately. The inline view query is executed two times, and results are materialized into two separate derived tables. (The EXPLAIN output will show two separate derived tables, <code>a</code> and <code>q</code>).</p>

