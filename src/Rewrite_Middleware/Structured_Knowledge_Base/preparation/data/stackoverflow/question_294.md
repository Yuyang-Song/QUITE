# Map reduce output to oracle database?
[Link to question](https://stackoverflow.com/questions/19769301/map-reduce-output-to-oracle-database)
**Creation Date:** 1383573526
**Score:** -2
**Tags:** java, oracle-database, hadoop, mapreduce
## Question Body
<p>We are developing a network monitoring tool which continously monitor and collect cpu usage%, memory usage% data from the configured systems. We currently put the data into oracle db. Our intention is to produce graphical reports based on the data .For example CPU usage for Last 12 Hrs will show a line graph with 12 plotting points.ie, interval is 1 hour.
Still then the performance is bit slow. Our plan is to increase plotting poins . ie, we plot graphs wit interval 10 sec. ,30 sec, ... With oracle querying it seems to be harder.</p>

<p>So we plan to use hadoop for storing time series monitoring data and shedule a map reduce job to obtain averages for various time intervals.One option I think is to read output directly from hdfs. It make our programmers to rewrite the graphloading section.Can we write this output to <strong>oracle</strong> database so that we can readily query this data ?</p>

## Answers
### Answer ID: 19769410
<p>You might want to look into <a href="http://docs.oracle.com/cd/E37231_01/doc.20/e36961/olh.htm" rel="nofollow" title="Oracle Loader for Hadoop">Oracle Loader for Hadoop</a>. It appears to be a free library from Oracle for doing essentially exactly what you are looking for. It appears to come with an OutputFormat that will write directly to an Oracle instance.</p>

### Answer ID: 19769399
<p>It is possible to move data from HDFS to database using sqoop. It takes out the heavy-lifting you'd have to do manually.</p>

