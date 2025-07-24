# multiple URL rewrites in same .htaccess
[Link to question](https://stackoverflow.com/questions/65509033/multiple-url-rewrites-in-same-htaccess)
**Creation Date:** 1609340576
**Score:** 0
**Tags:** .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I currently have a site that contains individual pages for a companies stores as well as standard pages such as about, contact etc.</p>
<p>I have a simple URL rewrite rule in the htaccess file so that these urls are written as</p>
<p><code>https://sitename.com/manchester</code> or <code>https://sitename.com/about</code> instead of <code>https://sitename.com/manchester.php</code> and <code>https://sitename.com/about.php</code> etc</p>
<p>As its growing I'm now moving to a database structure for the stores, so instead of creating individual pages for each store I'm serving them up in a query with a <code>select_store.php</code> file ie <code>https://sitename.com/select_store.php?store=manchester</code> etc</p>
<p>I want to continue however rewriting the urls as before so still just <code>/manchester</code> etc but how does this work when I have some URLs that should redirect to select_store.php and others that should simply add .php onto the end of the url?</p>
<p>What's the best way to do this? Do I write individual rewrites for the standard pages? about, contact etc? and then a catch all for anything else to go the <code>select_store.php</code>?</p>
<p>Or do I redirect everything to select_store and then redirect the likes of about, contact in there? (doesn't sound very SEO friendly though).</p>
<p>My current .htaccess is:</p>
<pre><code>RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^([^\.]+)$ $1.php [NC,L]
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</code></pre>
<p>edited to add additional examples.</p>
<p>currently all pages are suffixed with .php so we have the following:
<a href="https://sitename.com/manchester" rel="nofollow noreferrer">https://sitename.com/manchester</a> redirects to <a href="https://sitename.com/manchester.php" rel="nofollow noreferrer">https://sitename.com/manchester.php</a>
<a href="https://sitename.com/liverpool" rel="nofollow noreferrer">https://sitename.com/liverpool</a> redirects to <a href="https://sitename.com/liverpool.php" rel="nofollow noreferrer">https://sitename.com/liverpool.php</a>
<a href="https://sitename.com/about" rel="nofollow noreferrer">https://sitename.com/about</a> redirects to <a href="https://sitename.com/about.php" rel="nofollow noreferrer">https://sitename.com/about.php</a></p>
<p>I want the stores (in above example manchester &amp; liverpool, but in reality theres a dozen and more adding regularly) to redirect to the likes of:
<a href="https://sitename.com/select_shop.php?shop=manchester" rel="nofollow noreferrer">https://sitename.com/select_shop.php?shop=manchester</a></p>
<p>while the standard pages (about, contact, menu etc) to continue to redirect as:
<a href="https://sitename.com/about.php" rel="nofollow noreferrer">https://sitename.com/about.php</a></p>
<pre><code>https://sitename.com/contact.php
</code></pre>

## Answers
### Answer ID: 65849023
<p>So the answer to this turned out to be far simpler than I assumed.</p>
<p>You have a single line for each of the &quot;standard&quot; pages index, about, menu etc, for example</p>
<pre><code>RewriteRule ^about$ about.php [NC,L]
</code></pre>
<p>telling them to redirect to the .php file and then have the code to pass anything else to the select_shop page</p>
<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^([^\.]+)$ select_shop.php?shop=$1 [NC,L]
</code></pre>
<p>so the complete file would be something like:</p>
<pre><code>RewriteEngine On
RewriteRule ^about$ about.php [NC,L]
RewriteRule ^menu$ menu.php [NC,L]
RewriteRule ^franchise$ franchise.php [NC,L]
RewriteRule ^meet-the-team$ meet-the-team.php [NC,L]
RewriteRule ^events$ events.php [NC,L]
RewriteRule ^find-contact-us$ find-contact-us.php [NC,L]
RewriteRule ^join-our-team.php$ join-our-team.php [NC,L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^([^\.]+)$ select_shop.php?shop=$1 [NC,L]

RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
</code></pre>

