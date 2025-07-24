# Entity Framework Query using Contains with mulitple options
[Link to question](https://stackoverflow.com/questions/43874298/entity-framework-query-using-contains-with-mulitple-options)
**Creation Date:** 1494344641
**Score:** 2
**Tags:** sql, sql-server, entity-framework, entity-framework-core
## Question Body
<p>Using entity framework to return a list of people where the forename contains text in a string array.</p>

<p>Let's say:</p>

<pre><code>string[] search = new string[] { "bert", "rob" };
</code></pre>

<p>and query</p>

<pre><code>dataContext.People.Where(w =&gt; search.Any(a =&gt; w.Forename.Contains(a)));
</code></pre>

<p>This compiles and works BUT the process is actually calling all records from the database and then performing my where clause on the returned data. This makes sense.</p>

<p>Is there a way to rewrite the query so the where clause is generated in SQL? </p>

## Answers
### Answer ID: 43874767
<p>One way to do this is to use <a href="https://msdn.microsoft.com/en-us/library/jj592907(v=vs.113).aspx" rel="nofollow noreferrer">SqlQuery</a> and perform and actual SQL query.</p>

<pre><code>dataContext.Database.SqlQuery&lt;People&gt;("SELECT Forename, Lastname FROM myTable WHERE Forename LIKE '%bert%' or Forename LIKE '%rob%'");
</code></pre>

### Answer ID: 43874777
<p>I assume that dataContext.People is an <code>IQueryable</code> from the <code>DbSet</code> and that there is no materialization instruction involved such as <code>ToList()</code> or <code>AsEnumerable()</code>.</p>

<p>the answer is here: <a href="http://www.albahari.com/nutshell/predicatebuilder.aspx" rel="nofollow noreferrer">http://www.albahari.com/nutshell/predicatebuilder.aspx</a></p>

<p>in your case:</p>

<pre><code>var predicate = PredicateBuilder.False&lt;People&gt;();

foreach (string keyword in keywords)
{
    string temp = keyword;
    predicate = predicate.Or (p =&gt; p.Forename.Contains (temp));
}
dataContext.People.Where (predicate);
</code></pre>

