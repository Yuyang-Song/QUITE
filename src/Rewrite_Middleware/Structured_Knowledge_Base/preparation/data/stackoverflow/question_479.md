# .htaccess Redirect/Rewrite rules
[Link to question](https://stackoverflow.com/questions/27970861/htaccess-redirect-rewrite-rules)
**Creation Date:** 1421348078
**Score:** 2
**Tags:** apache, .htaccess, mod-rewrite, http-redirect
## Question Body
<p>On a website, I have a <code>.htaccess</code> file setup for rules on rewriting the url. All of my content pages are generated dynamically, so there is only one file, <code>content.php</code>, and its basically generating the page based on a query parameter. The link structure of the site is then determined off of the main navigation.</p>

<p>So on content.php, its pulling the page from the database by looking at the URL. Behind the scenes, the URL would basically look like this:</p>

<p>www.website.com/content.php?page=my-page</p>

<p>However using rewrites, the url actually shows and displays like this:</p>

<p>www.website.com/my-page/</p>

<p>This works great, except for one issue I'm experiencing. You could pretty much add any directory you wanted before /my-page/, and the content for /my-page/ would still show. For example:</p>

<p>www.website.com/test1/test2/test3/my-page/</p>

<p>shows the same things as:</p>

<p>www.website.com/my-page/</p>

<p>If the actual link I want to use is: www.website.com/section/my-page/
how can I redirect any request that ENDS in /my-page/ to www.website.come/section/my-page/</p>

<p>I have tried using the following, but that ultimately ends up in an endless loop</p>

<pre><code>RewriteRule (.*)/my-page/?$ http://www.website.com/section/my-page/ [L,R=301]
</code></pre>

## Answers
### Answer ID: 33839616
<p>I had this problem, messed with regex for <em>hours</em> to no avail, following these answers. It turned out to be quite simple.</p>

<p><strong>Turn off MutliViews</strong></p>

<p>In short, in your server configuration, look for something like this...</p>

<pre><code>Options -Indexes +FollowSymLinks +MultiViews
</code></pre>

<p>...and change it to this...</p>

<pre><code>Options -Indexes +FollowSymLinks -MultiViews
</code></pre>

<p>Of course, that line may look very different, depending on your file. The point is, put a <code>-</code> in front of MultiViews.</p>

<blockquote>
  <p>NOTE: If you don't see any symbols on that line, just remove
  <code>MultiViews</code> instead. Apache2 is all-or-nothing about use of symbols.</p>
</blockquote>

<p>If you cannot (or don't want to) change server configuration, stick this line in your <code>.htaccess</code>...</p>

<pre><code>Options -MultiViews
</code></pre>

<p>That fixed it for me!</p>

### Answer ID: 27973228
<p>Replace this rule:</p>

<pre><code>RewriteRule (.*)/my-page/?$ http://www.website.com/section/my-page/ [L,R=301]
</code></pre>

<p>By this rule:</p>

<pre><code>RewriteRule ^(?!my-page/my-second-page)(?:.+?/)?(my-second-page)/?$ /my-page/$1/ [L,NC,R=302]

RewriteRule ^.+?/(my-page)/?$ /$1/ [L,NC,R=302]
</code></pre>

<p>Also test this in a new browser to avoid old 301 cache.</p>

### Answer ID: 27972424
<p>Your rewrite <code>(.*)</code> is saying anything/you/like/before/my-page will match, and you also have a 301 permanent redirect <code>R=301</code> at the end of it which isn't needed.</p>

<p>In your .htaccess you can do the rewrites without the trailing slash:</p>

<pre><code>RewriteEngine On
    RewriteRule ^/section/([^/\.]+)$ /content.php?page=section&amp;id=$1
    RewriteRule ^/([^/\.]+)$ /content.php?page=$1 [L]
</code></pre>

<p>And then in content.php:</p>

<pre><code>$page = (!isset($_GET['page'])) ? 'indexPage' : $_GET['page'];

switch($page){

    case 'my-page':

 // process request for /my-page

    break;

    case 'my-other-page':

 // process request for /my-other-page

    break;

    case 'section':
    $section_id = (!isset($_GET['id'])) ? 'NONE' : $_GET['id'];

 // process /section/$section_id - i.e $section_id = my-section-1

    break;

    case 'indexPage':

 // process request for index page, i.e /

    break;

    default:

 // This should stop /the/anything/matching/my-page issue
    header("HTTP/1.0 404 Not Found");
}
</code></pre>

<p>In the above php, <code>$page</code> is set to <code>indexPage</code> if <code>$page</code> is empty or not set - and if <code>$page</code> is set but doesn't match anything in the switch/case section it returns a 404 header.</p>

<p><code>$section_id</code> is handled the same way but set to <code>NONE</code> if it isn't set or is empty; like the <code>$page</code> variable, you can also send a 404 header if <code>$section_id</code> is sent but doesn't match anything.</p>

