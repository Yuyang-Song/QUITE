# How can I manually join cached Entity Framework objects?
[Link to question](https://stackoverflow.com/questions/23232267/how-can-i-manually-join-cached-entity-framework-objects)
**Creation Date:** 1398210328
**Score:** 0
**Tags:** linq, entity-framework, caching
## Question Body
<p>I'm having a performance issue with lookups using the navigation properties of an EF model.</p>

<p>My model is something like this (conceptually):</p>

<pre><code>public class Company
{
    public int ID { get; set; }
    public string CompanyName { get; set; }

    public EntityCollection&lt;Employee&gt; Employees { get; set; }
}

public class Employee
{
    public int CompanyID { get; set; }
    public string EmployeeName { get; set; }

    public EntityReference&lt;Company&gt; CompanyReference { get; set; }
}
</code></pre>

<p>Now let's say I want to get a list of all <strong>Companies</strong> that have (known) <strong>Employees</strong>. </p>

<p>Additionally, assume that I've already cached lists of the both the <strong>Companies</strong> and the <strong>Employees</strong> through previous calls:</p>

<pre><code>var dbContext = new EmploymentContext();

var allCompanies = dbContext.Companies.ToList();
var allEmployees = dbContext.Employees.ToList();

bool activeCompanies = 
        allCompanies.Where(company =&gt; company.Employees.Any()).ToList();
</code></pre>

<p>This (in my environment) generates a new SQL statement for each <strong>.Any()</strong> call, following the <em>Employees</em> navigation property.</p>

<p>I already have all the records I need in my cached lists, but they're not 'connected' to each other on the client side.</p>

<p>I realize I can add .Include() calls to my initial cache-fill statement. I want to avoid doing this because in my actual environment I have a large number of relations and a large number of lists I'm populating up front. I'm caching largely to keep Linq from generating overly-complicated nested SQL statements that tend to bog down my database server.</p>

<p>I also realize I can modify my query so as to do an in-memory join:</p>

<pre><code>bool activeCompanies = allCompanies.Where
(
    company =&gt; allEmployees.Any(employee =&gt; employee.CompanyID == company.ID)
);
</code></pre>

<p>I'm trying to avoid doing such a rewrite, because the actual business logic gets rather involved. Using Linq statements has significantly improved the readability of this logic, and I'd prefer not to lose that if at all possible.</p>

<hr>

<p>So my question is this: can I connect them together manually somehow, in the way that the Entity Framework would connect them? </p>

<p>I'd like to continue to use the <strong>.Any()</strong> operator, but I want it to examine only the objects I have in memory in my <strong>dbContext</strong> - without going back to the database repeatedly.</p>

