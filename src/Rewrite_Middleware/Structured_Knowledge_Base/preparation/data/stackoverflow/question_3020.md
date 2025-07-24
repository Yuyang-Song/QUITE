# T-SQL Clustered Index Seek Performance
[Link to question](https://stackoverflow.com/questions/62545833/t-sql-clustered-index-seek-performance)
**Creation Date:** 1592959197
**Score:** 0
**Tags:** sql-server, t-sql, statistics, sql-execution-plan
## Question Body
<p>Usual blather... query takes too long to run... blah blah. Long question. blah.
Obviously, I am looking at different ways of rewriting the query; but that is not what this post is about.</p>
<p>To resolve a &quot;spill to tempdb&quot; warning in a query, I have already</p>
<ol>
<li>rebuilt all of the indexes in the database</li>
<li>updated all of the statistics on the tables and indexes</li>
</ol>
<p>This fixed the &quot;spill to tempdb&quot; warning and improved the query performance.</p>
<p>Since rebuilding indexes and statistics resulted in a huge performance gain for one query (with out having to rewrite it), this got me thinking about how to improve the performance of other queries without rewriting them.</p>
<p>I have a nice big query that joins about 20 tables, does lots of fancy stuff I am not posting here, but takes about 6900ms to run.</p>
<p>Looking at the actual execution plan, I see 4 steps that have a total cost of 79%; so &quot;a-hah&quot; that is where the performance problem is. 3 steps are &quot;clustered index seek&quot; on PK_Job and the 4th step is an &quot;Index lazy spool&quot;.</p>
<p><a href="https://i.sstatic.net/lR8np.png" rel="nofollow noreferrer">execution plan slow query</a></p>
<p>So, I break out those elements into a standalone query to investigate further... I get the &quot;same&quot; 4 steps in the execution plan, with a cost of 97%, only the query time is blazing fast 34ms. ... WTF? where did the performance problem disappear to?</p>
<p><a href="https://i.sstatic.net/CT3Tq.png" rel="nofollow noreferrer">execution plan fast query</a></p>
<p>I expected the additional tables to increase the query time; but I am not expecting the execution time to query this one Job table to go from 30ms to 4500ms.</p>
<pre><code>-- this takes 34ms
select * 
from equip e 
left join job jf on (jf.jobid = e.jobidf) 
left join job jd on (jd.jobid = e.jobidd)
left join job jr on (jr.jobid = e.jobidd)


-- this takes 6900ms
select * 
from equip e 
left join job jf on (jf.jobid = e.jobidf) 
left join job jd on (jd.jobid = e.jobidd)
left join job jr on (jr.jobid = e.jobidd)
-- add another 20 tables in here..
</code></pre>
<p><strong>Question 1</strong>: what should I look at in the two execution plans to identify why the execution time (of the clustered index seek) on this table goes from 30ms to 4500ms?</p>
<p>So, thinking this might have something to do with the statistics I review the index statistics on the <code>PK_Job = JobID</code> (which is an <code>Int</code> column) the histogram ranges look useless... all the &quot;current&quot; records are lumped together in one range (row 21 in the image). Standard problem with a PK that increments, new data is always in the last range; that is 99.999% of the <code>JobID</code> values that are referenced are in the one histogram range. I tried adding a filtered statistic, but that had no impact on the actual execution plan.</p>
<p><a href="https://i.sstatic.net/vinCD.png" rel="nofollow noreferrer">output from DBCC SHOW_STAT for PK_Job</a></p>
<p><strong>Question 2</strong>: are the above <code>PK_Job</code> statistics a contributing factor to the complicated query being slow? That is, would &quot;fixing&quot; the statistics help with the complicated query? if so, what could that fix look like?</p>
<p>Again: I know, rewrite the query. Post more of the code (all 1500 lines of it that no one will find of any use). blah, blah.</p>
<p>What I would like are tips on what to look at in order to answer Q1 and Q2.
Thanks in advance!</p>
<p><strong>Question 3:</strong> why would a simple IIF add 100ms to a query? the &quot;compute scalar&quot; nodes all show a cost of 0%, but the IIF doubles the execution time of the query.</p>
<p>adding this to select doubles execution time from 90ms to 180ms; Case statements are just as bad too.</p>
<pre><code>IFF(X.Okay = 1, '', 'N') As OkayDesc
</code></pre>
<p>Next observation: Actual execution plan shows query cost relative to batch of 98%; but STATISTICS TIME shows cpu time of 141 ms; however batch cpu time is 3640 ms.</p>
<p><strong>Question 4:</strong> why doesn't the query cost % (relative to batch) match up with statement cpu time?</p>

## Answers
### Answer ID: 62548097
<p>The SQL Engine is pretty smart in optimizing badly written queries in most of the cases. But, when a query is too complex, sometimes it cannot use these optimizations and even perform bad.</p>
<p>So, you are asking:</p>
<blockquote>
<p>I break out those elements into a standalone query to investigate
further... I get the &quot;same&quot; 4 steps in the execution plan, with a cost
of 97%, only the query time is blazing fast 34ms? where did
the performance problem disappear to?</p>
</blockquote>
<p>The answer is pretty simple. Breaking the queries and materializing the data in @table or #table helps the engine to understand better with what amount of that it is working and built a better plan.</p>
<p>Brent Ozar wrote about <a href="https://www.brentozar.com/archive/2020/06/bad-idea-jeans-building-big-query-plans/" rel="nofollow noreferrer">this</a> yesterday giving an example how bad a big query can be.</p>
<p>If you want more details about how to optimize your query via rewriting, you need to provide more details, but in my practice, in most of the cases simplifying the query and materializing the data in #temp tables (as we can use parallel operations using them) is giving good results.</p>

