# replace sql query for hql
[Link to question](https://stackoverflow.com/questions/18146772/replace-sql-query-for-hql)
**Creation Date:** 1376051598
**Score:** 0
**Tags:** java, sql, hibernate, hql
## Question Body
<p>Tnis query must be return List!!!!
I want to know how to rewrite this SQL query for HQL:</p>

<pre><code>select candidate.* from candidate inner join candidate_skill on candidate.id = candidate_skill.candidate_id inner join skill on candidate_skill.skill_id = skill.id
where skill.id = 1
</code></pre>

<p>I want to get a candidate object (instead of <code>candidate.*</code>), and I want to replace <code>skill.id = 1</code> with a skill object.</p>

## Answers
### Answer ID: 18146935
<p>Doesn't this work?</p>

<pre><code>from Candidate as candidate
  left outer join candidate.skills as skill
    where skill.id = 1
</code></pre>

