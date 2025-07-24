# Using RewriteRule to write URL from page/unique_id to page.php?id=unique_id
[Link to question](https://stackoverflow.com/questions/32776443/using-rewriterule-to-write-url-from-page-unique-id-to-page-phpid-unique-id)
**Creation Date:** 1443163967
**Score:** 0
**Tags:** apache, .htaccess, url-rewriting, friendly-url
## Question Body
<p>I am trying to format my URL from <code>http://jacqueskoekemoer.co.za/article/5</code> to <code>http://jacqueskoekemoer.co.za/article?i=5</code> where <code>i</code> would be the article ID in the database.</p>

<p>Currently <a href="http://jacqueskoekemoer.co.za/article?i=5" rel="nofollow">this URL</a> works. But <a href="http://jacqueskoekemoer.co.za/article/5" rel="nofollow">this one</a> does not. It does change the url to <code>article.php</code> but it doesn't add the query string to the end.</p>

<p>I know this because it does not appear in <code>print_r($_REQUEST);</code> or <code>print_r($_GET);</code></p>

<p>What am I doing wrong in my <code>.htaccess</code> file, or can you suggest other resources that I could look at to resolve the problem?</p>

<p>I have used the following 2 URL's primarily to get the RewriteRule working.</p>

<p><a href="https://www.addedbytes.com/articles/for-beginners/url-rewriting-for-beginners/" rel="nofollow">URL 1</a></p>

<p><a href="http://www.smashingmagazine.com/2011/11/introduction-to-url-rewriting/" rel="nofollow">URL 2</a></p>

<p>In <code>.htaccess</code> file the rule rewrite section looks like this:
    RewriteEngine on</p>

<pre><code>RewriteRule ^article/$ article.php?i=$1 [L] # Handle requests for "article"
#RewriteRule ^article/$/ article.php?i=$1 [NC,L] # Handle requests for "article"

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php
</code></pre>

## Answers
### Answer ID: 32776546
<p>Use the following rule:</p>

<pre><code>RewriteEngine on

RewriteRule ^article/(\d+)$ article.php?i=$1 [L]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php [L]
</code></pre>

