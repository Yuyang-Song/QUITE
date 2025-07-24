# Can I use HttpHandler to fake the existence of aspx pages?
[Link to question](https://stackoverflow.com/questions/673736/can-i-use-httphandler-to-fake-the-existence-of-aspx-pages)
**Creation Date:** 1237820654
**Score:** 3
**Tags:** asp.net
## Question Body
<p>I am building a web site with ASP.NET 3.5, and most of the site structure is static enough to create a folder structure and aspx pages.  However, the site administrators want the ability to add new pages to different sections of the site through a web interface and using a WYSIWYG editor.  I am using nested master pages to give the different sections of the site their own menus.  What I would like to do is have a generic page under each section of the site that uses the appropriate master page and has a place holder for content that could be loaded from a database.  I would also like these "fake" pages to have a url like any other aspx page, as if they had corresponding files on the server.  So rather than have my url be:</p>

<pre><code>http://mysite.com/subsection/gerenicconent.aspx?contentid=1234
</code></pre>

<p>it would be something like:</p>

<pre><code>http://mysite.com/subsection/somethingmeaningful.aspx
</code></pre>

<p>The problem is that somethingmeaningful.aspx does not exist, because the administrator created it through the web UI, and the content is stored in the database.  What I'm thinking is that I'll implement an HTTP handler that handles requests for aspx files.  In that handler, I'll check to see if the URL that was requested is an actual file or one of my "fake pages".  If it is a request for a fake page, I'll re-route the request to the generic content page for the appropriate section, change the query string to request the appropriate data from the database, and rewrite the URL so that it looks to the user as if  the fake page really exists.  The problem I'm having right now is that I can't figure out how to route the request to the default handler for aspx pages.  I tried to instantiate a PageHandlerFactory, but the constuctor is protected internal.  Is there any way for me to tell my HttpHandler to call the HttpHandler that would normal be used to process a request?  My handler code currently looks like this:</p>

<pre><code>using System.Web;
using System.Web.UI;

namespace HandlerTest
{
    public class FakePageHandler : IHttpHandler
    {
        public bool IsReusable
        {
            get { return false; }
        }

        public void ProcessRequest(HttpContext context)
        {
            if(RequestIsForFakedPage(context))
            {
                // reroute the request to the generic page and rewrite the URL
                PageHandlerFactory factory = new PageHandlerFactory(); // this won't compile because the constructor is protected internal
                factory.GetHandler(context, context.Request.RequestType, GetGenericContentPath(context), GetPhysicalApplicationPath(context)).ProcessRequest(context);
            }
            else
            {
                // route the request to the default handler for aspx pages
                PageHandlerFactory factory = new PageHandlerFactory();
                factory.GetHandler(context, context.Request.RequestType, context.Request.Path, context.Request.PhysicalPath).ProcessRequest(context);
            }
        }

        public string RequestForPageIsFaked(HttpContext context)
        {
            // TODO
        }

        public string GetGenericContentPath(HttpContext context)
        {
            // TODO
        }

        public string GetPhysicalApplicationPath(HttpContext context)
        {
            // TODO
        }
    }
}
</code></pre>

<p>I still have some work to do to determine if the request is for a real page, and I haven't rewritten any URLs yet, but is something like this possible?  Is there another way to create a PageHandlerFactory other than calling its constructor?  Is there any way I can route the request up to the "normal" HttpHandler for an aspx page?  I'd basically be saying "process this ASPX request as you normally would."</p>

## Answers
### Answer ID: 673832
<p>You would be better off using an http module for this, as in this case you can use the RewritePath method to route the request for fake pages, and do nothing for actual pages which will allow them to be processed as normal.</p>

<p>There is a good explanation of this <a href="http://weblogs.asp.net/scottgu/archive/2007/02/26/tip-trick-url-rewriting-with-asp-net.aspx" rel="nofollow noreferrer">here</a> which also covers the benefits of using IIS 7.0 if that is an option for you.</p>

### Answer ID: 673787
<p>If you are using 3.5, look into using asp.net routing.</p>

<p><a href="http://msdn.microsoft.com/en-us/library/cc668201.aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/cc668201.aspx</a></p>

### Answer ID: 673786
<p>I've just pulled this off a similar system we've just written.</p>

<p>This method takes care of physical pages and "fake" pages. You'll be able to ascertan how this fits with your fake page schema, I'm sure.</p>

<pre><code>public class AspxHttpHandler : IHttpHandlerFactory
{
        #region ~ from IHttpHandlerFactory ~

        public IHttpHandler GetHandler(HttpContext context, string requestType, string url, string pathTranslated)
        {
                    string url=context.Request.Url.AbsolutePath;
            string[] portions = url.Split(new char[] { '/', '\\' });
                    // gives you the path, i presume this will help you identify the section and page
                    string serverSidePage=Path.Combine(context.Server.MapPath("~"),url);
                    if (File.Exists(serverSidePage))
                    {
                             // page is real
                            string virtualPath = context.Request.Url.AbsolutePath;
                string inputFile = context.Server.MapPath(virtualPath);

                try
                {
                                    // if it's real, send in the details to the ASPX compiler
                    return PageParser.GetCompiledPageInstance(virtualPath, inputFile, context);
                }
                catch (Exception ex)
                {
                        throw new ApplicationException("Failed to render physical page", ex);
                }
                      }
                      else
                      {
                            // page is fake
                            // need to identify a page that exists which you can use to compile against
                            // here, it is CMSTaregtPage - it can use a Master
                            string inputFile = context.Server.MapPath("~/CMSTargetPage.aspx");
                string virtualPath = "~/CMSTargetPage.aspx";
                            // you can also add things that the page can access vai the Context.Items collection
                            context.Items.Add("DataItem","123");
                            return PageParser.GetCompiledPageInstance(virtualPath, inputFile, context);
}

public void ReleaseHandler(IHttpHandler handler)
{

}
</code></pre>

