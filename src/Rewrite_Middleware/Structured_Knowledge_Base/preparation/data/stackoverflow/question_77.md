# URLs with /12 instead of ?var=12
[Link to question](https://stackoverflow.com/questions/12014860/urls-with-12-instead-of-var-12)
**Creation Date:** 1345250734
**Score:** -1
**Tags:** php, html, url-rewriting
## Question Body
<blockquote>
  <p><strong>Possible Duplicate:</strong><br>
  <a href="https://stackoverflow.com/questions/1039725/how-to-url-re-writing-in-php">How to: URL re-writing in PHP?</a><br>
  <a href="https://stackoverflow.com/questions/3655893/rewriting-an-arbitrary-number-of-path-segments-to-query-parameters">Rewriting an arbitrary number of path segments to query parameters</a>  </p>
</blockquote>



<p>Currently, on my website (<a href="http://www.sourceworldgaming.com" rel="nofollow noreferrer">source world gaming</a>), I use the $_GET method to display reviews/news articles. For example, "sourceworldgaming.com/reviews.php?id=40" will display review #40 in the database. </p>

<p>IGN doesn't do this. For example, they use <a href="http://www.ign.com/games/guild-wars-2/pc-896298" rel="nofollow noreferrer">http://www.ign.com/games/guild-wars-2/pc-896298</a> - with no $_GET[] needed. How is this done? Do they create an index for each individual game?</p>

<p>I want to be able to make the URL sourceworldgaming.com/reviews.php/40</p>

<p>Also, would doing this make my site more search engine friendly? Thanks.</p>

## Answers
### Answer ID: 12014928
<p>The fact that requests for <code>/foo.php</code> go to a file named <code>foo.php</code> on your server is just an implementation detail.  There's nothing about the web that requires this, it's just something that a lot of systems do, including PHP.  Lots of other systems use different conventions, such as routing tables or object traversal.</p>

<p>If you've already built a website that uses the file system to route requests, the easiest way of getting different URLs is to use mod_rewrite or its equivalent on whichever web server software you use.</p>

### Answer ID: 12014905
<p>Its done with mod_rewrite and the router part of the script:</p>

<p>The url: <code>http://www.example.com/games/guild-wars-2/pc-896298</code></p>

<p>Is actually passed to the script like: </p>

<p><code>http://www.example.com/?route=/games/guild-wars-2/pc-896298</code></p>

<p>By using mod_rewrite (example)</p>

<pre><code>RewriteEngine On
Options -Indexes
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ index.php?route=$1 [L,QSA]
</code></pre>

<p>Then basically <code>/games/guild-wars-2/pc-896298</code> is split up into pieces using</p>

<p><code>$route = explode('/',$_GET['route'])</code></p>

<p>So <code>$route[0]</code> would be the controller or query the categories. 
   <code>$route[1]</code> would be the action or query the game because <code>$route[0]</code> is a game category ect</p>

