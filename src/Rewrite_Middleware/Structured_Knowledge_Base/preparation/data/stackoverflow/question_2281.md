# PDO query with session doesn&#39;t return anything
[Link to question](https://stackoverflow.com/questions/27323019/pdo-query-with-session-doesnt-return-anything)
**Creation Date:** 1417806607
**Score:** 1
**Tags:** php, mysql, pdo
## Question Body
<p>I'm starting to learn <code>PDO</code> and while doing this decided to rewrite my old <code>mysql_*</code> code. So I have a login form which according to userlevel redirects to different locations. This is done (<code>I think since I can login correctly</code>). Next when redirects me I have query which depending of userlevel show some result from database. The problem is that it doesn't return anything and there are no errors in the logfile. This is my login. Am I doing it correctly?</p>

<pre><code>session_start();
if(isSet($_POST['submit'])) {
include 'misc/database.inc.php';
$pdo = Database::connect();

$username=$_POST['username']; 
$password=sha1($_POST['password']); 

    $stmt = $pdo-&gt;prepare("SELECT * FROM users WHERE username = :username AND password = :password");

    $stmt-&gt;bindParam(':username', $username);
    $stmt-&gt;bindParam(':password', $password);

    $stmt-&gt;execute();

    $res  = $stmt -&gt; fetch();

if ($res['userlevel'] == 1)
{
    // Save type and other information in Session for future use.
        $_SESSION['username'] = $username;
        $_SESSION['password'] = $password;
        $_SESSION['userlevel'] = $userlevel;

    header( "location: admins/main.php");   
}
elseif ( $res['userlevel'] &gt;= 4 ) 
{
        $_SESSION['user_id'] = $id; 
        $_SESSION['username'] = $username;
        $_SESSION['password'] = $password;
        $_SESSION['userlevel'] = $userlevel;
        $_SESSION['firstname'] = $firstname;
        $_SESSION['lastname'] = $lastname;
        $_SESSION['user_image'] = $user_image;
        $_SESSION['email'] = $email;    
        header('Location: users/main.php');
}
else 
{
    header("location: index.php");
}
// Closing MySQL database connection 
$pdo = null;
} else {
</code></pre>

<p>And this is the query which I want to perform in <code>main.php</code> when login according to userlevel</p>

<pre><code>&lt;?php
include '../misc/database.inc.php';
$pdo = Database::connect();
$q = "SELECT * FROM ras AS r 
    LEFT JOIN user_ras AS r2u ON r.userlevel = r2u.ras_userlevel
    LEFT JOIN users AS u ON r2u.user_userlevel = u.userlevel where menu = '".$_SESSION['userlevel']."'";

foreach($pdo-&gt;query($q) as $res)
{
    echo '&lt;a href="users/ras.php?rest_id='. $res['ras_id'] .'"&gt;'.$res['name'].'&lt;/a&gt;';

 }
 Database::disconnect();
 ?&gt;
</code></pre>

<p>As I said I'm completely new to PDO so please bear with me and if you can help me. Thank you.</p>

<p><strong>Update - database.inc.php</strong></p>

<pre><code>&lt;?php
class Database
{
private static $dbName = 'dbname' ;
private static $dbHost = 'localhost' ;
private static $dbUsername = 'user';
private static $dbUserPassword = 'pass';

private static $cont  = null;

public function __construct() {
    die('Init function is not allowed');
}

public static function connect()
{
   // One connection through whole application
   if ( null == self::$cont )
   {     
    try
    {
      self::$cont =  new PDO( "mysql:host=".self::$dbHost.";"."dbname=".self::$dbName, self::$dbUsername, self::$dbUserPassword); 
    }
    catch(PDOException $e)
    {
      die($e-&gt;getMessage()); 
    }
   }
   return self::$cont;
}

public static function disconnect()
{
    self::$cont = null;
}
}
?&gt;
</code></pre>

## Answers
### Answer ID: 27323349
<p>where are the variables defined that you are assigning to session  <code>$id, $userlevel, $firstname, $lastname, $user_image, $email</code> ?
They are undefined at this point:</p>

<pre><code>    $_SESSION['user_id']   = $id; 
    $_SESSION['userlevel'] = $userlevel;
    $_SESSION['firstname'] = $firstname;
    $_SESSION['lastname']  = $lastname;
    $_SESSION['user_image']= $user_image;
    $_SESSION['email']     = $email; 
</code></pre>

<p>I think what you need is this</p>

<pre><code>session_start();
if(isSet($_POST['submit'])) {
include 'misc/database.inc.php';
$pdo = Database::connect();

$username=$_POST['username']; 
$password=sha1($_POST['password']); 

    $stmt = $pdo-&gt;prepare("SELECT * FROM users WHERE username = :username AND password = :password");

    $stmt-&gt;bindParam(':username', $username);
    $stmt-&gt;bindParam(':password', $password);

    $stmt-&gt;execute();

    $res  = $stmt -&gt; fetch();

if ($res['userlevel'] == 1)
{
    // Save type and other information in Session for future use.
        $_SESSION['username'] = $username;
        $_SESSION['password'] = $password;
        $_SESSION['userlevel'] = $res['userlevel'];

    header( "location: admins/main.php");   
}
elseif ( $res['userlevel'] &gt;= 4 ) 
{
        $_SESSION['user_id']   = $res['id'];
        $_SESSION['username'] = $username;
        $_SESSION['password'] = $password;  
        $_SESSION['userlevel'] = $res['userlevel'];
        $_SESSION['firstname'] = $res['firstname'];
        $_SESSION['lastname']  = $res['lastname'];
        $_SESSION['user_image']= $res['user_image'];
        $_SESSION['email']     = $res['email']; 
        header('Location: users/main.php');
}
else 
{
    header("location: index.php");
}
}
</code></pre>

### Answer ID: 27323263
<p>You should check to see if you have a result set.</p>

<pre><code>    if ($res) {

    foreach($pdo-&gt;query($q) as $res)
    {
        echo '&lt;a href="users/ras.php?rest_id='. $res['ras_id'] .'"&gt;'.$res['name'].'&lt;/a&gt;';

     }
    } else {
    echo '&lt;p&gt;no result&lt;/p&gt;';
   }
</code></pre>

### Answer ID: 27323125
<p>Can you echo the contents of <code>$res</code>?
such as: </p>

<pre><code>echo "&lt;pre&gt;";
print_r($res);
echo "&lt;pre&gt;";
</code></pre>

<p>and see what the result is, maybe your array doesn't know the value of <code>$res['userlevel']</code>, your array might be accessed as <code>$res[0]['userlevel']</code> or something like that.</p>

<p>Let me know if it works</p>

