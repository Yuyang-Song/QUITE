# Downsize Growing Time-Related Mysql Table
[Link to question](https://stackoverflow.com/questions/1539082/downsize-growing-time-related-mysql-table)
**Creation Date:** 1255020505
**Score:** 2
**Tags:** mysql, time-series
## Question Body
<p>We have a database with the time related data in it. As you can imagine it growths (and slows down) with time. There is 50% read and 25% inserts and 25% update action on the present (this months) data, 100% read on the older data.</p>

<ul>
<li>The good thing is, the older data
also becomes less important.  </li>
<li>The bad thing is that sometimes we need to
query a whole period from present back to
last year.</li>
</ul>

<p>Now I want to have a mysql architecture, that serves the younger data faster than the older. </p>

<p>Is there a way to do that in mysql?</p>

<hr>

<p>post scriptum:
Of course, as we're working with ruby on rails and active record in the application layer, we could rewrite easily the active record base class to access multiple tables and move the older data to an other table. BUT because we have also read queries from other systems, like reporting, which should be able to access the old and the new data, and sometimes both at the same time, I would like to solve it on mysql.</p>

## Answers
### Answer ID: 1539126
<p>I'd split the table in to (at least) 2 tables and store current data in one and archival data it the other.  Then use a MySql view to create a "virtual" table that could be used when all the data is required, otherwise, access the required data directly using the actuall table.</p>

### Answer ID: 1539104
<p><a href="http://dev.mysql.com/doc/refman/5.1/en/partitioning.html" rel="nofollow noreferrer">MySQL partitioning</a> was pretty much made <em>just for you</em>.  It does require you to be on 5.1.</p>

