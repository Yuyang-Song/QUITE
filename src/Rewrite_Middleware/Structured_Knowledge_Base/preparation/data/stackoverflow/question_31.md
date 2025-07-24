# Querying multiple models for similar data in CakePHP (union?)
[Link to question](https://stackoverflow.com/questions/10546824/querying-multiple-models-for-similar-data-in-cakephp-union)
**Creation Date:** 1336719415
**Score:** 3
**Tags:** sql, cakephp, model, cakephp-2.0
## Question Body
<p>So I have the following example tables:</p>

<pre><code>Table A:
id
name
type
hat_size
created

Table B:
id
name
type
favorite_food
created

Table C:
id
name
type
some_other_thing
created
</code></pre>

<p>Let's say that I want to create a search with results from models <code>A</code>, <code>B</code>, and <code>C</code> using <code>id</code>, <code>name</code>, <code>type</code>, and <code>created</code>.</p>

<p>My goal would be to search all three tables, ordered by one of the fields (let's use <code>created</code> as the <code>ORDER_BY</code> field), and limited to say, 20 results.</p>

<p>Normally I would simply do a Union of these, order by the field, and <code>LIMIT</code> the result.</p>

<p>Now, I know I can just create a raw query to do this... but that means that I have to rewrite the paginate methods, always sanitize, etc.  Plus it's clunky and not necessarily portable across multiple SQL databases.  I'd prefer to do this a more MVC friendly way, using the models themselves, if possible.</p>

<p>What's the best way I can approach this with CakePHP?</p>

<p>Thank you,
James</p>

## Answers
### Answer ID: 10610483
<p>One option is to create a <code>VIEW</code> which holds the <code>UNION</code> query.  And then perform your Cake query on the view.  </p>

<p>I'm starting to avoid views recently, however, because of the difficulty in transferring them between servers (and the annoying <code>DEFINER</code> command that is usually included in exports).</p>

