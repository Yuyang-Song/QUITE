# rewrite urls for product name
[Link to question](https://stackoverflow.com/questions/8630457/rewrite-urls-for-product-name)
**Creation Date:** 1324830731
**Score:** 17
**Tags:** php, mysql, apache, .htaccess, mod-rewrite
## Question Body
<p>i want to rewrite a rule for my products.</p>

<p>i want to use the id and name in the url separated by a dash like this:</p>

<blockquote>
  <p>123-name means product id = 123 and name = name</p>
</blockquote>

<p>so in my php i can get the $_GET[id] and then query my database using this id like this:</p>

<pre><code>$sql = "SELECT * from Products Where productid = " . $_GET[id];
</code></pre>

<p>here's what i have:</p>

<pre><code>RewriteEngine On
RewriteRule ^products/([0-9+])\-([a-z]+)/?$ products.php?id=$2 [NC,L] 
</code></pre>

<p>but when i put this as url, i get a 404</p>

<p>why?</p>

## Answers
### Answer ID: 8630466
<p><strong>First:</strong> you have a syntax error. <code>[0-9+]</code> is a character class that can match (i) digits in the range <code>0</code> through <code>9</code>, or (ii) a <code>+</code> sign. To use the <code>+</code> as a quantifier (as intended), move the <code>+</code> after the <code>]</code>, like so: <code>([0-9]+)</code>.</p>

<p><strong>Second:</strong> You are using <code>$2</code> in your item which is the product name. If you want to use the ID, you have to use <code>$1</code>.</p>

<p>Here's what you need to use:</p>

<pre><code>RewriteEngine On
RewriteRule ^products/([0-9]+)\-([a-z0-9_\-]+)/?$ products.php?product_id=$1 [NC,L,QSA]
</code></pre>

<p><em>I added in the product numbers, dash and underscore in case you need it someday.</em></p>

<p><strong>Third:</strong> 
You should be aware of <a href="http://en.wikipedia.org/wiki/SQL_injection" rel="nofollow noreferrer">sql injections</a>, your script is not safe. You can fix this by using <a href="http://php.net/manual/en/function.mysql-real-escape-string.php" rel="nofollow noreferrer">mysql_real_escape_string</a>.</p>

### Answer ID: 8630499
<p>I think you should use products.php?id=$1 because the first argument matched is the product id.</p>

