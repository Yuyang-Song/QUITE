# SQL Outer Join on multiple summed columns in same table
[Link to question](https://stackoverflow.com/questions/8835567/sql-outer-join-on-multiple-summed-columns-in-same-table)
**Creation Date:** 1326373640
**Score:** 1
**Tags:** sql, join, self, outer-join
## Question Body
<p>I am working with a SQL Library (Programming library, ANSI SQL Compliant, called ABS Database,(http://www.componentace.com/help/absdb_manual/absdbmanual_content.htm). It supports the various joins, CASE, etc...</p>

<p>I have a single table (appt), which is a table of appointments.</p>

<pre><code>ApptKey - Integer - Primary Key
SA_ID -  Integer  (a person’s ID, think employee number),
Layer - Integer – only 4 different values, 1, 2, 3 or 4 (think Appt Category)
Number_Of_Minutes  - Integer – the length of the appointment
</code></pre>

<p>Note that some SA_ID/Layer combinations may be empty (i.e. no rows for that combination).  Other SA_ID/Layer combinations may have multiple rows (I am not showing other columns as they are not relevant here). I need a report to show the sum of minutes, for each person (SA_ID), for each layer, in one row… i.e. each SA_ID has their own row, showing the sum for Layer =1, the sum for layer =2 , the sum for Layer =3, and the sum for layer = 4.</p>

<p>Example data…</p>

<pre><code>SA_ID         LAYER        Number_of_Minutes
1             1            10
1             1            30
2             1            10
3             2            10
1             4            10
</code></pre>

<p>I need a query that gives this result.</p>

<pre><code>SA_ID      LAYER_1     LAYER_2    LAYER_3     LAYER_4
1          40          0          0           10
2          10          0          0           0
3          0           10         0           0
</code></pre>

<p>I need this type of format, because this query feeds a Chart/graph component…</p>

<p>I think I need to use a right join a multiple correlated subqueries, but I just can’t get it to work. Is this the right approach. What I have below runs, but as a straight join.  Can I (or how do I) rewrite this to use a right outer join? Is a right outer join the best approach?</p>

<pre><code>select g.sa_id,  l1.totalsum, l2.totalsum, l3.totalsum, l4.totalsum
from  (select sa_id, layer, sum(number_of_minutes) totalsum from appt where layer = 1 group by sa_id, layer) l1,
           (select sa_id, layer, sum(number_of_minutes) totalsum from appt where layer = 2 group by sa_id, layer) l2,
           (select sa_id, layer, sum(number_of_minutes) totalsum from appt where layer = 3 group by sa_id, layer) l3,
          (select sa_id, layer, sum(number_of_minutes) totalsum from appt where layer = 4 group by sa_id, layer) l4,
          (select distinct sa_id "sa_id" from appt) g
where
      (l1.sa_id = g.sa_id)
and   (l2.sa_id = g.sa_id)
and   (l3.sa_id = g.sa_id)
and   (l4.sa_id = g.sa_id)
</code></pre>

## Answers
### Answer ID: 8835656
<pre><code>SELECT
    t.sa_id,
    Layer1=(SELECT SUM(Number_of_Minutes) FROM appt WHERE sa_id = t.sa_id AND Layer = 1),
    Layer2=(SELECT SUM(Number_of_Minutes) FROM appt WHERE sa_id = t.sa_id AND Layer = 2),
    Layer3=(SELECT SUM(Number_of_Minutes) FROM appt WHERE sa_id = t.sa_id AND Layer = 3),
    Layer4=(SELECT SUM(Number_of_Minutes) FROM appt WHERE sa_id = t.sa_id AND Layer = 4)

FROM
(
    SELECT DISTINCT
        sa_id
    FROM appt
) t
</code></pre>

### Answer ID: 8835651
<pre><code>SELECT SA_ID,
SUM(CASE WHEN LAYER = 1 THEN Number_of_Minutes ELSE 0 END) AS LAYER_1, 
SUM(CASE WHEN LAYER = 2 THEN Number_of_Minutes ELSE 0 END) AS LAYER_2,
SUM(CASE WHEN LAYER = 3 THEN Number_of_Minutes ELSE 0 END) AS LAYER_3,
SUM(CASE WHEN LAYER = 4 THEN Number_of_Minutes ELSE 0 END) AS LAYER_4
FROM Appt
GROUP BY SA_ID
</code></pre>

<p>EDIT: Because it supports <a href="http://www.componentace.com/help/absdb_manual/conditionalexpressions.htm" rel="nofollow"><code>CASE</code></a> expressions.</p>

