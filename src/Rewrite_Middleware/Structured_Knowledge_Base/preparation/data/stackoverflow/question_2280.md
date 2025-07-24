# JQuery and AJAX .post return undefined index in PHP
[Link to question](https://stackoverflow.com/questions/27263061/jquery-and-ajax-post-return-undefined-index-in-php)
**Creation Date:** 1417576790
**Score:** 1
**Tags:** php, jquery, ajax, post
## Question Body
<p>I realize this question has been answered numerous times, but I can't seem to find a solution that works. I've been stuck on this all day and am about to lose my mind. Everything seems to work fine, the data is correct, it just isn't getting passed to the PHP. I've tried using both .post with jquery and ajax. </p>

<p>The HTML and JQuery/AJAX</p>

<pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt; Today's Clients&lt;/title&gt;

&lt;link href="../_css/jquery-ui.min.css"&gt;
&lt;script src="../_js/jquery.min.js"&gt;&lt;/script&gt;
&lt;script src="../_js/jquery-ui.min.js"&gt;&lt;/script&gt;

&lt;script&gt;
$(document).ready(function(){
    $(".clientSubmit").submit(function(event) {
        event.preventDefault();
        var clientInformation = $(this).serialize();
        $.post('IRCpopulatecheckin.php',clientInformation,clientForm);
        function clientForm(data) {
            if (data!='') {
                $('#clientform').load("IRCpopulatecheckin.php");
                alert(clientInformation);
            } else {
                alert("your data returned nothing!!! rewrite the code...");
            }
        } // end clientForm
    }); // end .submit  
}); // end ready

/*

    $(".clientSubmit").submit(function() {
        var clientInformation = $(this).serialize();
    $.ajax({
        type: 'POST',
        url: 'IRCpopulatecheckin.php',
        data: { 'clientInformation':clientInformation },
        cache: false,
        success: function(result){
            $('#clientform').load("IRCpopulatecheckin.php");
            alert(clientInformation);
            } // end result
        }) // end .ajax
    return false;
    }); // end .submit

*/
&lt;/script&gt;

&lt;style&gt;

/* css to style and remove everything but text */
    #hiddenInput {
                position    :relative;
                width       :0px;
                height      :8px;
                top         :-40px;
                left        :-230px;260
                }
    input[name="dailyClient"] {
                background-color: white;
                border: none;
                font-weight :bold;
                font-family :sans-serif;
                font-size: 15px;  
                color: black;
                cursor: default;
                line-height: normal;
                padding: 6px;
                text-align: center;
                text-shadow: none;
                white-space: pre;
                }

    input[name="dailyClient"]:hover {
                color: blue;
                }
&lt;/style&gt;                
&lt;body&gt;
&lt;div id="clientform"&gt;&lt;/div&gt;

&lt;?php 

ini_set('display_errors',1);  error_reporting(E_ALL);

if(isset($_POST['DATE'])) {
    $DATE = $_POST['DATE'];
    }else{
        $DATE = date('Y-m-d');
         }

require_once 'IRCconfig.php';

$connection = new mysqli($db_hostname, $db_username, $db_password, $db_database);
    if ($connection-&gt;connect_error) die($connection-&gt;connect_error);

$query  = "SELECT * FROM CLIENT_CHECKIN WHERE DATE&gt;='$DATE' ORDER BY F_NAME ASC";
    $result = $connection-&gt;query($query);

if (!$result) die ("Database access failed: " . $connection-&gt;error);

$rows = $result-&gt;num_rows;

for ($j = 0 ; $j &lt; $rows ; ++$j)
    {
        $result-&gt;data_seek($j);
        $row = $result-&gt;fetch_array(MYSQLI_NUM);

        echo &lt;&lt;&lt;_END
        &lt;pre&gt;
            &lt;div id="hiddenInput"&gt;&lt;div style="display:none"&gt;

            &lt;form class="clientSubmit" name="clientSubmit" action="IRCpopulatecheckin.php" method="POST"&gt;

            &lt;input type="hidden" name="DATE"   value="$row[0]"&gt;
            &lt;input type="hidden" name="F_NAME" value="$row[1]"&gt;
            &lt;input type="hidden" name="M_NAME" value="$row[2]"&gt;
            &lt;input type="hidden" name="L_NAME" value="$row[3]"&gt;

            &lt;/div&gt;&lt;/div&gt;

            &lt;input type="submit" name="dailyClient" value="$row[1] $row[2] $row[3]"&gt;&lt;/form&gt;
            &lt;/pre&gt;
_END;
    }

?&gt;
&lt;/body&gt;
&lt;/html&gt; 
</code></pre>

<p>Relevant PHP code</p>

<pre><code>&lt;?php  
//IRCpopulatecheckin.php
ini_set('display_errors',1);  error_reporting(E_ALL);
require_once 'IRCconfig.php';

$connection = new mysqli($db_hostname, $db_username, $db_password, $db_database);
    if ($connection-&gt;connect_error) die($connection-&gt;connect_error);

//Doesn't work
if(!isset($_POST['DATE'])){
    echo "something is wrong here"; 
}else{
    $DATE=$_POST["DATE"]; 
     }
if(!isset($_POST['F_NAME'])){
    echo "something is wrong here"; 
}else{
    $DATE=$_POST["F_NAME"]; 
     }
if(!isset($_POST['M_NAME'])){
    echo "something is wrong here"; 
}else{
    $M_NAME=$_POST["M_NAME"]; 
     }
if(!isset($_POST['L_NAME'])){
    echo "something is wrong here"; 
}else{
    $L_NAME=$_POST["L_NAME"]; 
     }


/*Doesn't work

$DATE   = isset($_GET['DATE'])   ? $_GET['DATE']   : $_POST['DATE'];
$F_NAME = isset($_GET['F_NAME']) ? $_GET['F_NAME'] : $_POST['F_NAME'];
$M_NAME = isset($_GET['M_NAME']) ? $_GET['M_NAME'] : $_POST['M_NAME'];
$L_NAME = isset($_GET['L_NAME']) ? $_GET['L_NAME'] : $_POST['L_NAME'];

*/


/* Doesn't work

if(isset($_POST['DATE']))
    $DATE = $_POST['DATE'];
if(isset($_POST['F_NAME']))
    $F_NAME = $_POST['F_NAME'];
if(isset($_POST['M_NAME']))
    $M_NAME = $_POST['M_NAME'];
if(isset($_POST['L_NAME']))
    $L_NAME = $_POST['L_NAME'];

*/

$query  = "SELECT * FROM CLIENT_CHECKIN WHERE DATE='$DATE' AND F_NAME='$F_NAME' AND M_NAME='$M_NAME' AND L_NAME='$L_NAME'";   
$result = $connection-&gt;query($query);
    if (!$result) die ("Database access failed: " . $connection-&gt;error);
</code></pre>

## Answers
### Answer ID: 27264127
<p>Try this. </p>

<pre><code>$(document).ready(function(){
   $(".clientSubmit").submit(function(e) {
       e.preventDefault();

       var $form = $(this); 
       var clientInfo = $form.serialize();

       console.log(clientInfo);

       $.ajax({
          type: 'POST',
          url: 'IRCpopulatecheckin.php',
          data: clientInfo,
          cache: false,
          success: function(result) {
              // try seeing if you can get this alert to pop up first
              alert(result);
              //$('#clientform').load("IRCpopulatecheckin.php");
          }
       }); // don't forget semi-colon
   });
});
</code></pre>

