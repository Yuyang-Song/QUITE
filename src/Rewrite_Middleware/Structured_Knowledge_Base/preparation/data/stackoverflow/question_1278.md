# Find n most referenced records by foreign_key in related table
[Link to question](https://stackoverflow.com/questions/67924664/find-n-most-referenced-records-by-foreign-key-in-related-table)
**Creation Date:** 1623340671
**Score:** 0
**Tags:** ruby-on-rails, postgresql, rails-activerecord
## Question Body
<p>I have a table <code>skills</code> and a table <code>programs_skills</code> which references <code>skill_id</code> as a foreign key, I want to retrieve the 10 most present skills in table <code>programs_skills</code> (I need to count the number of occurrence of <code>skill_id</code> in <code>programs_skills</code> and then order it by descending order).
I wrote this in my <code>skill</code> model:</p>
<pre><code>  def self.most_used(limit)
    Skill.find(
      ActiveRecord::Base.connection.execute(
        'SELECT programs_skills.skill_id, count(*) FROM programs_skills GROUP BY skill_id ORDER BY count DESC'
      ).to_a.first(limit).map { |record| record['skill_id'] }
    )
  end
</code></pre>
<p>This is working but I would like to find a way to perform this query in a more elegant, performant, &quot;activerecord like&quot; way.</p>
<p>Could you help me rewrite this query ?</p>

## Answers
### Answer ID: 67935601
<pre class="lang-rb prettyprint-override"><code>ProgramsSkills.select(&quot;skill_id, COUNT(*) AS nb_skills&quot;)
.group(:skill_id).order(&quot;nb_skills DESC&quot;).limit(limit)
.first(limit).pluck(:skill_id)
</code></pre>

### Answer ID: 67931632
<p>Just replace your query by:</p>
<pre><code>WITH
T AS
(
SELECT skill_id, COUNT(*) AS NB, RANK() OVER(ORDER BY COUNT(*) DESC) AS RNK 
FROM   programs_skills  
GROUP  BY skill_id
)
SELECT wojewodztwo, NB
FROM   T
WHERE  RNK &lt;= 10
</code></pre>
<p>This use CTE and windowed function.</p>

