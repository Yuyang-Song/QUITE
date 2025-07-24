# How to manipulate collection without hitting the database?
[Link to question](https://stackoverflow.com/questions/26344146/how-to-manipulate-collection-without-hitting-the-database)
**Creation Date:** 1413215915
**Score:** 0
**Tags:** ruby-on-rails, ruby, activerecord
## Question Body
<p>In my Rails application I have this little helper method that takes a collection as a parameter:</p>

<pre><code>def calculate_column_width(collection)
  if collection.where(:sample =&gt; true).present?
    "10%"
  else
    "20%"
  end
end
</code></pre>

<p>It works but I don't like the fact that it creates two additional database queries.</p>

<p>How can I rewrite the function so it runs on the collection (e.g. <code>@people</code>) which has already been loaded into memory by Rails?</p>

<p>Thanks for any help.</p>

## Answers
### Answer ID: 26344337
<p>You'd be best served by not using an ActiveRecord method and instead treating the collection like an array. To your example above:</p>

<pre><code>def calculate_column_width(collection)
  if collection.find { |object| object.sample == true }
    "10%"
  else
    "20%"
  end
end
</code></pre>

<p>Note that this <code>find</code> method is the one that exists on ruby arrays and will just return the first thing that matches the condition. It should avoid doing additional database queries.</p>

