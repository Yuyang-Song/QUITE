# Extending rewrite rule via .htaccess to include pagination fields and values in query string
[Link to question](https://stackoverflow.com/questions/10573779/extending-rewrite-rule-via-htaccess-to-include-pagination-fields-and-values-in)
**Creation Date:** 1336930425
**Score:** 0
**Tags:** .htaccess
## Question Body
<p>I have a page on a site that displays images according to records it pulls from a database.  The page uses a query string for the purpose, like this:</p>

<pre><code>www.example.com/category.php?category=cars
</code></pre>

<p>But I wanted to have a "pretty" address in the browser for this, to look like this:</p>

<pre><code>www.example.com/category/cars
</code></pre>

<p>So I placed this directive in the root .htaccess file:</p>

<pre><code>RewriteEngine on
RewriteRule ^category/(\w+)/?$ category.php?category=$1
</code></pre>

<p>This did the trick: now, a link to:</p>

<pre><code>www.example.com/category/cars
</code></pre>

<p>... fetches the page contents that would have been fetched by:</p>

<pre><code>www.example.com/category.php?category=cars
</code></pre>

<p>(and that latter original query string version still works).</p>

<p>But now I'd like to introduce pagination into category.php, so that it will take two query strings: "category" (as before) and now "page" as well.</p>

<p>My question is, how can I amend/extend the .htaccess directive, so that a link to:</p>

<pre><code>www.example.com/category/cars/9
</code></pre>

<p>... fetches the output of:</p>

<pre><code>www.example.com/category.php?category=cars&amp;page=9
</code></pre>

<p>Also, could such an extending of the rewrite work so that, if a site visitor manually changed what obviously appears to be the page number, say from:</p>

<pre><code>www.example.com/category/cars/9
</code></pre>

<p>to:</p>

<pre><code>www.example.com/category/cars/2
</code></pre>

<p>... the address would actually fetch the corresponding "page":</p>

<pre><code>www.example.com/category.php?category=cars&amp;page=2
</code></pre>

<p>(if it exists as per the pagination)?</p>

## Answers
### Answer ID: 10573845
<p>see this:</p>

<p><a href="https://stackoverflow.com/questions/1514756/pagination-and-htaccess">Pagination and .htaccess</a></p>

<p>and consider a empty page as a first page, for example</p>

