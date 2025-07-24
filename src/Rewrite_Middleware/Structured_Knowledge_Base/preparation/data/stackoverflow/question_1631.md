# Linq Query slow on host but not on dev machine
[Link to question](https://stackoverflow.com/questions/1989308/linq-query-slow-on-host-but-not-on-dev-machine)
**Creation Date:** 1262372224
**Score:** 0
**Tags:** sql-server, asp.net-mvc, linq-to-entities, performance
## Question Body
<p>I'm running ASP.NET MVC 2 Preview 2 (With VS 2010 Beta 2) using Entity Framework.</p>

<p>Earlier yesterday, for some unknown reason, a single page in my app started to load very slowly on my host.</p>

<p>The problem is, this only occurs on my host and I haven't changed anything for it to load slow.</p>

<p>Here is the action that is loading very slow:</p>

<pre><code>public ActionResult Index()
{
    MyEntitiesContext db = new MyEntitiesContext();
    IEnumerable&lt;City&gt; cities = db.Cities.Where(x =&gt; x.Orders.Count != 0).OrderBy(x =&gt; x.Name);
    return View(cities);
}
</code></pre>

<p>and this is my Index.aspx</p>

<pre><code>       &lt;ul&gt;
         &lt;% foreach (City g in Model){ %&gt;
            &lt;li&gt;
              &lt;%= Html.ActionLink(g, "View", "Cities", new { CityID = g.CityID}, null)%&gt;(&lt;%= g.City %&gt;)
           &lt;/li&gt;         
         &lt;% } %&gt;
       &lt;/ul&gt;
</code></pre>

<p>Now this works perfectly fine on my dev machine, and it worked fine on my host until late last night.</p>

<p>Here are some diagnostics I tested:</p>

<ol>
<li>The code works/loads fine on my dev machine using my dev machine's SQL database</li>
<li>When I switch the connection string on my dev machine app to my hosts sql server, the code takes forever to load</li>
<li>When I run the LINQ against my dev machine SQL server using <code>LINQ Pad</code> it runs quick (.3 seconds) and when I run it against my host's SQL server it also runs quick (.3 seconds)</li>
<li><p>One time I used my host's SQL server for the connection string and ran the app in VS 2010 debug, after a some time, I received this error</p>

<pre><code>Execution of the command requires an open and available connection. 
The connection's current state is broken.
</code></pre></li>
</ol>

<p>The table Cities has over 7000 rows, with (as of now) only about 4-5 rows that actually have Orders (so those are the ones that will be displayed).</p>

<p>I talked to my host, they said they don't see anything wrong with the server (Which makes sense because other pages on the website that query the server run fine). They restarted it, but I'm still getting the same slow load times.</p>

<p>This is a weird problem, I have no idea what could be causing this, any help would be greatly apprecaited.</p>

<h2>UPDATE 1:</h2>

<p>Here is the stop watch results</p>

<pre><code>        Stopwatch s = new Stopwatch();
        s.Start();
        IEnumerable&lt;City&gt; cities = db.Cities.Where(x =&gt; x.Orders.Count != 0).OrderBy(x =&gt; x.Name);
        s.Stop();
        long t = s.ElapsedTicks;
        return View(cities);
</code></pre>

<p>When I place a break point at <code>return View(cities)</code>, <code>t</code> had the value of <code>387</code> which makes sense since cities is just making the statement, which also means the issue lies in the <code>foreach</code> that executes the statement in the view.</p>

<p>Since I can't put break points into the view, I went ahead and did the following:</p>

<pre><code>        s.Start();
        List&lt;City&gt; list = cities.ToList();
        s.Stop();
        long q = s.ElapsedTicks;
</code></pre>

<p>to mimic executing the statement (from my understanding, running a <code>foreach</code> on an <code>IEnumerable</code> is equivalent to calling <code>.ToList()</code>)</p>

<p>After a very long time (note: I'm still using my shared host's SQL server in the connection string), q's value was <code>890489194</code>. So the issue is executing the query. Is this an obvious indication to an issue with the SQL database/server?</p>

<h2>Update 2:</h2>

<p>If I rewrite the query as such:</p>

<pre><code>  db.Orders.Select(x =&gt; x.City).Distinct();
</code></pre>

<p>This runs fast and the page loads fine. My only concern is scaling. Which query would be better for a large database.</p>

<p>Again, each <code>Order</code> has a single <code>City</code> associated with it, and a <code>City</code> can have many <code>Orders</code>.</p>

## Answers
### Answer ID: 1989929
<p>I am going to  just come out and say you need an index for the join to your <code>Order</code> table.</p>

