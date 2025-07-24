# mod_rewrite adding trailing slash
[Link to question](https://stackoverflow.com/questions/27372539/mod-rewrite-adding-trailing-slash)
**Creation Date:** 1418105582
**Score:** 0
**Tags:** php, linux, apache, mod-rewrite
## Question Body
<p>I have a lot of URL's like domain.com/something/ &lt;-notice the trailing slash that are indexed with google thanks to a previous developer implementing wordpress which now means i'm stuck trying to make a lot of highly SEO ranked pages do a redirect on the new website that will replace the wordpress website and needs to have the same URL's.</p>

<p>The things is on my new site I have a page that functions as a catchall and does a database query to check to see if we have a members name that exists(the /something in the example URL above), and displays the content at domain.com/something</p>

<p>Now first I thought I had this in the bag by doing the following rewrite rule(s)</p>

<pre><code>RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /membersite.php [L]
</code></pre>

<p>Well this was half the battle I got domain.com/something AND domain.com/something/ working great but now the issue with this is I have duplicate content in the eyes of google one set of the content at domain.com/something AND another at domain.com/something/</p>

<p>So I need to modify the rewrite to do a 301 on domain.com/something/ to domain.com/something.</p>

<p>I should also mention that any other non-existent directories or file requests should be redirected to domain.com without the trailing slash.</p>

<p>Also this part is working fine but figured I should mention the page membersite.php never shows in the URL but instead /something which is the users "profile" page, just so everyone see the whole picture</p>

## Answers
### Answer ID: 27493902
<p>Full working solution which i finally figured out it's an order of operations</p>

<pre><code>RewriteEngine On
RewriteOptions inherit

RewriteBase /
RewriteRule ^index\.php$ - [L]

**RewriteRule ^(.+?)/$ $1 [R=301,L] // this part first strips the trailing slash**

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /membersite.php [L] //this part handles internally which file i'm loading from the server to process the request.
</code></pre>

