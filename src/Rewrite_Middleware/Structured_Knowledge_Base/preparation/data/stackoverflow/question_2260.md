# pHp/htaccess 301 Redirect rewrite for dynamic page &amp; friendly url?
[Link to question](https://stackoverflow.com/questions/26465858/php-htaccess-301-redirect-rewrite-for-dynamic-page-friendly-url)
**Creation Date:** 1413808470
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, http-redirect
## Question Body
<p>I have a page, Product1.php, that is dynamic for populating my products from a database. I have searched and searched, including at this site, but been unable to ascertain a solution that exactly addresses the 301 redirect I need which will retain my custom friendly url rubric <strong>while forcing the user and bot to it in lieu of the query string</strong>?</p>

<p>All my query string urls are as such: </p>

<pre><code>http://www.example.com/Product1.php?=Product_ID=1
http://www.example.com/Product1.php?=Product_ID=2
http://www.example.com/Product1.php?=Product_ID=3
</code></pre>

<p>This is the rubric I have the rewritten urls to follow, based on the column names in my database:</p>

<pre><code>http://www.example/category/subcategory/model_name-model_id/product_id
</code></pre>

<p>Here is the htaccess function I have written to make the rewrite work:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f 
RewriteCond %{REQUEST_FILENAME} !-d 
RewriteRule ^.*/.*/.*/([0-9]+)$ Product1.php?Product_ID=$1 [L,QSA]
</code></pre>

<p>These rewritten urls are already in place and fully functional. <strong>What I can't figure out is how to write the redirect so that the user is forced to see the SEO-friendly url when she types in</strong> <code>http://www.example.com/Product1.php?=Product_ID=1</code><strong>, or when the search-engine bot crawls my page.</strong></p>

<p>Thanks in advance!</p>

<p>EDITED for clarity
FURTHER EDIT for clarity -- sorry!</p>

## Answers
### Answer ID: 26466163
<p>You need to have "category", "subcategory" and "model_name-model_id" in your URL before you start any redirection like this. At the moment I cannot see anything like that (Product1.php?=Product_ID=1) If you have them you can use </p>

<p>RewriteCond
..
.. 
RewriteRule </p>

<p>kind of method for this.</p>

