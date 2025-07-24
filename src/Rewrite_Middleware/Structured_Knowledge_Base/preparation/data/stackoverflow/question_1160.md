# HTML displayed as text
[Link to question](https://stackoverflow.com/questions/61448217/html-displayed-as-text)
**Creation Date:** 1587935752
**Score:** 0
**Tags:** php, html
## Question Body
<p>I have a <strong>.php</strong> file which contains html code. The issue I am having is that it's being displayed as text, not as html elements. I have found several other questions regarding the same problem:</p>

<p><a href="https://stackoverflow.com/questions/46107855/why-is-this-html-showing-up-as-plain-text-in-browser">Why is this HTML showing up as plain text in browser?</a></p>

<p><a href="https://stackoverflow.com/questions/14439513/browser-shows-plain-text-instead-of-html-in-mac">Browser shows plain text instead of HTML in mac</a></p>

<p><a href="https://stackoverflow.com/questions/21066660/page-shows-code-not-rendering">Page shows code not rendering</a></p>

<p>However, I believe that everything the people suggested there applies to my code.</p>

<p>My code:</p>

<pre><code>&lt;?php
// required headers
header("Access-Control-Allow-Origin: null");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Max-Age: 3600");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

// files needed to connect to database
include_once '../config/database.php';

// get database connection
$database = new Database();
$conn = $database-&gt;getConnection();

$error = "";
if (isset($_GET["key"]) &amp;&amp; isset($_GET["email"]) &amp;&amp; isset($_GET["action"]) &amp;&amp; ($_GET["action"]=="reset") &amp;&amp; !isset($_POST["action"])) {
    $key = $_GET["key"];
    $email = $_GET["email"];
    $curDate = date("Y-m-d H:i:s");

    $query = "SELECT * FROM password_reset_temp WHERE email=:email AND `key`=:key";
    $stmt = $conn-&gt;prepare($query);
    $stmt-&gt;bindParam(":key", $key);
    $stmt-&gt;bindParam(":email", $email);
    try {
        $stmt-&gt;execute();
    } catch (PDOException $e) {
        echo json_encode(array("message" =&gt; $e-&gt;getMessage()));
    }
    if ($stmt-&gt;rowCount() == 0) {
        $error .= '&lt;h2&gt;Invalid Link&lt;/h2&gt;
        &lt;p&gt;The link is invalid/expired. Either you did not copy the correct link
        from the email, or you have already used the key in which case it is 
        deactivated.&lt;/p&gt;
        &lt;p&gt;&lt;a href="..."&gt;
        Click here&lt;/a&gt; to reset password.&lt;/p&gt;';
    } else {
        $row = $stmt-&gt;fetch();
        $expDate = $row['expDate'];
        if ($expDate &gt;= $curDate){
// the part that is not showing begins here                
?&gt;
            &lt;br /&gt;
            &lt;form method="post" action="" name="update"&gt;
            &lt;input type="hidden" name="action" value="update" /&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;label&gt;&lt;strong&gt;Enter New Password:&lt;/strong&gt;&lt;/label&gt;&lt;br /&gt;
            &lt;input type="password" name="pass1" maxlength="15" required /&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;label&gt;&lt;strong&gt;Re-Enter New Password:&lt;/strong&gt;&lt;/label&gt;&lt;br /&gt;
            &lt;input type="password" name="pass2" maxlength="15" required/&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;input type="hidden" name="email" value="&lt;?php echo $email;?&gt;"/&gt;
            &lt;input type="submit" value="Reset Password" /&gt;
            &lt;/form&gt;
            &lt;?php
        } else {
            $error .= "&lt;h2&gt;Link Expired&lt;/h2&gt;
            &lt;p&gt;The link is expired. You are trying to use the expired link which 
            as valid only 24 hours (1 days after request).&lt;br /&gt;&lt;br /&gt;&lt;/p&gt;";
        }
    }
    if($error!=""){
        echo "&lt;div class='error'&gt;".$error."&lt;/div&gt;&lt;br /&gt;";
    } 
} // isset email key validate end


if(isset($_POST["email"]) &amp;&amp; isset($_POST["action"]) &amp;&amp;
 ($_POST["action"]=="update")){
$error="";
$pass1 = mysqli_real_escape_string($con,$_POST["pass1"]);
$pass2 = mysqli_real_escape_string($con,$_POST["pass2"]);
$email = $_POST["email"];
$curDate = date("Y-m-d H:i:s");
if ($pass1!=$pass2){
$error.= "&lt;p&gt;Password do not match, both password should be same.&lt;br /&gt;&lt;br /&gt;&lt;/p&gt;";
  }
  if($error!=""){
echo "&lt;div class='error'&gt;".$error."&lt;/div&gt;&lt;br /&gt;";
}else{
$pass1 = md5($pass1);
mysqli_query($con,
"UPDATE `users` SET `password`='".$pass1."', `trn_date`='".$curDate."' 
WHERE `email`='".$email."';"
);

mysqli_query($con,"DELETE FROM `password_reset_temp` WHERE `email`='".$email."';");

echo '&lt;div class="error"&gt;&lt;p&gt;Congratulations! Your password has been updated successfully.&lt;/p&gt;
&lt;p&gt;&lt;a href="..."&gt;
Click here&lt;/a&gt; to Login.&lt;/p&gt;&lt;/div&gt;&lt;br /&gt;';
   } 
}
?&gt;
</code></pre>

<p>My .htaccess looks like this </p>

<pre><code># Turn on the rewrite engine
RewriteEngine  on
# If the request doesn't end in .php (Case insensitive) continue processing rules
RewriteCond %{REQUEST_URI} !\.php$ [NC]
# If the request doesn't end in a slash continue processing the rules
RewriteCond %{REQUEST_URI} [^/]$
# Rewrite the request with a .php extension. L means this is the 'Last' rule
RewriteRule ^(.*)$ $1.php [L]
</code></pre>

<p>The output:</p>

<pre><code>&lt;br /&gt;
            &lt;form method="post" action="" name="update"&gt;
            &lt;input type="hidden" name="action" value="update" /&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;label&gt;&lt;strong&gt;Enter New Password:&lt;/strong&gt;&lt;/label&gt;&lt;br /&gt;
            &lt;input type="password" name="pass1" maxlength="15" required /&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;label&gt;&lt;strong&gt;Re-Enter New Password:&lt;/strong&gt;&lt;/label&gt;&lt;br /&gt;
            &lt;input type="password" name="pass2" maxlength="15" required/&gt;
            &lt;br /&gt;&lt;br /&gt;
            &lt;input type="hidden" name="email" value="..."/&gt;
            &lt;input type="submit" value="Reset Password" /&gt;
            &lt;/form&gt;
</code></pre>

<p>All the other <strong>.php</strong> files in that directory work perfectly. If you need any other information, let me know.</p>

## Answers
### Answer ID: 61448257
<blockquote>
<pre><code>header("Content-Type: application/json; charset=UTF-8");
</code></pre>
</blockquote>

<p>You said it was JSON and not HTML.</p>

<p>The browser is trying to treat it as JSON, failing, and showing it as text instead.</p>

