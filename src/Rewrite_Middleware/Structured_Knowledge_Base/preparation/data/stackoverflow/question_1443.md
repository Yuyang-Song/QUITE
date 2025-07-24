# MSSQL replace full condition of WHERE clause with a CASE
[Link to question](https://stackoverflow.com/questions/7661958/mssql-replace-full-condition-of-where-clause-with-a-case)
**Creation Date:** 1317821075
**Score:** 1
**Tags:** mysql, sql-server, sql-server-2008, postgresql
## Question Body
<p>I need to replace a where clause in a subquery with a clause that depend on the value of the master query.
I have to replace the full condition, not only the right side of the condition, so i have created a query like the one below : </p>

<pre><code>SELECT p.par_des AS description,
COALESCE(
(SELECT SUM(ope_tot) FROM operator WHERE 
</code></pre>

<p><strong><code>(CASE WHEN p.par_cod = 'TEN01' THEN ope_cau = 'TEN01' OR ope_cau LIKE 'BAN__' ELSE ope_cau = p.par_cod END)</code></strong></p>

<pre><code>AND (ope_tim BETWEEN '00:00:00' AND '23:59:59' ) )
,0)  AS value 
FROM parameters p WHERE par_cod LIKE 'TEN__';
</code></pre>

<p>As you can see in the bold part of the query i replace a condition of the where clause based on the value of the field in the master query, and i have to specify also an or operator if the condition is satisfied .</p>

<p>This query work well on PostgreSQL and MySQL, but it doesn't work in MSSQL, how can rewrite the query and let it work also in Microsoft SQL ?</p>

<p>The best would be that the same query can run without any changes in all these three database server : MySQL, PostgreSQL, MSSQL.</p>

## Answers
### Answer ID: 7662237
<p>SQL Server doesn't allow boolean expressions as you are trying here. </p>

<pre><code>   CASE
     WHEN p.par_cod = 'TEN01' THEN ope_cau = 'TEN01'
                                    OR ope_cau LIKE 'BAN__'
     ELSE ope_cau = p.par_cod
   END  
</code></pre>

<p>The following should work in all three.</p>

<pre><code> CASE
         WHEN p.par_cod = 'TEN01' THEN CASE
                                         WHEN ope_cau = 'TEN01'
                                               OR ope_cau LIKE 'BAN__' THEN 1
                                       END
         ELSE CASE
                WHEN ope_cau = p.par_cod THEN 1
              END
       END = 1  
</code></pre>

<p>Note that <code>CASE</code> expressions in <code>WHERE</code> clauses are completely unsargable</p>

