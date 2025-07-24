# Rewriting a legacy-proprietary Web Application to MVC3/Entity-Code-First
[Link to question](https://stackoverflow.com/questions/4840233/rewriting-a-legacy-proprietary-web-application-to-mvc3-entity-code-first)
**Creation Date:** 1296345149
**Score:** 7
**Tags:** c#, asp.net, asp.net-mvc, entity-framework, ef-code-first
## Question Body
<p>I've posted a few questions over the months about structure of ASP.NET applications and Database-Abstraction-Layers, for the purposes of rewriting (from the ground-up), a legacy web application.  I've recently stumbled on MVC3/Entity-Code-First and after spending some time with it, have fallen in love with how it works, how things are abstracted out, and I'm looking for any excuse to use it!  </p>

<p>The legacy application is a C++/CLI windows service that generates it's own HTML (very old-school HTML at that with CSS just used for colours, and tables-abound), and with interface very tightly coupled to business-logic.  Basically, anything is going to be an improvement.</p>

<p>However, and perhaps this is because I have not spent enough time yet with MVC, I have a few nagging doubts and wondered if some of you MVC-Pros could waft their experience in my direction.</p>

<ul>
<li><p>The legacy app uses custom controls (it's own form of them) to bind combo-boxes to data, and dynamically repopulate dependent combo-boxes based on selections in another.  In ASP.NET, this question is answered easily as one just throws an <code>asp:DataList</code> control on the page, binds it to a data source and voila.  A bit of simple code allows you to then filter other combo boxes on the selected value.  It also would be easy in ASP.NET, to implement another data-list that even automated dependent data in this fashion (which would mimic the behavior of the legacy app quite nicely).  I can't seem to find a notion of custom controls in MVC, though I assume this kind of stuff is handled by jQuery calls to get data and throw it in to a combo box.  But is this done for every combo-box on every page that has one?  Is this a case for partial views with appropriate parameters being passed, or this just stupid?</p></li>
<li><p>I guess this relates more to the Entity Framework than MVC, but most of the examples I've found on the web, and tutorials, perform LINQ queries to return a collection of objects to display, e.g this, from the MvcMovie example:</p>

<pre><code>public ActionResult Index()
{
    var movies = from m in db.Movies
                 where m.ReleaseDate &gt; new DateTime(1984, 6, 1)
                 select m;

    return View(movies.ToList());
}
</code></pre>

<p>Which is then rendered using a <code>@foreach</code> loop in the view.  This is all great.  The legacy application has a single browse page that is used by all the other areas of the system (there are over 50).  It does this by inspecting the column order defined for the user logged on, flattening any foreign keys (so that the field on the foreign table is displayed as opposed to the non-user-friendly primary key value) and also allows the user to apply custom filters to any column.  It does this also for tables that have upward of 100k rows.  How would one go about writing something similar using the Entity-framework and views?  In ASP.NET I'd probably solve this by dynamically generating a grid view of some sort and have it auto-generate the columns and apply the filters.  This seems like it might me more work in MVC.  I am missing something?</p></li>
<li><p>The legacy application has several operations that operate over large sets of data.  Now because it was a service, it could launch these threads without worrying about being shut-down.  One of my questions here on SO was about static managers being around and the introduction of an AppPool recycle, but I have decided that having an auxiliary service is a good option.  That said, the legacy app applies an update statement to large groups of records rather than single rows.  Is this possible with Entity-Framework without writing custom SQL against the database that bypasses the normal models?  I hope I don't have to do something like this (not that I would, this is just for example)</p>

<pre><code>var records = from rec in myTable
              where someField = someValue
              select rec;
foreach(rec in records)
    rec.applyCalculation();
db.SaveDbChanges();
</code></pre>

<p>I suspect this could take a lot of time, whereas the legacy app would just do:</p>

<pre><code>UPDATE myTable
SET field1 = calc
WHERE someField = someValue
</code></pre>

<p>So it's not entirely clear to me how we use our models in this manner.</p></li>
<li><p>The legacy application has some data panels in the layout that get carried around whatever page you're on.  Looking here on Stackoverflow, I found <a href="https://stackoverflow.com/questions/924879/passing-model-to-layout-in-ms-mvc">this</a> question, which implies that <em>every</em> view needs to pass this information to the layout?  Is this so, or is there a better way?  Ideally, I'd like my layout to be able to access a particular model/repository and display the data in a side-panel.  Adding to every view page could be quite repetitive and prone to error.  Not to mention the time it would take if I needed to modify something.  A partial view would do here, but again I am unsure how to pass a model to it on the layout page.</p></li>
<li><p>Finally, I was disappointed, after installing Ef-Code-First, to find that a really nice attribute, <code>SourceName</code> has not made it in, yet.  This would be very nice in mapping against legacy tables/columns and I am not entirely sure why it has been left out at this point (at least, my intellisense says it's not there!)  Has anyone got an idea when this might come about?  I could do without it for a while, but ultimately it would be incredibly useful.</p></li>
</ul>

<p>Sorry for the lengthy questions.  After ages of investigative work in ASP.NET and MVC3, I really want to go with MVC3!  </p>

## Answers
### Answer ID: 4928046
<p>You might not like it, but it could make a lot more sense to just refactor the c++ application. Especially to the business. There's nothing wrong with generating html. Much easier to refactor to modern html/css than a set of templates. </p>

### Answer ID: 4840507
<p>If I managed to extract the questions correctly then this would be my reply:</p>

<ol>
<li><p>You are right in your thinking about master - detail dropdowns (or other controls, for that matter). jQuery AJAX/JSON calls (mostly GETs) will be what you need. If you only have one dropdown on your page, then of course you don't need that kind of interactivity - you can just prepare the model for it in your controller action (you create a SelectList object).</p></li>
<li><p>Here you would most likely end up using some kind of a grid system like jqGrid or Flexigrid. They do most of the stuff regarding filtering/searching/querying themselves. Still you will have to provide JSON controller actions that will be serving data.</p></li>
<li><p>Yes you can execute SQL via EF. There's <code>ExecuteStoreQuery()</code> and <code>ExecuteStoreCommand()</code>. Here's more on those <a href="http://msdn.microsoft.com/en-us/library/ee358769.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/ee358769.aspx</a></p></li>
<li><p>You can call <code>RenderAction()</code> from the view and have this action prepare the data on demand (whenever you call it) and render out the Partial (or normal) view and feed the data (model) to it. <code>RenderPartial()</code> is a bit more clumsy with this - it requires you to have the model already available in the view in which you are calling <code>RenderPartial()</code>. <code>RenderPartial()</code> never goes back to the controller action - it just renders out that HTML defined in the template using the model you provided in its call from within the view.</p></li>
<li><p>Unfortunately I don't know the answer to this.</p></li>
</ol>

<p>HTH</p>

