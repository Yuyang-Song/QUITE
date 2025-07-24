# Linq to SQL NullReferenceException&#39;s: A random needle in a haystack!
[Link to question](https://stackoverflow.com/questions/2633636/linq-to-sql-nullreferenceexceptions-a-random-needle-in-a-haystack)
**Creation Date:** 1271197615
**Score:** 1
**Tags:** linq-to-sql, nullreferenceexception
## Question Body
<p>I'm getting NullReferenceExeceptions at seemly random times in my application and can't track down what could be causing the error. </p>

<p>I'll do my best to describe the scenario and setup. </p>

<p>Any and all suggestions greatly appreciated!</p>

<ul>
<li><p>C# .net 3.5 Forms Application, but I use the WebFormRouting library built by Phil Haack (<a href="http://haacked.com/archive/2008/03/11/using-routing-with-webforms.aspx" rel="nofollow noreferrer">http://haacked.com/archive/2008/03/11/using-routing-with-webforms.aspx</a>) to leverage the Routing libraries of .net (usually used in conjunction with MVC) - intead of using url rewriting for my urls.</p></li>
<li><p>My database has 60 tables.  All Normalized. It's just a massive application. (SQL server 2008)</p></li>
<li><p>All queries are built with Linq to SQL in code (no SP's). Each time a new instance of my data context is created. I use only one data context with all relationships defined in 4 relationship diagrams in SQL Server.</p></li>
<li><p>the data context gets created a lot.  I let the closing of the data context be handled automatically.  I've heard arguments both sides about whether you should leave to be closed automatically or do it yourself. In this case I DONT do it myself.</p></li>
<li><p>It doesnt seem to matter if I'm creating a lot of instances of the data context or just one.</p></li>
</ul>

<p>For example, I've got a vote-up button.  with the following code, and it errors probably 1 in 10-20 times.</p>

<pre><code>protected void VoteUpLinkButton_Click(object sender, EventArgs e)
{
    DatabaseDataContext db = new DatabaseDataContext();

    StoryVote storyVote = new StoryVote();
    storyVote.StoryId = storyId;
    storyVote.UserId = Utility.GetUserId(Context);
    storyVote.IPAddress = Utility.GetUserIPAddress();
    storyVote.CreatedDate = DateTime.Now;
    storyVote.IsDeleted = false;

    db.StoryVotes.InsertOnSubmit(storyVote);
    db.SubmitChanges();

    // If this story is not yet published, check to see if we should publish it.  Make sure that
    // it is already approved.
    if (story.PublishedDate == null &amp;&amp; story.ApprovedDate != null)
    {
        Utility.MakeUpcommingNewsPopular(storyId);
    }

    // Refresh our page.
    Response.Redirect("/news/" + category.UniqueName + "/"
        + RouteData.Values["year"].ToString() + "/"
        + RouteData.Values["month"].ToString() + "/"
        + RouteData.Values["day"].ToString() + "/"
        + RouteData.Values["uniquename"].ToString());
}
</code></pre>

<p>The last thing I tried was the "Auto Close" flag setting on SQL Server. This was set to true and I changed to false.  Doesnt seem to have done the trick although has had a good overall effect.</p>

<p>Here's a detailed that wasnt caught. I also get slighly different errors when caught by my try/catch's.</p>

<pre><code>System.Web.HttpUnhandledException: Exception of type 'System.Web.HttpUnhandledException' was thrown. ---&gt;
System.NullReferenceException: Object reference not set to an instance of an object. at
System.Web.Util.StringUtil.GetStringHashCode(String s) at
System.Web.UI.ClientScriptManager.EnsureEventValidationFieldLoaded() at
System.Web.UI.ClientScriptManager.ValidateEvent(String uniqueId, String argument) at
System.Web.UI.WebControls.TextBox.LoadPostData(String postDataKey, NameValueCollection postCollection) at
System.Web.UI.Page.ProcessPostData(NameValueCollection postData, Boolean fBeforeLoad) at
System.Web.UI.Page.ProcessRequestMain(Boolean includeStagesBeforeAsyncPoint, Boolean includeStagesAfterAsyncPoint) --- End of inner exception stack trace --- at
System.Web.UI.Page.HandleError(Exception e) at System.Web.UI.Page.ProcessRequestMain(Boolean includeStagesBeforeAsyncPoint, Boolean includeStagesAfterAsyncPoint) at
System.Web.UI.Page.ProcessRequest(Boolean includeStagesBeforeAsyncPoint, Boolean includeStagesAfterAsyncPoint) at System.Web.UI.Page.ProcessRequest() at
System.Web.UI.Page.ProcessRequest(HttpContext context) at
ASP.forms_news_detail_aspx.ProcessRequest(HttpContext context) at
System.Web.HttpApplication.CallHandlerExecutionStep.System.Web.HttpApplication.IExecutionStep.Execute() at
System.Web.HttpApplication.ExecuteStep(IExecutionStep step, Boolean&amp; completedSynchronously)
</code></pre>

<p>HELP!!!</p>

## Answers
### Answer ID: 2633958
<p>oh boy, fingers crossed.</p>

<p>came accross this. <a href="http://forums.asp.net/t/1170677.aspx" rel="nofollow noreferrer">http://forums.asp.net/t/1170677.aspx</a></p>

<p>where it talks about setting: enableEventValidation="false" in the page or in web.config for all pages.</p>

<p>I would prefer not having to do this and technically it doesnt 'fix' the error, just avoids it by the looks of things.</p>

<p>On the live site, i'd be happy with a bandaid for now.</p>

<p>thanks Evgeny, you put me on the right track.   I suppose I suspected Linq to SQL wrongly and it should have been perhaps more obvious from the stacktrace.</p>

<p>Unfortunately (or fortunately), I'm trying a lot of 'new stuff', so lots of not yet seen errors.</p>

### Answer ID: 2633722
<p>From the stack trace it doesn't look like anything to do with LINQ. Looking at System.Web in Reflector it would appear that <code>Page.RequestViewStateString</code> is null somehow. I'd confirm that in the debugger when the exception occurs and try to track back what happens from there (using Reflector).</p>

