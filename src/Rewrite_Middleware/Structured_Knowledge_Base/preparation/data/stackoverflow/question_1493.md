# Efficient selection of comparable rows from a table
[Link to question](https://stackoverflow.com/questions/78893342/efficient-selection-of-comparable-rows-from-a-table)
**Creation Date:** 1724168672
**Score:** 1
**Tags:** sql, ms-access, time-series
## Question Body
<p>I have a table of data recording information from two sensors:</p>
<pre><code>Measurement (_sensorName_, _measureName_, _dateTime_, reading)
</code></pre>
<p>I query this data, in a view, <code>inColumns</code>, with a to obtain a wider table, like this:</p>
<pre><code>SELECT 
    do, temp, t.dateTime, t.sensorName
FROM 
    (SELECT 
         reading AS do, dateTime, sensorName 
     FROM 
         measurement 
     WHERE 
         measureName = &quot;DOppm&quot;) AS ppm,
    (SELECT 
         reading AS temp, dateTime, sensorName 
     FROM 
         measurement 
     WHERE 
         measureName = &quot;Temperature&quot;) AS t
WHERE 
    ppm.dateTime = t.dateTime 
    AND ppm.sensorName = t.sensorName
ORDER BY 
    ppm.dateTime, ppm.sensorName;
</code></pre>
<p>Which produces a table of readings putting oxygen and temperature side-by-side:</p>
<div class="s-table-container"><table class="s-table">
<thead>
<tr>
<th style="text-align: center;">do</th>
<th style="text-align: center;">temp</th>
<th>dateTime</th>
<th>sensorName</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">10</td>
<td style="text-align: center;">15</td>
<td>2024-08-20 16:59:00</td>
<td>sensor22</td>
</tr>
<tr>
<td style="text-align: center;">11</td>
<td style="text-align: center;">15</td>
<td>2024-08-20 16:56:00</td>
<td>sensor44</td>
</tr>
</tbody>
</table></div>
<p>My problem is this: each sensor measures each the state of water (temperature, dissolved oxygen) every 12 minutes but the two are not in sync. So two compare the outcome of the two sensors I look for &quot;similar&quot; times - similar meaning, less than 6 minutes apart; which will always be the two closest readings from the two sensors.</p>
<p>I use much the same technique as above to obtain the closest reading:</p>
<pre><code>SELECT 
    s22.doppm, s44.doppm, s22.temp, s44.temp, s22.dT
FROM
    (SELECT 
         doppm, temp, t.dateTime AS dT 
     FROM
         dataInColumns 
     WHERE 
         sensorName = &quot;sensor22&quot;)  AS s22,
    (SELECT 
         doppm, temp, t.dateTime AS dT 
     FROM
         dataInColumns 
     WHERE
         sensorName = &quot;sensor44&quot;) AS s44
WHERE
    ABS(DATEDIFF(&quot;n&quot;, s22.dT, s44.dT)) &lt; 6
ORDER BY 
    s22.dateTime;
</code></pre>
<p>But the database computes the date difference for every pair of records so O(N^2) for N records. In the small data set (2000 readings of each) I have, this takes minutes to run the query. Yet as the times are indexed, and that it is known there is a recording from each sensor every 12 minutes, it should be possible to run this query in linear time O(N).</p>
<p>Is there a way to rewrite the query to run in linear time? I can do this in other languages than SQL, but as the data is in a relational database, I'd rather use an SQL query if it can be done efficiently.</p>

## Answers
### Answer ID: 78893472
<p>You can join on the time condition instead of making a Cartesian product.</p>
<p>Also, there is no need for sub-selects. You can select <code>FROM dataInColumns AS s22</code> and move the condition <code>sensorName=&quot;sensor22&quot;</code> to the WHERE clause (and for s44 as well).</p>
<pre class="lang-sql prettyprint-override"><code>SELECT s22.doppm, s44.doppm, s22.temp, s44.temp, s22.dateTime as dT
FROM
    dataInColumns AS s22
    INNER JOIN dataInColumns AS s44
        ON Abs(DateDiff(&quot;n&quot;, s22.dateTime, s44.dateTime)) &lt; 6
WHERE
    s22.sensorName=&quot;sensor22&quot; AND
    s44.sensorName=&quot;sensor44&quot;
ORDER BY s22.dateTime;
</code></pre>
<p>Keep in mind that you cannot infer the speed in SQL Server from the speed in Access. A query performing well (or badly) on one DB does not necessarily do so on the other one.</p>

