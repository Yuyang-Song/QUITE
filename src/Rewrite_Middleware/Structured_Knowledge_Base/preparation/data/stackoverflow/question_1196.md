# Using htaccess to &quot;fake&quot; an XML file?
[Link to question](https://stackoverflow.com/questions/6297992/using-htaccess-to-fake-an-xml-file)
**Creation Date:** 1307646730
**Score:** 4
**Tags:** php, xml, .htaccess, sitemap
## Question Body
<p>Here's the problem I'm trying to solve: I have a dynamic php-driven website that is constantly being updated with new content, and I want my XML sitemap to stay up to date automatically. Two options I see:</p>

<ol>
<li>Write a php script that queries my database to get all my content and outputs to <a href="http://mysite.com/sitemap.xml" rel="nofollow">http://mysite.com/sitemap.xml</a>, execute the script regularly using a cron job.</li>
<li>Simply create my sitemap as a php file (sitemap.php), query the db and write directly to that file, and use the htaccess rewrite rule <code>RewriteRule ^sitemap.xml$ sitemap.php</code> so that whenever someone requests sitemap.xml they're directed to the php file and get a fresh sitemap file.</li>
</ol>

<p>I'd much rather go with option #2 since it's simpler and doesn't require setting up a cron, but I'm wondering if Googlebot will not recognize sitemap.xml as valid if it's actually a php file?</p>

<p>Does anyone know if option #2 would work, and if not whether there's some better way to automatically create an up-to-date sitemap.xml file? I'm really surprised how much trouble I've had with this... Thanks!</p>

## Answers
### Answer ID: 6298046
<p>Google will only get the headers and the body of the response. If your php script returns the same headers and the same body as your webserver would return, then there is technically no difference between the PHP script response or the XML file response by your server. Use <code>curl -i <a href="http://example.com/" rel="nofollow">http://example.com/</a></code> to inspect the response headers of a request if you would like to test that on your own.</p>

<p>So you can safely do this, that's for what mod_rewrite has been designed (next to the many other things).</p>

### Answer ID: 6298018
<p>Just make sure your script generates the appropriate <code>Content-Type</code> header. You can do so with <a href="http://php.net/header" rel="noreferrer">header()</a>.</p>

