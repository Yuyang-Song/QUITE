# Query hint &#39;NO_PERFORMANCE_SPOOL&#39; being ignored?
[Link to question](https://stackoverflow.com/questions/68012036/query-hint-no-performance-spool-being-ignored)
**Creation Date:** 1623896184
**Score:** 1
**Tags:** sql-server, sql-server-2017
## Question Body
<p>I am working in a vendor's large SQL Server database and I have been tasked with data warehousing large volume of data from there. The server is SQL Server 2017 (14.0.3391.2) and DB where queries are running is set to compatibility level of 140.</p>
<p>I have several queries where the optimizer is deciding to use lazy/eager index spooling within the query plan. In the past (SQL Server 2016 forward) I have been able to easily prevent this using the query hint of 'NO_PERFORMANCE_SPOOL'. In the past, this has always led all index spools in the query plan being removed. <strong>For some reason, when applying that hint in the database, index spools still remain in the execution plan?</strong> I know I am viewing the actual execution plan (viewed plan provided in SSMS after allowing the query to execute with 'Include Actual Execution Plan' checked). I have not been able to find any other documented examples of someone claiming this is happening to them, so that leads me to believe I am missing something? I know hints can be ignored (or even cause errors) if the plan is not produceable using the provided hints, but I can't imagine that being the case here? <strong>I don't understand how it would be possible for an index spool to be REQUIRED for a plan to be compiled? Is my hint just straight up being ignored for some reason?</strong></p>
<p>So I am at a bit of a loss. I know I could eliminate the index spools using other methods like rewriting the queries or adding indexes, but I am not interested in that at this point. I just want to know why this query hint seems like it is being ignored?</p>
<p>PS: For anyone wondering, these queries suffer significantly when plans using index spooling are used. This server in general suffers from I/O bottlenecking and resource semaphore waits (related to memory grants. Again, not my server/issue), so index spooling ends of becoming a large issue.</p>
<p>PS PS: I would post query plans, but I think the data structure/naming and produced query plans are proprietary to the vendor. Plus I don't think it is really needed here. If anyone thinks that might be helpful then I can do more work to see if I can recreate using AdventureWorks or something.</p>

## Answers
### Answer ID: 68314397
<p><a href="https://sqlperformance.com/2019/11/sql-performance/eager-index-spool-optimizer" rel="nofollow noreferrer">To quote the great @PaulWhite on this subject</a>:</p>
<blockquote>
<p>While an eager index spool may only appear on the inner side of an nested loops apply, it is not a “performance spool. <strong>An eager index spool cannot be disabled with trace flag 8690 or the NO_PERFORMANCE_SPOOL query hint.</strong></p>
</blockquote>
<p>A performance spool is a &quot;lazy spool&quot;, not an eager spool, and is placed there using different optimization rules.</p>
<p>He also says</p>
<blockquote>
<p>In some respects, an eager index spool is the ultimate missing index suggestion</p>
</blockquote>
<p><strong>I therefore strongly suggest you index that table to remove the spool</strong></p>

