# Rewrite the URL from Database
[Link to question](https://stackoverflow.com/questions/14185993/rewrite-the-url-from-database)
**Creation Date:** 1357501411
**Score:** 0
**Tags:** mod-rewrite
## Question Body
<p>I need some help.
What I found here is this:</p>

<p><a href="https://stackoverflow.com/questions/12972608/url-rewrite-query-database">URL Rewrite query database?</a></p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</code></pre>

<p></p>

<p>But I cant change it to what I need :-(</p>

<p>Here is what I need.</p>

<p>www.mySite.de/person.php?p=122</p>

<p>www.mySite.de/alias-of-person-from-database</p>

<p>Where is the name of the variable I need to have to get the recordset from my database?</p>

<p>It must be some $_GET, or?</p>

<p>Anyone can help me?
Cheers,
Denis</p>

## Answers
### Answer ID: 14186703
<p>I get my answer here.</p>

<p><a href="https://stackoverflow.com/questions/4907730/how-to-dynamically-rewrite-a-url-like-facebook">How to Dynamically Rewrite a URL like Facebook</a></p>

<p>Thanks Gumbo!</p>

<p>Cheers,
Denis</p>

