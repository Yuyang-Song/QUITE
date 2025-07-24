# How to rewrite this SQL query using Rails 3 finders method?
[Link to question](https://stackoverflow.com/questions/12271839/how-to-rewrite-this-sql-query-using-rails-3-finders-method)
**Creation Date:** 1346795454
**Score:** 0
**Tags:** sql, ruby-on-rails, activerecord
## Question Body
<p>I want rewrite this SQL query :</p>

<pre><code>SELECT p.id, p.name, p.gender, (p.work_done/p.work_total * 100) r1, (p.work_success/p.work_total * 100) r2, p.StartTime, p.EndTime 
FROM Persons p 
WHERE p.id= params[:id] 
AND p.gender = params[:gender]
ORDER BY r1 desc
GROUP BY p.gender
</code></pre>

<p>Using latest rails 3 finder method (e.g. <code>where, select, group, order</code>....)</p>

<p>I tried this but it doesn't work:</p>

<pre><code>@list = Persons.select("id, name, gender, (work_done/work_total * 100) r1, (work_success/work_total * 100) r2, StartTime, EndTime").where("id = ? AND gender = ?", params[:id],  params[:gender]).order("r1 desc").group("name")
</code></pre>

<p>Any idea where I do it wrong?</p>

<p>EDIT:
Previously I used this :</p>

<pre><code>@list = Persons.find_by_sql("same sql code above").group_by {|t| t.name}
</code></pre>

<p>in my view:</p>

<pre><code>&lt;% @list.each do |person, person_list| %&gt;
</code></pre>

<p>....</p>

<p>And it worked, but I when I try to use the finder method it says:</p>

<pre><code>(undefined method `each' for nil:NilClass)
</code></pre>

<p>and give me this error when querying the database:</p>

<pre><code>Completed 500 Internal Server Error in 280ms
</code></pre>

## Answers
### Answer ID: 12271952
<p>Does this work?</p>

<pre><code>@list = Persons.select("id, name, gender, (work_done/work_total * 100) r1, (work_success/work_total * 100) r2, StartTime, EndTime").where("testrun_id = ? AND gender = ?", params[:id],  params[:gender]).order("r1 desc").group("gender")
</code></pre>

