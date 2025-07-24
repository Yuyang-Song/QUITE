# An `ORDER BY` clause is added even though uninstructed
[Link to question](https://stackoverflow.com/questions/54740794/an-order-by-clause-is-added-even-though-uninstructed)
**Creation Date:** 1550466615
**Score:** 0
**Tags:** sql, ruby-on-rails, postgresql, activerecord
## Question Body
<p>I am trying to process records in my database like so:</p>

<pre><code>rows = MyModel.joins("JOIN other_model ON other_model.my_model_id = my_model.id")
                      .joins("JOIN &lt;some other join&gt;")
                      .where("&lt;conditions&gt;")
rows.find_each(batch_size: 50, &amp;:destroy)
</code></pre>

<p>I am not specifying any row order, so I expect that there won't be any <code>ORDER BY</code> clause in the final SQL. However, when I run this code, <code>ActiveRecord</code> adds an <code>ORDER BY</code> clause; the query actually looks like this:</p>

<pre><code>... WHERE &lt;conditions&gt; ORDER BY "my_model"."id" ASC LIMIT 50;
</code></pre>

<p>This is a problem as I have many records in the table, and <code>ORDER BY</code> clause slows everything down.</p>

<p>I could probably rewrite my code so as to not use <code>ActiveRecord</code> to select the ids, but I'm wondering why <code>ActiveRecord</code> behaves like this. Why does it add an <code>ORDER By</code> when I'm not asking it to? Is there any way to prevent this?</p>

