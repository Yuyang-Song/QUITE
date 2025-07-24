# 301 htaccess Redirect that will force?
[Link to question](https://stackoverflow.com/questions/26468178/301-htaccess-redirect-that-will-force)
**Creation Date:** 1413815565
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, http-redirect
## Question Body
<p>Trying this again because I realize how very poorly I worded my original post.</p>

<p>I have a page, Product1.php, that is dynamic for populating my products from a database.</p>

<p>This is the rubric of my SEO-friendly urls:</p>

<pre><code>http://www.example/category/subcategory/model_name-model_id/product_id
</code></pre>

<p>This is the original url with query string that it rewrites to:</p>

<pre><code>http://www.example.com/Product1.php?=Product_ID=1
</code></pre>

<p>This is the rewrite function I have in htaccess that makes this happen:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f 
RewriteCond %{REQUEST_FILENAME} !-d 
RewriteRule ^category/.*/.*/([0-9]+)$ Product1.php?Product_ID=$1 [L,QSA]
</code></pre>

<p>However, if a user manually-types in <code>http://www.example.com/Product1.php?=Product_ID=1</code> in the address bar, this is the one they still see. Moreover, it's the same for the search engine bots, which is dividing the value of my pages.</p>

<p>How do I write a 301 redirect that will <strong>force the user and bot to see the SEO-friendly url only</strong>, regardless of how they access the page? I have researched for days and various solutions I have tried give me only 404 or 500 errors.</p>

<p>Please help. Thanks in advance.</p>

<p>**EDIT: OK, looks like I can't invoke RewriteMap because I don't have access to my host's config files. (Need to upgrade our account to do so and employer is unwilling.) So will have to do a Rewrite Rule for each individual page, which is unfortunate but doable.</p>

<p><strong>But still need to find out how to force the redirect with causing 404 or 500 errors. Anyone?</strong></p>

## Answers
### Answer ID: 37992078
<p>I used a little trick adding an "Internal" parameter to a rule responsible for main rewrite, and the check of this parameter in the 301 redirect. The solution with environment variables is also allows to process requests where the parameters may be presented in any order.</p>

<pre><code>RewriteEngine on

# perform collecting parameters from query string to an environment variables

RewriteCond %{QUERY_STRING} Category=([^&amp;]+)
RewriteRule . - [E=category:%1]

RewriteCond %{QUERY_STRING} SubCategory=([^&amp;]+)
RewriteRule . - [E=subcategory:%1]

RewriteCond %{QUERY_STRING} Product_ID=([^&amp;]+)
RewriteRule . - [E=productid:%1]

#...etc...

# give a right 301 redirect
RewriteCond %{REQUEST_URI} Product1.php
# make sure it's not an internal redirect
RewriteCond %{QUERY_STRING} !^Internal=1(.*)$
RewriteRule . /%{ENV:category}/%{ENV:subcategory}/%{ENV:productid}/? [L,R=301]

# now rewrite rule with the additional "Internal" parameter to label it as an internal redirect
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_URI} ([^/]+)/([^/]+)/([^/]+)
RewriteRule .* Product1.php?Internal=1&amp;Category=%1&amp;SubCategory=%2&amp;Product_ID=%3 [L]
</code></pre>

<p>Thus, the following request</p>

<pre><code>/Products1.php?Category=cat1&amp;SubCategory=subcat1&amp;Product_ID=321
</code></pre>

<p>will result in 301 redirect to</p>

<pre><code>/cat1/subcat1/321/
</code></pre>

<p>and the appropriate page will be shown.</p>

<p>One more way is to remove the "Internal" trick and use another name of the script, Products2.php for example. I.e. you need something to distinguish external request from internal rewrite. to avoid infinite loop ("too much redirects" error).</p>

