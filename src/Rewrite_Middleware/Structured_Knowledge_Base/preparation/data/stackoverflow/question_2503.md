# Htaccess Mod Rewrite Not working for Pretty URL
[Link to question](https://stackoverflow.com/questions/37557133/htaccess-mod-rewrite-not-working-for-pretty-url)
**Creation Date:** 1464736822
**Score:** 2
**Tags:** apache, .htaccess, mod-rewrite
## Question Body
<p>I feel like such a tool for having to post this question, but for the life of me, I cannot figure out how to resolve my issue. (I've also read/tried previous posts but none have helped me)</p>

<p>I'm trying to turn <a href="https://mywebsite.com/article.php?slug=pretty-url" rel="nofollow">https://mywebsite.com/article.php?slug=pretty-url</a> to <a href="https://mywebsite.com/article/pretty-url" rel="nofollow">https://mywebsite.com/article/pretty-url</a></p>

<p>The problem I'm having is the <code>$_GET</code> method is not recognizing the slug, so it's giving me a 404 error. The slug is definitely in my database. I'm not sure why I cannot retrieve it.</p>

<p>Below is my htaccess code and my php code to call the page.</p>

<p>Htaccess Code:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
Options +FollowSymLinks
RewriteEngine On

# Redirect www urls to non-www
RewriteEngine on
RewriteCond %{HTTP_HOST} ^www\.mywebsite\.com [NC]
RewriteRule (.*) https://mywebsite.com/$1 [L]

RewriteEngine On 
RewriteCond %{SERVER_PORT} 80 
RewriteRule ^(.*)$ https://mywebsite.com/$1 [L]

ErrorDocument 404 /404.php

#Pretty URL for Blog
RewriteRule ^article/([0-9a-zA-Z]+) article.php?slug=$1


#Rewrite for certain files with .php extension
RewriteRule ^about$ about.php
RewriteRule ^services$ services.php
RewriteRule ^portfolio$ portfolio.php
RewriteRule ^blogs$ blogs.php
RewriteRule ^tutorials$ tutorials.php
RewriteRule ^contact$ contact.php
RewriteRule ^privacy-policy$ privacy-policy.php
RewriteRule ^terms-of-service$ terms-of-service.php
RewriteRule ^sitemap$ sitemap.php
&lt;/IfModule&gt;
</code></pre>

<p>PHP Code on the article.php page:</p>

<pre><code>//Get the blog. Only blogs that are published
$slug = $_GET['slug'];
$publish = intval(1);

//Query the database
$sql =  "SELECT * FROM blogs WHERE publish = $publish AND slug = $slug";   


//Execute the query
$stmt = $db-&gt;query($sql); 
$row = $stmt-&gt;fetch(PDO::FETCH_ASSOC);
</code></pre>

## Answers
### Answer ID: 37582651
<p><code>([0-9a-zA-Z]+)</code> will not capture <code>pretty-url</code> because the group doesn't allow for hyphens. Change that to <code>([A-Za-z0-9-]+)</code> and add <code>[L]</code> to the end of that line.</p>

<p>Also, for the sake of doing things properly, remove the second and third calls to <code>RewriteEngine On</code>.</p>

### Answer ID: 37566273
<p>Never apologise for a question! If you're stuck, we will try to help.</p>

<p>What you need in your htaccess is the following:</p>

<pre><code>RewriteEngine On
RewriteRule ^([^/]*)\.html$ /article.php?slug=$1 [L]
</code></pre>

<p>That should change your url to <a href="https://mywebsite.com/pretty-url.html" rel="nofollow">https://mywebsite.com/pretty-url.html</a></p>

