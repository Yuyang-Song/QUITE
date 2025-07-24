# URL Rewrite query database?
[Link to question](https://stackoverflow.com/questions/12972608/url-rewrite-query-database)
**Creation Date:** 1350643512
**Score:** 0
**Tags:** php, mysql, url, url-rewriting, seo
## Question Body
<p>I'm trying to understand how URL rewriting works. I have the following link.</p>

<pre><code>mysite.com/profile.php?id=23
</code></pre>

<p>I want to rewrite the above url with the users first and last name.</p>

<pre><code>mysite.com/directory/liam-gallagher
</code></pre>

<p>From what I've read however you specify the rule for what the url should be output as, but how do I query my table to get each user name? </p>

<p>Sorry if this is hard to understand, I've confused myself!</p>

## Answers
### Answer ID: 12972693
<p>You are looking at this from the wrong direction. You can't do that kind of automatic url rewrite. The best is to create an all over url rewrite:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.php [L]
&lt;/IfModule&gt;
</code></pre>

<p>and create a specific name for a user in the db that will be used as an url.</p>

<pre><code>+---------+----------+------+-----------+----------------+
| user_id | username | name | surname   | url            |
+---------+----------+------+-----------+----------------+
|      23 | liam     | Liam | Gallagher | liam-gallagher |
+---------+----------+------+-----------+----------------+
</code></pre>

<p>Now when someone accesses your <code>http://mysite.com/directory/liam-gallagher</code>, you can read the last entry and find the <code>user_id</code> in you database and make your script do the rest.</p>

<p>The other way is as <a href="https://stackoverflow.com/users/187606/pekka">Pekka</a> suggested. Create an url like <code>http://mysite.com/directory/23/liam-gallagher</code> and read the id from the link. But I personally don't like that kind of urls. They are just fast/lazy workarounds in my opinion.</p>

### Answer ID: 12972681
<p>One approach I've used works as follows.</p>

<p>Make a rewrite rule, e.g.</p>

<pre><code>mysite.com/directory/(.*)
</code></pre>

<p>That redirects to:</p>

<pre><code>mysite.com/profile.php?user=%1
</code></pre>

<p>Having %1 as the parameter captured from the rule.</p>

<p>Then grab the user from the query parameter on the profile page and fetch the ID for that user from the db.</p>

<p><a href="http://httpd.apache.org/docs/current/mod/mod_rewrite.html" rel="nofollow">http://httpd.apache.org/docs/current/mod/mod_rewrite.html</a></p>

### Answer ID: 12972675
<p>Something like (just a draft, adapt to your own needs...):</p>

<pre><code>RewriteEngine On
RewriteRule ^([a-zA-Z]+)/([a-zA-Z]+)/([0-9]+)/([-0-9a-zA-Z]+)/?$ /$1/$2.php?id=$3 [L]
</code></pre>

