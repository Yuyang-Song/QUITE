# SegmentCacheManager - warmup segments strategy/SQL in parallel?
[Link to question](https://stackoverflow.com/questions/44504770/segmentcachemanager-warmup-segments-strategy-sql-in-parallel)
**Creation Date:** 1497286343
**Score:** 1
**Tags:** mondrian
## Question Body
<p>We run Mondrian (version "3.7.preview.506") on a Tomcat Webserver. 
We have some long running MDX-queries.
For example: The first calculation takes 276.764 ms and sends 84 SQL requests to the database (30 to 700ms for each SQL statement).</p>

<p>We see that the SQL-Statements are not executed in parallel - only two "mondrian.rolap.agg.SegmentCacheManager$sqlExecutor" are running at the same time.</p>

<ol>
<li>Is there a way to force Mondrian/olap4j to execute the SQL statments more in parallel?</li>
<li>What is about the property "mondrian.rolap.maxSqlThreads" which is set to 100 by default?</li>
</ol>

<p>Afterwards we execute the same MDX query and the calculation is finished in 4.904 ms.
Conclusion - if the "internal cache" (mondrian.rolap.agg.SegmentCacheManager) has loaded the segments the calculation is executed without any database request - but ...
3.How can we "warm up" the internal cache?</p>

<p>One way we tried was to rewrite the MDX-queries - we load several month into the cache by once (<em>MDX-B</em>):</p>

<p><strong>MDX-A</strong>: <code>SELECT ... ON ROWS FROM cube01 WHERE {[Time].[Default].[2017].[4]}</code>
becomes 
<strong>MDX-B</strong>: <code>SELECT ... ON COLUMNS, CrossJoin( ... ,{[Time].[Default].[2017].[2]:[Time].[Default].[2017].[4]})" + " ON ROWS FROM cube01</code></p>

<p>The rewriten MDX query takes 1.235.128 ms (244 SQL requests) - afterwards we execute our orgin MDX query (<em>MDX-A</em>) and the calculating takes 6.987 ms
- the interessting part for us was, that the calculation takes longer as 5 sec. (compared with the second execution of the same query),
even if we did not have any SQL request anymore.
The warm-up of the cache does not work as expected (in our opinion) - <em>MDX-B</em> takes much longer to collect data with one statement, as we would run the the monthly execution in three steps (Febrary to April) - and the calculation in memory also takes more time - why - how does loading segmentation really works?</p>

<ol start="4">
<li>What is the best practice to load the segments to speed up calculation in memory?</li>
<li>Is there a way to feed the "Mondrian-Cube" with simple SQL statements? </li>
</ol>

<p>Thanks in advance.</p>

<hr>

<p>Fact table with 3.026.236 rows - growing daily</p>

<p>6 dimension tables.</p>

<p>Date dimension table 21.183 rows.</p>

<p>We have monitored our test classes with JVM's VisualAdmin. </p>

<p>Mondrian 3.7.preview.506 - olap4j-1.1.0</p>

<p>Database: Oracle Database 11g Release 11.2.0.4.0 - 64bit</p>

<p>(we tried to use also memSQL database, we was only 50% faster ...)</p>

