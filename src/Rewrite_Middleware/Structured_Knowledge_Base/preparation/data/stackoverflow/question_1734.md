# Need help rewriting this Linq query to move it from code-behind to DAL as reusable object
[Link to question](https://stackoverflow.com/questions/5531267/need-help-rewriting-this-linq-query-to-move-it-from-code-behind-to-dal-as-reusab)
**Creation Date:** 1301852314
**Score:** 2
**Tags:** asp.net, linq, linq-to-entities, data-access-layer, webforms
## Question Body
<p>I'm working to move my simple asp.net website to a three layer architecture.  Currently I have Linq queries like the one below in my code-behind files.  Basically this code snippet retrieves a collection of customer data from the database and then binds it to a grid control.</p>

<p>I'm wondering if someone can guide me on how to rewrite this in order to move it to my newly-created data access layer.  I'm thinking I will turn it into a class (e.g. GetUserBoxesByStatus()) that can be reused throughout the site.</p>

<pre><code>            var boxes = from p in sbm.Packages
                    where p.UserID == CurrentUserId &amp;&amp; p.StatusID &gt; 1 &amp;&amp; p.StatusID &lt; 3
                    select new { p.PackageTag, p.PackageName, p.DateReceived, p.DateShipped };
        GridView1.DataSource = boxes;
        DataBind();
</code></pre>

<p>Some of the options that I've investigated but have not had success implementing are the following:</p>

<p><li> DataTable --- returning a DataTable seems like the best solution but it also appears to require a lot of potentially unecessarry code to define a table (isn't the data source already mapped in my Linq 2 Entities dbml?)
<li> IEneuerable --- I think I could pass an IEnumerable list between the layers but after reading many tutorials about Linq I'm still a little lost
<li> DTO --- Conceptually I think I understand what a DTO is but I am not clear on how to begin implementing this approach
<li> POCO --- Again, the concept seems logical enough but I don't know how to put this into practice</p>

<p>I'm hoping someone here can look at my code example and propose how they would tackle this using one of the above or some other solution.</p>

## Answers
### Answer ID: 5531355
<p>Create a class with the properties you need.  Select into that class.  Return a strongly-typed List (so that the query is actually performed in the DAL, not in your view).  Bind your data source to the list.</p>

<pre><code>public class PackageViewModel
{
   public string Tag { get; set; }
   public string Name { get; set; }
   public DateTime Received { get; set; }
   public DateTime Shipped { get; set; }
}
</code></pre>

<p>DAL</p>

<pre><code>public List&lt;PackageViewModel&gt; GetUserBoxesByStatus( int userID, int minStatus, int maxStatus )
{
    return sbm.Packages
              .Where( p =&gt; p.UserID == userID
                            &amp;&amp; p.StatusID &gt; minStatus
                            &amp;&amp; p.StatusID &lt; maxStatus )
              .Select( p =&gt; new PackageViewModel
               {
                   Tag = p.PackageTag,
                   Name = p.PackageName,
                   Received = p.DateReceived,
                   Shipped = p.DateShipped
               })
              .ToList();
}
</code></pre>

