# Rewriting a method to be unit-testable
[Link to question](https://stackoverflow.com/questions/19846690/rewriting-a-method-to-be-unit-testable)
**Creation Date:** 1383858331
**Score:** 0
**Tags:** ruby-on-rails, performance, unit-testing, activerecord, ruby-on-rails-4
## Question Body
<p>I find that I often like to write methods that just query database and return the results. This is really helpful with complex filters or query 'chaining'. For example, here is a model <code>Clazz</code> that represents an academic class of students. <code>Clazz</code> has many <code>Enrollment</code>s. So I wrote this method to keep my code DRY, since I used this criteria a lot.</p>

<pre><code>class Clazz
    def cash_enrollments
        enrollments.where(payment_type: 'cash')
    end
end
</code></pre>

<p>As I get more into unit testing, I noticed that this pattern is problematic because it is too tightly coupled with the database. The problem is exacerbated when testing large datasets as the database transactions run. </p>

<p>Is there a "unit test friendly" way to rewrite this code? Is there another common pattern that would be better?</p>

## Answers
### Answer ID: 19846756
<p>You could probably try this <a href="http://blog.codeclimate.com/blog/2012/10/17/7-ways-to-decompose-fat-activerecord-models/" rel="nofollow">http://blog.codeclimate.com/blog/2012/10/17/7-ways-to-decompose-fat-activerecord-models/</a> Extract Query Objects or Service Objects</p>

