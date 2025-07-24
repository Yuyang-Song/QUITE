# How do I extract a field from an array of my models in order to form a single query?
[Link to question](https://stackoverflow.com/questions/39960582/how-do-i-extract-a-field-from-an-array-of-my-models-in-order-to-form-a-single-qu)
**Creation Date:** 1476109578
**Score:** 0
**Tags:** ruby-on-rails, arrays, ruby, postgresql, model
## Question Body
<p>I’m using Rails 4.2.7.  I have an array of my model objects and currently I’m iterating through that array to find matching entries in the database based on a field my each object …</p>

<pre><code>    my_object_times.each_with_index do |my_object_time, index|
      found_my_object_time = MyObjectTime.find_by_my_object_id_and_overall_rank(my_object_id, my_object_time.overall_rank)
</code></pre>

<p>My question is, how can I rewrite the above to run one query instead of N queries, if N is the size of the array.  What I wanted was to force my underlying database (PostGres 9.5) to do a “IF VALUE IN (…)” type of query but I’m not sure how to extract all the attributes from my array and then pass them in appropriately to a query.</p>

## Answers
### Answer ID: 39960756
<p>I would do something like this:</p>

<pre><code>found_my_object_times = MyObjectTime.where(
  object_id: my_object_id, 
  overall_rank: my_object_times.map(&amp;:overall_rank)
)
</code></pre>

