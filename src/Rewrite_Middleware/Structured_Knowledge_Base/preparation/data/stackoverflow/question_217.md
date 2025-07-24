# Why does the same query takes different amount of time to run?
[Link to question](https://stackoverflow.com/questions/16948164/why-does-the-same-query-takes-different-amount-of-time-to-run)
**Creation Date:** 1370460323
**Score:** 7
**Tags:** oracle-database
## Question Body
<p>I have this problem that has been going on for months. I automate reports at my job, we use oracle. I write a procedure, time it, it runs in a few minutes. I then set it up for monthly runs.</p>

<p>And then every month, some report runs for hours. It's all the same queries that ran in a few minutes for months before and all of a sudden they're taking hours to run.</p>

<p>I end up rewriting my procedures every now and then and to me this defeats the purpose of automating. No one here can help me. </p>

<p>What am I doing wrong? How can I ensure that my queries will always take the same amount of time to run.</p>

<p>I did some research and it says that in a correctly setup database with correct statistics you don't even have to use hints, everything should consistently run in about the same time.</p>

<p>Is this true? Or does everyone have this problem and everyone just rewrites their procedures whenever they run?</p>

<p>Sorry for 100 questions, I'm really frustrated about this.</p>

<p>My main question is, why does the same query takes different amount of time (drastic difference, from minutes to hours) to run on different days?</p>

## Answers
### Answer ID: 16950032
<p>this is not an answer, this is a reply to Justin Cave, i couldn't format it in any readable way in the comments.</p>

<p>Different Data Volume
When ….. data. </p>

<p><strong>Yes, I’m using the same archive tables that I then use for months to come. Of course, data changes but it’s a pretty consistent rise, for example, if a table has 10M rows this month – it might gain 100K rows the next, 200K the next, 100K the next and so on. There are no drastic jumps as far as I know. And I’d understand if today the query took 2 minutes and next month it’d take 5. But not 3 hours. However, thank you for the idea, I will start counting rows in tables from month to month as well.
Question though, so how do people code to account for this? let’s say someone works with tables that will get large amounts of data at random times, is there a way to write the query to ensure the run times are at least in the ball park? Or do people just put up with the fact that any month their reports will run 10-20 hours.</strong></p>

<p>Different System Load
If I take a …. to process. </p>

<p>*<strong>*No, I run my queries on different days and times but I have logs of the days and the times so I will see if I can find a pattern.</strong></p>

<p>Different system load …hard to do. </p>

<p><strong>So are you saying that the fast times I may be getting at the time of the report design might be fast because of the things I ran on my computer previously?
Also, does the cache get stored on my computer or on the database under my login or where?**</strong> </p>

<p>Different Query Plans
Over time, your query plan … different load at different times. </p>

<p><strong>Thank you for your explanations, you’ve given me enough to start digging.</strong></p>

### Answer ID: 16949117
<p>There are three broad reasons that queries take longer at different times.  Either you are getting different performance because the system is under a different sort of load, you are getting different performance because of data volume changes, or you are getting different performance because you are getting different query plans.</p>

<p><strong>Different Data Volume</strong></p>

<p>When you generate your initial timings, are you using data volumes that are similar to the volumes that your query will encounter when it is actually run?  If you test a query on the first of the month and that query is getting all the data for the current month and performing a bunch of aggregations, you would expect that the query would get slower and slower over the course of the month because it had to process more and more data.  Or you may have a query that runs quickly outside of month-end processing because various staging tables that it depends on only get populated at month end.  If you are generating your initial timings in a test database, you'l very likely get different performance because test databases frequently have a small subset of the actual production data.</p>

<p><strong>Different System Load</strong></p>

<p>If I take a query and run it during the middle of the day against my data warehouse, there is a good chance that the data warehouse is mostly idle and therefore has lots of resources to give me to process the query.  If I'm the only user, my query may run very quickly.  If I try to run exactly the same query during the middle of the nightly load process, on the other hand, my query will be competing for resources with a number of other processes.  Even if my query has to do exactly the same amount of work, it can easily take many times more clock time to run.  If you are writing reports that will run at month end and they're all getting kicked off at roughly the same time, it's entirely possible that they're all competing with each other for the limited system resources available and that your system simply isn't sized for the load it needs to process.  </p>

<p>Different system load can also encompass things like differences in what data is cached at any point in time.  If I'm testing a particular query in prod and I run it a few times in a row, it is very likely that most of the data I'm interested in will be cached by Oracle, by the operating system, by the SAN, etc.  That can make a dramatic difference in performance if every read is coming from one of the caches rather than requiring a disk read.  If you run the same query later after other work has flushed out most of the blocks your query is interested in, you may end up doing a ton of physical reads rather than being able to use the nicely warmed up cache.  There's not generally much you can do about this sort of thing-- you may be able to cache more data or arrange for processes that need similar data to be run at similar times so that the cache is more efficient ut that is generally expensive and hard to do.</p>

<p><strong>Different Query Plans</strong></p>

<p>Over time, your query plan may also change because statistics have changed (or not changed depending on the statistic in question).  Normally, that indicates that Oracle has found a more efficient plan or that your data volumes have changed and Oracle expects a different plan would be more efficient with the new data volume.  If, however, you are giving Oracle bad statistics (if, for example, you have tables that get much larger during month-end processing but you gather statistics when the tables are almost empty), you may induce Oracle to choose a very bad query plan.  Depending on the version of Oracle, there are various ways to force Oracle to use the same query plan.  If you can drill down and figure out what the problem with statistics is, Oracle probably provides a way to give the optimizer better statistics.</p>

<p>If you take a look at AWR/ ASH data (if you have the appropriate licenses) or Statspace data (if your DBA has installed that), you should be able to figure out which camp your problems originate in.  Are you getting different query plans for different executions (you may need to capture a query plan from your initial benchmarks and compare it to the current plan or you may need to increase your AWR retention to retain query plans for a few months in order to see this).  Are you doing the same number of buffer gets over time but getting vastly different amounts of I/O waits?  Do you see a lot of contention for resources from other sessions?If so, that probably indicates that the issue is different load at different times.  </p>

### Answer ID: 16948261
<p>One possibility is that your execution plan is cached so it takes a short amount of time to rerun the query, but when the plan is no longer cached (like after the DB is restarted) it might take significantly longer.</p>

<p>I had a similar issue with Oracle a long while ago where a very complex query for a report ran against a very large amount of data, and it would take hours to complete the first time it was run after the DB was restarted, but after that it finished in a few minutes.</p>

