# How to write two-step first-l2e-then-l2o IQueryable?
[Link to question](https://stackoverflow.com/questions/38565065/how-to-write-two-step-first-l2e-then-l2o-iqueryable)
**Creation Date:** 1469441759
**Score:** 0
**Tags:** entity-framework, linq, dynamic-linq
## Question Body
<p>Let's say I have an Entity Framwork query</p>

<pre><code>var query = db.Entities
  .FancyQueryStuff()
  .Where(GetFilter()) // *
  .OrderBy(GetSort()) // *
  .Take(GetNumberOfRows()) // *
;
</code></pre>

<p>and figure that this query is very slow. Testing reveals that the following rewrite is much faster:</p>

<pre><code>var ids = db.Entities
  .FancyQueryStuff()
  .Where(GetFilter()) // *
  .OrderBy(GetSort()) // *
  .Take(GetNumberOfRows()) // *
  .Select(x =&gt; x.Id)
  .ToArray()
;

var query = db.Entries
  .FancyQueryStuff()
  .OrderBy(GetSort()) // *
  .Where(x =&gt; ids.Contains(x.Id));
</code></pre>

<p>Whether that is quicker depends on a lot of things, including the sql database used, but I have a scenario in which this is the case with SQL Server and a particular query doing heavy joining.</p>

<p>Now the problem I have is that I want to use libraries that take <code>IQueryable</code>s and apply <code>Where</code>, <code>OrderBy</code>, <code>Take</code> and <code>Skip</code> internally according to UI information the get from somewhere else (DevExpress/Telerik grids with paging, where the user clicks on captions to sort, etc.).</p>

<p>That means I have to write the query in a form where all the rows marked with an asterisk can be applied by a third-party framework.</p>

<p>With Devextreme, for example, you have a method that takes the query plus a data structure representing the filter/sorting/paging in a custom format and returns the query results you are supposed to pass to a client in an html application:</p>

<pre><code>var result = DataSourceLoader.Load(query, loadOptions);
</code></pre>

<p><code>DataSourceLoader.Load</code> applies everything of the kind I marked with an asterisk to the end of the query, executes it and returns the result.</p>

<p>I guess it's possible to do what I want with some heavy guns of linq magic (dynamic linq?), but before I try myself I thought maybe someone already has a snippet ready for this probably not too uncommon use case.</p>

