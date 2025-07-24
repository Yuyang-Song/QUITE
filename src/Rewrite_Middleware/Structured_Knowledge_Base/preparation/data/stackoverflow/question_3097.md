# ORA-1427 in inline view
[Link to question](https://stackoverflow.com/questions/66279101/ora-1427-in-inline-view)
**Creation Date:** 1613743617
**Score:** 0
**Tags:** oracle-database, ora-01427
## Question Body
<p>We have a query that fails in our Prod environment that fails with ora-01427 single-row subquery returns more rows.
This is oracle 11g database. Query as below. This query runs fine till we add the final left outer join with SQ3, once added it fails with ORA-1427 after some time.</p>
<pre><code>select c1,c2..c8 from
t1 left join
(subquery with joins)SQ1
left join
(subquery with joins)SQ2
left join
(subquery with joins)SQ4
left join
(subquery with joins)SQ5
left join
(SELECT DISTINCT MAX(c1) c1, c2, c3, c4, c5,c6 
     FROM s1.t1 WHERE  c2='NY' AND c7&lt;'2' AND c8='Y' 
GROUP BY c1, c2, c3, c4, c5,c6) SQ3 ON sq3.c3=t1.c3
                                                 AND sq3.c8=t1.c8
                                                  AND sq3.c7=t2.c6
                                                  AND sq3.c6 &lt;'2'
                                                AND sq3.c4='Y' 
</code></pre>
<p>When i rewrite this query using WITH clause then it runs fine, see below. Any idea on why the first query fails when the second one below executes with no change to logic.</p>
<pre><code>with
(SELECT DISTINCT MAX(c1) c1, c2, c3, c4, c5,c6 
     FROM s1.t1 WHERE  c2='NY' AND c7&lt;'2' AND c8='Y' 
GROUP BY c1, c2, c3, c4, c5,c6) as SQ3
select c1,c2..c8 from
t1 left join
(subquery with joins)SQ1
left join
(subquery with joins)SQ2
left join
(subquery with joins)SQ4
left join
(subquery with joins)SQ5
left join
 SQ3 ON sq3.c3=t1.c3
 AND sq3.c8=t1.c8
 AND sq3.c7=t2.c6
 AND sq3.c6 &lt;'2'
 AND sq3.c4='Y' 
</code></pre>

## Answers
### Answer ID: 66285869
<p>You don't need to group by the column you are using with your aggregate function. So change your last query to -</p>
<pre><code>SELECT MAX(c1) c1, c2, c3, c4, c5,c6 
  FROM s1.t1
 WHERE c2 = 'NY'
   AND c7 &lt; '2'
   AND c8 = 'Y' 
 GROUP BY c2, c3, c4, c5,c6
</code></pre>

### Answer ID: 66279278
<p>Mira a ver esto de agrupar por la columna del agregado, no parece correcto
(SELECT DISTINCT <strong>MAX(c1) c1</strong>, c2, c3, c4, c5,c6
FROM s1.t1 WHERE  c2='NY' AND c7&lt;'2' AND c8='Y'
**</p>
<p>GROUP BY <strong>c1</strong></p>
<p>**</p>

