# PHP: mod_rewrite if query contains value
[Link to question](https://stackoverflow.com/questions/6015116/php-mod-rewrite-if-query-contains-value)
**Creation Date:** 1305536583
**Score:** 0
**Tags:** php, .htaccess, mod-rewrite, http-redirect
## Question Body
<p>Recently I solved my issue with mod_rewrite to redirect a domain to a subfolder. Now that I've fixed my original issue, I've hit a another wall.</p>

<p>Here is an example structure:</p>

<pre><code>/
/index.php
/content/
/content/styles.css
/domain/
/domain/index.php
</code></pre>

<p>For simplicity, <code>/domain/</code> is the current and top-most folder. <strong>In <code>/domain/index.php</code> I am trying to access <code>/content/styles.css</code>. How can I accomplish this?</strong> Assume there is no web link to the previous directories. Also <code>../</code> does not work as <code>../</code> returns the same directory as <code>./</code>.</p>

<p>I thought of a way, but my .htaccess skills aren't very strong and I don't want to spend hours or days piecing together an answer. Let's say I have:</p>

<pre><code>&lt;link rel="stylesheet" type="text/css" href="content/styles.css" /&gt;
</code></pre>

<p>If I am right, <code>href</code> performs a request for the file. How can I use .htaccess to capture the request and point it to the correct folder? Like if the query string looks like <code>^/content/(.*)$</code>, and rewrite it back one directory to access <code>../content</code> instead.</p>

<p>Hopefully this made some type of sense.</p>

## Answers
### Answer ID: 6015335
<p>You could use an Alias:</p>

<pre><code>&lt;VirtualHost *:80&gt;
    DocumentRoot "/domain"
    Alias /content "/content"
&lt;/VirtualHost&gt;
</code></pre>

### Answer ID: 6015319
<p>You could create a dummy <code>/domain/content</code> directory with another .htaccess file which has something like</p>

<pre><code>RewriteRule ^([^/]+)$ /content/$1 [NC,L]
</code></pre>

### Answer ID: 6015290
<p>I considered that;</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME} !-f
</code></pre>

<p>exist in your <code>.htaccess</code> file.
Why aren't you trying like that?</p>

<pre><code>$dir = dirname(__FILE__);
$link = $_SERVER['HTTP_HOST'];
// $link = preg_replace('/^www\./i', '', $link);
</code></pre>

<p>for hrefs;</p>

<pre><code>href="&lt;?php echo $link . '/content/content.css'; ?&gt;"
</code></pre>

<p>for imports;</p>

<pre><code>include($dir . '/example.php');
</code></pre>

### Answer ID: 6015187
<p>if <code>/content/</code> is NOT inside <code>/domain/</code> and <code>/domain/</code> is your <code>DOCUMENT_ROOT</code> on your webserver, then you can't access the <code>/content/</code> folder at all using a <code>&lt;link&gt;</code> tag &amp; mod_rewrite. </p>

<p>You could access it via PHP and include it's contents, but that's a different story.</p>

