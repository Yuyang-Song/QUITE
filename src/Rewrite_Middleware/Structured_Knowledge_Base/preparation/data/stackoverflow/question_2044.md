# DB of URL Rewrites - Need to point all old URLs to the same new URL
[Link to question](https://stackoverflow.com/questions/16870271/db-of-url-rewrites-need-to-point-all-old-urls-to-the-same-new-url)
**Creation Date:** 1370071881
**Score:** 0
**Tags:** php, mysql, magento, loops
## Question Body
<p>I have a table in my site's database (Magento, but that's irrelevant as I'll be working with my data outside of Magento) full of URL rewrites. This table has existed for quite some time and my URLs have changed more than once in that time. For each URL, I now have something like the following:</p>

<pre><code>REWRITES(Request, Target)

really-old-url, old-url
old-url, recent-url
recent-url, current-url
</code></pre>

<p>This works as expected, with <code>really-old-url</code> being redirected to <code>current-url</code> but only after <code>really-old-url</code> is redirected to <code>old-url</code>, which is redirected to <code>recent-url</code>, which is then redirected to <code>current-url</code>. Not a very efficient setup: more 301 redirects than needed &amp; more db requests per page. There are often five or more redirects between the oldest and current URLs, and there are thousands of pages redirecting in this way.</p>

<p>I would like to use PHP+MySQL to loop though this table to end up with the following:</p>

<pre><code>REWRITES(Request, Target)

really-old-url, current-url
old-url, current-url
recent-url, current-url
</code></pre>

<p>As should be obvious, now whenever any one of the old URLs for a page is requested, it will only be directed once to the current URL.</p>

<p>How would I go about doing this?</p>

<p>Edit - here is the correct answer from Gordon using Magento's field names in case anyone else wants to do the exact same thing:</p>

<pre><code>update core_url_rewrite r join (select r.request_path, r.target_path from core_url_rewrite r left outer join core_url_rewrite r1 on r.target_path = r1.request_path where r1.request_path is null) r2 on r.target_path = r2.request_path set r.target_path = r2.target_path;
</code></pre>

<p>Edit #2 - I only performed this query on rows where <code>is_system = 0</code>. Using all rows may produce unexpected behaviour.</p>

## Answers
### Answer ID: 16870354
<p>To start, consider the set of targets that are the correct targets.  These are correct, because there are no redirections:</p>

<pre><code>select target
from rewrites r left outer join
     rewrites r1
     on r.target = r1.request
where r1.request is null
</code></pre>

<p>Now, the following update will update back "one link" in the chain by updating any record whose target is a source in the above query:</p>

<pre><code>update rewrites r join
       (select r.source, r.target
        from rewrites r left outer join
             rewrites r1
             on r.target = r1.request
        where r1.request is null
       ) r2
       on r.target = r2.source
    set r.target = r2.target;
</code></pre>

<p>You can keep repeating these updates until no records are being updated.</p>

