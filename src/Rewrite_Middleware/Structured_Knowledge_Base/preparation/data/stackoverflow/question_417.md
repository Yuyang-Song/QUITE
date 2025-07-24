# rewritecond with query string works, but when i submit a new query from the clean url, it just appends the url with the old query string
[Link to question](https://stackoverflow.com/questions/25418141/rewritecond-with-query-string-works-but-when-i-submit-a-new-query-from-the-clea)
**Creation Date:** 1408594401
**Score:** 0
**Tags:** regex, .htaccess, mod-rewrite, query-string
## Question Body
<p>Here is are my rewrite rules and conditions</p>

<pre><code>#link ReWrite
RewriteRule ^searchresults/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ /searchresults.php?search=1&amp;year_search_type=single&amp;isused=$1&amp;year=$2&amp;make=$3&amp;model=$4&amp;price=$5 [L]

#query Rewrite
RewriteCond %{ENV:REDIRECT_STATUS} 200
RewriteRule .* - [L]
RewriteCond %{REQUEST_URI} ^/searchresults.php [NC]
RewriteCond %{QUERY_STRING} ^.*[&amp;]?isused=(\w+).*&amp;year=(\w+).*&amp;make=(\w+).*&amp;model=(\w+).*&amp;price=(\w+).*$ [NC]
RewriteRule . /searchresults/%1/%2/%3/%4/%5? [R=301,L]
</code></pre>

<p>Situation - 
i have a search page that searches the database and shows results. This setup catches the Query and rewrites it to clean urls (awesome!) BUT if i run a query a second time, aka from the cleaned url, the search request now just adds the original ?key=value&amp;key=value to the clean url to make the request.</p>

<p>searchresults.php?make=value&amp;model=value turns into searchresults/value/value as i want it to  </p>

<p>but when i run the second query from searchresults/value/value  it ends up turning it into<br>
        /searchresults/value/value?make=value&amp;model=value</p>

<p>any way to defeat that from within .htaccess as the search query itself is in some deep php crazy land of code, and i honestly cant even find the thing, so editing the php is not in the cards.</p>

<p>ALSO, as a bonus, if anyone can tell me what edits to make so that when the query sends a request that looks like   key=value+with+spaces  i get the correct clean url back? right now it takes  key=value+with+spaces and gives me back "value" but drops off with+spaces and moves onto the next key value pair....</p>

<p>THANKS </p>

## Answers
### Answer ID: 25418387
<p>Not sure why you're having the problem, your rules worked perfectly fine for me on a vanilla apache install in a blank htaccess file. But you can try changing your rules a little:</p>

<p>The first thing you need to do is swap the order of your two rules. The redirect rule <strong>must be before</strong> any internal rewrites. This prevents two rules from being applied to the same request (the rewrite engine loops through all the rules until the URI stops changing). Second, you need to match against the actual request instead of the <code>%{QUERY_STRING}</code> match against the <code>%{THE_REQUEST}</code> variable:</p>

<pre><code>RewriteCond %{THE_REQUEST} \ /+searchresults\.php\?.*[&amp;]?isused=(\w+).*&amp;year=(\w+).*&amp;make=(\w+).*&amp;model=(\w+).*&amp;price=(\w+).*$ [NC]
RewriteRule ^ /searchresults/%1/%2/%3/%4/%5? [R=301,L]

RewriteRule ^searchresults/([^/]*)/([^/]*)/([^/]*)/([^/]*)/([^/]*)$ /searchresults.php?search=1&amp;year_search_type=single&amp;isused=$1&amp;year=$2&amp;make=$3&amp;model=$4&amp;price=$5 [L]
</code></pre>

