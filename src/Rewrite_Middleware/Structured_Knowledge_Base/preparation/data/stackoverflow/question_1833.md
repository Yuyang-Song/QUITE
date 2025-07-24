# Subdomains with htaccess not working as expected
[Link to question](https://stackoverflow.com/questions/9673302/subdomains-with-htaccess-not-working-as-expected)
**Creation Date:** 1331579508
**Score:** 0
**Tags:** apache, .htaccess, mod-rewrite
## Question Body
<p>I know this is a very highly discussed topic, but I can't figure out what I'm doing wrong using my search skills.</p>

<p>With the following folder structure as root of both <code>domain.local</code> and <code>board.domain.local</code></p>

<pre><code>/
 app/
 bin/
 board/
     index.php
 src/
 vendor/
 web/
     index.php
</code></pre>

<p>And this .htaccess in the <code>/</code> folder</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
    RewriteEngine On
    RewriteCond %{HTTP_HOST} ^board.domain.local$
    RewriteRule ^(.*)$ board/$1 [QSA,L]
    RewriteCond %{HTTP_HOST} ^domain.local$
    RewriteRule ^(.*)$ web/$1 [QSA,L]
&lt;/IfModule&gt;
</code></pre>

<p>I get an internal server error when accessing <code>board.domain.local</code>. Accessing <code>domain.local</code> works perfectly and redirects the queries to <code>web/</code>.</p>

<p>Why does the first rewrite not work?</p>

## Answers
### Answer ID: 9676360
<p>This is really a supplement to Kaz's comment since I agree with them, but it doesn't fit into the comment character limit.  If an .htaccess file is processed (in a Per Directory context) if one or more rewrites have occurred which change the URI then an internal redirect occurs.  The .htaccess scan is restarted and the rules are evaluated.</p>

<p>By default only one set of rewrite rules is used: and that is those in the lowest <code>.htaccess</code> on the path with <code>RewriteEngine On</code>. So in the case of a <code>domain.local</code> request on the second pass and  <em>if</em> <code>DOCROOT/web/.htaccess</code> then this would be executed instead of <code>DOCROOT/.htaccess</code> for requests to <code>domain.local</code>.</p>

<p>Another aspect is the looping problem which I see that you've addressed the second rewritecond on each rule.  However, this can fail is you have options such as <code>MultiViews</code> enabled (another bizarre Apache botch which pays havoc with rewrite rules) because this splits the query apart and does subqueries which can foil this type of anti-recursion condition. </p>

<p>So I always turn of MultiViews and DirectoryIndex with search list.  </p>

<p>You can also add the [NS] flag to all rules as none are applicable in a subquery.  I also set an environment variable END=true to force exit, when I want to do this and use this stopper at the top of my rules:</p>

<pre><code> RewriteCond  %{IS_SUBREQ}%{ENV:END} true
 RewriteRule  ^                      -    [L]
</code></pre>

### Answer ID: 9674623
<p>You're doing relative path rewrites in a per-directory context without <code>RewriteBase</code>. Why one works but the other doesn't is due to some compensating factor elsewhere which is inconsistent between <code>board</code> and <code>web</code>. The internal server error is likely a loop. Check your error log.</p>

<pre><code>RewriteEngine On
RewriteBase /   # need this sucker
RewriteCond %{HTTP_HOST} ^board.domain.local$
RewriteRule ^(.*)$ board/$1 [QSA,L]
RewriteCond %{HTTP_HOST} ^domain.local$
RewriteRule ^(.*)$ web/$1 [QSA,L]
</code></pre>

<p>In a per-directory context, rewrites are done on file system paths, not URL's. The rewrites are done on just the part of the path after the directory, which is stripped off. If you do a relative rewrite, the directory part is put back after. And then, a moronic thing happens: the rewrite is treated as a URL! <code>RewriteBase</code> specifies the prefix to put on the rewrite (instead of naively restoring the path prefix) to make it a valid URL. <code>RewriteBase</code> says, "although we are handling the directory <code>/var/www/docroot</code> it actually represents the URL space <code>/</code> so when URLs are re-generated from rewrites, they should be in that space, and not in <code>/var/www/docroot</code> which is not a URL".</p>

<p>Ask yourself: what is the <code>DocRoot</code>? And so what will the URL-s be coming out of the relative rewrite when the <code>DocRoot</code> is (wrongly) stuck on as a prefix due to the missing <code>RewriteBase</code>? Trace the handling of those bogus URL-s through your configuration and you will surely discover the reason why one gets into an infinite loop and the other doesn't.</p>

### Answer ID: 9673558
<p>Try adding a few more conditions to keep the rewrite engine from looping (your URI will eventually become /board/board/board/board/board/board/board/board/ etc.)</p>

<pre><code>RewriteEngine On

RewriteCond %{HTTP_HOST} ^board.domain.local$
RewriteCond %{REQUEST_URI} !^/board
RewriteRule ^(.*)$ board/$1 [QSA,L]

RewriteCond %{HTTP_HOST} ^domain.local$
RewriteCond %{REQUEST_URI} !^/web
RewriteRule ^(.*)$ web/$1 [QSA,L]
</code></pre>

