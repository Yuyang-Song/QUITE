# MSL insert Query not working in PHP
[Link to question](https://stackoverflow.com/questions/45052063/msl-insert-query-not-working-in-php)
**Creation Date:** 1499847324
**Score:** 1
**Tags:** php, sql
## Question Body
<p>I have the following code but its not working no new entry is created in the database + its returning error, I cannot get the query to execute.</p>

<pre><code>$query = "INSERT INTO request_send ('message,create_time,sdate,edate,guest,from_userid,to_userid,hostid') VALUES(':ms,:create_tim,:sdat,:edat,:gues,:from_useri,:to_useri,:hosti')";
$stmt = $DBcon-&gt;prepare( $query );
        $stmt -&gt;bindParam(':ms', $req);
        $stmt-&gt;bindParam(':create_tim', $c_time);
        $stmt-&gt;bindParam(':sdat', $start);
        $stmt-&gt;bindParam(':edat', $end);
        $stmt-&gt;bindParam(':gues', $guest);
        $stmt-&gt;bindParam(':from_useri', $fromid);
        $stmt-&gt;bindParam(':to_useri', $touser);
        $stmt-&gt;bindParam(':hosti', $hostid);
        $stmt-&gt;bindParam(':whoareyou', $whoareyou);
     // check for successfull query
        if ( $stmt-&gt;execute() ){
             $response['status'] = 'success';
           } else {
                $response['status'] = 'error';
}
</code></pre>

<p>Help me to fix the issue.
[edit] managed to solve it after rewriting the query</p>

## Answers
### Answer ID: 45052146
<p>You got an excess <code>bind_param()</code></p>

<pre><code>$stmt-&gt;bindParam(':whoareyou', $whoareyou);
</code></pre>

<p>Either remove it or add <code>:whoareyou</code> in the query</p>

