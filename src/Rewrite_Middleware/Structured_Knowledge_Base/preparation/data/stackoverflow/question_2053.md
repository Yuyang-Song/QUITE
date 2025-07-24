# Rewrite object.count(conditions: [ ]) SQL query
[Link to question](https://stackoverflow.com/questions/17115890/rewrite-object-countconditions-sql-query)
**Creation Date:** 1371238036
**Score:** 0
**Tags:** sql, ruby-on-rails, ruby, ruby-on-rails-3
## Question Body
<p>I have a question and answer model, answers belong to questions and a question has many answers. Answers have a boolean <code>:correct</code> column so answers can be marked as correct. </p>

<p>The code below checks whether a question has any correct answers and then displays a different div accordingly. The code works however it performs a laborious count query on the database which I would like to avoid. </p>

<p>Is there a way to rewrite this query or is it best to have a column in the questions table which is toggled to true when an answer is marked as correct?</p>

<pre><code>&lt;div class="&lt;%= question.answers.count(conditions: ['correct = ?', true]) == 1 ? 'correct-answer' : 'no-correct-answer' %&gt;"&gt;
  &lt;%= question.answers_count %&gt;
&lt;/div&gt;
</code></pre>

<p><strong>EDIT</strong></p>

<p>Thanks to the guys below who posted answers, however even with an questions_id index on the answers table, both queries were using a count query which i want to avoid, as there is likely to be quite a few answers to have to loop through.</p>

<p>My solution was to create a :correct boolean column on the question table, and when  an answer is marked/toggled as correct it toggled this column as well, so when rendering a view i didnt have to perform any dynamic SQL queries.</p>

<p>answer.rb</p>

<pre><code>def toggle_correct(attribute)
    toggle(attribute).update_attributes({attribute =&gt; self[attribute]})
  end

def toggle_question_correct
    self.question.toggle_correct(:correct)
end
</code></pre>

## Answers
### Answer ID: 17116211
<p>You're counting how many correct answers there is for the question (i.e. check every answer), whereas you only need to check if a correct answer exists (i.e. stop as soon as the correct answer is spotted). This could be written with <a href="http://guides.rubyonrails.org/association_basics.html#has_many-association-reference" rel="nofollow"><code>exists?</code></a></p>

<pre><code>question.answers.exists?(:correct =&gt; true)
</code></pre>

<p>Unless you have a lot of answers for each question, it should not change significantly the response time. You said this part of code was 'laborious', you should check that you created an index on the column <code>question_id</code> of the table <code>answers</code>. Without it, <code>question.answers</code> generate a full scan of the <code>answers</code> table.</p>

### Answer ID: 17116094
<p>I would suggest that you create two scopes on Answer model</p>

<pre><code>scope :correct, -&gt; { where(correct: true) }
scope :correct, -&gt; { where(correct: false) }
</code></pre>

<p>then you may select count correnct answers for question like that:</p>

<pre><code>question.answers.correct.count
</code></pre>

<p>You might also want to create a method on Question</p>

<pre><code>def has_correct_answer?
    ! answers.correct.count.zero?
end
</code></pre>

<p>If you're showing many questions and answers on single page I would suggest going for AR#includes with where clause so it will make less SQL queries (<a href="http://guides.rubyonrails.org/active_record_querying.html#eager-loading-multiple-associations" rel="nofollow">http://guides.rubyonrails.org/active_record_querying.html#eager-loading-multiple-associations</a>)</p>

