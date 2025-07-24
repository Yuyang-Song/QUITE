# How can I stop my .htaccess file from including the full file path when testing locally?
[Link to question](https://stackoverflow.com/questions/57747994/how-can-i-stop-my-htaccess-file-from-including-the-full-file-path-when-testing)
**Creation Date:** 1567357900
**Score:** 0
**Tags:** apache, .htaccess, xampp
## Question Body
<p>I've built a website which uses the url to load pages from a database. The traffic is redirected to the <code>index.php</code> file, which then queries the url and loads the appropriate page. To make this work I'm using some rewrite rules in the <code>.htaccess</code> file.</p>

<p>Although I have been able to make this work in a live environment, I'm struggling to make it work locally, using XAMPP.</p>

<p>I'm using the following rules:</p>

<pre><code>Options +FollowSymLinks
RewriteEngine On
RewriteCond %{REQUEST_URI} !.*\.png$ [NC]
# Various other exceptions

RewriteRule .* /index.php
</code></pre>

<p>Which are returning the following url</p>

<p><code>http://localhost/C:/xampp/htdocs/project-folder/localhost/project-folder/</code></p>

<p>but I'd like the following page to be loaded:</p>

<p><code>localhost/project-folder/index.php</code></p>

<p>I can't understand where/why the full file path is being included, nor how I can exclude it.</p>

<p>Can anyone help?</p>

