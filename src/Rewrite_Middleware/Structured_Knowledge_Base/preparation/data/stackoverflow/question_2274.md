# htaccess mod rewritten urls, 301 redirect on dynamic page?
[Link to question](https://stackoverflow.com/questions/27019811/htaccess-mod-rewritten-urls-301-redirect-on-dynamic-page)
**Creation Date:** 1416408724
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, http-redirect
## Question Body
<p>I am utilizing mod-rewrite and my htaccess file to translate query string urls to friendly ones. These are products that pull from a database and which populate a single dynamic php file - <strong>product1.php</strong>. </p>

<p>I introduced this rewrite function fairly recently and have seen my site traffic plummet. I am thinking this is because I need to add 301 redirects to the rewritten urls. (I have noticed a massive spike in url errors, mostly nonsensical, for some reason.)</p>

<p>Can you use 301 redirects if it's just one file (<strong>product1.php</strong>), only the url's are different; and, if so, how do you write it? I have searched this specific question, no luck.</p>

<p>FYI, here's what I have currently in my htaccess utilizing mod-rewrite:</p>

<pre><code>RewriteEngine On

#Redirect all requests missing "www"
RewriteCond %{HTTP_HOST} ^example\.com$ [NC]
RewriteRule ^ http://www.%{HTTP_HOST}%{REQUEST_URI} [NE,L,R=301]

#Truncate extension ".php" from requests
RewriteCond %{THE_REQUEST} /index\.php [NC]
RewriteRule ^(.*?)index\.php$ /$1 [L,R=301,NC,NE]

#Look for the word "category" followed by slash, product type, slash, model name and model id, slash, product id
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^category/.*/.*/([0-9]+)$ product1.php?product-id=$1 [L,QSA]

#Rewrite static file url
RewriteRule ^category/subcategory/?$ subcategory-index.php [NC]
</code></pre>

<p>I have about forty of this last rewrite for the various static pages I am renaming.</p>

<p>Thanks :)</p>

