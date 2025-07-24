# .htaccess rewrite to remove extension and query string and make into folder structure but if page doesn&#39;t exist send to another page
[Link to question](https://stackoverflow.com/questions/48029681/htaccess-rewrite-to-remove-extension-and-query-string-and-make-into-folder-stru)
**Creation Date:** 1514591996
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I currently have the an .htaccess (included below) which works wonderfully.  It takes a user to the content.php page and shows them the page that is stored in the database.  However, there are some pages which required me to hardcode and thus are listed with the .php extension.  Is there any way to add a rewrite rule that will allow me to remove the extension and send the query string as directories.</p>

<blockquote>
  <p><strong>Example</strong></p>
  
  <p>Current: <a href="http://www.example.com/dashboard.php?ax=clients&amp;do=save&amp;miscthirdparam=doitnow" rel="nofollow noreferrer">http://www.example.com/dashboard.php?ax=clients&amp;do=save&amp;miscthirdparam=doitnow</a></p>
  
  <p>To: <a href="http://www.example.com/dashboard/clients/save/doitnow/" rel="nofollow noreferrer">http://www.example.com/dashboard/clients/save/doitnow/</a></p>
</blockquote>

<p>However, if the dashboard.php page doesn't exist, then just send it to content.php as it does now to check if there is a page in the database to display?  (I have an Error 404 show if there is no page in the db).</p>

<p>**My Current .htaccess **</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^([a-zA-Z]*)/(.*)$ /content.php?url=$1/$2 [L]
    Options +FollowSymLinks
    RewriteEngine on
&lt;/IfModule&gt;
&lt;IfModule !mod_rewrite.c&gt;
    ErrorDocument 404 /content.php?err=404
&lt;/IfModule&gt;
</code></pre>

## Answers
### Answer ID: 48034068
<p>You can use <a href="http://httpd.apache.org/docs/current/mod/mod_rewrite.html#rewritecond" rel="nofollow noreferrer"><strong>RewriteCond backreference</strong></a>. We can extract the first URL path, and find out if the php file exists. Given your example, we extract <code>dashboard</code> and check if <code>%{DOCUMENT_ROOT}/dashboard.php</code> file exists. If so, rewrite the url with specified paramaters. The regex <code>[^/]*</code> matches all characters except followed by forward slash <code>/</code>.</p>

<pre><code>RewriteCond %{REQUEST_URI} ^/([^/]*)
RewriteCond %{DOCUMENT_ROOT}/%1.php -f
RewriteRule ^([^/]*)(/([^/]*))?(/([^/]*))?(/([^/]*))? /$1.php?ax=$3&amp;do=$5&amp;miscthirdparam=$7 [L]
</code></pre>

