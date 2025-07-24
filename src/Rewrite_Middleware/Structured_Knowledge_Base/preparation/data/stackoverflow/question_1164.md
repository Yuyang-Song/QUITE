# DayOfWeek in LINQ query
[Link to question](https://stackoverflow.com/questions/61638030/dayofweek-in-linq-query)
**Creation Date:** 1588776003
**Score:** 2
**Tags:** linq, entity-framework-core, ef-core-3.1
## Question Body
<p>I have a simple list of integers that represent days of week. I am trying to check if Date property of my entity is in the selected days of week. But if I try to pass it in query that targets database like this:</p>

<pre><code>query.Where(e =&gt; selectedDaysOfWeek.Contains((int)e.Date.DayOfWeek));
</code></pre>

<p>I got the exception: </p>

<blockquote>
  <p>The LINQ expression ... could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().</p>
</blockquote>

<p>If I on the other hand, first execute query by calling <code>ToList()</code> (for example) and then add the same where condition on resulting list, it works:</p>

<pre><code>var items = query.ToList();
items = items.Where(e =&gt; selectedDaysOfWeek.Contains((int)e.Date.DayOfWeek)).ToList();
</code></pre>

<p>Although in my case this is acceptable, I would like to fetch less items from the database. Is there a way to check DayOfWeek when querying db as was my initial intent?</p>

## Answers
### Answer ID: 61639226
<p>You are accessing the <code>DayOfWeek</code> property from a <code>DateTime</code> reference in the query.</p>

<p>Entity Framework "doesn't know" how to translate that to SQL thus in the first piece of code you getting an exception.</p>

<p>And in the second piece it is working after you have fetch all of the data from database at the <code>.ToList()</code> call, and the <code>.Where</code> filtering is happening in the memory.</p>

<p>If you wish to implement that logic on the database side, you will have to write your own SQL statement.</p>

