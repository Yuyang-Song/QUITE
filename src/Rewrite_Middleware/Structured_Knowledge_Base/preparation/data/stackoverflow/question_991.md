# Querying the same table in the where clause
[Link to question](https://stackoverflow.com/questions/53665474/querying-the-same-table-in-the-where-clause)
**Creation Date:** 1544169831
**Score:** 0
**Tags:** sql, case, where-clause, teradata-sql-assistant
## Question Body
<pre><code>SELECT

M.Id_x as Id 
max(case when SA.TYP = 'CHRG' then    SA.AMT end)  CHRG,

max(case when SA.TYP = 'NTCV' then SA.AMT end) NC,

max(case when SA.TYP = 'COV' then SA.SRC end) COV

FROM database.tableA M
LEFT OUTER JOIN  
database.tableB SA

On
(SA.Id_x = M.id_x
AND SA.date = m.date
AND SA.SRC=M.SRC)

Where M.date &gt;= '2018-01-01'
And m.src = 'ox'
And sa.type IN ('CHRG', 'NTCV', 'COV')

Group by 
M.id_x 
M.date
</code></pre>

<hr>

<p>Known
NTCV/COV can = '?' Or numeric value</p>

<p>Background 
 The reason I use a max case when argument is to work how the database associates each Id with a type and each type may or may not have a numeric value. I dont want the data to have so many rows as there are other tables joined. For simplicity I'm only showing these 2. Further more the max case when argument allows the data to result as a row versus multiple rows. </p>

<p>Issue
At times I might need to query for multiple scenarios where the NTVC = COV but I am unsure as to how to that in the where clause. If I try to write it as such it gives me an error. If I try to call the same table 3 times then it uses to much CPU and spools. </p>

<p>I am interested how you would rewrite this query in order to accomplish </p>

<p>Where ntvc = cov for expected results of sometimes 1m rows</p>

<p>Technology used: teradata sql assistant </p>

## Answers
### Answer ID: 53669133
<p>I am guessing that you want a <code>HAVING</code> clause, not a <code>WHERE</code> clause, with:</p>

<pre><code>having (max(case when SA.TYP = 'NTCV' then SA.AMT end) = 
        max(case when SA.TYP = 'COV' then SA.SRC end) 
       )
</code></pre>

