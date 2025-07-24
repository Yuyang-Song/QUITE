# Efficiently using two-column ranges in SQLite
[Link to question](https://stackoverflow.com/questions/7727996/efficiently-using-two-column-ranges-in-sqlite)
**Creation Date:** 1318344694
**Score:** 1
**Tags:** performance, sqlite
## Question Body
<p>I have a table of <code>(start_date, end_date, description)</code> -- in order to find events that happen within a given period, I am doing</p>

<pre><code>SELECT *
FROM table
WHERE start_date &lt; $view_end AND end_date &gt; $view_start
</code></pre>

<p>This works correctly, and many database products would be able to use an index on both columns to efficiently find the result -- but SQLite only supports using one range index at a time (I can do lots of indexed equals comparisons, but only one indexed greater-than or less-than). As a result, if I want to view the middle 10 events in a table of a million, I can only use one index to eliminate half of them, and have to do a full table scan on the other 500,000.</p>

<p>Are there any cool tricks I can do to rewrite this query in a way that is efficient, given SQLite's limitations?</p>

## Answers
### Answer ID: 7739872
<p>This wont be as fast as if you could use two indexes but will be much faster than just using a table scan on the second column:</p>

<pre><code>SELECT *
FROM table
WHERE start_date BETWEEN $view_start AND $view_end AND end_date &gt; $view_start
</code></pre>

<p>It will cut your table scan down to only the records that started between the data range you're looking for (rather than all records that started before your end date)</p>

