# How do I re-write this code without using PEAR::DB?
[Link to question](https://stackoverflow.com/questions/2395513/how-do-i-re-write-this-code-without-using-peardb)
**Creation Date:** 1267946990
**Score:** -2
**Tags:** php, twitter, oauth, pear
## Question Body
<p>I am trying to install the <a href="http://pligg.com/" rel="nofollow noreferrer">Pligg</a> Twitter login module from <em><a href="http://blog.eamonnfaherty.co.uk/2009/08/08/log-into-pligg-using-twitter-oauth/" rel="nofollow noreferrer">Log into Pligg using Twitter OAuth</a></em>.</p>

<p>I downloaded the ZIP file from the above page and followed all the instructions. Then I realized one of the files are using <a href="http://en.wikipedia.org/wiki/PEAR" rel="nofollow noreferrer">PEAR</a>, which is not provided by my hosting company.</p>

<p>The entire code from <code>confirm.php</code> is here:</p>

<p>How do I rewrite this code so I don't have to use PEAR? Is that even possible? I am a really a novice with PHP.</p>

<pre><code>&lt;?php
include 'EpiCurl.php';
include 'EpiOAuth.php';
include 'EpiTwitter.php';
include 'secret.php';
require_once 'DB.php';

$twitterObj = new EpiTwitter($consumer_key, $consumer_secret);

$twitterObj-&gt;setToken($_GET['oauth_token']);
$token = $twitterObj-&gt;getAccessToken();
$twitterObj-&gt;setToken($token-&gt;oauth_token, $token-&gt;oauth_token_secret);

try {
    setcookie('oauth_token', $token-&gt;oauth_token);
    setcookie('oauth_token_secret', $token-&gt;oauth_token_secret);

    $twitterInfo= $twitterObj-&gt;get_accountVerify_credentials();
    $twitterUserName = $twitterInfo-&gt;screen_name;
    $twitterAvatar = $twitterInfo-&gt;profile_image_url;
} catch (Exception $e) {
    die("Sorry, there was an error connecting to twitter:".$e-&gt;getMessage());
}

$DB =&amp; DB::connect('mysqli://USER:PASS@localhost/DB');
if (DB::isError($DB))
{
    echo 'Cannot connect to database: ' . $DB-&gt;getMessage();
}
else
{
    $query = 'select twitter_user_name, pligg_user_name, pligg_password FROM twitter_user_map where twitter_user_name = ?';
    $result = $DB-&gt;query($query, $twitterUserName);
    if (DB::isError ($result)) {
             die ("Select failed: " . $result-&gt;getMessage () . "\n");
        }
    $userDetails = $result-&gt;fetchRow(DB_FETCHMODE_OBJECT);
    if ($result-&gt;numRows() == 0) {
        createAccount($DB,$twitterUserName, 0, $twitterUserName);
    } else {
        redirectToLogin($userDetails-&gt;pligg_user_name, $userDetails-&gt;pligg_password);
    }
}

function createAccount($DB, $username, $delta, $twitterUsername) {
    $pass = genRandomString();
    $query = "insert into twitter_user_map( twitter_user_name, pligg_user_name, pligg_password) values ('$twitterUsername', '$username','$pass' )";
    $result = $DB-&gt;query($query);
    if (DB::isError ($result)) {
         die ("INSERT failed: " . $result-&gt;getMessage () . "\n");
    }
    if ($DB-&gt;affectedRows() == 0) {
        $newUsername = $twitterUsername;
        if ($delta != 0) {
            $newUsername = $username . "" . $delta;
        }
        createAccount($DB,$newUsername, $delta + 1, $twitterUsername);
    } else {
        redirectToRegister($username, $pass);
    }
}

function redirectToRegister($username, $pass) {
    print "redirectToRegister";
    $postdata = http_build_query(
        array(
            'reg_username' =&gt; $username,
            'reg_email' =&gt; "",
            'reg_password' =&gt; $pass,
            'reg_password2' =&gt; $pass,
            'recaptcha_challenge_field' =&gt; '02kOXNvO91qx4TJ6dC8evG6SkqQvGlUfjxF8bvaurguiAsftwQYut68EfNxZh6ZYMTyqcrWNT4RooYxxfjueRVFIkcN_UwRI-J6bjWZczbLk4p0Tqml6tVHQeyocVvU0SwUKUn_kmtDV4Y7kGfbn-qyiYt55-iaFojc060MJ-jAZ68z5Vlw8xrvPRhLW6JAO1F2D6oAY7vsWI_e1Nmhww1lQ6qsL10W4wWrCWLywOIZVIZnsa5p61_IQf9Yn_NV-Nir_DCWxKMUZieZkL1pril6_kMaj0B',
            'recaptcha_response_field' =&gt; '',
            'regfrom' =&gt; "full",
            'from_external' =&gt; "1"
        )
    );
    $opts = array('http' =&gt;
        array(
            'method'  =&gt; 'POST',
            'header'  =&gt; 'Content-type: application/x-www-form-urlencoded',
            'content' =&gt; $postdata
        )
    );
    $context  = stream_context_create($opts);
    $result = file_get_contents('sitename/register.php', false, $context);
    print $result;
}

function redirectToLogin($username, $password) {
    $postdata = http_build_query(
        array(
            'username' =&gt; $username,
            'password' =&gt; $password,
            'persistent' =&gt; "on",
            'from_external' =&gt; "1"
        )
    );
    $opts = array('http' =&gt;
        array(
            'method'  =&gt; 'POST',
            'header'  =&gt; 'Content-type: application/x-www-form-urlencoded',
            'content' =&gt; $postdata
        )
    );
    $context  = stream_context_create($opts);
    $result = file_get_contents('sitename/login.php', false, $context);
    print $result;
}

function genRandomString() {
    $length = 10;
    $characters = '123456789abcdefghijklmnopqrstuvwxyz';
    $string = '';
    for ($p = 0; $p &lt; $length; $p++) {
        $string .= $characters[mt_rand(0, strlen($characters))];
    }
    return $string;
}

?&gt;
</code></pre>

<p><strong>Update</strong></p>

<p>From <a href="http://docstore.mik.ua/orelly/webprog/php/ch08_03.htm" rel="nofollow noreferrer">PEAR DB Basics</a>,</p>

<blockquote>
  <p>Example 8-1 is a program to build an HTML table of information about James Bond movies. It demonstrates how to use the PEAR DB library (which comes with PHP) to connect to a database, issue queries, check for errors, and transform the results of queries into HTML. The library is object-oriented, with a mixture of class methods (DB::connect( ), DB::iserror( )) and object methods ($db->query( ), $q->fetchInto( )).</p>
</blockquote>

<p>Yeah. I guess it is not that hard to re-write this thing. I will figure it out.</p>

## Answers
### Answer ID: 2395535
<p>PEAR is nothing more than another PHP script and can be installed to the any hosting manually.
And I guess there is no way to "show a way to rewrite", this is more likely "rewrite this code for me" question.</p>

<p>or even pligg promotion question</p>

