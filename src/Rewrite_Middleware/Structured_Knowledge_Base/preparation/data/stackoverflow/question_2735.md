# Max and min bounds on number of DB results without affecting performance
[Link to question](https://stackoverflow.com/questions/49864573/max-and-min-bounds-on-number-of-db-results-without-affecting-performance)
**Creation Date:** 1523905662
**Score:** 0
**Tags:** sql, h2
## Question Body
<p>I want to select rows from a database with bounds on the number of results. I always want to have a minimum number of results returned, even if that means ignoring my other criteria, and I never want to have more than a maximum amount.</p>

<p>My current query looks like this:</p>

<pre><code>(SELECT * FROM Athletes WHERE Height &gt; 72
    FETCH FIRST 10 ROWS ONLY)
UNION
(SELECT * FROM Athletes
    ORDER BY Height DESC
    FETCH FIRST 3 ROWS ONLY)
FETCH FIRST 10 ROWS ONLY
</code></pre>

<p>The idea here is that I want to find all athletes taller than six feet (72"). If there are more than ten, I just want any ten of them, but if there are fewer than three, I want the three tallest athletes even if some are under six feet.</p>

<p>This works fine on my test data, but I'd like to get rid of the <code>UNION</code> for production. How can I rewrite this without any performance-draining bits like <code>UNION</code> or <code>DISTINCT</code>?</p>

## Answers
### Answer ID: 49865844
<p>One method is to use a CTE:</p>

<pre><code>with ten as (
      SELECT *
      FROM Athletes
      WHERE Height &gt; 72
      FETCH FIRST 10 ROWS ONLY
     )
select t.*
from ten
where (select count(*) from ten) &gt;= 3
union all
select a.*
from atheletes
where (select count(*) from ten) &lt; 3
order by height desc
fetch first 3 rows only;
</code></pre>

<p>I think this should be pretty fast, because counting 10 rows in a table should be quite fast and there is no duplicate elimination.</p>

<p>EDIT:</p>

<p>Another method uses window functions but is likely to be less performant:</p>

<pre><code>select a.*
from (select a.*,
             sum(case when height &gt; 72 then 1 else 0 end) over () as num_gt72,
             row_number() over (order by height desc) as seqnum
      from (select a.*
            from athletes a
            order by height desc
            fetch first 10 rows only
           ) a
     ) a
where seqnum &lt;= num_gt72 or
      (seqnum &lt;= 3 and num_gt72 &lt; 3);
</code></pre>

