# URL Rewriting with multiple rules: wrong $_GET variable
[Link to question](https://stackoverflow.com/questions/23502584/url-rewriting-with-multiple-rules-wrong-get-variable)
**Creation Date:** 1399401970
**Score:** 1
**Tags:** php, apache, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I'm very new to URL rewriting. What I'd like to achieve is to have 2 main rules:</p>

<ol>
<li>Hide all .php extensions</li>
<li>Rewrite <code>domain.com/p.php?id=1</code> to <code>domain.com/p/1</code></li>
</ol>

<p>Here's what I have so far:</p>

<pre><code>RewriteEngine On

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}\.php -f
RewriteRule ^(.*)$ $1.php
RewriteRule   ^p/(.+)$   p.php?id=$1   [L]
</code></pre>

<p>This seemed to work at first: all .php extensions are hidden, and typing domain.com/p/1 displayed domain.com/p.php?id=1.</p>

<p>However, I've just realized that the PHP GET method on this page picks up a wrong value: whereas I want it to pick up <code>1</code>, it actually picks up <code>1.php/1</code>. I didn't notice it at first because the database query based on <code>$_GET</code> actually works, which seems odd to me now that I know the value is wrong.</p>

<p>How could I make the combination of these two rewrite rules work as intended?</p>

<p>Thank you!</p>

## Answers
### Answer ID: 23502758
<p>Place this code in your <code>DOCUMENT_ROOT/.htaccess</code> file:</p>

<pre><code>RewriteEngine On

RewriteCond %{THE_REQUEST} \s/+p\.php\?id=([0-9]+) [NC]
RewriteRule ^ /p/%1? [R=301,L]

RewriteRule ^p/([0-9]+)/?$ /p.php?id=$1 [L,QSA,NC]

RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{DOCUMENT_ROOT}/$1\.php -f [NC]
RewriteRule ^(.+?)/?$ /$1.php [L]
</code></pre>

### Answer ID: 23502685
<p>If you just want to rewrite the numerical values, you should restrict your second rule:</p>

<pre><code>RewriteRule   ^p/(\d+)$   p.php?id=$1   [L]
</code></pre>

