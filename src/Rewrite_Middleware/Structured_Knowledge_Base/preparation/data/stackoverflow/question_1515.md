# URL rewriting problem
[Link to question](https://stackoverflow.com/questions/814234/url-rewriting-problem)
**Creation Date:** 1241243388
**Score:** 0
**Tags:** php, url-rewriting
## Question Body
<p>i have made a website in php.</p>

<p>There is a list of stories title stored in database and when user click any title among them then user is redirected to a page with a query string on it. like story.php?id=25</p>

<p>This means story with id 25 is now going to be displayed. 
Now i want to rewrite URL but when i rewrite it there occurs a problem.</p>

<p>In story.php page i am reading the query string like $_GET['id'].. but after URL rewriting i am unable to read it like this. Can any body suggests what to do </p>

## Answers
### Answer ID: 815027
<p>If you made some adjustments to your url string you could do this.</p>

<p><a href="http://www.domain.com/story.php?story=25&amp;title=some_name" rel="nofollow noreferrer">http://www.domain.com/story.php?story=25&amp;title=some_name</a></p>

<p>Which after re-write could be this.</p>

<p><a href="http://www.domain.com/25/some_name.html" rel="nofollow noreferrer">http://www.domain.com/25/some_name.html</a></p>

<p><strong>Code:</strong></p>

<pre><code>RewriteEngine On
RewriteRule ^story/([^/]*)/([^/]*)\.html$ /story.php?story=$1&amp;title=$2 [L]
</code></pre>

### Answer ID: 814248
<p>You could use .htaccess to rewrite the long URLs server side, but not redirect the browser(so it still shows the long URL in the address bar), something like:</p>

<pre><code> RewriteEngine on
 RewriteRule story\/(\d+)\/(.+) story.php?id=$1
</code></pre>

<p>Just make you're long links look like www.site.com/story/25/This_is_the_title</p>

