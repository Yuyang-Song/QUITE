# Google not indexing my URLs as expected
[Link to question](https://stackoverflow.com/questions/19018662/google-not-indexing-my-urls-as-expected)
**Creation Date:** 1380164892
**Score:** 0
**Tags:** .htaccess, url, mod-rewrite, seo
## Question Body
<p>My site passes a variable (a phone number) in the URL between pages.  It grabs the phone number from the database and writes the URL link as: url.com/phone-number/id. </p>

<p>However, if the target page does not have a phone number it is replaced with a 0, so,
url.com/0/id.  </p>

<p>In my .htaccess file to rewrite old query php parameters to clean urls I put a default url.com/0/id in the rewrite.  Old pages did not have a phone number so all redirect will have the 0.</p>

<pre><code># 301 redirects ad
RewriteCond %{REQUEST_URI}  ^/page\.php$
RewriteCond %{QUERY_STRING} ^id=(\d+)$ [NC]
RewriteRule ^page.php$ /page/0/%1? [R=301,NE,NC,L]
</code></pre>

<p>My problem is Google is indexing all new pages with the url.com/0/id and not url.com/phone-number/id, even though if you browse the site you will see url.com/phone-number/id for pages with phone numbers.  </p>

<p>I am not sure if it is my URL rewrite or Google bot's behavior that is causing this.  </p>

## Answers
### Answer ID: 19021009
<p>Don't use <code>R=301</code> for above rule as 301 means permanent redirect. Use 302 (temporary redirect):</p>

<pre><code>RewriteCond %{QUERY_STRING} ^id=(\d+)$ [NC]
RewriteRule ^page\.php$ /page/0/%1? [R=302,NC,L]
</code></pre>

