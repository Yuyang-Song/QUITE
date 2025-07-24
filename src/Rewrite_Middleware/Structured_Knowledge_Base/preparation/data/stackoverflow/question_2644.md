# URL Rewrite with parameter and php query
[Link to question](https://stackoverflow.com/questions/44390284/url-rewrite-with-parameter-and-php-query)
**Creation Date:** 1496752842
**Score:** 3
**Tags:** apache, .htaccess, mod-rewrite, url-rewriting, friendly-url
## Question Body
<p>Directories:
 <strong>eventfinder</strong> is project folder</p>

<ul>
<li>Localhost<br>
-- project1<br>
-- project2<br>
-- <strong>eventfinder</strong><br>
--- .htaccess</li>
</ul>

<p>User comes to the page <a href="http://localhost/eventfinder/" rel="nofollow noreferrer">http://localhost/eventfinder/</a> and types 'randomevent123' after /eventfinder/</p>

<p>then php query happens with ?event=randomevent123 </p>

<pre><code>$event = $_GET['event'];

$stmt = $conn-&gt;prepare("SELECT * FROM events WHERE name = :name");
$stmt-&gt;bindParam(":name", $event);
$stmt-&gt;execute();
</code></pre>

<p>and returns data from database</p>

<p>I am trying to rewrite my url but I don't understand what is the problem...</p>

<pre><code>http://localhost/eventfinder/index.php?event=randomevent123
</code></pre>

<p>to </p>

<pre><code>http://localhost/eventfinder/randomevent123
</code></pre>

<p>With .htaccess</p>

<pre><code>RewriteEngine On
RewriteRule ^([^/]*)$ /index.php?event=$1 [L] 
</code></pre>

<p>But query won't work.</p>

## Answers
### Answer ID: 44391404
<pre><code>RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([^/]+)/?$ /eventfinder/index.php?event=$1 [L]
</code></pre>

<p>You can us <code>!-f</code> and <code>!-d</code> checks on the requested filename to ensure that the URL that's being typed is <strong>not</strong> a file and <strong>not</strong> a directory before doing the rewrite itself - it prevents a recursive loop on <code>index.php</code></p>

### Answer ID: 44391167
<p>Give the following a try:</p>

<ol>
<li>Confirm that <code>mod_rewrite</code> is loaded</li>
<li>Check that <a href="https://devdocs.io/apache_http_server/mod/core#allowoverride" rel="nofollow noreferrer"><code>AllowOverride</code></a> allows htaccess parsing</li>
<li><p>The following rule (inside <code>eventfinder</code> directory):</p>

<pre><code>RewriteEngine On
RewriteBase /eventfinder/

RewriteCond %{THE_REQUEST} ^GET\ /eventfinder/index\.php\?event=([^\s&amp;]+) [NC]
RewriteRule ^index\.php$ %1 [R,L,QSD]

RewriteRule ^(?!index\.php([^/]+))$ index.php?event=$1 [L] 
</code></pre></li>
</ol>

