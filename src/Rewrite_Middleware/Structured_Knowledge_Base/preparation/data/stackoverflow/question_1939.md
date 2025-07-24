# Rewriting a URL to a query string on Apache and Nginx
[Link to question](https://stackoverflow.com/questions/12946437/rewriting-a-url-to-a-query-string-on-apache-and-nginx)
**Creation Date:** 1350529389
**Score:** 10
**Tags:** regex, apache, mod-rewrite, url-rewriting, nginx
## Question Body
<p>I'm trying to set up some path rewrites on two separate servers, one using mod-rewrite on Apache and one using HttpRewriteModule on Nginx. I don't think I'm trying to do anything too complex, but my regex skills are a little lacking and I could really use some help.</p>

<p>Specifically, I'm trying to transform a formatted URL into a query string, so that a link formatted like this:</p>

<pre><code>http://www.server.com/location/
</code></pre>

<p>would point to this:</p>

<pre><code>http://www.server.com/subdirectory/index.php?content=location
</code></pre>

<p>Anything extra at the end of the formatted URL should be appended to the "content" parameter in the query string, so this:</p>

<pre><code>http://www.server.com/location/x/y/z
</code></pre>

<p>should point to this:</p>

<pre><code>http://www.server.com/subdirectory/index.php?content=location/x/y/z
</code></pre>

<p>I'm pretty sure this should be possible using both Apache mod-rewrite and Nginx HttpRewriteModule based on the research I've done, but I can't see to get it working. If anyone could give me some pointers on how to put together the expressions for either or both of these setups, I'd greatly appreciate it. Thanks!</p>

## Answers
### Answer ID: 40334028
<p>In nginx you match "/location" in a rewrite directive, capture the tailing string in the variable $1 and append it to the replacement string.</p>

<pre><code>server {
...
rewrite ^/location(.*)$ /subdirectory/index.php?content=location$1 break;
...
}
</code></pre>

<p>In Apache's httpd.conf this looks quite similar:</p>

<pre><code>RewriteEngine On
RewriteRule ^/location(.*)$ /subdirectory/index.php?content=location$1 [L]
</code></pre>

<p>Have a look at the examples at the end of this page: <a href="https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html" rel="nofollow">https://httpd.apache.org/docs/2.4/mod/mod_rewrite.html</a></p>

### Answer ID: 40446689
<p>This would probably be the best way to do it in nginx:</p>

<pre><code>location ^~ /location/ {
    rewrite ^/(location/.*)$ /subdirectory/index.php?content=$1 last;
}
</code></pre>

<p>For more details, see:</p>

<ul>
<li><a href="http://nginx.org/r/location" rel="nofollow noreferrer">http://nginx.org/r/location</a></li>
<li><a href="http://nginx.org/r/rewrite" rel="nofollow noreferrer">http://nginx.org/r/rewrite</a></li>
</ul>

### Answer ID: 12948543
<p>For Apache, in the htaccess file in your document root, add:</p>

<pre><code>RewriteEngine On
RewriteCond %{REQUEST_URI} !^/subdirectory/index\.php$
RewriteRule ^(.*)$ /subdirectory/index.php?content=$1 [L]
</code></pre>

<p>In nginx, you want to first make sure requests for <code>/subdirectory/index.php</code> get passed through, then rewrite everything else:</p>

<pre><code>location ~ /subdirectory/index\.php$ 
{ 
} 

location / 
{ 
    rewrite ^(.*)$ /subdirectory/index.php?content=$1 break; 
}
</code></pre>

### Answer ID: 12946503
<p>Search string: <code>(.+)/location/(.*)$</code></p>

<p>replacement string: <code>$1/subdirectory/index.php?content=location/$2</code></p>

