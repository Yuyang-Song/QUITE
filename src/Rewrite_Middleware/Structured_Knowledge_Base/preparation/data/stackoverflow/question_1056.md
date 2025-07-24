# looping a query from multiple variables?
[Link to question](https://stackoverflow.com/questions/5689613/looping-a-query-from-multiple-variables)
**Creation Date:** 1302987954
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>I'm rewriting my newsletter mailer to throttle sending to certain domains. basically subscribers are saved in <code>mailer_lists</code> in another form, then they get assigned the mailing ip to use with that mailing ip's limit for the specified domain. the code below is my attempt to gather that information.</p>

<p>What I'm trying to do is pull records for query matches, looping through <code>$node_ip</code>, <code>$throttle_domain</code>, and <code>$throttle_speed</code> and then stop pulling records if it hits the global limit, then send. i'm having trouble getting it to work right..</p>

<pre><code>function queue(){
$query = "SELECT * FROM `mailer_lists` WHERE `ip` = '$node_ip' AND `email` LIKE '%".$throttle_domain."' LIMIT ".$throttle_speed."" ;
$result = mysql_query($query) or die(mysql_error());
$num_rows = mysql_num_rows($result);
$count = $num_rows;
}
if ($count &lt; $global){
queue();
}else{
mail();
</code></pre>

<p><BR>
Wish I had 1/2 the skills some of you have. Looking forward to any ideas..</p>

## Answers
### Answer ID: 5690275
<p>I don't really if this will work at all :D</p>

<pre><code>&lt;?php

function queue($ptr, $glbl){
/* each time we increment our range by $glbl */
$newPtr = $ptr + 100;
/* we use limit keyword to only fetch 100 rows each time */
$query = "SELECT * FROM `mailer_lists` WHERE `ip` = '$node_ip' LIMIT '$ptr', '$newPtr'" ;
$result = mysql_query($query) or die(mysql_error());
/* fetch the rows and send to theme an email */
while($row = mysql_fetch_row($result))
 {
    mail(mail($row['email'], $subject, $message));
 }

}
/* here we use a static variable to track where we are we in the range */
static $next = 0;
$i = 0;
/* sending emails*/
queue($next, $glbl);
/* put pur next beginning range in 
$next ant it will end with $next + $glbl as it in line 5 */
$next += $glbl;
?&gt;
</code></pre>

### Answer ID: 5689726
<p>Make you function return number of rows like this:</p>

<pre><code>function queue(){
$query = "SELECT * FROM `mailer_lists` WHERE `ip` = '$node_ip' AND `email` LIKE '%".$throttle_domain."' LIMIT ".$throttle_speed."" ;
$result = mysql_query($query) or die(mysql_error());
return mysql_num_rows($result);
}
</code></pre>

<p>No you can make your condition:</p>

<pre><code>if (queue() &lt; $global){
queue();
}else{
mail();
</code></pre>

### Answer ID: 5689683
<p>The count in your function isn´t marked as global so is not updated.. Add global $count as the first line of the queue function.</p>

<p>Another issue is that when the count never reaches the global var, it will never mail. So the last batch wont be sent.</p>

