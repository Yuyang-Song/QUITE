# PHP Magic Quotes quick fix
[Link to question](https://stackoverflow.com/questions/4259676/php-magic-quotes-quick-fix)
**Creation Date:** 1290538571
**Score:** 1
**Tags:** php, security, sql-injection
## Question Body
<p>My Magic_Quotes has always been on and only today I've seen it's becoming depriciated. If I have it off could I just escape all user input (whether it's being used in my database or not). I definitely can't go back and rewrite all my database queries to use mysql_real_escape_string().</p>

<p>Could I just loop through all my $_GET, $_POST and $_SESSION and apply mysql_real_escape_string() ?</p>

## Answers
### Answer ID: 36579683
<p><a href="https://stackoverflow.com/a/520298/6194547">See here click</a></p>

<p>This is the method I use. If you are using case method switch, simply connect the index.php file. <strong><em>second method, you need to add to each page.</em></strong></p>

<blockquote>
  <ol>
  <li>index.php?page=home</li>
  <li>index.php?page=two ...</li>
  </ol>
</blockquote>

<p><strong>SECOND METHOD ADD CODE PER PAGE</strong></p>

<blockquote>
  <ol>
  <li>index.php</li>
  <li>contact.php</li>
  <li>product.php ....</li>
  </ol>
</blockquote>

<p>Recommended : simple page query case / switch</p>

<pre><code>// Magic Quotes Fix
if (ini_get('magic_quotes_gpc')) {
    function clean($data) {
        if (is_array($data)) {
            foreach ($data as $key =&gt; $value) {
                $data[clean($key)] = clean($value);
            }
        } else {
            $data = stripslashes($data);
        }

        return $data;
    }           

    $_GET = clean($_GET);
    $_POST = clean($_POST);
    $_REQUEST = clean($_REQUEST);
    $_COOKIE = clean($_COOKIE);
}
</code></pre>

### Answer ID: 4259732
<p>Yes, you can,  but don't forget that you can also send arrays via GPC.  <code>?var[1]=data</code>.  It should be noted that magic_quotes_gpc was removed for a damn good reason and I bet many beers that your application is highly vulnerable to sql injection. </p>

<pre><code>if (!get_magic_quotes_gpc()) {
    function my_escape(&amp;$value, $key) {$value = mysql_real_escape_string($value);}
    $gpc = array(&amp;$_GET, &amp;$_POST, &amp;$_COOKIE, &amp;$_REQUEST);
    array_walk_recursive($gpc, 'my_escape');
}
</code></pre>

### Answer ID: 4259713
<p><code>mysql_real_escape_string</code> and <code>magic_quotes_gpc</code> are two different things. Magic quotes does not render your input safe enough for SQL queries.</p>

<p>Whether you like it or not, you <strong>should</strong> convert all your database queries to use a proper escaping mechanism, or you otherwise leave your application open to security issues like SQL injection.</p>

<p>You can't really apply <code>mysql_real_escape_string</code> directly on $_GET, $_POST, etc. because it might mess up your input data if you need it for anything else than SQL (like form validation and such).</p>

### Answer ID: 4259730
<p>Turn it off. The pain of recoding by hand, case by case, pales compared to the agony of being hacked.</p>

