# htaccess rewrite changes for localhost
[Link to question](https://stackoverflow.com/questions/33246556/htaccess-rewrite-changes-for-localhost)
**Creation Date:** 1445374259
**Score:** 2
**Tags:** php, apache, .htaccess, mod-rewrite
## Question Body
<p>I've been trying to get this website to work on my local machine but the links no longer work due to .htaccess file settings which I've been unsuccessfully trying to alter. The page content is in a database, and the links look like </p>

<pre><code>&lt;a href="&lt;?=$linkLocations?&gt;" id="bestLoc"&lt;?=$activeBest?&gt;&gt;Best Locations&lt;/a&gt;
</code></pre>

<p>that variable is defined as a global as </p>

<pre><code>$linkLocations = $URL . '/best-locations';
</code></pre>

<p>and bestLocations is actually a .php file that queries the database.  The .htaccess file is showing a lot of rewrite rules, here is the complete file</p>

<pre><code># compress text, html, javascript, css, xml:
AddOutputFilterByType DEFLATE text/plain

AddOutputFilterByType DEFLATE text/html

AddOutputFilterByType DEFLATE text/xml

AddOutputFilterByType DEFLATE text/css

AddOutputFilterByType DEFLATE application/xml

AddOutputFilterByType DEFLATE application/xhtml+xml

AddOutputFilterByType DEFLATE application/rss+xml

AddOutputFilterByType DEFLATE application/javascript

AddOutputFilterByType DEFLATE application/x-javascript



ExpiresActive On

ExpiresByType image/gif A2592000

ExpiresByType image/jpeg A2592000

ExpiresByType image/jpg A2592000

ExpiresByType image/png A2592000

ExpiresByType image/x-icon A2592000

ExpiresByType text/css A604800

ExpiresByType application/javascript A604800

ExpiresByType application/x-shockwave-flash A2592000

&lt;FilesMatch "\.(gif¦jpe?g¦png¦ico¦css¦js¦swf)$"&gt;

Header set Cache-Control "public"

&lt;/FilesMatch&gt;



RewriteEngine on
fafaf


RewriteCond %{HTTP_HOST} !^$

RewriteCond %{HTTP_HOST} !^www\. [NC]

RewriteCond %{HTTPS}s ^on(s)|

RewriteRule ^ http%1://www.%{HTTP_HOST}%{REQUEST_URI} [R=301,L]



RewriteRule ^communities/([a-zA-Z0-9\_\-]+)$ communities/index.php?community=$1 [NC]

RewriteRule ^communities/([a-zA-Z0-9\_\-]+)/$ communities/index.php?community=$1 [NC]



RewriteRule ^communities/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)$ communities/index.php?community=$1&amp;commPage=$2 [NC]

RewriteRule ^communities/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/$ communities/index.php?community=$1&amp;commPage=$2 [NC]



RewriteRule ^communities/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)$ communities/index.php?community=$1&amp;commPage=$2&amp;model=$3 [NC]

RewriteRule ^communities/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/$ communities/index.php?community=$1&amp;commPage=$2&amp;model=$3 [NC]



RewriteRule ^([a-zA-Z0-9\_\-]+)$ subpage.php?page=$1 [NC]

RewriteRule ^([a-zA-Z0-9\_\-]+)/$ subpage.php?page=$1 [NC]



RewriteRule ^([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)$ subpage.php?page=$1&amp;sp=$2 [NC]

RewriteRule ^([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/$ subpage.php?page=$1&amp;sp=$2 [NC]



RewriteRule ^([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)$ subpage.php?page=$1&amp;sp=$2&amp;spd=$3 [NC]

RewriteRule ^([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/([a-zA-Z0-9\_\-]+)/$ subpage.php?page=$1&amp;sp=$2&amp;spd=$3 [NC]
</code></pre>

<ul>
<li>I haven't altered the rewrites from the live version.</li>
<li>I'm accessing the URL via localhost/bentley/ via WAMP</li>
<li>The live site is <a href="http://bentleyhomes.com" rel="nofollow">http://bentleyhomes.com</a></li>
<li>The directory structure of the website doesn't have the linked pages,
but rather php files outputting database data</li>
</ul>

<p>I know I'm missing a lot here and probably out of my depth but if anyone could point me in a general direction I would be grateful; I've spent a morning on htaccess tutorials but this is still a bit tough for me.</p>

## Answers
### Answer ID: 33248222
<p>Try with:</p>

<pre><code>RewriteEngine on
RewriteRule ^([a-zA-Z0-9\_\-]+)$ subpage.php?page=$1 [NC,L]
</code></pre>

<p>And now (after your edit), without :</p>

<pre><code>fafaf
RewriteCond %{HTTP_HOST} !^$
RewriteCond %{HTTP_HOST} !^www\. [NC]
RewriteCond %{HTTPS}s ^on(s)|
RewriteRule ^ http%1://www.%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
</code></pre>

