# SEO Friendly URL to Dynamic Arabic Category URL using PHP
[Link to question](https://stackoverflow.com/questions/3952200/seo-friendly-url-to-dynamic-arabic-category-url-using-php)
**Creation Date:** 1287295161
**Score:** 1
**Tags:** php, .htaccess, mod-rewrite, seo
## Question Body
<p>Currently I have a url like this</p>

<p>domain/index.php?cat=مال_وأعمال</p>

<p>I want to set things up so that our Marketing people can publish url's like</p>

<p>domain/مال_وأعمال </p>

<p>I've tried several solutions including:</p>

<p>mod_rewrite - the problem with this approach is that it becomes a huge .htaccess file since we need to write a rule for each category.</p>

<p>RewriteMap - this came pretty close since I could query the database to build map file for output. However, I've since learned we don't have access to httpd.conf.</p>

<p>index.php - I've tried running everything through our index.php file which works, but doesn't keep the URL in the browser friendly for SEO purposes.</p>

<p>I'm hoping somebody has another idea which might help, I'd really appreciate it. If you've got a reference to something on the web that would help that'd be great too.</p>

<p>php .htaccess mod-rewrite seo-friendly</p>

## Answers
### Answer ID: 3953835
<p>You can use the following rule to map every request that’s URI path does only contain a single path segment onto the <em>index.php</em> while excluding existing files:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^[^/]+$ index.php?cat=$0 [L]
</code></pre>

<p>Note that you actually have to request <code>/مال_وأعمال</code> to have it internally rewritten to <code>/index.php?cat=مال_وأعمال</code>.</p>

### Answer ID: 3953799
<p>You can still use the mod_rewrite solution. The trick is the <code>[L]</code> parameter, meaning to stop mod_rewriting after that line. Suppose you have three pages "index.php", "about_us.php", and "contact_us.php", then <strong>anything</strong> else that they type you want to redirect to a category. You could do something like the following:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On
RewriteBase /
RewriteRule index\.php index.php [L]
RewriteRule about_us(\.php)? about_us.php [L]
RewriteRule contact_us(\.php)? contact_us.php [L]
RewriteRule (.*) index.php?cat=$1
&lt;/IfModule&gt;
</code></pre>

<p>This way if they go to <code>index.php</code> (or just <code>index</code>) they get your index.php file. If they go to <code>about_us.php</code> (or just <code>about_us</code>) they get your about_us.php file. But if they go to <code>test</code> (which wasn't specified in the first three lines) they get redirected to <code>index.php?cat=test</code></p>

### Answer ID: 3952289
<p>First of all you need to create a catch all subdomain which will send all requests to your single VirtualHost:</p>

<pre><code>ServerAlias *.website.com
</code></pre>

<p>Then you can either:</p>

<ol>
<li>Inspect the HTTP host at the application level and do whatever needs to be done (either serve content from the virtual subdomain, or do a 301 redirect to the www.</li>
<li>Use a single mod_rewrite rule to rewrite the URL as you initially suggested.</li>
</ol>

