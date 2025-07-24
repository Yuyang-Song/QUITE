# Modification to existing .htaccess (using PHP)
[Link to question](https://stackoverflow.com/questions/9813337/modification-to-existing-htaccess-using-php)
**Creation Date:** 1332366307
**Score:** 1
**Tags:** .htaccess, url-rewriting
## Question Body
<p>I am using URL rewriting via htaccess. Following are contents:</p>

<pre><code>Options +FollowSymLinks
RewriteEngine on
#RewriteBase /
RewriteCond  %{REQUEST_FILENAME} !-f
RewriteCond  %{REQUEST_FILENAME} !-d

RewriteRule ^([0-9a-zA-Z_-]+)\.php$ index.php?slug=$1 [L]
</code></pre>

<p>My current navigation menu structure:</p>

<pre><code>&lt;a href="home.php"&gt;Home&lt;/a&gt;
&lt;a href="about-us.php"&gt;About Us&lt;/a&gt;
&lt;a href="contact-us.php"&gt;Contact Us&lt;/a&gt;
</code></pre>

<p>I have database column called slug and by using $_GET['slug'], I am able to query the DB and show the results. So far, its working fine.</p>

<p><strong>WHAT I AM TRYING TO DO:</strong></p>

<p>I am trying to let user change the language in which reads the text. I have 2 flag images and they are hyperlinked (there are actually more languages).</p>

<p><strong>Examples:</strong></p>

<pre><code>&lt;a href="&lt;?php echo '?lang=en'; ?&gt;"&gt;English&lt;/a&gt;
&lt;a href="&lt;?php echo '?lang=pt'; ?&gt;"&gt;Portugese&lt;/a&gt;
</code></pre>

<p>I have added another line in .htaccess:</p>

<pre><code>RewriteRule ^([0-9a-zA-Z_-]+)\.php?lang=[a-z]$ index.php?slug=$1&amp;lang=$2 [L,QSA]
</code></pre>

<p>So lets say I am currently on About us page. The url would read as:
<a href="http://localhost/mysite/about-us.php" rel="nofollow">http://localhost/mysite/about-us.php</a></p>

<p>Now lets say I click on "pt" to change language, the page navigates to:
<a href="http://localhost/mysite/about-us.php?lang=pt" rel="nofollow">http://localhost/mysite/about-us.php?lang=pt</a></p>

<p>If I echo $_GET['lang'] now, it gives me PHP notice: </p>

<pre><code>Notice: Undefined index: lang
</code></pre>

<p>Because the $_GET['lang'] is not defined, I am unable to grab its value and hence, I am unable to query the database. I also want to make sure that I arrive on the same page as I was on, when I made the request to change the language. So if I was on Contact Us page and I clicked on the flag to change language to PT, I expect the page to reload, with/without showing the ?lang=pt in URL and I want to be able to grab this value using $_GET['lang'] so that I can query the DB. How to do this?</p>

## Answers
### Answer ID: 9813502
<p>Your other rule isn't going to work:</p>

<pre><code>RewriteRule ^([0-9a-zA-Z_-]+)\.php?lang=[a-z]$ index.php?slug=$1&amp;lang=$2 [L,QSA]
</code></pre>

<p>The query string isn't part of the URI and won't be matched by your regular expression: <code>^([0-9a-zA-Z_-]+)\.php?lang=[a-z]$</code>, you'll need to use a <code>RewriteCond %{QUERY_STRING} (your regex)</code> and a <strong>%1</strong> back reference. The other thing is there is no <strong>$2</strong> backreference, since there's only one parentheses in your regular expression, so that's always going to be blank. However, you don't really need this as your original rule is fine, you just need to add a <strong>QSA</strong> as an option in the brackets:</p>

<pre><code>RewriteRule ^([0-9a-zA-Z_-]+)\.php$ index.php?slug=$1 [L,QSA]
</code></pre>

<p>This means whatever existing query string in the request gets appended to the target. So:</p>

<pre><code>http://localhost/mysite/about-us.php --&gt; index.php?slug=about-us
http://localhost/mysite/about-us.php?lang=pt --&gt; index.php?slug=about-us&amp;lang=pt
</code></pre>

<p>The query string <code>lang=pt</code> in the second request simply gets appended in the rewrite target.</p>

