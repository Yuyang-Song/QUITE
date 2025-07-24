# Mod rewrite with PHP and MySQL
[Link to question](https://stackoverflow.com/questions/32925668/mod-rewrite-with-php-and-mysql)
**Creation Date:** 1443895017
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite
## Question Body
<p>I am trying to get a mod rewrite script to work, but for some reason I cannot seem to get things functioning properly.  I know that mod_rewrite is working, because if I run the following test it redirects correctly:</p>

<pre><code>RewriteEngine on
RewriteRule ^oranges.html$ apples.html
</code></pre>

<p>However, if I try and push all queries to an index file or something to process using php then it does not work:</p>

<pre><code>RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule .? index.php [L]
</code></pre>

<p>What I am trying to achieve is to have a database table with two columns, one with an ID and the other with a rewrite URL.  So what I mean by this is:</p>

<pre><code>ID | URL
16 | nice-url-1
17 | nice-url-2
</code></pre>

<p>So the actual URL is /index.php?id=16, but I want there to be a table lookup and there to be a redirect to /nice-url-1.  Now I would have thought I would go with the second rewrite conditions, but the problem is it just does not redirect.</p>

<p>I am running Centos 6 with Apache 2.2.15, so I am wondering if {REQUEST_FILENAME} is just not supported.  I did try adding DOCUMENT_ROOT, but that made absolutely no difference.</p>

<p>Any help most appreciated.</p>

## Answers
### Answer ID: 32927954
<p>You want to add an other element to your rule, to actually pass the whole url, <code>QSA</code>. This will append the existing query string to the url.</p>

<pre><code>RewriteRule ^ index.php [L,QSA]
</code></pre>

<p>I also normally use the single <code>^</code> to match any url possible.</p>

