# using a text file for visitor counters / what happens when different requests updating one file ?
[Link to question](https://stackoverflow.com/questions/20429858/using-a-text-file-for-visitor-counters-what-happens-when-different-requests-up)
**Creation Date:** 1386350427
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>i have a simple visitor counters in y website using db </p>

<p>pleas ignore the syntax errors</p>

<pre><code>    $date = date('Y/m/d');
        $record = $this-&gt;db-&gt;query("select * from `page_view` where `date` = '$date' ");

        if (empty($record))
            $this-&gt;db-&gt;query(" insert into `page_view`(`date`,`view` ) value ('$date' ,'1') ");
        else {
            $sql = "UPDATE `page_view` SET `view` = `view`+1 WHERE  `date` = '{$date}'";
            $this-&gt;db-&gt;query($sql);
            }
</code></pre>

<p>i'm having about 500k visitors per day which is a bit high and so is my mysql load .
i was wondering if i could use a text file to store each day hits and at the end of the day i would move/store the total visit count from text file to database .</p>

<p>at least until i identify and rewrite slow queries .</p>

<pre><code>$today = date('Y/m/d');
list ($counter , $date ) = explode('#' , file_get_contents('counter.txt'));
$counter++;
if( $today == $data )
file_put_contents('counter.txt' , $counter.'#'.$date );
else
file_put_contents('counter.txt' , '1#'.$today);
</code></pre>

<p>is there any reason i shouldn't do this ?i'm i going to have any problem ?
and what would happen when couple of visitors want to update this file at the same time  ?  </p>

## Answers
### Answer ID: 20430180
<p>A third argument to file_put_contents() could be passed, "LOCK_EX", to "Acquire an exclusive lock on the file while proceeding to the writing."  I agree with @jszobody, though, a database would be the way to go.</p>

<p><a href="http://php.net/file_put_contents" rel="nofollow">http://php.net/file_put_contents</a></p>

<pre><code>int file_put_contents ( string $filename , mixed $data [, **int $flags = 0** [, resource $context ]] )

LOCK_EX  Acquire an exclusive lock on the file while proceeding to the writing.
</code></pre>

### Answer ID: 20430148
<p>I believe php only handles one request at the time so updating the file should not be a problem, but why don't you just use analytics or any other. saves you some load and gives you a lot of info</p>

