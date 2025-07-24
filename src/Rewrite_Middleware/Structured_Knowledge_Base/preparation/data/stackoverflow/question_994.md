# SQL Server : &quot;Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries.&quot;
[Link to question](https://stackoverflow.com/questions/53746431/sql-server-some-part-of-your-sql-statement-is-nested-too-deeply-rewrite-the)
**Creation Date:** 1544628982
**Score:** 1
**Tags:** sql, sql-server
## Question Body
<p>When I'm executing the code shown here on the SQL Server database (v12.0), I'm getting an error</p>

<blockquote>
  <p>Some part of your SQL statement is nested too deeply. Rewrite the query or break it up into smaller queries</p>
</blockquote>

<p>My code:</p>

<pre><code>CREATE TABLE [dbo].[Table]
(
    [test] [INT] NOT NULL
) ON [PRIMARY]
GO

SELECT * 
FROM [dbo].[Table] AS [Table]
WHERE 1 = 1 
  AND (1 = 1 AND 
( (((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((( 
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
((((((((((((((((((((((((((((((((((((((((((((((((((
[Table].[test] BETWEEN 1 AND 1
) ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
))))))))))))))))))))))))))))))))))))))))))))))))))))

DROP TABLE [dbo].[Table]
GO
</code></pre>

<p>If I remove one bracket, everything will work (the number of brackets needed to reproduce this differs from version to version).</p>

<p>Does anybody get the same issue?</p>

## Answers
### Answer ID: 53750843
<p>This occurs when the query you have simply has to nest too much.  And versions can differ in how the optimizer parses and organizes your query, in which case, the effective upper limit on nesting can be different depending on where you are running it.</p>

<p>I have typically gotten this while working <em>ad hoc</em> through some data cleanup activities, where it is useful to build a monster query, nest-nest-nesting, sub-selects, big case statements, etc. as you successively encounter one issue after the other.  In this regard, it's helpful (and saving lots of time) to have it in one monster query before trying to optimize and come up with the final solution.  But take it too far, and here you are.</p>

<p>To address this, I end up chunking it with temp tables, replacing a self-contained chunk/subquery of the SQL (or more) with temp tables.  For example, say a super-simplified version of the query is this:</p>

<pre><code>select ...
from 
(
  select ...
  from
    (
      select innerfield1, innerfield2, innerfield3, ...
      from ...
      where ...
    ) inner
    join ...
) outer
</code></pre>

<p>Then you might do this:</p>

<pre><code>if object_id('tempdb.dbo.#temp_inner', 'U') is not null drop table #temp_inner;
create table #temp_inner
(
  [innerfield1] int, 
  [innerfield2] nvarchar(100), 
  [innerfield3] datetime, 
  ...
)
</code></pre>

<p>then populate it once...</p>

<pre><code>insert into #temp_inner
select innerfield1, innerfield2, innerfield3, ...
from ...
where ...
</code></pre>

<p>and now replace this portion of the original query:</p>

<pre><code>select ...
from 
(
  select ...
  from #temp_inner inner
    join ...
) outer
</code></pre>

<p>And now you can run this outer query over and over with the now-cached inner.  This can even be a good idea even if you haven't hit any kind of limit and just have an inner portion has gotten stable and you're now working on the outer.</p>

<p>As commenters mention, there isn't a case for this in production code; queries should be broken up not just because usually it is optimal, but also for basic reasons like ability to troubleshoot, support, etc.  But above is nice for complex, <em>ad hoc</em>/initial investigation queries.</p>

### Answer ID: 53746917
<p>Why are you doing this? I don't find the sense in it, but I believe the problem is having too many parenthesis, the server doesn't know what to do with it, the difference between how many brackets do you require to get the error might be on the version since every version has a different way to play with the memory but also the Ram from the server.</p>

