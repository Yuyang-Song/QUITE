# Using AJAX to send form information to another page using a button
[Link to question](https://stackoverflow.com/questions/34616001/using-ajax-to-send-form-information-to-another-page-using-a-button)
**Creation Date:** 1452009724
**Score:** 0
**Tags:** javascript, php, jquery, mysql, ajax
## Question Body
<p>Hello I have two files that are supposed to be connected to one another. I want to send an AJAX request to another page that uses a sql query to send form information.</p>

<p>The application that I'm trying to create is a questionnaire with eight questions, each questions has four answers paired together with the same id (qid) and each answer has a value from the database. After you answer eight questions you will see a button that sends an AJAX request to the page test.php, (named submitAJAX).</p>

<p>The problem is that although my connection with AJAX is working, the values from the form are not being sent to my database. Previously I thought that the problem may lie with the form page, but now I I think the problem lies in this file:</p>

<p><strong>test.php (file with json)</strong></p>

<pre><code>&lt;?php
$localhost = "localhost";
$username = "root";
$password = "";
$connect = mysqli_connect($localhost, $username, $password) or die ("Kunde inte koppla");
mysqli_select_db($connect, 'wildfire');
if(count($_GET) &gt; 0){
   $answerPoint = intval($_GET['radiobtn']);
   $qid = intval($_GET['qid']);
$tid = intval($_GET['tid']);
   $sql2 = "INSERT INTO result (qid, points, tid) VALUES ($qid, $answerPoint, $tid)";
   $connect-&gt;query($sql2); 
   $lastid = $connect-&gt;insert_id;
   if($lastid&gt;0) {
    echo json_encode(array('status'=&gt;1));
}
   else{
    echo json_encode(array('status'=&gt;0));
} 
}
?&gt;
</code></pre>

<p>I think that the problem may lie in the row where:  <code>if($lastid&gt;0) {</code>
$lastid should always be more than 0, but whenever I check test.php I get this message: <code>{"status":0}</code> What's intended is that I get this message: <code>{"status":1}</code></p>

<pre><code>&lt;html&gt;
    &lt;head&gt;
        &lt;meta charset="utf-8"&gt;
    &lt;/head&gt;
    &lt;body&gt;
&lt;?php
$localhost = "localhost";
$username = "root";
$password = "";
$connect = mysqli_connect($localhost, $username, $password) or die ("Kunde inte koppla");
mysqli_select_db($connect, 'wildfire');

$qid = 1;
if(count($_POST) &gt; 0){
    $qid = intval($_POST['qid'])+1;

}


?&gt;

&lt;form method="post" action=""&gt;
&lt;input type="hidden" name="qid" id="qid" value="&lt;?=$qid?&gt;"&gt;
&lt;?php
$sql1 = mysqli_query($connect,"SELECT * FROM question where answer != '' &amp;&amp; qid =".intval($qid));
while($row1=mysqli_fetch_assoc($sql1)){
?&gt;
&lt;input type='radio' name='answer1' class="radiobtn" value="&lt;?php echo $row1['Point'];?&gt;"&gt;
&lt;input type='hidden' name='tid' class="tid" value="&lt;?php echo $row1['tid'];?&gt;"&gt;
&lt;?php echo $row1['answer'];?&gt;&lt;br&gt;
&lt;?php
}
?&gt;
&lt;?php if ($qid &lt;= 8) {  ?&gt;
&lt;button type="button" onclick="history.back();"&gt;Tillbaka&lt;/button&gt;
&lt;button type="submit"&gt;Nästa&lt;/button&gt;
&lt;?php } else { ?&gt;
&lt;button id="submitAjax" type="submit"&gt;Avsluta provet&lt;/button&gt;
     &lt;?php } ?&gt;  
&lt;/form&gt;

&lt;script src="https://code.jquery.com/jquery-1.11.3.js"&gt;&lt;/script&gt; 
  &lt;script type="text/javascript"&gt;
function goBack() {
    window.history.go(-1);
}
$(document).ready(function(){ 
$("#submitAjax").click(function(){
        if($('.radiobtn').is(':checked')) { 
            var radiobtn = $('.radiobtn:checked').val();
            var qid = $('#qid').val();            
             var answer = $('input[name=answer1]:radio').val();
            $.ajax(
            {
                type: "GET",
                url: 'test.php',
                dataType: "json",
                data: "radiobtn="+radiobtn+"&amp;qid="+qid,
                success: function (response) {
                    if(response.status == true){
                        alert('points added');
                    }
                    else{
                        alert('points not added');   
                    }
                }
            });

            return false;
        }
    });
});
  &lt;/script&gt;

    &lt;/body&gt;
</code></pre>

<p>The values that I want to send to my database from test.php are:</p>

<p>qid(int), tid(int), Point(int)</p>

<p>There is a database connection, and my test.php file's sql query should work, but its not sending form information. Is there something that I need to rewrite or fix to make it work? </p>

## Answers
### Answer ID: 34616207
<p><strong>First</strong>, your data parameter in the AJAX call is not using the correct syntax.  You're missing brackets.  It should look like:</p>

<pre><code>data: JSON.stringify({ radiobtn: radiobtn, qid: qid }),
</code></pre>

<p><strong>Second</strong>, I'd suggest using POST instead of GET:</p>

<pre><code>type: "POST",
</code></pre>

<p>which means that you need to look for your data in $_POST['radiobtn'] and $_POST['qid'] on test.php.  NOTE:  you should check for the key you expect using <a href="http://php.net/manual/en/function.isset.php" rel="nofollow">isset()</a> before assigning the value to a variable, like so:</p>

<pre><code>$myBtn = isset($_POST['radiobtn']) ? $_POST['radiobtn'] : null;
</code></pre>

<p><strong>Third</strong>, for testing, use a console.log() inside your condition that checks for the checkbox being checked in order to verify that condition is working as expected.</p>

<pre><code>if($('.radiobtn').is(':checked')) {
    console.log('here');
</code></pre>

<h2><strong>UPDATE:</strong></h2>

<p><strong>Fourth:</strong>  You should specify the content type in your AJAX call, like so:</p>

<pre><code>contentType: "application/json; charset=utf-8",
</code></pre>

### Answer ID: 34616151
<blockquote>
  <p><a href="http://php.net/manual/en/mysqli.insert-id.php" rel="nofollow">mysqli_insert_id()</a> <em>returns the ID generated by a query on a table with a column having the <code>AUTO_INCREMENT</code> attribute.</em></p>
</blockquote>

<p>In your SQL, you are providing the ID yourself, there is no auto-increment. So you should get <strong>0</strong> from <code>$connect-&gt;insert_id</code>, because <em>the function returns zero if there was no previous query on the connection or if the query did not update an <code>AUTO_INCREMENT</code> value</em>. </p>

<p>For your purpose, you can use the <code>return</code> value of <a href="http://php.net/manual/en/mysqli.query.php" rel="nofollow">mysqli_query()</a> instead, which returns <code>TRUE</code> on success and <code>FALSE</code> on failure. </p>

<pre><code>if($connect-&gt;query($sql2)) {
   echo json_encode(array('status'=&gt;1));
}
else{
   echo json_encode(array('status'=&gt;0));
} 
</code></pre>

### Answer ID: 34616443
<p>After you execute your query that inserts the result you can use a sql statement to select the last insert id. Try something like</p>

<pre><code>$sql2 = "INSERT INTO result (qid, points, tid) VALUES ($qid, $answerPoint,         $tid)";
$connect-&gt;query($sql2); 
$result = $connect-&gt;query("SELECT LAST_INSERT_ID()");
$row = $result-&gt;fetch_row();
$lastid = $row[0];
</code></pre>

<p>That should return the correct last insert id, if that was where your error was occurring.</p>

