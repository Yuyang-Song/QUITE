# Self-referencing updates in HQL
[Link to question](https://stackoverflow.com/questions/433268/self-referencing-updates-in-hql)
**Creation Date:** 1231695249
**Score:** 2
**Tags:** mysql, hibernate, hql, mysql-error-1093
## Question Body
<p>I have the following query in HQL:</p>

<pre><code>update ProjectFile pf1 
set pf1.validUntil.id =123
where pf1 = (
select pf from ProjectVersion pv, ProjectFile as pf 
where pf.validFrom.sequence &lt;= pv.sequence 
and pf.validUntil.sequence &gt;= pv.sequence
and pf.state &lt;&gt; 12
and pf.projectVersion.project.id = 1
and pv.project.id = 1
and pv.id = 12
and pf.id not in (2,3,4)
)
</code></pre>

<p>Hibernate parses the query correctly and generates SQL, but the database (MySQL) fails with error: </p>

<blockquote>
  <p>You can't specify target table 'ProjectFile' for update in FROM clause</p>
</blockquote>

<p>The problem seems to be that the table to be updated is queried in the same context. Is there any way to rewrite the HQL query to produce SQL that can be executed in MySQL correctly? The other approach would be to create an intermediate table, which is what exactly I am trying to avoid.</p>

## Answers
### Answer ID: 910760
<p>I bumped into the same problem and posted a question here: <a href="https://stackoverflow.com/questions/839938/mysql-sql-update-with-correlated-subquery-from-the-updated-table-itself">MySQL/SQL: Update with correlated subquery from the updated table itself</a>.</p>

<p>To solve your problem, you need to join at the UPDATE level, please take a look at the answer to my question.</p>

