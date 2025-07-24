# Searching by Date.parse(string) incredibly slow?
[Link to question](https://stackoverflow.com/questions/7682755/searching-by-date-parsestring-incredibly-slow)
**Creation Date:** 1317958008
**Score:** 2
**Tags:** ruby-on-rails, ruby, ruby-on-rails-3
## Question Body
<p>I've used <a href="http://railscasts.com/episodes/240-search-sort-paginate-with-ajax" rel="nofollow">Ryan Bate's search with Ajax episode</a> to write some basic search functionality.</p>

<p>What it basically does is take a string from a form, and performs a like query via a model method. What I'm trying to do is conditionally search to different columns(due_date and name) in the database with a single string that I parse with the Date class. That way a user can search for items by a date, or the item name witht he same form. My method looks like:</p>

<pre><code>def self.search(search) 
    if search
      search_date = Date.parse(search) rescue nil
    end

    if search_date
      where('due_date = ?', search_date)
    elsif search
      where('UPPER(name) LIKE ?', "%#{search.upcase}%")
    else
      scoped
    end
  end  
</code></pre>

<p>This works, as if the user types in a date, the Date class is able to parse it, an look in the database for any objects that have that due_date. The problem is, if it is a date and it's able to be parse, the search is incredibly slow.</p>

<p>I was wondering if anyone had a way of speeding this up. Is it the Date class that is so slow? Should I have two different methods? or Should I completely rewrite my search?</p>

## Answers
### Answer ID: 7683106
<p>While the previous answers about looking for slow queries and leveraging an index are likely going to get you more bang for you buck, you should also check out Ryan Evan's C implementation of Date/DateTime, the <a href="https://github.com/jeremyevans/home_run" rel="nofollow">home_run gem</a>.</p>

### Answer ID: 7682786
<p>While date-handling in Ruby is notoriously slow, it would not be noticeable for a single call like this...</p>

<p>It's probably a missing index in your database...</p>

<p>Check what you've defined as indexes for your table in question...  You should be doing a migration with this in it:</p>

<pre><code>add_index :my_table, :due_date
</code></pre>

<p>Then your database will be able to find the records quickly.</p>

### Answer ID: 7682784
<p>I really doubt it's <code>Date.parse</code> being slow. You should check <code>log/development.log</code> to see what the query execution times are. What you're most likely experiencing is a table scan because you're missing an index on <code>due_date</code>.</p>

<p>Always check slow queries using <code>EXAMINE</code>. An example:</p>

<pre><code>EXAMINE SELECT * FROM items WHERE due_date='2011-01-01'
</code></pre>

<p>You'll get some information on the number of rows it will have to sort through, plus any indexes that could be used.</p>

