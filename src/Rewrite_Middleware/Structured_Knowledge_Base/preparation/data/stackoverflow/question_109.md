# Pretty Urls with Mod_Rewrite
[Link to question](https://stackoverflow.com/questions/13119216/pretty-urls-with-mod-rewrite)
**Creation Date:** 1351504282
**Score:** 0
**Tags:** mod-rewrite, url-rewriting, friendly-url, pretty-urls
## Question Body
<p>I would like to rewrite the following URL string from:</p>

<p>product.php?category=abstract_and_patterns&amp;page=1</p>

<p>To:</p>

<p>abstract-and-patterns</p>

<p>Now it's important to note that both the category and page variables will always be different depending on what page the user is on or which category they have selected.</p>

<p>I have spent hours trying to figure this out with no success.</p>

<p><strong>[EDIT]</strong></p>

<p>I've tried a ton of things but the latest rewrite I've tried works but comes up with a 404 error.</p>

<pre><code>RewriteCond %{QUERY_STRING} ^category=([^&amp;]+)&amp;page=([^&amp;]+)$
RewriteRule ^product.php$ /%1/%2? [L,R=301]
</code></pre>

<p><strong>[EDIT]</strong></p>

<p>Just so you guys know, there is actually only 1 page, that is the products.php page. The information on that page is pulled from the database based on the values in the query string. Now obviously for both user friendliness and also SEO purposes I need the URLs to be clean rather than category=abstrsct_and_patterns&amp;page=3 but I also need the query strings to be remembered, especially for pages, so that the site still functions. Is this even possible? Thanks.</p>

## Answers
### Answer ID: 13766485
<p>Turns out that this cannot be achieved the way I wanted it to be.</p>

