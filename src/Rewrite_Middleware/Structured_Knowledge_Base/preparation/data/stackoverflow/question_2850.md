# htaccess rewrite url to overwrite characters after hyphen
[Link to question](https://stackoverflow.com/questions/55722416/htaccess-rewrite-url-to-overwrite-characters-after-hyphen)
**Creation Date:** 1555487119
**Score:** 0
**Tags:** .htaccess, url-rewriting
## Question Body
<p>The file 'location-chunk.php' consists of database queries etc. Now, If any user visits 'city-{anything}.html', the htaccess should show him the output of file 'location-chunk.php'. The word 'anything' can contain any character or number. I am trying the following rewrite rule but it is redirecting to the 404 page.</p>

<pre><code>    RewriteRule ^city-([a-zA-Z0-9_-]+).html$ location-chunk.php [NC,L]
</code></pre>

