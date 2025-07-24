# Vanity urls + REST + Web crawler
[Link to question](https://stackoverflow.com/questions/14711523/vanity-urls-rest-web-crawler)
**Creation Date:** 1360079716
**Score:** 0
**Tags:** php, apache, api, url, rest
## Question Body
<p>I have an app that uses data from several applications APISs (Facebook,Twitter,Instagram etc..), accessing them from REST endpoints in PHP.</p>

<p>I am building a vanity URL for my app users, say <a href="http://www.myapp.com/username" rel="nofollow">http://www.myapp.com/username</a>.</p>

<p>If i had a database, i could fetch user data from database to display in the user page.</p>

<p>With REST services, each time i go into the URL, there is a call to the API that fetches information from the main websites.</p>

<p>The problem is getting big since the app is going to receive a lot of traffic from search engine crawlers (i would not lower the crawling rate)</p>

<p>1st problem: Since the API offers limited access (2000 query per hours), there is a way to skip the api call (for example, using memcache) ?</p>

<p>2nd problem: I want to make a vanity url, so each time i call <a href="http://www.myapp.com/username" rel="nofollow">http://www.myapp.com/username</a> i have to call the api to get the userid and then the username, i wonder if this is the correct way to do this, most websites do it with url rewrite, but how to deal with it when you have external data and not your internal database?</p>

<p>Thanks for the reading, any help is needed!</p>

## Answers
### Answer ID: 14711781
<p>Try using some kind of framework. It should make the routing much simpler. </p>

<p>The url rewriting would happen vi .htaccess so the user would never see a rewrite for the url. </p>

<p>Two ways that I can think of are: </p>

<ol>
<li><p>Rewrite in the .htaccess such that all your defined routes are left untouched and in all other cases(that is <a href="http://www.example.com/username" rel="nofollow">http://www.example.com/username</a>) the user controller method is injected in between the username and the url.</p></li>
<li><p>Define routes so that all your known routes are handled and have the defualt route take care of figuring out the user id and doing everything that is necessary. </p></li>
</ol>

<p>For caching use memcache/redis to cache your queries/user objects/anything else accessed frequently. </p>

### Answer ID: 14711736
<p>About using memcache, the big problem you will encounter is validating and expiring the cache data. </p>

<p>Let's say you implement it like this:</p>

<pre><code>function getSomeData() {
    if (Memcache::has('key-for-data')) {
        return Memcache::get('key-for-data');
    } else {
        $data = RestApi::getData();
        Memcache::put('key-for-data', $data);
        return $data;
    }
}
</code></pre>

<p>This seems sensible enough but then, what happens if the REST API is accessed through any other means?  (Like another third party app POSTing data to the same API).  Then, the cached data can be invalid and you will not know about it.  </p>

<p>From your application's perspective, changes to the underlying data store are completely random and furthermore, totally opaque and unknowable, and therefore it is not a good target for caching.</p>

<p>If on the other hand you can get some kind of "push" notification from the service whenever data is updated (i.e. a subscription service), you could use this as a trigger to invalidate the relevant cache entries.  However this is additional complexity and would need to be supported at both ends.</p>

<p>Sorry this isn't really an answer but it is a partial answer and it was too long for a comment :-)</p>

