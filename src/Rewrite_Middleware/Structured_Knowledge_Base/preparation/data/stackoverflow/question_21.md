# REST with PHP, how to choose query string
[Link to question](https://stackoverflow.com/questions/10357199/rest-with-php-how-to-choose-query-string)
**Creation Date:** 1335557439
**Score:** 2
**Tags:** php, web-services, rest
## Question Body
<p>I'll show two type of query string for this example.
I know that a query string for a web service, should be look like more 1 than 2</p>

<ol>
<li><a href="http://localhost/findbyproductcode/4xxheua" rel="nofollow">http://localhost/findbyproductcode/4xxheua</a></li>
<li><a href="http://localhost/findbyproductcode?productcode=4xxheua" rel="nofollow">http://localhost/findbyproductcode?productcode=4xxheua</a></li>
</ol>

<p>My question is: how do you manage the first one in php? isnt this just an url rewrite for the second one?</p>

<p>with the #2 query string, I suppose there's a findbyproductcode.php page that process the GET variable(?productcode=4xxheua), check some databases with this productcode and send back some data.</p>

<p>How the #1 is supposed to work? should I have a 4xxheua.php? (obviously not...) ... i just dont get this.</p>

## Answers
### Answer ID: 10357527
<p>One example to achieve #1,</p>

<p>1: Send all path without image, css(, and so on) to <code>root/index.php</code>(e.g. mod_rewrite on Apache)<br>
2: In <code>index.php</code>, get parameters from <code>$_SERVER['pathinfo']</code> or another way.<br>
3: parse and process it.</p>

<p>If you use Apatche and mod_rewrite, check the docs:</p>

<ul>
<li><a href="http://www.sitepoint.com/article/guide-url-rewriting/" rel="nofollow">mod_rewrite: A Beginner's Guide to URL Rewriting</a></li>
<li><a href="http://httpd.apache.org/docs/2.0/misc/rewriteguide.html" rel="nofollow">URL Rewriting Guide</a></li>
</ul>

### Answer ID: 10357592
<p>Yep, just URL rewriting. I'm using Symfony 1.3 at the moment, and their htaccess looks like this:</p>

<pre><code>Options +FollowSymLinks +ExecCGI

&lt;IfModule mod_rewrite.c&gt;
  RewriteEngine On

  # uncomment the following line, if you are having trouble
  # getting no_script_name to work
  #RewriteBase /

  # we skip all files with .something
  #RewriteCond %{REQUEST_URI} \..+$
  #RewriteCond %{REQUEST_URI} !\.html$
  #RewriteRule .* - [L]

  # we check if the .html version is here (caching)
  RewriteRule ^$ index.html [QSA]
  RewriteRule ^([^.]+)$ $1.html [QSA]
  RewriteCond %{REQUEST_FILENAME} !-f

  # no, so we redirect to our front web controller
  RewriteRule ^(.*)$ index.php [QSA,L]
&lt;/IfModule&gt;
</code></pre>

<p>In this case, just make index.php your controller, and you can get all URLs for this vhost sent to it. Easy!</p>

### Answer ID: 10357246
<p>If you're trying to write an API, thre's a bunch to do - yes, there's rewriting involved, but there doesn't have to be a page for all the paramters - Luracast has a great opensource Rest API call ed restler to get started with.</p>

### Answer ID: 10357244
<p>The only reason you'd prefer 1 over 2 is because 1 is more semantically intuitive.</p>

<p>It makes sense to have a URL like:</p>

<p><a href="http://www.myblog.com/article/2012-04-29/i-did-nothing-all-day" rel="nofollow">http://www.myblog.com/article/2012-04-29/i-did-nothing-all-day</a></p>

<p>Rather than</p>

<p><a href="http://www.myblog.com/index.php?page=article&amp;id=23423" rel="nofollow">http://www.myblog.com/index.php?page=article&amp;id=23423</a></p>

<p>Supposedly it also helps your SEO score.</p>

<p>If you're just building a webservice, as in: machines talk to machines - then it doesn't matter what the URL looks like. You could also just have one URL that accepts <em>all</em> inputs and do the 'routing' internally based on the input data.</p>

