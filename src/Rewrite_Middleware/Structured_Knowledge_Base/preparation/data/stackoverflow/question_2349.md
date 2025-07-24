# Run a rails query in batches
[Link to question](https://stackoverflow.com/questions/30439204/run-a-rails-query-in-batches)
**Creation Date:** 1432559431
**Score:** 19
**Tags:** ruby-on-rails, postgresql, performance, ruby-on-rails-3, database-cursor
## Question Body
<p>I have a table <code>A(:name, :address, :phone)</code> consisting of 500,000 entries. I want to run this query :</p>

<pre><code>johns = A.where(:name =&gt; "John")
</code></pre>

<p>This query should return 150,000 results. But running this query gives me this result : <code>Killed</code>.</p>

<p>How should I rewrite this query so that the query runs on batches of 1000 in the database?</p>

## Answers
### Answer ID: 65028519
<h2><code>.in_batches</code></h2>
<p>The issue with <code>find_each</code> or <code>find_in_batches</code> is that you have consumed query results.</p>
<p><strong>The cleanest solution is using <code>in_batches</code>, because it yield the actual query (without consuming it):</strong></p>
<pre class="lang-rb prettyprint-override"><code>User.find_in_batches do |users|
  users.select(:id) # error
end

User.in_batches do |users|
  users.select(:id)                   # works as expected
  users.pluck(&quot;complext pluck query&quot;) # works as expected
end
</code></pre>

### Answer ID: 30464343
<pre><code> A.where(:name =&gt; "John").find_each(batch_size: 1000) do |a|
    # your code
 end
</code></pre>

### Answer ID: 30439970
<p>An alternative to using <code>find_each</code> is to use <code>find_in_batches</code>.</p>

<p>There's a distinct difference - <code>find_each</code> will give your block each item and will loop through your batch item by item. <code>find_in_batches</code> will deliver your batch of items in an array to your block.</p>

<p>I've assumed your <code>A</code> model is actually called <code>Address</code>. You could do something like this:</p>

<pre><code>Address.where(name: "John").find_in_batches(batch_size: 1000) do |addresses|

  # Your code that you might want to run BEFORE processing each batch ...

  addresses.each do |address|
    # Your code that you want to run for each address
  end

  # Your code that you might want to run AFTER processing each batch ...

end
</code></pre>

<p>As you can see, this gives you a little more flexibility around how you handle the processing of your batches. However, if your needs are simple, just stick with <code>find_each</code>.</p>

### Answer ID: 30439275
<p>You need to use <a href="http://apidock.com/rails/ActiveRecord/Batches/find_each" rel="noreferrer"><code>find_each</code></a> with the option <em>batch_size</em>.</p>

<pre><code>A.where(:name =&gt; "John").find_each(batch_size: 1000) do |a|
  # your code
end
</code></pre>

