# How to easily reuse POCO classes that have a reference to a third party POCO class - .NET Core EF
[Link to question](https://stackoverflow.com/questions/51057490/how-to-easily-reuse-poco-classes-that-have-a-reference-to-a-third-party-poco-cla)
**Creation Date:** 1530086281
**Score:** 1
**Tags:** c#, mysql, asp.net-core, entity-framework-core
## Question Body
<p>This post is pretty specific but ill try to generalize it as much as possible.
Without jumping directly in all the background information, the central question is:
<strong><em>What is the best way or implementation, for an API project build in .NET Core 2 and EF Core, to easily reuse your own set of POCO classes that have a reference to a third party their POCO classes, and with reuse I mean that your own POCO classes should not be reliant on the third party their POCO class properties, but your endpoints still should be able to (easily) get the data (values/properties) from the third party's POCO classes.</em></strong> </p>

<p>It is easy to write endpoints that get the fields and values of your own POCO classes and the third party their POCO classes by using a simple <code>.Include</code> and by making sure the referenced table / POCO class is in your own POCO class. This would however also mean that when the third party becomes another party, all the endpoints should be rewritten because the new third party have their own set of properties / POCO classes. Our front-end / application functionality will however more or less stay the same and the third party their values / properties are more or less the same (the naming / set up for certain tables or columns can be different though). </p>

<p><strong>Some background information</strong></p>

<p>I'll try to draw out the current situation as it is now, for this i'll be using our Commodity POCO class / table as an example. 
So our API solution, which is being called by a front-end application, has 2 projects, a DAL project which houses all the data / database logic <code>(Fluent API)</code> and the API project itself which houses the endpoints, viewmodels, user management logic etc. I simplified it as much as possible:</p>

<p><a href="https://i.sstatic.net/cJcDu.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/cJcDu.png" alt="enter image description here"></a></p>

<p>All the tables / POCO classes of our own database are present in the <code>OwnModels</code> folder while the models of the third party are created in the <code>TheirModels</code> folder. Their POCO classes are recreated with a specification document (swagger file) they have send us. In our database we have some tables that are self-made and another set of tables that act as a <code>reference table</code> between our database table and their table, <code>Commodity</code> is one of those. We have a process running which syncs the data of their database / tables to our own database (in the recreated tables).  </p>

<p>In this example they have a table called <code>TheirCommodity</code> with 3 fields <code>TheirCommodityID</code>, <code>Name</code> and <code>SortOrder</code>. Now we have created a Reference table (POCO class) with has the same name but without the prefix, so <code>Commodity</code>. This table has a column for it's own ID (<code>CommodityID</code>) and the reference ID of their table (TheirCommodityID), in <code>Fluent</code> this is set up as a one-to-one relation. 
Most of the endpoints of the reference tables are read-only (<code>GET</code> endpoint), simply because we are not allowed to modify/delete/insert data in their table's directly. </p>

<p>The above Commodity tables are now set up as follows:</p>

<p><strong>Their Commodity POCO class:</strong></p>

<pre><code>public class TheirCommodity
{
    public TheirCommodity()
    {   
    }

    public long TheirCommodityID { get; set; }

    public string Name { get; set; }

    public long? SortOrder { get; set; }

    [JsonIgnore]
    public virtual Commodity Commodity { get; set; }
}
</code></pre>

<p><strong>Our (reference) Commodity POCO class:</strong></p>

<pre><code>public class Commodity
{
    public Commodity()
    {
    }

    public long CommodityID { get; set; }

    public long TheirCommodityID { get; set; }

    public virtual TheirCommodity TheirCommodity { get; set; }
}
</code></pre>

<p><em>The [JsonIgnore] attribute is added because if not, it falls in a circular reference when retrieving data for our Commodity table (both POCO classes reference each otter for getting the one-to-one relationship done right in FLUENT).</em> </p>

<p>In the API I created a GET endpoint for this commodity as follows: </p>

<pre><code>[HttpGet]
public async Task&lt;IEnumerable&lt;Commodity&gt;&gt; GetCommodities()
{
    return await this.Context.Commodity
        .Include(i =&gt; i.TheirCommodity)
        .ToListAsync();
}
</code></pre>

<p><strong>The question</strong></p>

<p>The above all works fine but is an enormous hassle when to <strong>reuse</strong> this code for another company which has a different third party with their set of tables and properties. 
This set-up would mean we will have to rewrite all our endpoints and some more. 
So ideally, at least I think (but that’s also the question), you would want to get all the properties of their POCO class in our own POCO class so that we are not reliant (with the Include) on their POCO classes. But that would also mean you need some logic that when you get values from their tables/properties, you need to write a backing field or something that queries the third party's table.<br>
I can’t entirely wrap my head around how this should be accomplished. I know you can’t write a perfectly piece of code which is entirely reusable (also since we will always have the step of getting the third party tables in your own database for the syncing of data), but at least there should be something of not having to rewrite all our endpoints. 
My apologies for the big text wall but I couldn’t find a way to write it shorter. And also my apologies for incorrect usage of words (English is not my native language :) ) </p>

