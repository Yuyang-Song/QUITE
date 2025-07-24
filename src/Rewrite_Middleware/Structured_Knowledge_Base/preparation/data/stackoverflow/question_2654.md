# Keep question mark on $_GET with rewrite rule
[Link to question](https://stackoverflow.com/questions/45029729/keep-question-mark-on-get-with-rewrite-rule)
**Creation Date:** 1499763048
**Score:** 1
**Tags:** php, apache, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>So I've found <a href="https://stackoverflow.com/questions/35658832/parse-question-mark-as-normal-character-after-mod-rewrite?noredirect=1&amp;lq=1">this interesting question</a> on making the question mark symbol appear on $_GET variable after using rewrite rules.</p>

<p>However, as much as I've tried to accomplish this myself, I didn't quite understand how it works to have the same result on my website.</p>

<p>Here's my rewrite rule:</p>

<pre><code>RewriteRule ^(.+)$ index.php?uri=$1 [QSA,L]
</code></pre>

<p>This basically allows me to route users to specific places without hard coding each page on my htaccess file, so if a user goes to /about/contact page, he's actually going to index.php?uri=/about/contact.</p>

<p>The problem is that sometimes I WANT the question mark to be kept in $_GET. Let's say a topic title of "What's up?" then my url would search for a topic like /topic/what-s-up? and would match with what-s-up? in the database. But, right now, my $_GET variable stores just "what-s-up" (without the "?") and my database still stores "what-s-up?" (with the "?"), which would say that there's no topic with that title when there actually is.</p>

<p>How can I keep the question mark so /topic/what-s-up? still translates to /topic/what-s-up? in the query string?</p>

<p><strong>EDIT: FULL .HTACCESS FILE FOR TEST PURPOSES</strong></p>

<pre><code>Options -Indexes

DirectoryIndex index.html index.php

RewriteEngine On

RewriteBase /

RewriteCond %{REQUEST_FILENAME} !-f

RewriteCond %{REQUEST_FILENAME} !-d

RewriteRule ^(.+)$ index.php?uri=$1 [QSA,L]
</code></pre>

## Answers
### Answer ID: 57631665
<p>I know its late, but i used php <a href="https://www.php.net/manual/es/function.urlencode.php" rel="nofollow noreferrer">urlencode()</a> to pass the question mark, as it converts ? to %3F</p>

### Answer ID: 45032471
<p>You can change your rule to this to capture optional <code>?</code> in <code>uri</code> parameter:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{THE_REQUEST} \s/+([^?]*\??\S*)\sHTTP [NC]
RewriteRule ^(.+)$ index.php?uri=%1 [QSA,L]
</code></pre>

<p>Since we want <code>?</code> also to be captured we are using <code>RewriteCond %{THE_REQUEST}</code> since pattern in <code>RewriteRule</code> only matches REQUEST_URI. Since we are capturing value from <code>RewriteCond</code> hence we are using <code>%1</code> instead of <code>$1</code> as back-reference.</p>

<p><code>THE_REQUEST</code> variable represents complete original request received by Apache from your browser and it doesn't get overwritten after execution of some rewrite rules. Example value of this variable is <code>GET /index.php?id=123 HTTP/1.1</code></p>

