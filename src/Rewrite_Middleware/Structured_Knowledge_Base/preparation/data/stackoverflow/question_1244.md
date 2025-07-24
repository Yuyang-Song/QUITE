# How would you rewrite this without a loop?
[Link to question](https://stackoverflow.com/questions/6577031/how-would-you-rewrite-this-without-a-loop)
**Creation Date:** 1309824982
**Score:** 2
**Tags:** php, mysql, sql, algorithm, optimization
## Question Body
<p>I am trying to rewrite this messy code, so that I only make one database query and eliminate the for loop. I am hoping the code will be faster with one query instead of two. </p>

<p>The loop exists for one reason: The date attribute, which is either "Today" or "Tomorrow" followed by the formatted date.</p>

<p>The <strong>main point</strong> here is that I want to keep the data structure (dayReport) the same. I want to know what date the result set belongs to (either "Today" or "Tomorrow"). </p>

<p>It seems silly to have a loop for that reason alone. </p>

<p>So here is the code. It's in PHP, but really this is a language agnostic question:</p>

<pre><code>for ($a=1; $a&lt;=2; $a++)
{
    $b = $a - 1;
    $result = mysql_query("SELECT
                            name,
                            time,
                            date_format(time,'%M %d %Y %h:%i %p') as ftime,
                            date_format(time,'%l:%i %p') as ttime,
                            fee
                            FROM `foo_bar`
                            WHERE `cityId` = $cityId
                            AND time_utc &gt; utc_timestamp()
                            AND time &gt;= DATE_ADD(curdate(),INTERVAL $b day)
                            AND time &lt; DATE_ADD(curdate(),INTERVAL $a day)
                            ORDER BY time ASC
                            " ) or die(mysql_error());


  if ($result &amp;&amp; mysql_num_rows($result) &gt; 0)
  {
    $day = new Day();
    $day-&gt;date = $a == 1 ? 'Today' . date(' - l, F d') : 'Tomorrow' . date(' - l, F d',strtotime('+'.$b.' day'));
    $dayStuff = array();
    while ($row = mysql_fetch_object($result))
    {
        $dayStuff[] = $row;
    }
    $day-&gt;foo = $dayStuff;
    $dayReport[] = $day;
  }
}
</code></pre>

## Answers
### Answer ID: 6577444
<p>You could rewrite your query in this way, plain SQL no php code</p>

<pre><code>SELECT
    name, time,
    date_format(time,'%M %d %Y %h:%i %p') as ftime,
    date_format(time,'%l:%i %p') as ttime,
    fee,
    `time` = CURDATE() AS is_today -- Note this flag
    FROM `foo_bar`
    WHERE `cityId` = $cityId
    AND time_utc &gt; utc_timestamp()
    AND time BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 1 day) -- rewritten clause for clarity
    ORDER BY time ASC
</code></pre>

<p>Then you could completely remove the outer php for statement and use the <code>is_today</code> flag to distinguish between today and tomorrow records.</p>

<p>For what regards the Day structure you can build two of them before the inner while and fill id according to the <code>is_today</code> flag, something like</p>

<pre><code>while ($row = mysql_fetch_object($result))
{
    if ($row['is_today']) {
        $todayStuff[] = $row;   
    } else {
        $tomorrowStuff[] = $row;
    }
}
</code></pre>

### Answer ID: 6577276
<p>You could combine the two queries into a <code>UNION</code> or expand the rank of the <code>WHERE</code> clause to cover both days. However, the <code>while()</code> loop will need to know how to process the rows differently without the flag variable. You could do that by getting the SQL to create a flag.</p>

### Answer ID: 6577107
<p>Use stored procedure if your goal is to lessen the exchange of data between your web application and your database.</p>

