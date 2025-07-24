# Reload data from db into IQueryable&lt;T&gt; without rewriting the expression
[Link to question](https://stackoverflow.com/questions/11920313/reload-data-from-db-into-iqueryablet-without-rewriting-the-expression)
**Creation Date:** 1344754575
**Score:** 0
**Tags:** entity-framework, entity-framework-4.1, iqueryable
## Question Body
<blockquote>
  <p><strong>Possible Duplicate:</strong><br>
  <a href="https://stackoverflow.com/questions/3686810/dbcontexts-internal-caching">DbContext&#39;s internal caching (?)</a>  </p>
</blockquote>



<p>I have an instance of my <code>DbContext</code> and a <code>IQueryable</code> in the <code>ViewModelBase</code> which fills from <code>BootStrapper</code> and the <code>IQueryable</code> needs to reload from the database several times, and I want to do it by calling some simple method without caring about what the query expression is.</p>

<p><strong>In simple words :</strong></p>

<p>I'd like to load the data into an <code>IQueryable&lt;T&gt;</code> without rewriting the expression and tools I have are:</p>

<p>1 => An <code>IQueryable</code></p>

<p>2 => An instance of <code>DbContext</code></p>

<p>As I change data in the database and try IQueryable.ToList() , the result does not update.</p>

<pre><code>IQueryable&lt;Person&gt; ViewModelDataContext;
ViewModelDataContext = repository.GetAll&lt;Person&gt;();
var x = ViewModelDataContext.ToList();
//Some changes into database
repository = new Repository();
var y = ViewModelDataContext.ToList();
//But as result, the x is exactly returns the same result as y and I'd like the y to be updated after  database changes.
</code></pre>

<p>Any suggestions?</p>

## Answers
### Answer ID: 11921477
<p>Most likely, the problem is that Entity Framework returns you (rightfully) the same entity instances every time. This is an important feature of an ORM. It does not without your permission overwrite their fields with fresh values from the database. If it did it would lead to spurious state corruption and non-local side-effects across your application.</p>

<p>If you were to load a non-entity type using this approach it would work. Or read about merge options.</p>

