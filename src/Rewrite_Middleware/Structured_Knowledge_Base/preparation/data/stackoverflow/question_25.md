# Redirecting url to index.aspx page using standard asp.net3.5 and web.config
[Link to question](https://stackoverflow.com/questions/10398164/redirecting-url-to-index-aspx-page-using-standard-asp-net3-5-and-web-config)
**Creation Date:** 1335878111
**Score:** 0
**Tags:** c#, asp.net, url-rewriting
## Question Body
<p>I have a subdomain that is <a href="http://trade.businessbazaar.in" rel="nofollow">http://trade.businessbazaar.in</a> . I am dynamically creating  urls from database something in this manner  <a href="http://trade.businessbazaar.in/mycompany" rel="nofollow">http://trade.businessbazaar.in/mycompany</a>. To display details, I have an index.aspx file there,thinking that on every request the index.aspx page will load and display data accodingly. Also, There is a masterpage on the index.aspx page from where i am capturing the text mycompany and query it in database to fetch result. But nothing seems to work.</p>

<p>A genuine link is <a href="http://trade.businessbazaar.in/Symparlife" rel="nofollow">http://trade.businessbazaar.in/Symparlife</a>. But its unable to load index.aspx. I need a clean approach without any third party dll or rewriters. Directly to push some lines in config and start working. That is url will be the same but index page will get loaded...</p>

<p><strong>In short, i want to say</strong></p>

<p>I need the StackOverflow type clean url mechanism to fetch pages</p>

<p>Thanks in Advance</p>

## Answers
### Answer ID: 10398278
<p><strike>You can handle the Begin_Request event in Global.asax and add custom code to redirect to index.aspx and convert the parts of the URL into query string arguments. You should use Server.Transfer to keep the URL in the browser.</p>

<p>I'd recommend upgrading to 4.0 and using the Routing enine though. You should check if the standard routing is available as a download for ASP.NET 3.5. I am sure your code will get messy very soon. Been there, done that.</strike></p>

<p>As @Mike Miller mentions in the comments the Routing engine ships with ASP.NET 3.5. You can check the documentation here - <a href="http://msdn.microsoft.com/en-us/library/system.web.routing(v=vs.90).aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/system.web.routing(v=vs.90).aspx</a></p>

<p>Here is a tutorial on how to use it with Web Forms - <a href="http://weblogs.asp.net/scottgu/archive/2009/10/13/url-routing-with-asp-net-4-web-forms-vs-2010-and-net-4-0-series.aspx" rel="nofollow">http://weblogs.asp.net/scottgu/archive/2009/10/13/url-routing-with-asp-net-4-web-forms-vs-2010-and-net-4-0-series.aspx</a></p>

<p>For your case the code would be something like:</p>

<pre><code>routes.MapPageRoute("company-index", "/{company}", "~/index.aspx")
</code></pre>

<p>And in index.aspx you can access the route value for company like this:</p>

<pre><code>string company = (string)Page.RouteData.Values["company"];
</code></pre>

<p>Keep in mind that you'd better add something in the URL before your actual argument (the company name). If you don't you will have problems later on when because you may want to add a URL like "/Login" but then you will have to validate that users can't create a company named "Login". Not how Stack Overflow has "/questions/" before the actual question info in the URL.</p>

