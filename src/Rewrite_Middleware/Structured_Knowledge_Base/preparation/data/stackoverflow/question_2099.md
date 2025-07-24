# MVC RouteConfig vs URL rewrite (in Global.asax)
[Link to question](https://stackoverflow.com/questions/18721093/mvc-routeconfig-vs-url-rewrite-in-global-asax)
**Creation Date:** 1378821887
**Score:** 0
**Tags:** c#, asp.net-mvc, asp.net-mvc-4
## Question Body
<p>Myself and a colleague had a problem that we solved in two different ways.  But we don't know which is best.</p>

<p>We have a generic MVC page that is populated with specific data (widgets, content, etc) from a database.  The user enters a specific URL (user friendly, so trying to keep the query string disguised if we can help it).  </p>

<p>Now, the generic page has to take this URL and use it to get the corresponding data from the database to generate a specific page.</p>

<p>Solution 1: In the <code>Global.asax</code> file rewrite the URL, basically creating a Querystring that the generic controller can understand.</p>

<p>Soloution 2: Use the <code>RouteConfig.cs</code> file to force all page requests to route to the generic controller, which then reads the URL.</p>

<p>Any ideas,</p>

<p>Thanks.</p>

## Answers
### Answer ID: 18721148
<p>RouteConfig.cs is the cleanest way.</p>

<p>If you change your routing configuration, then by using <code>Url.RouteUrl</code> or <code>Url.Action</code> your generated Url's will update along with your routing configuration.</p>

