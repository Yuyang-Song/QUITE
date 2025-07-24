# Optimizing Spark SQL Query for Data Aggregation
[Link to question](https://stackoverflow.com/questions/76844792/optimizing-spark-sql-query-for-data-aggregation)
**Creation Date:** 1691305520
**Score:** 0
**Tags:** azure, apache-spark-sql
## Question Body
<p>I am trying to aggregate data from an Azure database using Spark SQL. The original way I saw someone else do it was like this:</p>
<pre><code>select
max(Timestamp),
mean(datacolumn1),
median(datacolumn2),
max(datacolumn3)
from myTable where datacolumn2 = &quot;Yes&quot;
and Timestamp between &quot;1684738800000000&quot; and &quot;1684825200000000&quot;
GROUP BY FLOOR((Timestamp)/(N*U*1E6))*(N*U*1E6)
</code></pre>
<p>Where N = Numerical, integer multiplier against the aggregation type and U = The number of seconds in the aggregation type (ie. second = 1, minute = 60, hour = 3600, etc.). This should average the data within these groups, yet the issue I am seeing is that when I convert the timestamps locally, the are not correct and it's definitely a problem with the query but I don't know exactly what. So I tried rewriting it entirely:</p>
<pre><code>WITH Aggregated AS (
    -- Filter data, convert timestamps, and aggregate in one step
    SELECT
        FLOOR(Timestamp / (1000000 * N * U)) * (N * U) AS grouped_timestamp,
        min(Timestamp) as min_timestamp,
        AVG(data1) AS data1,
        AVG(data2) AS data2,
        AVG(data3) AS data3
    FROM dataBaseTable
    WHERE Timestamp BETWEEN UNIXtstart AND UNIXtstop
    GROUP BY FLOOR(Timestamp / (1000000 * N * U))
)

SELECT
    grouped_timestamp,
    from_unixtime(CAST(grouped_timestamp / 1000000 AS BIGINT)) AS datetime_representation,
    data1,
    data2,
    data3
FROM Aggregated
ORDER BY grouped_timestamp;
</code></pre>
<p>Although it works very well, it is also extremely slow. About 120x slower which is not realistic because the data density is on the order of micro-seconds. So if I try to query data for timestamps on a monthly or even annual basis it ends up running through multi-billions of rows on the server. So I tried optimizing it by changing some things around:</p>
<pre><code>WITH Aggregated AS (
    -- Filter data, convert timestamps, and aggregate in one step
    SELECT
        CAST(FLOOR(CAST(Timestamp AS BIGINT) / (1000000 * N * U)) * (N * U) AS BIGINT) AS grouped_timestamp,
        MIN(Timestamp) as min_timestamp,
        AVG(data1) AS data1,
        AVG(data2) AS data2,
        AVG(data3) AS data3
    FROM dataBaseTable
    WHERE Timestamp BETWEEN UNIXtstart AND UNIXtstop
    GROUP BY FLOOR(CAST(Timestamp AS BIGINT) / (1000000 * N * U))
)

SELECT
    grouped_timestamp,
    from_unixtime(CAST(grouped_timestamp / 1000000 AS BIGINT)) AS datetime_representation,
    data1,
    data2,
    data3
FROM Aggregated
ORDER BY grouped_timestamp;
</code></pre>
<p>However, this produces incorrect timestamps (ie. -8741307600) which when I looked it up, meant an integer overflow possibly. I tried avoiding it by explicitly casting Timestamp as bigint, but this did not work. Even though this is last option is faster, I don't think it's doing the math correctly. The first option is ideal, but just not correct. Second option is correct but too slow. Is there a way to be able to get a correct and fast way of aggregating large data sets that contain billions of rows?</p>
<p>Note: UNIXtstart, UNIXtstop, N and U are all user inputs that change with each query. Here is a test matrix that mimics the data structures I am working with: <a href="https://dbfiddle.uk/JadOeVwF" rel="nofollow noreferrer">https://dbfiddle.uk/JadOeVwF</a></p>
<p>PS - This is Spark SQL and there wasn't a tag I could find for it when I typed in spark or at least there may be a name that is different but means the same thing in tags. IDK</p>

## Answers
### Answer ID: 76849149
<p>I tried your query on your sample data in my environment, with <code>N</code> as 1 and <code>U</code> as 3600 for an hour.
Even I got the same results as you, the wrong timestamps.</p>
<p><img src="https://i.imgur.com/XsNp0SZ.png" alt="enter image description here" /></p>
<p>But when I give <code>U</code>  35 (2100) minutes is working.</p>
<p><img src="https://i.imgur.com/YaDil4r.png" alt="enter image description here" /></p>
<p>So, you can use below altered query for correct timestamps.</p>
<pre><code>WITH Aggregated AS (
    SELECT
        CAST(floor(CAST(Timestamp  AS  BIGINT) /  1000000  /  N  /  U) * (N  *  U) AS  BIGINT) AS grouped_timestamp,
        MIN(Timestamp) as min_timestamp,
        AVG(data1) AS data1,
        AVG(data2) AS data2,
        AVG(data3) AS data3
        FROM sample1
        WHERE  Timestamp  BETWEEN  &quot;1684738800000000&quot;  and  &quot;1684825200000000&quot;
        GROUP  BY  FLOOR(CAST(Timestamp  AS  BIGINT) /  1000000  /  N /  U)
        )
        
SELECT
    grouped_timestamp,
    from_unixtime(CAST(grouped_timestamp AS  BIGINT)) AS datetime_representation,
    data1,
    data2,
    data3
FROM Aggregated
ORDER  BY grouped_timestamp;
</code></pre>
<p>Output:</p>
<p><img src="https://i.imgur.com/B2rQ6yZ.png" alt="enter image description here" /></p>
<p>Here, you can see I am getting aggregated values over 1 hour timeframe
and for 2 hour timeframe.</p>
<p><img src="https://i.imgur.com/mMWr1n7.png" alt="enter image description here" /></p>

