# Is it possible to query a database using a value passed in a URL, and write the result of the query to the URL using mod_rewrite?
[Link to question](https://stackoverflow.com/questions/18621538/is-it-possible-to-query-a-database-using-a-value-passed-in-a-url-and-write-the)
**Creation Date:** 1378320525
**Score:** 4
**Tags:** php, mysql, apache, .htaccess, mod-rewrite
## Question Body
<p>Is it possible to use mod_rewrite to write an htaccess rule that takes a url parameter value (for example: id=1, where 'id' is the parameter, and '1' is the parameter value), query a database with the parameter value specified, and then write the value returned from the query as a part of the url of the requested page?</p>

<p>I know the basics of mod_rewrite, for example rewriting a url that appears like:</p>

<pre><code>www.example.com/item.php?id=1
</code></pre>

<p>to the following:</p>

<pre><code>www.example.com/item/1
</code></pre>

<p>An example of what I would require is writing the following url:</p>

<pre><code>www.example.com/item.php?id=1
</code></pre>

<p>to this:</p>

<pre><code>www.example.com/item/name-of-item-based-on-id-specified-in-original-url
</code></pre>

<p>However I have no idea if what I am looking to do is possible using mod_rewrite.</p>

<p>If anyone has a solution to this problem I'd be very grateful if you could help me. If what I am trying to do is not possible using htaccess and mod_rewrite, can someone please point me in the direction of how I may go about solving this problem?</p>

## Answers
### Answer ID: 18621739
<p>It's possible, but you need to use a <a href="http://httpd.apache.org/docs/2.2/mod/mod_rewrite.html#rewritemap">RewriteMap</a> to define a mapping that you can use within a <code>RewriteRule</code>.</p>

<p>Apache version 2.2 doesn't have direct database access so you'll need to write a script that does the actual query then return the result. You can define this map using the <a href="http://httpd.apache.org/docs/current/rewrite/rewritemap.html#prg">"External Rewriting Program"</a>.</p>

<p>So if you have a script that takes "cats" from stdin, then queries the database, and returns "1", you'd define it like so:</p>

<pre><code>RewriteMap item_lookup prg:/path/to/item_lookup.php
</code></pre>

<p>That directive has to be in your server or vhost config, it can't be in an htaccess file. But you can use the mapping in an htaccess file:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /item.php?id=${item_lookup:$1} [L]
</code></pre>

<p>So this takes the URI <code>/cats</code> and rewrites that to <code>/item.php?id=1</code>.</p>

<p>If you are using apache 2.4, then you can take advantage of the <a href="http://httpd.apache.org/docs/current/rewrite/rewritemap.html#dbd">"DBD" map</a>. You can insert a query right into the map definition, bypassing having to use an external script. You'd use it in the same way.</p>

<pre><code>RewriteMap item_lookup "fastdbd:SELECT id FROM items WHERE name = %s"
</code></pre>

<p>Then use it in the same way:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /item.php?id=${item_lookup:$1} [L]
</code></pre>

<p>Without using a DBD/FastDBD query, I think you're honestly better off just doing the database lookup from <code>item.php</code>, since you'd be duplicating all of that work in a second external script anyways. Just add something like:</p>

<pre><code>RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^item/([0-9]+)$ /item.php?id=$1 [L]

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^([A-Za-z0-9-]+)$ /item.php?name=$1 [L]
</code></pre>

<p>And in your <code>item.php</code> script, check for both <strong>id</strong> and <strong>name</strong>. If you have a <strong>name</strong>, do the database lookup in order to turn that into an id. It's much easier to manage, you don't need to have server/vhost config access, and you're not complicating matters by using a rewrite map.</p>

