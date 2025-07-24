# Php variable not holding data
[Link to question](https://stackoverflow.com/questions/35593269/php-variable-not-holding-data)
**Creation Date:** 1456288094
**Score:** 2
**Tags:** php, html, mysql, variables
## Question Body
<p>I am pretty new to php.  I have a php page that contains a form that uses GET to send the data.  When the form is submitted I have some PHP that queries a database. My issue: I set a variable named '$id3' that when I echo the var_dump right away shows the correct value.  If I echo the var_dump after my database query, it returns a 0.  What could be causing this variable to lose its value? Thanks. </p>

<p>EDIT:  I think I discovered that the id3 is being set once when the page is loaded, then again when the submit button of the form is pressed.  The second time it was rewriting the variable. I have now added an else on the <code>if (isset($_GET('1'])){</code>, but when i navigate to the next page my <code>$id3</code> is not set. </p>

<pre><code>&lt;?php  require_once('includes/connection.php'); ?&gt;
&lt;?php   



$pos = strpos($_SERVER['REQUEST_URI'],"=");
$pos2 = $pos - strlen($_SERVER['REQUEST_URI'])+1;

$fin = substr($_SERVER['REQUEST_URI'], $pos2);

$id3 = intval($fin);


echo var_dump($id3);


$error = array();

if ( isset($_GET['1']) ) {

    if ( sizeof($error) == 0 ) {
$q1 = mysqli_real_escape_string($mysqli, $_GET['1']);
$q2 = mysqli_real_escape_string($mysqli, $_GET['2']);
$q3 = mysqli_real_escape_string($mysqli, $_GET['3']);
$q4 = mysqli_real_escape_string($mysqli, $_GET['4']);
$q5 = mysqli_real_escape_string($mysqli, $_GET['5']);
$q6 = mysqli_real_escape_string($mysqli, $_GET['6']);
$q7 = mysqli_real_escape_string($mysqli, $_GET['7']);
$q8 = mysqli_real_escape_string($mysqli, $_GET['8']);
$q9 = mysqli_real_escape_string($mysqli, $_GET['9']);
$q10 = mysqli_real_escape_string($mysqli, $_GET['10']);
$q11 = mysqli_real_escape_string($mysqli, $_GET['11']);
$q12 = mysqli_real_escape_string($mysqli, $_GET['12']);
$q13 = mysqli_real_escape_string($mysqli, $_GET['13']);
$q14 = mysqli_real_escape_string($mysqli, $_GET['14']);
$q15 = mysqli_real_escape_string($mysqli, $_GET['15']);
$q16 = mysqli_real_escape_string($mysqli, $_GET['16']);
$q17 = mysqli_real_escape_string($mysqli, $_GET['17']);
$q18 = mysqli_real_escape_string($mysqli, $_GET['18']);
$q19 = mysqli_real_escape_string($mysqli, $_GET['19']);
$q20 = mysqli_real_escape_string($mysqli, $_GET['20']);
$q21 = mysqli_real_escape_string($mysqli, $_GET['21']);
$q22 = mysqli_real_escape_string($mysqli, $_GET['22']);
$q23 = mysqli_real_escape_string($mysqli, $_GET['23']);
$q24 = mysqli_real_escape_string($mysqli, $_GET['24']);
$q25 = mysqli_real_escape_string($mysqli, $_GET['25']);

$sql = "UPDATE ms2 SET 
q1='$q1',
q2='$q2',
q3='$q3',
q4='$q4',
q5='$q5',
q6='$q6',
q7='$q7',
q8='$q8',
q9='$q9',
q10='$q10',
q11='$q11',
q12='$q12',
q13='$q13',
q14='$q14',
q15='$q15',
q16='$q16',
q17='$q17',
q18='$q18',
q19='$q19',
q20='$q20',
q21='$q21',
q22='$q22',
q23='$q23',
q24='$q24',
q25='$q25' WHERE id=$id3";

$mysqli-&gt;query($sql);

//Check here of $id3 returns 0

header('Location: game.php?id='.$id3);        

        }
    }
?&gt;

&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
    &lt;head&gt;
        &lt;title&gt;Mobile Security Notifications&lt;/title&gt;
        &lt;meta name="apple-mobile-web-app-capable" content="yes" /&gt;
        &lt;meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1.0, maximum-scale=1.0" /&gt;
    &lt;link rel="stylesheet" href="css/bootstrap.min.css" /&gt;
    &lt;link rel="stylesheet" href="css/bootstrap-responsive.min.css" /&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;div class="container"&gt;
        &lt;div class="row"&gt;
            &lt;div class="span12"&gt;
                &lt;form class="form-horizontal" action="" method="GET"&gt;
                    &lt;!--25 question form here--&gt;    
                    &lt;div class="form-actions"&gt;
                        &lt;button type="submit" class="btn btn-success"&gt;Agree&lt;/button&gt;
                            &lt;a href="javascript:window.history.back();"class="btn"&gt;Cancel&lt;/a&gt;
                        &lt;/div&gt;
                    &lt;/form&gt;
                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/body&gt;
&lt;/html&gt;

&lt;?php require_once('includes/connection_end.php');?&gt;
</code></pre>

## Answers
### Answer ID: 35593964
<blockquote>
  <p>when i navigate to the next page my $id3 is not set.</p>
</blockquote>

<p>PHP does not hold data between different requests. The only data you can access here to are GET (from url) and POST (hidden) variables (+ external sources like user and server variables, cookies, database, file etc). 
Your "$id3" variable is in $_GET['id'] after you redirected user to game.php?id=$id3 location.</p>

<p>Moreover, you should use POST method to send that amount of data.</p>

