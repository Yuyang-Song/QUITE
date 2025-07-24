# Remove query from URL .htaccess
[Link to question](https://stackoverflow.com/questions/13093241/remove-query-from-url-htaccess)
**Creation Date:** 1351279890
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>So I have successfully removed the database query from the url with the following in the .htaccess file:</p>

<pre><code>RewriteRule ^([A-Za-z0-9-]+)$ /page.php?page_url=$1
</code></pre>

<p>However, now every request goes to this page. This is creating problems:</p>

<p>(1) Page request's that don't exist go to this page instead of the error404.html, so I wrote in the page:</p>

<pre><code>&lt;?php if ($row ['page_url'] == '') { header( 'Location: http://www.mysite.com/error404.html' ); } ?&gt;
</code></pre>

<p>(2) Other page query stripping doesn't work and redirects to the error404.html:</p>

<pre><code>RewriteRule ^([A-Za-z0-9-]+)$ /database.php?database_url=$1
</code></pre>

<p>(3) Pages go to whichever RewriteRule comes first:</p>

<pre><code>RewriteRule ^([A-Za-z0-9-]+)$ /page.php?page_url=$1
RewriteRule ^([A-Za-z0-9-]+)$ /database.php?database_url=$1
</code></pre>

<p>With the rewrites above, the database requests go to the "page.php" document, not the "database.php"</p>

