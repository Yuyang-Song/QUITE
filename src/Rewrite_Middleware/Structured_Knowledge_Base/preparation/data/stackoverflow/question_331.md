# MySQL query from different databases in time to output in one graph
[Link to question](https://stackoverflow.com/questions/21125928/mysql-query-from-different-databases-in-time-to-output-in-one-graph)
**Creation Date:** 1389740653
**Score:** 0
**Tags:** php, mysql, data-structures, highcharts
## Question Body
<p>I've build 2 different databases:
1 - temperature measure each 5 minutes
2 - temperature forecast for each 3 hours</p>

<p>I would like to get a 12 hour data of measurements and forecast in one (highcharts) graph.
In the graph, the x bar needs to just display each hour, and the Y bar the temperature.</p>

<p>With php, I can get the 2 separate datastructures, and put them all together, but I would like to do this more dynamicaly by making a sql query with a time dependacy, so I could query for 1 hour, or 24 hours and still get a nice graph.
This would be easy with 2 databases that have the same structure, 
but that's not going to happen when I'm into play :)</p>

<p>Database 1:</p>

<pre><code>id  created_on          timestamp           temp
1   2014-01-04 17:15:12 2014-01-04 17:15:02 23.75
2   2014-01-04 17:20:12 2014-01-04 17:20:02 23.75
3   2014-01-04 17:25:12 2014-01-04 17:25:02 23.75
4   2014-01-04 17:30:12 2014-01-04 17:30:02 23.69
5   2014-01-04 17:35:12 2014-01-04 17:35:02 23.75
</code></pre>

<p>Database 2:
t0000 t/m t2100 are the timestamps for the forecast temperatures</p>

<pre><code>day         created_on          t0000   t0300   t0600   t0900   t1200   t1500   t1800   t2100
2014-01-12  2014-01-13 00:00:10 2.52    4.24    5.83    6.51    7.58    7.55    6.23    0.34
2014-01-13  2014-01-14 02:00:10 4.31    6.54    6.32    8.28    9.13    8.46    5.38    4.13
2014-01-14  2014-01-14 23:00:08 4.18    2.58    2.95    8.24    7.54    6.7 4.96    4
2014-01-15  2014-01-14 23:00:08 3.58    2.77    2.64    2.53    4.56    4.56    4.54    4.58
</code></pre>

<p>I've come up with the database2 structure, as each day get's updated 8 times a day.
And it's not only one day of information I receive, but I receive multiple day updates each 8 times a day, this produces to much rows, so now I rewrite the column each time I receive an update. This solution saved me bigtime in rows (as I like to keep some history), but now gives me another puzzle to deal with: joining them together.</p>

<p>I'm out for my sql magic, hoping there is some greater power out there... somewhere ;)</p>

## Answers
### Answer ID: 21126156
<p>It seems to me you need a <code>temperature</code> table with each row containing:</p>

<pre><code>  station      the location name of the measurement, e.g. BOS, LHR, etc.
  timestamp    the time of the measurement 
  temp         (FLOAT) the measurement
</code></pre>

<p>Each time a new measurement arrives you need to insert a new row.  You can use a composite of (<code>station</code>, <code>timestamp</code>) for the primary key on this table.</p>

<p>To summarize by day, you simply do</p>

<pre><code> SELECT station, DATE(timestamp), 
        MIN(temp) AS low,
        AVG(temp) AS avg,
        MAX(temp) AS high
   FROM temperature
  GROUP BY station, DATE(timestamp)
  ORDER BY station, DATE(timestamp)
</code></pre>

<p>This pattern for querying can produce all sorts of interesting summaries.</p>

<p>Don't worry about too many rows in your observation table.  Reports like this take well under a minute even when summarizing decades of measurements.</p>

<p>I happen to have been working on this problem lately. Here is a writeup.
<a href="http://www.plumislandmedia.net/mysql/sql-reporting-time-intervals/" rel="nofollow">http://www.plumislandmedia.net/mysql/sql-reporting-time-intervals/</a></p>

<p>An excellent source of worldwide historical data is here: <a href="http://mesonet.agron.iastate.edu/request/download.phtml" rel="nofollow">http://mesonet.agron.iastate.edu/request/download.phtml</a></p>

