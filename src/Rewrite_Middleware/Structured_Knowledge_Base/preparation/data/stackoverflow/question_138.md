# Applying two separate filters on a Rails database query
[Link to question](https://stackoverflow.com/questions/14147301/applying-two-separate-filters-on-a-rails-database-query)
**Creation Date:** 1357247463
**Score:** 0
**Tags:** sql, ruby-on-rails, ruby
## Question Body
<p>I am trying to apply two filters to a database query in Rails 3.  The first filter shows only media of type images.  The second filter shows the highest saluted stories.  On their own the filters work ok, but when I try to combine both filters, I get errors.</p>

<p>There are 3 tables involved.  Stories, memories, and salutes.  The salutes table keeps track of how many times someone 'salutes' a memory.  Each story is composed of multiple memories.  A story's total salutes is the sum of the salutes of that story's memories.  I want to retrieve records of image-only stories in the order of highest to lowest salutes.</p>

<p><strong>models/story.rb</strong></p>

<pre><code>def self.where_contains_image()
  joins(
    'INNER JOIN memories AS wci_memories ON wci_memories.story_id = stories.id'
  )
  .where(
    'wci_memories.media_type_cd = ?', Memory.image
  ).uniq
end
</code></pre>

<p><strong>controllers/stories_controller.rb</strong></p>

<pre><code>if params[:filter_content] == 'image'
  stories = stories.where_contains_image
end

if (params[:filter_trends] == 'most_saluted')
  stories = stories.order("(SELECT COUNT(1) FROM salutes
    LEFT JOIN memories AS ms_memories ON salutes.content_id = ms_memories.id
    LEFT JOIN stories AS ms_stories ON ms_stories.id = ms_memories.story_id
    WHERE ms_stories.id = stories.id AND salutes.content_type = 'Memory')
    DESC");
end
</code></pre>

<p>On its own, when the 'most_saluted' param is set, the query works as expected.  When both the 'most_saluted' param and the 'image' param are set, I get an error:</p>

<pre><code>for SELECT DISTINCT, ORDER BY expressions must appear in select list
</code></pre>

<p>I understand what the error is, but I cannot figure out how to rewrite the queries so that it can return only images in the order of most saluted.</p>

<p>When I run this SQL query on the database, it returns the records I'm looking for.  But I cannot figure out how to make rails return the same records.  Furthermore, this query combines the two filters (only images and highest salutes).  I want to keep them separate so that I can apply one filter individually, or both together.</p>

<pre><code>SELECT DISTINCT stories.*, (SELECT COUNT(1) FROM salutes
    LEFT JOIN memories AS ms_memories ON salutes.content_id = ms_memories.id
    LEFT JOIN stories AS ms_stories ON ms_stories.id = ms_memories.story_id
    WHERE ms_stories.id = stories.id AND salutes.content_type = 'Memory') 
AS total_salutes FROM stories INNER JOIN memories AS wci_memories 
ON wci_memories.story_id = stories.id WHERE wci_memories.media_type_cd = 0
ORDER BY total_salutes DESC
</code></pre>

<p>Any thoughts on how I can resolve this?</p>

## Answers
### Answer ID: 14147957
<p>You can use scope to achieve this, actually the Activerecord scope are the more cleaner/moduler way to chain conditions </p>

<p><a href="http://guides.rubyonrails.org/active_record_querying.html#scopes" rel="nofollow">read here about scopes</a> </p>

<p>HTH</p>

