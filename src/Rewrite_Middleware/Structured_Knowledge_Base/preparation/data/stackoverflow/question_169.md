# HTACCESS: rewrite a uri request [properties/a-zto myphp php file
[Link to question](https://stackoverflow.com/questions/15419049/htaccess-rewrite-a-uri-request-properties-a-zto-myphp-php-file)
**Creation Date:** 1363291236
**Score:** 1
**Tags:** .htaccess, http-redirect, url-rewriting
## Question Body
<p>My goal is to achieve the following:</p>

<p><strong>My query:</strong> <code>properties.php?id=1234-N-StreetName-etc</code></p>

<p><strong>to be turned into:</strong></p>

<pre><code>properties/1234-N-Beverly-Blvd.html
</code></pre>

<p><code>properties.php</code> will evaluate the value of <code>$id</code> (In this case <code>any-address.html</code>) against a mysql database. If a value is not in the database, the file properties.php will redirect the user to a 404 page.
<strong>Where $id's value can be any combination of</strong> alphabetical characters, dash '-', or numbers.</p>

<p>The code I have is not working:</p>

<pre><code>Options +FollowSymlinks
RewriteEngine on
RewriteRule ^(.*)\.html$ $1.php [nc]
RewriteRule ^properties/([a-zA-Z0-9_-]+)\.html$ properties.php?id=$1
</code></pre>

<p>Can you please help me get the right htaccess rewrite-code?</p>

<p>PS. I know nothing about .htaccess. I modified this code form a sample website.</p>

## Answers
### Answer ID: 15420009
<p>You will need L flag to mark that rule as <strong>Last</strong> and QSA for <strong>Query String Append</strong>.</p>

<p>Use this code in .htaccess under <code>DOCUMENT_ROOT</code> directory:</p>

<pre><code>Options +FollowSymLinks -MultiViews
# Turn mod_rewrite on
RewriteEngine On
RewriteBase /

RewriteRule ^properties/([^.]+)\.html$ /properties.php?id=$1 [L,NC,QSA]
</code></pre>

<h3>To apply this rule in a sub directory sun use this code:</h3>

<pre><code>Options +FollowSymLinks -MultiViews
# Turn mod_rewrite on
RewriteEngine On
RewriteBase /sub

RewriteRule ^properties/([^.]+)\.html$ /sub/properties.php?id=$1 [L,NC,QSA]

# translate html -&gt; php
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{DOCUMENT_ROOT}/$1.php -f
RewriteRule ^([^.]+)\.html$ /$1.php [L,NC]
</code></pre>

<p>This will handle URI such as <code>/sub/properties/abc-123.html</code> and forward it to <code>/sub/properties.php?id=abc-123</code></p>

