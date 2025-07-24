# Rewrite URL to MySQL value
[Link to question](https://stackoverflow.com/questions/23860413/rewrite-url-to-mysql-value)
**Creation Date:** 1401055592
**Score:** 0
**Tags:** php, .htaccess, url-rewriting
## Question Body
<p>I have a PHP script that queries the database with the id specified in the URL:</p>

<pre><code>http://www.example.com/articles.php?id=5
</code></pre>

<p>But I want the URL not to have the id in it but the title that's in the same database in another column. So I basically need to have a link that looks like this:</p>

<pre><code>http://www.example.com/articles/title-of-the-fifth-article
</code></pre>

<p>and search for this title in the database so I can rewrite the URL in the .htacces file to where it specifies the id.</p>

## Answers
### Answer ID: 23860457
<p>This should work:<br>
Add this to the .htaccess file</p>

<pre><code>RewriteEngine On
RewriteRule ^articles/(.*) articles.php?title=$1 [L]
</code></pre>

<p>and the following to the articles.php file:</p>

<pre><code>&lt;?php
    echo $_GET['title'];
?&gt; 
</code></pre>

