# Filtering the same query 3 different times. Performance?
[Link to question](https://stackoverflow.com/questions/61075216/filtering-the-same-query-3-different-times-performance)
**Creation Date:** 1586245867
**Score:** 0
**Tags:** sql, t-sql, sql-server-2008, reporting-services, database-performance
## Question Body
<p>I have a query that is really slow. I will post pseudo code here.</p>

<pre><code>SELECT 
    ListofDates.Date as Event,
    (SELECT COUNT(DISTINCT TableofExtensiveJoins1.ID)
     FROM TableofExtensiveJoins1)
    WHERE Event=TableofExtensiveJoins1.Date AND Condition1
   (SELECT COUNT(DISTINCT TableofExtensiveJoins2.ID)
    FROM TableofExtensiveJoins2
    WHERE Event = TableofExtensiveJoins2.Date AND Condition2)
   (SELECT COUNT(DISTINCT TableofExtensiveJoins3.ElementID)
    FROM TableofExtensiveJoins3
    WHERE Event = TableofExtensiveJoins3.Date AND Condition3)
FROM
    ListOfDates
</code></pre>

<p>One thing to notice here is that TableOfExtensiveJoins1 , 2 and 3 are exactly the same query. But the Where condition is different on every one. Running the same query 3 times just to filter 3 times differently seems a little bit extensive. But as you can see it is necessary because i want to count stuff on the table. The table is each time filtered differently. But because of the "count" I have the fear that SQL compiles the table every time again.</p>

<p>I have that fear because the query runs exceptionally long. The subqueries are really complicated itself. To give you an example: To get only one record of the main query takes around 15 seconds. The sub query itself takes 5 seconds which would explain the 15 seconds, 3*5=15. And to run the whole main query it would likely get a few thousand records. I let it run 50 Minutes one day and it didn't finish. Obviously its not linear but that is beside the point. I just wanted to stress how bad the query is.</p>

<p>So obviously I need to increase performance on that query. For the sake of the optimization lets say i can not create new tables in the database. Else it would be to easy I guess. Lets also assume that TableoExtensiveJoins is already optimized. </p>

<p>So my question here is how can i rewrite the query to run it faster. Compile the table one once and then run the filter on the compilation. The query is run in Microsoft SQL Reporting Services. So there might be limitation on what kind of query are run able. But I'm not 100% sure about this. </p>

<p>Edit: The desired result might be helpful for the right answer. </p>

<p>TableOfExtensiveJoins is basically an event table. Evertime something specific happens (Doesnt matter) a new entry is created. </p>

<p>I now want for any given date to count the number of events with certain conditions. The ListOfDates has a list of dates. It takes the first occurence of the event and then creats a list of dates that than is filtered with Day(Date) % 5=1. So every 5. date. </p>

## Answers
### Answer ID: 61079269
<p>I think you want <code>OUTER APPLY</code>:</p>

<pre><code>SELECT lod.Date as Event, tej.*
From ListOfDates lod OUTER APPLY
     (SELECT SUM(CASE WHEN &lt;condition 1&gt; THEN 1 ELSE 0 END) as col1,
             SUM(CASE WHEN &lt;condition 2&gt; THEN 1 ELSE 0 END) as col2,
             SUM(CASE WHEN &lt;condition 3&gt; THEN 1 ELSE 0 END) as col3
      FROM TableofExtensiveJoins tej
      WHERE lod.Event = tej.Date
     ) tej;
</code></pre>

<p>Assuming that <code>tej.ID</code> is unique, you don't need the <code>COUNT(DISTINCT)</code>.  However, if you do:</p>

<pre><code>SELECT lod.Date as Event, tej.*
From ListOfDates lod OUTER APPLY
     (SELECT COUNT(DISTINCT CASE WHEN &lt;condition 1&gt; THEN tej.ID END) as col1,
             COUNT(DISTINCT CASE WHEN &lt;condition 2&gt; THEN tej.ID END) as col2,
             COUNT(DISTINCT CASE WHEN &lt;condition 3&gt; THEN tej.ID END) as col3
      FROM TableofExtensiveJoins tej
      WHERE lod.Event = tej.Date
     ) tej;
</code></pre>

<p>This generalizes to whatever conditions you might have in the subqueries.  As a bonus, lateral joins (the technical term for what <code>APPLY</code> is doing in this case) often have the best performance in SQL Server.</p>

### Answer ID: 61077416
<p>The below should perform better as it only evaluates <code>TableofExtensiveJoins</code> once and only needs one operation to get the distinct counts</p>

<pre><code>WITH DistCounts
     AS (SELECT COUNT(DISTINCT ID) AS DistCount,
                condition_flag,
                Date
         FROM   TableofExtensiveJoins
                CROSS APPLY (SELECT 1 WHERE  Condition1
                             UNION ALL
                             SELECT 2 WHERE  Condition2
                             UNION ALL
                             SELECT 3 WHERE  Condition3) CA(condition_flag)
         GROUP  BY condition_flag,
                   Date),
     Pivoted
     AS (SELECT Date,
                MAX(CASE WHEN condition_flag = 1 THEN DistCount END) AS DistCount1,
                MAX(CASE WHEN condition_flag = 2 THEN DistCount END) AS DistCount2,
                MAX(CASE WHEN condition_flag = 3 THEN DistCount END) AS DistCount3
         FROM   DistCounts
         GROUP  BY Date)
SELECT lod.Date as Event,
        DistCount1,
        DistCount2,
        DistCount3
from ListOfDates lod
left join Pivoted p on lod.Date=p.Date
</code></pre>

### Answer ID: 61075715
<p>Try conditional aggregation, kind of</p>

<pre><code>SELECT ListofDates.Date as Event,
        COUNT(DISTINCT CASE WHEN Condition 1 THEN tej.ID END) cnt1,
        COUNT(DISTINCT CASE WHEN Condition 2 THEN tej.ID END) cnt2,
        COUNT(DISTINCT CASE WHEN Condition 3 THEN tej.ID END) cnt3
from ListOfDates lod
left join TableofExtensiveJoins tej on lod.Event=tej.Date
group by lod.Event
</code></pre>

