# Oracle left join throws an error, but inner join works
[Link to question](https://stackoverflow.com/questions/48067918/oracle-left-join-throws-an-error-but-inner-join-works)
**Creation Date:** 1514927639
**Score:** 0
**Tags:** oracle-database, join
## Question Body
<p>I have a query that consists of a join between two tables.  When it is an inner join, the query works fine.  However, when I change it to an outer join, it throws an error as if the secondary table was not defined in the query.</p>

<p>Here is what I mean:</p>

<pre><code>select a.unit
     , a.data_date
from ( 
        select unit
             , person
             , data_date
        from the_data
     ) a
     join personnel b
     on (
          b.person = a.person
          and b.first_date &lt;= a.data_date
          and b.last_date &gt;= a.data_date
        )
</code></pre>

<p>the_data and personnel are tables</p>

<p>This works as written, but if you change the join to a left join, it reports that a.data_date is an invalid identifier (and if you rewrite the ON clause so the top line is at the bottom, it will say that a.person is invalid).</p>

<p>I vaguely remember coming across this once before, and it turned out to be an internal Oracle bug.</p>

<p>The database is 64-bit version 11.2.0.4.0.</p>

