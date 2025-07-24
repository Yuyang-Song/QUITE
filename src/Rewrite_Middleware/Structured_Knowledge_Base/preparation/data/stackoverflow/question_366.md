# SQL stored procedure temporary table memory problem
[Link to question](https://stackoverflow.com/questions/227994/sql-stored-procedure-temporary-table-memory-problem)
**Creation Date:** 1224720691
**Score:** 3
**Tags:** sql, sql-server, stored-procedures
## Question Body
<p>We have the following simple Stored Procedure that runs as an overnight SQL server agent job. Usually it runs in 20 minutes, but recently the MatchEvent and MatchResult tables have grown to over 9 million rows each. This has resulted in the store procedure taking over 2 hours to run, with all 8GB of memory on our SQL box being used up. This renders the database unavailable to the regular queries that are trying to access it.</p>

<p>I assume the problem is that temp table is too large and is causing the memory and database unavailablity issues.</p>

<p>How can I rewrite the stored procedure to make it more efficient and less memory intensive?</p>

<p>Note: I have edited the SQL to indicate that there is come condition affecting the initial SELECT statement. I had previously left this out for simplicity. Also, when the query runs CPU usage is at 1-2%, but memoery, as previously stated, is maxed out</p>

<p><pre><code>
CREATE TABLE #tempMatchResult
(
    matchId VARCHAR(50)
)</p>

<p>INSERT INTO #tempMatchResult
SELECT MatchId FROM MatchResult WHERE SOME_CONDITION</p>

<p>DELETE FROM MatchEvent WHERE<br>
MatchId IN (SELECT MatchId FROM #tempMatchResult)</p>

<p>DELETE FROM MatchResult WHERE
MatchId In (SELECT MatchId FROM #tempMatchResult)</p>

<p>DROP TABLE #tempMatchResult
</pre></code></p>

## Answers
### Answer ID: 21703229
<p>Can you just turn cascading deletes on between matchresult and matchevent? Then you need only worry about identifying one set of data to delete, and let SQL take care of the other.</p>

<p>The alternative would be to make use of the OUTPUT clause, but that's definitely more fiddle.</p>

<p>Both of these would let you delete from both tables, but only have to state (and execute) your filter predicate once. This may <em>still</em> not be as performant as a batching approach as suggested by other posters, but worth considering. YMMV</p>

### Answer ID: 13495590
<pre><code>DELETE FROM MatchResult WHERE
MatchId In (SELECT MatchId FROM #tempMatchResult)
</code></pre>

<p>can be replaced with </p>

<pre><code>DELETE FROM MatchResult WHERE SOME_CONDITION
</code></pre>

### Answer ID: 229048
<h3>Avoid the temp table if possible</h3>

<p>It's only using up memory.<br>
You could try this: </p>

<pre><code>DELETE MatchEvent
FROM MatchEvent  e , 
     MatchResult r
WHERE e.MatchId = r.MatchId 
</code></pre>

<h3>If you can't avoid a temp table</h3>

<p>I'm going to stick my neck out here and say:  <strong>you don't need an index on your temporary table</strong> because you want the temp table to be the smallest table in the equation and you want to table scan it (because all the rows are relevant).  An index won't help you here.  </p>

<h3>Do small bits of work</h3>

<p>Work on a few rows at a time.<br>
This will probably slow down the execution, but it should free up resources.  </p>

- One row at a time

<pre><code>SELECT @MatchId = min(MatchId) FROM MatchResult

WHILE @MatchId IS NOT NULL
BEGIN
    DELETE MatchEvent 
    WHERE  Match_Id = @MatchId 

    SELECT @MatchId = min(MatchId) FROM MatchResult WHERE MatchId &gt; @MatchId 
END
</code></pre>

- A few rows at a time

<pre><code>CREATE TABLE #tmp ( MatchId Varchar(50) ) 

/* get list of lowest 1000 MatchIds: */ 
INSERT #tmp 
SELECT TOP (1000) MatchId 
FROM MatchResult 
ORDER BY MatchId 

SELECT @MatchId = min(MatchId) FROM MatchResult

WHILE @MatchId IS NOT NULL
BEGIN
    DELETE MatchEvent
    FROM MatchEvent e , 
         #tmp       t
    WHERE e.MatchId = t.MatchId 

    /* get highest MatchId we've procesed: */  
    SELECT @MinMatchId = MAX( MatchId ) FROM #tmp  

    /* get next 1000 MatchIds: */  
    INSERT #tmp 
    SELECT TOP (1000) MatchId 
    FROM MatchResult 
    WHERE MatchId &gt; @MinMatchId
    ORDER BY MatchId 

END
</code></pre>

<p>This one deletes up to 1000 rows at a time.<br>
The more rows you delete at a time,  the more resources you will use but the faster it will tend to run (until you run out of resources!).  You can experiment to find a more optimal value than 1000.  </p>

### Answer ID: 228822
<p>First, indexes are a MUST here see Dave M's answer. </p>

<p>Another approach that I will sometime use when deleting very large data sets, is creating a shadow table with all the data, recreating indexes and then using sp_rename to switch it in. You have to be careful with transactions here, but depending on the amount of data being deleted this can be faster.</p>

<p><em>Note</em> If there is pressure on tempdb consider using joins and not copying all the data into the temp table. </p>

<p>So for example </p>

<pre><code>CREATE TABLE #tempMatchResult (
    matchId VARCHAR(50) NOT NULL PRIMARY KEY /* NOT NULL if at all possible */
);

INSERT INTO #tempMatchResult
SELECT DISTINCT MatchId FROM MatchResult;

set transaction isolation level serializable
begin transaction 

create table MatchEventT(columns... here)

insert into MatchEventT
select * from MatchEvent m
left join #tempMatchResult t on t.MatchId  = m.MatchId 
where t.MatchId is null 

-- create all the indexes for MatchEvent

drop table MatchEvent
exec sp_rename 'MatchEventT', 'MatchEvent'

-- similar code for MatchResult

commit transaction 


DROP TABLE #tempMatchResult
</code></pre>

### Answer ID: 228204
<p>There's probably a lot of stuff going on here, and it's not all your query. </p>

<p>First, I agree with the other posters.  Try to rewrite this without a temp table if at all possible.</p>

<p>But assuming that you need a temp table here, you have a BIG problem in that you have no PK defined on it.  It's vastly going to expand the amount of time your queries will take to run.  Create your table like so instead:</p>

<pre><code>CREATE TABLE #tempMatchResult (
    matchId VARCHAR(50) NOT NULL PRIMARY KEY /* NOT NULL if at all possible */
);

INSERT INTO #tempMatchResult
SELECT DISTINCT MatchId FROM MatchResult;
</code></pre>

<p>Also, make sure that your TempDB is sized correctly.  Your SQL server may very well be expanding the database file dynamically on you, causing your query to suck CPU and disk time.  Also, make sure your transaction log is sized correctly, and that it is not auto-growing on you.  Good luck.</p>

### Answer ID: 228052
<p>You probably want to process this piecewise in some way. (I assume queries are a lot more complicated that you showed?) In that case, you'd want try one of these:</p>

<ul>
<li>Write your stored procedure to iterate over results. (Might still lock while processing.)</li>
<li>Repeatedly select the N first hits, eg <code>LIMIT 100</code> and process those.</li>
<li>Divide work by scanning regions of the table separately, using something like WHERE M &lt;= x AND x &lt; N.</li>
<li>Run the "midnight job" more often. Seriously, running stuff like this every 5 mins instead can work wonders, especially if work increases non-linearly. (If not, you could still just get the work spread out over the hours of the day.)</li>
</ul>

<p>In Postgres, I've had some success using conditional indices. They work magic by applying an index if certain conditions are met. This means that you can keep the many 'resolved' and the few unresolved rows in the same table, but still get that special index over just the unresolved ones. Ymmv.</p>

<p>Should be pointed out that this is where using databases gets <em>interesting</em>. You need to pay close attention to your indices and use <code>EXPLAIN</code> on your queries a lot.</p>

<p>(Oh, and remember, <em>interesting</em> is a good thing in your hobbies, but not at work.)</p>

### Answer ID: 228003
<p>Looking at the code above, why do you need a temp table?</p>

<pre>
<code>
DELETE FROM MatchEvent WHERE
MatchId IN (SELECT MatchId FROM MatchResult)


DELETE FROM MatchResult
-- OR Truncate can help here, if all the records are to be deleted anyways.
</code>
</pre>

