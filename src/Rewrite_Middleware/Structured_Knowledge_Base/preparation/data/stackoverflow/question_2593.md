# c# .net access parent obj
[Link to question](https://stackoverflow.com/questions/41903571/c-net-access-parent-obj)
**Creation Date:** 1485553721
**Score:** 0
**Tags:** c#, asp.net, asp.net-mvc
## Question Body
<p>I am using .net c# MVC controller to query database for many of my projects.  Every time i create a new controller, I find myself having to rewrite some of the same function for the new controller hence, I thought about writing a basic controller to handle some of the basic task that I use in all my controller (e.g., run a query and run json).</p>

<p>In my controller, I reference the basic controller like this. </p>

<pre><code>namespace myWebAPI.Controllers
{
    public class esrcController : Controller
    {
        //
        // GET: /esrc/
        string db = "esrc-";
        basicController BasicController = new basicController();


        public string test()
        {
            return "test" + Request.ServerVariables["HTTP_REFERER"];
        }
        public string getCodingException()
        {

            return @"{""data"":" + BasicController.getDataNconvertToJSON(
                "select * from z_codingexception order by nc_key",
                BasicController.getEnviroment(db)) + "}";
        }
    }
}
</code></pre>

<p>in my <code>BasicController</code>, the <code>getEnviroment</code> looks at the url to determine the environment hence I need access to :</p>

<pre><code>Request.ServerVariables["HTTP_REFERER"] and Request.ServerVariables["HTTP_HOST"].ToString().ToLower();
</code></pre>

<p>but Request is null in this controller, I only have access to request in the main controller.  How do I reference httpRequest from basic controller?</p>

## Answers
### Answer ID: 41903637
<p>Just because you instantiate a new instance of a controller, doesn't mean you'll have access to the context.</p>

<p>One option is to create an abstract base controller that all of your other controlers would inherhit from. You'll then have access to the specific objects like <code>Request</code></p>

<p><strong>WebApiConfig.cs</strong></p>

<pre><code> config.MapHttpAttributeRoutes();
</code></pre>

<p><strong>Your Controller</strong> </p>

<pre><code>public abstract class MyBaseController : Controller
{
 protected void myMethod()
 {
  // you have access to Request here
 }
}

public class MyController : MyBaseController
{
    [HttpGet]
    [Route("my/getstuff")]
    public IHttpActionResult GetStuff() 
    {
       // do stuff
       base.myMethod();
       return Ok();
    }
}
</code></pre>

### Answer ID: 41903696
<p>Create an action filter and add it as an attribute to that class. Within the action filter yuo wil have access to the <code>Request</code> object. If you override the <code>OnActionExecuting</code> function, the functionality in your filter will be executed before your controller.</p>

<p>Create a custom filter</p>

<pre><code>public class CustomAttribute : ActionFilterAttribute
{
    public override void OnActionExecuting(ActionExecutingContext filterContext)
    {
      //DO STUFF WITH YOUR REQUEST OBJECT HERE..
    }
}
</code></pre>

<p>Add the filter as an attribute to your controller</p>

<pre><code>[CustomAttribute]
public class esrcController : Controller
</code></pre>

