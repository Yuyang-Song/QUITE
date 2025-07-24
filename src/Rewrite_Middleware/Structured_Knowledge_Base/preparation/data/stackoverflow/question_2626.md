# PDO error: Can&#39;t initialize character set utf8_general_ci
[Link to question](https://stackoverflow.com/questions/43360455/pdo-error-cant-initialize-character-set-utf8-general-ci)
**Creation Date:** 1491972163
**Score:** 0
**Tags:** php, mysql, pdo
## Question Body
<p>PHP on my web host was recently updated and now my old MySQL queries are showing the "deprecated" error message.  I need to convert mysql_query code to PDO.  Here's what I am starting with:</p>

<pre><code>&lt;?

    $con = mysql_connect("localhost", "username", "password");
    if (!$con) { die('Could not connect: ' . mysql_error()); } mysql_select_db("database_name", $con);

        $result = mysql_query("select * from event_calendar where event_year &gt;= '2017' order by event_datenumber asc")
        or die(mysql_error());

     while($row = mysql_fetch_array($result)) {

                $event_date = $row['event_date'];
                $event_month = $row['event_month'];
                $event_monthname = $row['event_monthname'];
                $event_year = $row['event_year'];
                $event_datenumber = $row['event_datenumber'];
                $event_starttime = $row['event_starttime'];
                $event_location = $row['event_location'];
                $event_city = $row['event_city'];
                $event_state = $row['event_state'];
                $event_directions = $row['event_directions'];

    $testmonth = date("F");
    $testmonth2 = date("m");
    $testdate = date("d");
    $testyear = date("Y");
    $testdatenumber = $testyear.$testmonth2.$testdate;

    ?&gt;

    &lt;?

    if ($testdatenumber &lt;= $event_datenumber){

    ?&gt;

    &lt;p&gt;
    &lt;b&gt;&lt;? echo $event_monthname.' '.$event_date ?&gt;&lt;/b&gt; - &lt;? echo $event_starttime ?&gt;&lt;br&gt;
    &lt;? echo $event_location ?&gt;&lt;br&gt;
    &lt;? echo $event_city ?&gt;, &lt;? echo $event_state ?&gt;&lt;br&gt;
    &lt;a href="&lt;? echo $event_directions ?&gt;" target="_blank"&gt;&lt;b&gt;Directions&lt;/b&gt;&lt;/a&gt;
    &lt;/p&gt;

    &lt;? } else {} ?&gt;

&lt;?  } ?&gt;
</code></pre>

<p>I'm totally new to this and don't know where to start.  I also noticed that today it is now saying "No database selected" as well.</p>

<p>I've been atempting to rewrite this myself in PDO line by line and so far I am getting:</p>

<blockquote>
  <p>Fatal error: Uncaught exception 'PDOException' with message 'SQLSTATE[HY000] [2019] Can't initialize character set utf8_general_ci (path: /usr/share/mysql/charsets/)' in /my_file_location/test-this.php:21 Stack trace: #0 /my_file_location/test-this.php(21): PDO->__construct('mysql:host=localhost', 'username', 'password') #1 {main} thrown in /my_file_location/test-this.php on line 21</p>
</blockquote>

<p>My line 21, referenced in the error above, is as follows:</p>

<pre><code>$db = new PDO('mysql:host=localhost;dbname=database_name;charset=utf8_‌​general_ci', 'username', 'password');
</code></pre>

<p>I've now changed utf8_general_ci to just utf8 and now have the following message:</p>

<blockquote>
  <p>Fatal error: Uncaught exception 'PDOException' with message
  'SQLSTATE[42000] [1044] Access denied for user 'username'@'localhost'
  to database 'database_name'' in /my_file_location/test-this.php:21
  Stack trace: #0 /my_file_location/test-this.php(21):
  PDO->__construct('mysql:host=localhost', 'username', 'password') #1
  {main} thrown in /my_file_location/test-this.php on line 21</p>
</blockquote>

<p>My web host is using a Windows operating system, I believe, and the PHP version it was just upgraded to is 5.6.30 but I have no idea about the mySQL database.</p>

<p>UPDATE:  OK, after a few days reading and poking around, I have managed to come up with a working rewrite.  I now have the following working:</p>

<pre><code>&lt;?php
    $db = new PDO('mysql:host=localhost;dbname=database_name;charset=utf8mb4', 'username', 'password', array(PDO::ATTR_EMULATE_PREPARES =&gt; false, 
                                                                                                PDO::ATTR_ERRMODE =&gt; PDO::ERRMODE_EXCEPTION));

    foreach($db-&gt;query('SELECT * FROM event_calendar WHERE event_year &gt;= 2017 ORDER BY event_datenumber ASC') as $row) {

    $testmonth = date("F");
    $testmonth2 = date("m");
    $testdate = date("d");
    $testyear = date("Y");
    $testdatenumber = $testyear.$testmonth2.$testdate;

if ($testdatenumber &lt;= $row['event_datenumber']) {

    echo "&lt;p&gt;";
    echo "&lt;u&gt;&lt;h4&gt;".$row['event_monthname']." ".$row['event_date'].", ".$row['event_year']."&lt;/h4&gt;&lt;/u&gt;";
    echo "&lt;b&gt;What:&lt;/b&gt; ".$row['event_title']."&lt;br/&gt;";
    echo "&lt;b&gt;Where:&lt;/b&gt; ".$row['event_location']." - ".$row['event_address1'].", ".$row['event_city'].", ".$row['event_state']." ".$row['event_zip']."&lt;br/&gt;";
    echo "&lt;b&gt;When:&lt;/b&gt; ".$row['event_starttime']."&lt;br/&gt;";
    echo "&lt;b&gt;When:&lt;/b&gt; &lt;a href='".$row['event_directions']."' target='_blank'&gt;&lt;b&gt;Click here&lt;/b&gt;&lt;/a&gt;";
    echo "&lt;/p&gt;";

    } else {}

    }

?&gt;
</code></pre>

<p>Now I just wish I could figure out how to limit results to only the first three rows that meet the criteria.  I've tried several things so far but have not yet been successful.  I guess it's back to reading and testing until I find something that works.</p>

## Answers
### Answer ID: 43371698
<p>The error message is clear: there is no such charset. And never has been.</p>
<p><code>utf8_general_ci</code> is a <em>collation</em>, while you need a <em>character set</em> here, which is called as just <s><code>utf8</code></s> or, rather, nowadays it should be <code>utf8mb4</code>.</p>
<p>Let me recommend you my <a href="https://phpdelusions.net/pdo" rel="nofollow noreferrer">PDO tutorial</a> which will help you to avoid a lot of confusions like this.</p>

### Answer ID: 43422196
<p>UPDATE: OK, after a few days reading and poking around, I have managed to come up with a working rewrite. I now have the following working:</p>

<pre><code>&lt;?php
    $db = new PDO('mysql:host=localhost;dbname=database_name;charset=utf8mb4', 'username', 'password', array(PDO::ATTR_EMULATE_PREPARES =&gt; false, 
                                                                                                PDO::ATTR_ERRMODE =&gt; PDO::ERRMODE_EXCEPTION));

    foreach($db-&gt;query('SELECT * FROM event_calendar WHERE event_year &gt;= 2017 ORDER BY event_datenumber ASC') as $row) {

    $testmonth = date("F");
    $testmonth2 = date("m");
    $testdate = date("d");
    $testyear = date("Y");
    $testdatenumber = $testyear.$testmonth2.$testdate;

if ($testdatenumber &lt;= $row['event_datenumber']) {

    echo "&lt;p&gt;";
    echo "&lt;u&gt;&lt;h4&gt;".$row['event_monthname']." ".$row['event_date'].", ".$row['event_year']."&lt;/h4&gt;&lt;/u&gt;";
    echo "&lt;b&gt;What:&lt;/b&gt; ".$row['event_title']."&lt;br/&gt;";
    echo "&lt;b&gt;Where:&lt;/b&gt; ".$row['event_location']." - ".$row['event_address1'].", ".$row['event_city'].", ".$row['event_state']." ".$row['event_zip']."&lt;br/&gt;";
    echo "&lt;b&gt;When:&lt;/b&gt; ".$row['event_starttime']."&lt;br/&gt;";
    echo "&lt;b&gt;When:&lt;/b&gt; &lt;a href='".$row['event_directions']."' target='_blank'&gt;&lt;b&gt;Click here&lt;/b&gt;&lt;/a&gt;";
    echo "&lt;/p&gt;";

    } else {}

    }

?&gt;
</code></pre>

<p>Now I just wish I could figure out how to limit results to only the first three rows that meet the criteria. I've tried several things so far but have not yet been successful. I guess it's back to reading and testing until I find something that works.</p>

### Answer ID: 43365593
<p>The correct <em>immediate</em> solution is to disable the showing of errors on your live site. This should be done anyway, since you <em>never</em> want to expose that information to users:</p>

<pre><code>ini_set('display_errors', false);
</code></pre>

<p>Do not do this on your non-live (test) sites, as you want to see errors there.</p>

<p>Once you have put this in place on your current site, your task to migrate away from this old database extension will be less urgent. My guess is that you're now on PHP 5.6, which still supports the <code>mysql_</code> functions, but you will still need to prepare for 7.x, where they have been removed.</p>

