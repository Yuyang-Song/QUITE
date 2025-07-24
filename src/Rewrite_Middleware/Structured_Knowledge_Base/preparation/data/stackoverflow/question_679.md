# Multiple queries with php code in mysqli one person at the time
[Link to question](https://stackoverflow.com/questions/36911636/multiple-queries-with-php-code-in-mysqli-one-person-at-the-time)
**Creation Date:** 1461838578
**Score:** 0
**Tags:** php, mysql, sql
## Question Body
<p>This code works but the problem is that if several people use it simultaneously it will cause problems in the sense that some people wont be registered. So I need to rewrite this in a way that all queries per person are executed and finished before the queries of the next person start.</p>

<p>First, the code reads from the database in order to get to the string of all the people that are registered so far.</p>

<pre><code>        $sql_s = $con -&gt; query("select * from schedule where date='$date'");
$row_schedule = $sql_s-&gt;fetch_array(MYSQLI_BOTH);
        $participants = $row_schedule['participants'];
</code></pre>

<p>$participants is a string that looks something like "'Sara':'Richard':'Greg'"</p>

<p>Now the current user (Fredrik) wants to add its name to the string like this</p>

<pre><code>$current_user='Fredrik';
$participants_new=add_participant($participants,$current_user);
</code></pre>

<p>add_participant is a php function that adds 'Fredrik' to the participant string. Then I want to replace the old participant string with the new one in the SQL database like this</p>

<pre><code>$sql = $con-&gt;query("UPDATE schedule SET participants='{$participants_new}' where date='{$date}'");
</code></pre>

<p>The specific problem is that if another person (Linda) reads the database before Fredrik executes</p>

<pre><code>$sql = $con-&gt;query("UPDATE schedule SET participants='{$participants_new}' where date='{$date}'");
</code></pre>

<p>Linda won't get a string that includes Fredrik, she will get "'Sara':'Richard':'Greg'". And when she has added her name it will look like "'Sara':'Richard':'Greg':'Linda'" and when she updates the database like this</p>

<pre><code>$sql = $con-&gt;query("UPDATE schedule SET participants='{$participants_new}' where date='{$date}'");
</code></pre>

<p>The string including Fredrik ("'Sara':'Richard':'Greg':'Fredrik'") will be overwritten with ("'Sara':'Richard':'Greg':'Linda'") and noone will ever know that Fredrik registered in the class. </p>

<p>Thus, how can I rewrite this code such that all Fredrik's queries are executed before Linda's queries start?</p>

## Answers
### Answer ID: 36912659
<p>Here is an approach to do it :</p>

<h1>Theoritically Explanation :</h1>

<p>Something like this could work.That everytime when user executes the query so it should check for time the request was made to update the query so.Now there must be time difference between user requests for updation query.</p>

<p><strong>Note :</strong> Still It's not guaranteed that it will work as because when you will be having internet problems and the user who submitted the request at first but having internet problems and that's why his update query execution is delayed during that time and the other user comes and he sent request late for the updation query but he was having no internet connection problem so his query will be updated before and I think hence that way first user query will get failed..!</p>

<p>Here is the Code :</p>

<pre><code>&lt;?php
// You need to add another column for saving time of last query execution

$current_time=time();
$current_date=date("Y-m-d",$t);
$query_execution_new_time = $current_time.":".$current_date;

if (empty($row_schedule['query_execution_time'])) {
$sql = $con-&gt;query("UPDATE schedule SET query_execution_time='{$query_execution_new_time}' where date='{$date}'");
} else {
$query_execution_time = explode(":",$row_schedule['query_execution_time']);
if ($query_execution_time[0] &lt; $current_time) {
$con-&gt;query("UPDATE schedule SET participants='{$participants_new}' where date='{$date}'");
$sql = $con-&gt;query("UPDATE schedule SET query_execution_time='{$query_execution_new_time}' where date='{$date}'");
}
}
?&gt;
</code></pre>

### Answer ID: 36913080
<p>Try this</p>

<p>No need to fetch first all participants and then update.
only update new participant user.</p>

<p>you can concat result of previous one result saved in database column field.</p>

<pre><code>
update schedule
 set participants = case when participants is null or participants ='' 

 then CONCAT(participants,'Fredrik') // assume Fredrik a new participant
 else CONCAT(participants,':','Fredrik')
 end
 where date='$date';
</code></pre>

<p>That way even if you have multiple participants came at the same time the queries won't run at exactly the same time and so you'll get the correct user at the end.<br/></p>

<p>you don't need to worry about multiple users clicking on them unless you've got millions of users
</p>

### Answer ID: 36913184
<p>Your question is very good example, showing why one should always learn database design basics and always follow them.</p>

<p>A separator-delimited string in a database is a deadly sin. For many reasons, but we are interesting in this particular case.</p>

<p>Had you designed your database properly, adding participants into separate rows, there would be not a single problem. </p>

<p>So, just change your design by adding a table with participants, and there will be not a single problem adding or removing any number of them.</p>

