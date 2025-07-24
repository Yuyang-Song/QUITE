# Insert Only: ActiveRecord or Queries?
[Link to question](https://stackoverflow.com/questions/3078974/insert-only-activerecord-or-queries)
**Creation Date:** 1277031350
**Score:** 1
**Tags:** sql, ruby, activerecord, insert
## Question Body
<p>All that I will do is insert records into the database.
However, I would definitly like the database-independence that Ruby/ActiveRecord can offer me.</p>

<p>What would be the reccommended choice?</p>

<ol>
<li>Using simple insert queries, and rewriting them, and also maintaining my own database class for things as batch insertions;</li>
<li>Using the power of ActiveRecord, but also having the overhead;</li>
<li>Some other solution, mayhaps?</li>
</ol>

<p>For the record, optimistically speaking I'll be doing an insertion per second/couple of seconds.
I'll also (<em>probably</em>) be using ActiveRecord for reading from the database later on - but, in a different application.</p>

## Answers
### Answer ID: 3079017
<p>The main reason for writing your own queries would be to optimize performance if Active Record would prove too inefficient.  But since one insert per second isn't really that much of a load, Active Record's performance will probably be more than enough for your needs.</p>

<p>Thus, I would definitely use Active Record in this situation -- there's no need to bother with your own database wrapper unless you really need to.  Also, an extra bonus is that you can reuse the model definitions for reading data later on.</p>

