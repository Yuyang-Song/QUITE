# subtracting time in php mysql query from int field
[Link to question](https://stackoverflow.com/questions/4905369/subtracting-time-in-php-mysql-query-from-int-field)
**Creation Date:** 1296885061
**Score:** 2
**Tags:** php, mysql, datetime
## Question Body
<p>I've been given the task of fixing up a bit of very messy code one of our clients had written by a dodgy freelancer.... I'm not terribly keen on rewriting the whole thing, as its been in use for some time, its only really caused problems now when they've asked for another feature. The database is utilised by various other parts of the program and this function is only a small portion of the overall system.  </p>

<p>Essentially the purpose of the script is to manage all meetings in a virtual office. 
They need a page to display "current" meetings.  This was there original query.</p>

<pre><code>$CURRENT_TIME=date("Gi");


mysql_connect(localhost,$USERNAME,$PASSWORD);
@mysql_select_db($DATABASE) or die( "Unable to select database");
$query="SELECT * FROM ROOM_1 WHERE 
EVENT_ROOM LIKE'%$URLROOMNAME%' 
AND EVENT_YEAR='$CURRENT_YEAR' 
AND EVENT_MONTH='$CURRENT_MONTH' 
AND EVENT_DATE='$CURRENT_DATE' 
AND START_TIME&lt;='$CURRENT_TIME'
AND END_TIME&gt;='$CURRENT_TIME' ";
$result=mysql_query($query);
$num=mysql_numrows($result);
mysql_close();
</code></pre>

<p>The time is stored in the mysql table in an int field as a 24hour value. Eg 3:43pm is stored simply as 1543. 
The new requirement was for a meeting to be able to have a setup time allowance. 
The freelancers... "ingenious" solutions was to add another int field to the table and change this line</p>

<pre><code>AND START_TIME&lt;='$CURRENT_TIME'
</code></pre>

<p>to..</p>

<pre><code>AND (START_TIME-APPEAR_START_TIME)&lt;='$CURRENT_TIME'
</code></pre>

<p>Now whilst it may work for some meetings it wont for others, eg A meeting starting at 1405 with a 20 minute setup allowance time would result in 1385... </p>

<p>So I'm looking for a clever solution that allows me to leave the rest alone and just subtract APPEAR_START_TIME field from the $START_TIME column in the query but by minutes. </p>

<p>Any ideas ?</p>

## Answers
### Answer ID: 4905508
<p>first of all , thanks Kel :)</p>

<p>I think this one is more easier :</p>

<p>(((START_TIME/100)*60+(START_TIME%100) - APPEAR_START_TIME) / 60) * 100 + (((START_TIME/100)*60+(START_TIME%100) - APPEAR_START_TIME)%60)</p>

### Answer ID: 4905424
<p>If I understand you correctly, you have two integer values in the form of "HHMM", where HH is hours, and MM is minutes; and you want to calculate difference between two time values.</p>

<p>You can get HH with <code>value / 100</code>, and MM with <code>value % 100</code>. Then you can calculate delta for hours and minutes separately.</p>

<p>Hours delta is (HH values delta + probably 1 hour caused by minutes delta, if MM-start &lt; MM-appear-start):</p>

<pre><code>(START_TIME / 100 - APPEAR_START_TIME / 100) + (START_TIME % 100 - APPEAR_START_TIME % 100) / 60
</code></pre>

<p>Minutes delta is:</p>

<pre><code>(START_TIME % 100 - APPEAR_START_TIME % 100) % 60
</code></pre>

<p>Then you can concatenate HH and MM parts of delta:</p>

<pre><code>HOURS_DELTA * 100 + MINUTES_DELTA
</code></pre>

