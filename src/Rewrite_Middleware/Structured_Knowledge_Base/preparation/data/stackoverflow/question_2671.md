# URL Rewrite &amp; Redirect
[Link to question](https://stackoverflow.com/questions/46070651/url-rewrite-redirect)
**Creation Date:** 1504687641
**Score:** 1
**Tags:** php, .htaccess, url-rewriting, http-redirect
## Question Body
<p>I have a query regarding URL rewriting and redirection that I can't find the answer to (if there is even a solution to this)</p>

<p>Currently I'm working with a website that lists locations and as such accesses them using the following URL with an ID as the variable (using "1" as an example to pull the corrasponding record from a MySQL database);</p>

<blockquote>
  <p>location.php?location=1</p>
</blockquote>

<p>The variable has since been changed from a number to a URL slug (which is now used to pull the record from the MySQL database), so for example;</p>

<blockquote>
  <p>location.php?location=exeter-devon-uk</p>
</blockquote>

<p>... and the URL above is now also rewritten using a .htaccess file to be;</p>

<blockquote>
  <p>/location/exeter-devon-uk</p>
</blockquote>

<p>All this works perfectly fine.</p>

<p>Now my problem is this ... Google (and other search engines) have already indexed/crawled the website in question so have all the old links with the original URL of - location.php?location=1(or whatever number) - and these obviously no longer work because the code works on the newer database URL slug and not the ID number.</p>

<p>I know with URL rewriting you are supposed to point the old URL to the new URL and do a 301 permanent redirect ... but I don't know how to do this (can it even be done?) for directing the old ID number to a slug, without knowing how to relate the two??</p>

