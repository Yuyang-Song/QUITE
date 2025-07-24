# Query to include non-protected resources only
[Link to question](https://stackoverflow.com/questions/15080721/query-to-include-non-protected-resources-only)
**Creation Date:** 1361848409
**Score:** 1
**Tags:** c#, asp.net, linq, entity-framework, linq-to-entities
## Question Body
<p>I am using Entity Framework to retrieve data from my database. You can see the database model here:</p>

<p><img src="https://i.sstatic.net/aC72g.png" alt="edmx"></p>

<p>I'm attempting to build a repeater where I show Resource Categories only if there is a resource <code>where IsProtected == false</code>.  Then an nested repeater showing the Resource itself.</p>

<p>Here is an abbreviated repeater to help clarify what I'm looking for</p>

<pre><code>&lt;asp:Repeater&gt;
    &lt;h2&gt;Category Name&lt;/h2&gt;
    &lt;ol&gt;
        &lt;asp:Repeater DataSource="&lt;%# ((ResourceCategory)Container.DataItem).Resource %&gt;"&gt;
            &lt;li&gt;Resource Name&lt;/li&gt;
        &lt;/asp:Repeater&gt;
    &lt;/ol&gt;
&lt;/asp:Repeater&gt;
</code></pre>

<p>The query that I'm currently uses does pull up any category that has a <code>Resource.Count() &gt; 0</code>, but not sure how to write my <code>where</code> statement since it is actually related to the <code>Resource</code> table:</p>

<pre><code>public List&lt;Model.ResourceCategory&gt; GetResourcesWithDocuments()
{
    using (var context = new SafetyInSightEntities())
    {
        return (from cat in context.ResourceCategory.Include("Resource")
                orderby cat.Name
                where cat.Resource.Count &gt; 0
                select cat).ToList();
    }
}
</code></pre>

<p>Can someone please help me rewrite my LINQ query so my inner repeater only shows resources where <code>IsProtected == false</code></p>

## Answers
### Answer ID: 15080921
<p>Try this:</p>

<pre><code>public IEnumerable&lt;ResourceCategoryFacade&gt; GetResourcesWithDocuments() // return weaker interface
{
    using (var context = new SafetyInSightEntities())
    {
        var q = from cat in context.ResourceCategory.Include(cat =&gt; cat.Resource)
                orderby cat.Name
                select new ResourceCategoryFacade // anonymous, or compiler-time type
                {
                    CategoryName = cat.Name,
                    Resources = cat.Resource.Where(r =&gt; !r.IsProtected).ToList() // or ToArray()
                };
        return q.ToList(); // or ToArray()
    }
}
</code></pre>

### Answer ID: 15080807
<p>I'm not exactly sure what you are asking, but I would assume you want this?</p>

<pre><code>public List&lt;Model.ResourceCategory&gt; GetResourcesWithDocuments()
{
    using (var context = new SafetyInSightEntities())
    {
        return (from cat in context.ResourceCategory
                orderby cat.Name
                where cat.Resource.Any()
                select new 
                {
                    CategoryName = cat.Name,
                    Resources = cat.Resource.Where(r =&gt; r.IsProtected == false).ToList()
                }).ToList();
    }
}
</code></pre>

<p>It's possible you want to use <code>All</code> rather than <code>Any</code>, but not sure based on the question.</p>

