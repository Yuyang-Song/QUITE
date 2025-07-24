# How to get Weekly data from MySQL database table using week number of month?
[Link to question](https://stackoverflow.com/questions/45758693/how-to-get-weekly-data-from-mysql-database-table-using-week-number-of-month)
**Creation Date:** 1503065302
**Score:** 0
**Tags:** mysql
## Question Body
<p>I have a database table <strong>studentvideos</strong>. I want to retrieve data from this table based on week number of month which means for how much time a video is watched in a week and time is specified as <strong>totaltime</strong> column in table structure and <strong>noofviews</strong> column specifies how many times a video is watched. Week number is specified as a column in the table structure as <strong>wofmonth</strong>.</p>

<p>Lets we have a video named vid1, vid1 is watched two time each for 10 secs in week 1 and one time for 10 secs in week 2.</p>

<p>I want to get back response in nested array/JSON form in which I have week number as tag for each week and for each week number video name, sum of the time for which that video is watched in that specific week (E.g. week 1 array will have vid1 with time 20 secs and week 2 array will have vid1 with time 10 secs) and similarly number of time that video is watched in that week.</p>

<p>Screenshot of studentvideos table:<br>
<a href="https://i.sstatic.net/aTWke.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/aTWke.png" alt="Screenshot of studentvideos table"></a></p>

<p>I tried the following query but I don't know how to modify or rewrite the query to get the desired result explained above.</p>

<pre><code>SELECT videoid, sum(noofviews), sum(totaltime) FROM studentvideos group by videoid
</code></pre>

<p>Result:
Result of above query:<br>
<a href="https://i.sstatic.net/p61Nr.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/p61Nr.png" alt="Result of above query"></a></p>

## Answers
### Answer ID: 45771193
<p>After trying so many different things the answer to this was simple. I am posting correct answer, may be someone face such a problem in future. Multiple GROUP BY did the trick for me.</p>

<p>Query:</p>

<pre><code>SELECT wofmonth as weekNumber,videoid,sum(noofviews)as totalTime,sum(totaltime) as noOfViews from studentvideos group by wofmonth,videoid
</code></pre>

