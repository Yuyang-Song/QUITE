# Is it possible to use query strings in URL routing in a webforms application
[Link to question](https://stackoverflow.com/questions/43738241/is-it-possible-to-use-query-strings-in-url-routing-in-a-webforms-application)
**Creation Date:** 1493729122
**Score:** 1
**Tags:** c#, asp.net, webforms
## Question Body
<p>I have a web forms application that has a few basic pages. I've created routes to make sure those pages don't need .aspx at the end. </p>

<pre><code>routes.MapPageRoute("About", "About", "~/About.aspx");
routes.MapPageRoute("Contact", "Contact", "~/Contact.aspx");
routes.MapPageRoute("faq", "faq", "~/faqs.aspx");
routes.MapPageRoute("Donation", "Donation", "~/Donation.aspx");
</code></pre>

<p>I have a sql server database that contains data regarding events that we are holding. This table holds simple values like eventID, location, date, our goal, etc. </p>

<p>Currently I only have one even in my database so I just created a new aspx page with the name of the event. So the url looks like this <code>https://example.com/awesome-event</code></p>

<p>And I added the appropriate route</p>

<pre><code>routes.MapPageRoute("Awesome-Event", "Awesome-Event", "~/Awesome-Event.aspx");
</code></pre>

<p>This works fine, but I want the ability to add new events without having to worry about adding new aspx pages every time. I figured I can use URL rewrite for this. What I want to achieve is to have a single .aspx page that is passed a query string but keep nice looking URLS. </p>

<p>So what I did was create a new aspx page named simply <code>event.aspx</code></p>

<pre><code>routes.MapPageRoute("Awesome-Event1", "Awesome-Event1", "~/event.aspx?id=1");
routes.MapPageRoute("Awesome-Event2", "Awesome-Event2", "~/event.aspx?id=2");
</code></pre>

<p>And in my code behind for the <code>event.aspx</code> page looks like this</p>

<pre><code>protected void Page_Load(object sender, EventArgs e)
{
    string query = Request.QueryString["id"];
    if(query != null)
    {
        PageLable.Text = query.ToString();
    }
}
</code></pre>

<p>So currently typing in <code>http://localhost:51197/Awesome-Event1</code> and <code>http://localhost:51197/Awesome-Event2</code> both take me to me to the event.aspx page (I can tell because I hit a break point) but it doesn't actually pass the query string of ID. </p>

<p>Am I going about this the right way? Is there a better solution. From my understanding, MVC makes this kind of thing easy but I don't really have much experience with it. The database is already set up and my project is a webforms application so I don't even know if adding MVC to my current project is possible. </p>

## Answers
### Answer ID: 43739814
<p>Take a look at the MapPageRoute() documentation:</p>

<blockquote>
  <p><a href="https://msdn.microsoft.com/en-us/library/system.web.routing.routecollection.mappageroute.aspx" rel="nofollow noreferrer">https://msdn.microsoft.com/en-us/library/system.web.routing.routecollection.mappageroute.aspx</a></p>
</blockquote>

<p>It has this example:</p>

<pre><code>routes.MapPageRoute("SalesSummaryRoute",
    "SalesReportSummary/{locale}", "~/sales.aspx");
</code></pre>

<p>which you can adapt for your event page like this:</p>

<pre><code>routes.MapPageRoute("Awesome-Event",
    "Awesome-Event/{id}/", "~/event.aspx");
</code></pre>

<p>That will allow you to use a url like this:</p>

<pre>https://example.com/Awesome-Event/2/</pre>

<p>And then you can see which event to render in your event.apsx page like this:</p>

<pre><code>protected void Page_Load(object sender, EventArgs e)
{
    if (Page.RouteData.Values["id"] != null)
    {
        int eventID = Convert.ToInt32(Page.RouteData.Values["id"]);
    }
}
</code></pre>

<p>If you want to get fancy, you can do something like this:</p>

<pre><code>protected void Page_Load(object sender, EventArgs e)
{
    if (Page.RouteData.Values["id"] != null)
    {
        int eventID;
        if (int.TryParse(Page.RouteData.Values["id"], out eventID))
        {
           //render event based on numeric ID
        }
        else
        {
           //lookup event based on a string title. Then you could use a url like:
           //https://example.com/Awesome-Event/SuperbowlLII
        }
    }
}
</code></pre>

<p>But be careful if you allow both an ID and a title reference the data information, or you could effectively split the search engine ranking for content across both pages. You'll need to specify a canonical url in your html so only one of the possible addresses for an event gets all the credit with search engines.</p>

