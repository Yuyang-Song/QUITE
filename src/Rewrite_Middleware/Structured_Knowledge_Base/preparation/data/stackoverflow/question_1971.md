# New NICE URLs with 301s. How to make them work Together?
[Link to question](https://stackoverflow.com/questions/14007435/new-nice-urls-with-301s-how-to-make-them-work-together)
**Creation Date:** 1356218670
**Score:** 0
**Tags:** mod-rewrite, friendly-url, url-scheme
## Question Body
<p>I have this old website URL structure:</p>

<p>site.com/folder/prod.php?cat=MAIN%20CAT%20&amp;prodid1=123&amp;prodtitle=PROD%20TITLE&amp;subcat=SUB%20CAT</p>

<p>and real example will be something like:</p>

<p>site.com/folder/prod.php?cat=CAR%20AUDIO&amp;prodid1=4444&amp;prodtitle=MTX%20AMPS&amp;subcat=AMPS</p>

<p>here you can see that for the product page there are 4 variables: category, produt id, product title and sub category. Some of this variables were used to open a menu. And yes, the URL pulls variables with space and both lower and uppercase.</p>

<p>The new site url has a new structure:</p>

<p>site.com/x/product-title-prodid2</p>

<p>a rel example will be like:</p>

<p>site.com/x/mtx-amps-8888</p>

<p>Which is accomplish by using two variables (friendly slug + a second product id: prodid2) with the following code in the .htaccess</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
Options +Indexes
Options +FollowSymlinks
RewriteEngine on
RewriteBase /

RewriteRule ^p/(.*)/$ product.php?prodid2=$1
RewriteRule ^p/(.*)$ product.php?prodid2=$1

&lt;/IfModule&gt;
</code></pre>

<p>Internally we can get prodid2 if we have prodid1 from the same table, but not viceversa.</p>

<p>Everything works fine, but we now have to create 301 redirects and apparently since the same variables are not used in the old / new url, then it becomes tricky since apparently we have to create a single rule for the nice URL creation and the 301s?</p>

<p>We have tried adding the following to the htaccess:</p>

<pre><code>RewriteCond %{QUERY_STRING} ^cat=CAR%20AUDIO&amp;prodid1=4444&amp;prodtitle=MTX%20AMPS&amp;subcat=AMPS$ [NC]
RewriteRule ite.com/folder/prod.php site.com/x/mtx-amps-8888? [R=301,L]
</code></pre>

<p>and it works for only 1 product, but when adding 2 or more, the site goes down. I imaging this would be an infinite loop?</p>

<p>An alternative would be adding a:</p>

<pre><code>ErrorDocument 404 /404.php
</code></pre>

<p>to get the URL and redirect to the page, but this would be ugly for SEs.</p>

<hr>

<p>UPDATE:</p>

<p>Sorry for my lack of understanding on this topic, am very new to this.</p>

<p>The product has 2 important ids. For example:</p>

<p>MTX AMP (which is the actual product title) if listed in 3 categories will have 1 single prodid2 repeated and 3 different prodid1 (1 for each category). They all reside in the same table. So, if we have a prodid1 we can get the prodid2 which is right next to it in the db table.</p>

<p>The rule to get a nice URL on the new site is pulled using prodid2</p>

<pre><code>RewriteRule ^p/(.*)$ product.php?prodid2=$1
</code></pre>

<p>which brings the complete value stored in the database. e.g. mtx-amps-8888 &lt;&lt; this is a mix of a slug + the prodid2</p>

<p>complete url is:</p>

<pre><code>site.com/p/mtx-amps-888
</code></pre>

<p>(the p is just a virtual forder and we take advantage of that variable to show the right page template)</p>

<p>So mtx-amps-888 are not 3 keys, these are generated when creating a product and saved all together in a single field in the db. They already include the separation - so this is not done in the htaccess.</p>

<p>The cat (key) value is really used to expand a menu used in the old site with, but to create the 301 redirect we would probably use prodid1 since we can match that value to get a prodid2. prodid2 is used as the main query to get the nice URL in the new site and its value will bring the nice URL stored in the db.</p>

<p>What makes sense from all my research would be the following:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
Options +Indexes
Options +FollowSymlinks
RewriteEngine on
RewriteBase /

RewriteRule ^p/(.*)$ product.php?prodid2=$1

RewriteCond %{QUERY_STRING} ^cat=CAR%20AUDIO&amp;prodid1=4444&amp;prodtitle=MTX%20AMPS&amp;subcat=AMPS$ [NC]
RewriteRule ite.com/folder/prod.php site.com/x/mtx-amps-8888? [R=301,L]

RewriteCond %{QUERY_STRING} ^cat=CAR%20AUDIO&amp;prodid1=5555&amp;prodtitle=BOSS%20AMPS&amp;subcat=AMPS$ [NC]
RewriteRule ite.com/folder/prod.php site.com/x/mtx-amps-8888? [R=301,L]

RewriteCond %{QUERY_STRING} ^cat=CAR%20VIDEO&amp;prodid1=6666&amp;prodtitle=ALPINE%20DVDS&amp;subcat=DVD%20PLAYERS$ [NC]
RewriteRule ite.com/folder/prod.php site.com/x/mtx-amps-8888? [R=301,L]

&lt;/IfModule&gt;
</code></pre>

<p>Pls note that I removed a line from the main rewrite rule:</p>

<pre><code>RewriteRule ^p/(.*)/$ product.php?prodid2=$1
</code></pre>

<p>This only assures that the user can also use / at the end of the URL: site.com/p/mtx-amps-888/</p>

<p>I also repeated the rewrite condition for the 301 redirects of 3 products, but i really have about 3K products to list here. If I keep 1, it will work but if I add 2, I believe a loop is created.</p>

<p>Hopefully this makes sense. You have no idea how important is for me to get this up and running, so my best wishes to those who can help :)</p>

## Answers
### Answer ID: 14011106
<p>Just re-create the file <code>/folder/prod.php</code> and have php do the redirect. This is the easiest and cleanest solution.</p>

<pre><code>&lt;?php
  $prodid1 = $_GET['prodid1'];
  //calculate prodid2 based on prodid1, or use mysql to retreive the prodid2 belonging to prodid1
  $prodid2 = $prodid1;//just for testing
  $newpath = "/p/$prodid2/";

  // redirect using 301
  header("Location: http://{$_SERVER['HTTP_HOST']}{$newpath}");
  header('HTTP/1.1 301 Moved Permanently');
?&gt;
</code></pre>

