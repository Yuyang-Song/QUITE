# IIS - how best to serve a different version of site to different users
[Link to question](https://stackoverflow.com/questions/17870740/iis-how-best-to-serve-a-different-version-of-site-to-different-users)
**Creation Date:** 1374796695
**Score:** 0
**Tags:** iis-7, url-rewriting, httphandler, httpmodule, isapi
## Question Body
<p>This is not regarding version control for the source.  This is a requirement of the business and how it interfaces with various vendors, so I'm trying to work out the best possible way to set this up.  Essentially we need to serve a different major version of a site out depending on who is hitting it - and <em>not</em> display that version in the URL.  Here's how it works right now:</p>

<p>The site is ASP.NET MVC 4 running on IIS 7.  Right now it's set up with a default site in IIS with applications underneath.  Each application is a version of the site.  When the initial request hits the site it runs through a custom ISAPI filter.  That filter grabs what is essentially a user ID variable from the URL and uses it to query a SQL database.  This database links the user ID to the version that needs to be served (the application in IIS), and appends it to the beginning of the URL.  So <code>http://site.com/1</code> becomes <code>http://site.com/2.1.0.0/1</code>, thus pointing to the correct directory in IIS.  Then within the site, custom HtmlHelpers are used to strip the version from the URL string when anchor links or buttons etc. are created.  When user clicks one of those links, it repeats.</p>

<p>This seems unnecessarily complicated.  I'd like to not use custom HtmlHelpers and just silently redirect the requests to a different virtual directory/physical path in IIS somehow.</p>

<p>For alternatives, we've looked at:</p>

<ul>
<li>Using the URL Rewrite in IIS - but this requires the version to come in on the initial request, and the end user isn't going to know that.</li>
<li>Using a custom HttpHandler - but that requires that a website be hit already - the request already well into IIS.  It could be that I don't quite know enough to make it work.</li>
<li>Attempting to not rewrite the URL but just the virtual directory/physical path with the ISAPI filter, but there doesn't seem to be any hook we can use to do so.</li>
<li>Create a custom HttpModule that calls <code>HttpContext.RewritePath()</code> but ran into issues with MVC routes and the HtmlHelpers, just as if there was no HttpModule doing anything.</li>
</ul>

<p>I don't have code to share, really - it's proprietary.  What I'm looking for is more theory.  How would such a crazy website versioning contraption be set up?</p>

## Answers
### Answer ID: 17956414
<p>After a lot more playing, we found the answer.  The issue with Garath's comments above is that, while outbound rules can rewrite <code>Html.ActionLink</code> and <code>Html.BeginForm</code>, they cannot do anything for <code>RedirectToRoute</code> or <code>RedirectToAction</code> and more.  Outbound rules only parse the generated HTML content and change it before sending it back to the browser.  Outbound rules are also incompatible with gzip, which is understandable but annoying.</p>

<p>In short, we created a custom rewrite provider that uses the SQL connection to pull the version and return the correct URL.  We also hooked into the IIS URL Rewrite capability to send custom server variables to prevent querying the database more than once per session.  It works like this:</p>

<ol>
<li>Request hits the IIS URL Rewrite module</li>
<li>First rule checks for a cookie value and, if it exists, rewrites the URL based on that and stops processing further rules.</li>
<li>If the cookie isn't there, it calls the custom provider, which uses SQL to rewrite the URL.</li>
<li>The second rule also sets a custom server variable passed in the header to the version.</li>
<li>The website checks for that header variable, and if set, creates a cookie with the version.</li>
<li>Rinse and repeat.</li>
</ol>

<p>Links that helped us out:</p>

<ul>
<li><a href="http://www.iis.net/learn/extensions/url-rewrite-module/developing-a-custom-rewrite-provider-for-url-rewrite-module" rel="nofollow">http://www.iis.net/learn/extensions/url-rewrite-module/developing-a-custom-rewrite-provider-for-url-rewrite-module</a></li>
<li><a href="http://www.iis.net/learn/extensions/url-rewrite-module/using-custom-rewrite-providers-with-url-rewrite-module" rel="nofollow">http://www.iis.net/learn/extensions/url-rewrite-module/using-custom-rewrite-providers-with-url-rewrite-module</a></li>
<li><a href="http://archive.msdn.microsoft.com/rewriteextensibility" rel="nofollow">http://archive.msdn.microsoft.com/rewriteextensibility</a></li>
<li><a href="http://forums.iis.net/t/1186281.aspx" rel="nofollow">http://forums.iis.net/t/1186281.aspx</a></li>
<li><a href="http://forums.iis.net/t/1188570.aspx/1" rel="nofollow">http://forums.iis.net/t/1188570.aspx/1</a></li>
<li><a href="http://www.iis.net/learn/extensions/url-rewrite-module/setting-http-request-headers-and-iis-server-variables" rel="nofollow">http://www.iis.net/learn/extensions/url-rewrite-module/setting-http-request-headers-and-iis-server-variables</a></li>
<li><a href="http://www.iis.net/learn/extensions/url-rewrite-module/url-rewrite-module-configuration-reference#UsingServerVars" rel="nofollow">http://www.iis.net/learn/extensions/url-rewrite-module/url-rewrite-module-configuration-reference#UsingServerVars</a></li>
</ul>

<p>Hopefully this can help someone else out in the future.</p>

<p>Side note - the custom rewrite provider must target .NET 2.0, which is left out of the first link above.</p>

