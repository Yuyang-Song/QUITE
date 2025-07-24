# .htaccess and regex: trying to convert parts of my url with mod_rewrite doesn&#39;t work as expected
[Link to question](https://stackoverflow.com/questions/57611924/htaccess-and-regex-trying-to-convert-parts-of-my-url-with-mod-rewrite-doesnt)
**Creation Date:** 1566484982
**Score:** 0
**Tags:** regex, apache, .htaccess, mod-rewrite
## Question Body
<p>I'm a bit stuck trying to figure out <code>.htaccess</code> and <code>mod_rewrite</code> properly.
I know that 90% of the problem is my terrible regex skill, 10% is due to apache (or my knowledge around its <code>mod_rewrite</code> best practices).</p>

<p>We have a web service that will soon be replaced by a new one, similar in functionality but different in terms of urls, params and other things.</p>

<p>What needs to happen for our users (most of them can't perform this update on their end, so we have to do it on our side; we also don't build the tool directly nor have access to the source code and we agreed with the vendor that these redirects will not be done on this new web service.</p>

<p>What I need apache to do, with <code>mod_rewrite</code> is to be able to replace parameters in the querystring one by one, based on a mapping I provide</p>

<p>Then it should replace certain separators; ultimately, it should replace the <code>HTTP_REFERER</code> as well and redirect with 301.</p>

<p>Here's the code I have so far:</p>

<pre><code>RewriteEngine On
RewriteBase /
RewriteRule ^(.*/)?\.svn/ - [F,L] ErrorDocument 403 "Access Forbidden"

# One group of RewriteCond/RewriteRule per parameter
RewriteCond %{QUERY_STRING} ^([^&amp;]*(?:&amp;.*)?)?param=([^&amp;]*(?:&amp;.*)?)$ [NC]
RewriteRule ^ %{REQUEST_URI}?%1param_changed=%2 [N,NE]


RewriteCond %{QUERY_STRING} ^([^&amp;]*(?:&amp;.*)?)?another_param=([^&amp;]*(?:&amp;.*)?)$ [NC]
RewriteRule ^ %{REQUEST_URI}?%1another_param_modified=%2 [N,NE]

...

# This is meant to replace all | with , within the url
RewriteRule ^(.*)|(.*)$ $1,$2 [N]


# This is the one that should finalise the url replace
RewriteCond %{REQUEST_URI} ^http://this.old.url/api/1/access/activity.(xml|csv)([^&amp;]*(?:&amp;.*)?))$ [NC]
RewriteRule ^ https://the.new.one/api/activities/?format=1&amp;%2$ [R=301,NE,L]
</code></pre>

<p>This is the result I'm expecting from an example call:</p>

<p>input:
<code>http://this.old.url/api/1/access/activity.xml?reporting-org=GB-GOV-1|GB-1&amp;recipient-country=BD&amp;stream=True</code></p>

<p>output:
<code>https://the.new.one/api/activities/?reporting_organisation=GB-GOV-1,GB-1&amp;recipient_country_id=BD&amp;format=xml</code></p>

<p>I'm trying it with the htaccess tester found <a href="https://htaccess.madewithlove.be/" rel="nofollow noreferrer">here</a> and these are the issues I am still facing:</p>

<ul>
<li><p>rewrite of parameters works fine, but each parameter's modified version does not get propagated to the next <code>RewriteCond/RewriteRule</code> group</p></li>
<li><p>I can't have that <code>|</code> matched (it gets converted in <code>%7C</code> in the url, but regardless, I can't have it match).</p></li>
<li><p>The resulting url, at the end is:
<code>https://the.new.one/api/activities/?format=1&amp;%2$</code> which leads me to think that the regex I specify in the associated <code>RewriteCond</code> is wrong and doesn't match, so this works partially as a side effect (it's basically replacing the whole url <em>I think</em>) but I need it to get that <code>.xml/csv</code> format and the query string afterwards. I can't seem to be able to fix that regex to work as I need it to.</p></li>
</ul>

<p>I know there's a lot in this post, so thanks In advance to whoever can help me sort out the 3 issues I'm still facing</p>

