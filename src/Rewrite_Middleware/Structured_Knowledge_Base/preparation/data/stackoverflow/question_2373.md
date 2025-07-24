# mod rewrite - have nice urls but still build menu dynamically from database
[Link to question](https://stackoverflow.com/questions/31661320/mod-rewrite-have-nice-urls-but-still-build-menu-dynamically-from-database)
**Creation Date:** 1438024155
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I am creating my menu dynamically from a database. I started by appending an id to the urls which I used to identify the page in the database and then get all urls from the subpages and so on..</p>

<p>so I had a lot of ids like this <code>www.page.com/somefolder/pagename.php?id=10</code>, where 10 is the id of the page and is the parent_id for a number of other pages.</p>

<p>Now I use mod rewrite to get nicer urls. So the above url is now <code>www.page.com/pagename.php</code> , which is mapped to the original url.
My pagenames are all gonna be unique.</p>

<p>The question: Do I have to do this for each and every url, since each url needs an id as query string or is there a better way to combine mod rewrite with dynamically generating a menu?</p>

## Answers
### Answer ID: 31661975
<p>No, not for every URL, but you will need to do this the other way around.</p>

<p>Turn the rewrite engine on</p>

<pre><code>RewriteEngine on 
</code></pre>

<p>Build a path to match against using a dynamic 'case' in brackets..</p>

<pre><code>RewriteRule ^/?somefolder/page/([0-9]+)/?$
</code></pre>

<p>.. complete the rule with the rewritten URL, using $1 for the 'case'</p>

<pre><code>/somefolder/pagename.php?id=$1 [L]
</code></pre>

<p>Put it all together using [L] to signify the 'last' rule to execute.</p>

<pre><code>RewriteRule ^/?somefolder/page/([0-9]+)/?$ /somefolder/pagename.php?id=$1 [NC,L]
</code></pre>

<p>This will rewrite <code>/somefolder/page/12345/</code> to <code>/somefolder/pagename.php?id=12345</code></p>

