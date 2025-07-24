# IQueryable with Where containing a list throws &quot;No mapping to a relational type can be found for the CLR type &#39;List&lt;string&gt;&#39;.&quot;
[Link to question](https://stackoverflow.com/questions/60526465/iqueryable-with-where-containing-a-list-throws-no-mapping-to-a-relational-type)
**Creation Date:** 1583326045
**Score:** 0
**Tags:** asp.net-core, db2, entity-framework-core
## Question Body
<p>While using IBM.EntityFrameworkCore and IBM.Data.DB2.Core an error is being thrown everytime when I have a <code>Where</code> statement containing a list on which some kind of verification is being performed.</p>

<p>The error is being thrown when the IQueryable is being materialized i.e. converted to a list using <code>ToList()</code>.</p>

<blockquote>
  <p>No mapping to a relational type can be found for the CLR type
  'List'.</p>
</blockquote>

<pre><code>private IQueryable&lt;CollectionActivityInOverview&gt; FilterActivitiesForAdvisor(IQueryable&lt;CollectionActivityInOverview&gt; activitiesList, List&lt;string&gt; advisorCodes)
{
    List&lt;AdvisorCustomerInfo&gt;advisorInformation = GetAdvisorCustomers(advisorCodes).Result;
    var advisorCustomers = advisorInformation.SelectMany(a =&gt; a.Customers)
        .Distinct()
        .ToList();

    // This is the problematic spot
    activitiesList = activitiesList.Where(a =&gt; advisorCustomers.Any(ac =&gt; ac == a.CustomerId));

    return activitiesList;
}
</code></pre>

<p>.</p>

<pre><code>public class AdvisorCustomerInfo
{
    public string AdvisorCode { get; set; }

    public List&lt;string&gt; Customers { get; set; }
}
</code></pre>

<p>What could the error be, since AFAIK, conditions using lists should not only be supported by Linq to Entities, but also supported by Linq to SQL.</p>

<p><strong>Is it possible that DB2 Entity Framework library doesn't support i.e. doesn't translate such conditions into SQL?</strong> </p>

<p>Can someone confirm it?</p>

<p>My main requirement is to keep IQueryable in order to execute the query against the database. Is it possible to rewrite the query using something else?</p>

## Answers
### Answer ID: 60799263
<p>It is true that DB2 EF Core Library (at the moment) doesn't support using of <code>.Any()</code> or <code>.Contains()</code>. It is, however, possible to "override" this behaviour by writing a custom Expression that mimics SQL <code>WHERE</code> function with multiple conditions in the query.</p>

<p>Basically you pass the list you want to iterate and you append each item of the list to the Expression body using <code>Expression.OrElse()</code>. At the end you return the expression using <code>Expression.Call()</code>.</p>

