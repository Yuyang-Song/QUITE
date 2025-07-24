# Passing List of KeyValuePairs to LINQ query and selecting the Value for the Key that matches the entity&#39;s Id
[Link to question](https://stackoverflow.com/questions/73500765/passing-list-of-keyvaluepairs-to-linq-query-and-selecting-the-value-for-the-key)
**Creation Date:** 1661515468
**Score:** 2
**Tags:** c#, linq, entity-framework-core, linq-to-entities, .net-5
## Question Body
<p>What is the best way to solve this?</p>
<p><strong>TL;DR version:</strong></p>
<p>Using LINQ and EntityFramework I am trying to pass in a <code>List</code> of <code>KeyValuePair</code>s to a LINQ query, then for each entity who's ID matches any Key in the list, selecting a new column with that key's value.</p>
<p>So if my <code>KeyValuePair</code>s are</p>
<pre><code>List&lt;KeyValuePair(int, long)&gt; keyValuePairs = new() 
{
    new(1, 10),
    new(2, 20),
    new(3, 30)
}
</code></pre>
<p>where the key is an <code>EmployeeId</code> and the value is a <code>CompanyId</code>,</p>
<p>and I'm querying an Employees table, with two columns, <code>Id</code> and <code>Name</code>,</p>
<p>and my <code>EmployeeModel</code> class is</p>
<pre><code>public int Id;
public int Name;
public long CompanyId;
</code></pre>
<p>I want to do something like this:</p>
<pre><code>var keys = keyValuePairs.Select(x =&gt; x.Key);

IQueryable&lt;EmployeeModel&gt; EmployeeModels = Db.Employees
    .Where(e =&gt; keys.Contains(p.Id))
    .Select(e =&gt; new EmployeeModel 
    {
        Id = e.Id,
        Name = e.Name,
        CompanyId = keyValuePairs.Where(x =&gt; x.Key == e.Id).Select(x =&gt; x.Value).First()
    });
</code></pre>
<p>Currently I get this exception:</p>
<blockquote>
<p>The LINQ expression 'x' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'.</p>
</blockquote>
<p>I want to avoid loading this into memory because the results could potentially be hundreds of thousands. In addition, I need to pass the result into a method that requires an IQueryable</p>
<p><strong>More context for understanding what I'm trying to do (and maybe someone can see if this is an x-y problem):</strong></p>
<p>I have two Databases
Database A has a Table called Companies and a join table called CompanyEmployees</p>
<p>Database B has a Table called Employees
The Employee table has a column for Employee Id, but no column for Company Id</p>
<p>My <code>EmployeeModel</code> class however, has a prop for the <code>CompanyId</code> of the company to which the employee belongs.
I'm trying to load a list of employees, and selecting a <code>EmployeeModel</code> which includes the <code>CompanyId</code></p>
<p>The way I'm trying to accomplish that is loading into memory a List of <code>KeyValuePair</code>s where the <code>Key = CustomerEmployee.EmployeeId</code> and the <code>Value = CustomerEmployee.CustomerId</code> and then using that List to Query the other Db.
(I don't see any alternative to loading the List of <code>KeyValuePair</code>s into memory, even though I'd obviously rather not)</p>

## Answers
### Answer ID: 73501127
<p>Also you probably have a problem with this part:</p>
<pre><code>CompanyId = keyValuePairs.Where(x =&gt; x.Key == e.Id).Select(x =&gt; x.Value)
</code></pre>
<p>As CompanyId is a long, and the result of your Linq expression is a IEnumerable.
If you're sure you have a result and only one, then you may use:</p>
<pre><code>CompanyId = keyValuePairs.Where(x =&gt; x.Key == e.Id).Select(x =&gt; x.Value).First()
</code></pre>

