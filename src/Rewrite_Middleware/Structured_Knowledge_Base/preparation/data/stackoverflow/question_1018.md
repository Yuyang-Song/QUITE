# What is the behaviour when returning a query result through a function and then continuing to query on that result?
[Link to question](https://stackoverflow.com/questions/5498257/what-is-the-behaviour-when-returning-a-query-result-through-a-function-and-then)
**Creation Date:** 1301566560
**Score:** 0
**Tags:** linq, asp.net-mvc-3, entity-framework-4
## Question Body
<p>I am using ASP.NET MVC 3 with Entity Framework 4 using POCOs and want to query a set and select some properties to put into my viewModel. I will sketch a simplified version of my situation:</p>

<h2>Situation:</h2>

<p>I have an entity <code>BananaTree</code> containing a collection of <code>Banana</code></p>

<pre><code>public class Banana
{
    public int Id { get; set; }
    public int Size { get; set; }
    public TimeSpan Age { get; set }
    public string Description { get; set; }
}

public class BananaTree
{
    public int Id { get; set; }
    public ICollection&lt;Banana&gt; Bananas { get; set; }
}
</code></pre>

<p>I also have a view model <code>BananaListItemViewModel</code> used in the view showing a list of bananas for a certain banana tree. This view is managed by the <code>BananaTreeController</code></p>

<pre><code>public class BananaListItemViewModel
{
    public int Id { get; set; }
    public TimeSpan Age { get; set }
}
</code></pre>

<p>I have a Details action on the controller like so:</p>

<pre><code>public ActionResult Details(int bananaTreeId)
{
    var viewModel = from bananaTree in bananaTreeRepository.BananaTrees
                    where bananaTree.Id == bananaTreeId
                    from banana in bananaTree.Bananas
                    select new BananaListItemViewModel
                    {
                        Id = banana.Id,
                        Age = banana.Age
                    };

    return View(viewModel);
}
</code></pre>

<h2>What I want to change</h2>

<p>This works fine and now I only select the items from the database that I need for my view model. However, I want to take out some more logic from my controller and am trying to do this as much as possible. </p>

<p>I would like to have a function in my repository like so:</p>

<pre><code>IQueryable&lt;Banana&gt; GetBananas(int bananaTreeId)
{
    return (from bananaTree in BananaTrees
            where bananaTree.Id == bananaTreeId
            select bananaTree.Bananas).Single().AsQueryable();
}
</code></pre>

<p>and use it like so:</p>

<pre><code>public ActionResult Details(int bananaTreeId)
{
    var viewModel = from banana in bananaTreeRepository.GetBananas(bananaTreeId)
                    select new BananaListItemViewModel
                    {
                        Id = banana.Id,
                        Age = banana.Age
                    };

    return View(viewModel);
}
</code></pre>

<h2>Question</h2>

<p>My question is, in this case, will the two queries be combined and go to the database in one go like in my first example or will this first get all the bananas from the tree completely out of the database and perform the second query on that list? I would prefer the first case. If not, could I rewrite the <code>GetBananas</code> query to get that behaviour (for example like the query below)?</p>

<pre><code>IQueryable&lt;Banana&gt; GetBananas(int bananaTreeId)
{
    return from bananaTree in BananaTrees
           where bananaTree.Id == bananaTreeId
           from banana in bananaTree.Bananas
           select banana;
}
</code></pre>

<p>Thanks very much in advance.</p>

## Answers
### Answer ID: 5498387
<p>In your specific case, it will be only one query, if the call to <code>Single()</code> doesn't lead to the query to be executed. Unfortunately, I couldn't find any info on whether it does or does not. The call to <code>AsQueryable</code> does <strong>not</strong> trigger the execution as long, as the <code>Bananas</code> property really is an <code>IQueryable</code>.<br>
According to <a href="http://msdn.microsoft.com/en-us/library/bb156472.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/bb156472.aspx</a>, the call to <code>Single</code> doesn't execute your query.<br>
<strong>Conclusion:</strong><br>
You code should result in only one query.</p>

<p>In general:<br>
You can pass an <code>IQueryable</code> from one method to another without it being implicitly executed.<br>
The following code will result in only <strong>one</strong> SQL statement executed at the end, when the call to <code>ToList</code> happens:</p>

<pre><code>IQueryable&lt;Banana&gt; GetBananasByWeight(int weight)
{
    return from banana in Bananas where banana.Weight = weight;
}

IQueryable&lt;Banana&gt; FilterByQuality(IQueryable&lt;Banana&gt; bananaQuery, int quality)
{
    return bananaQuery.Where(b =&gt; b.Quality == quality);
}

public List&lt;Banana&gt; GetBananas(int weight, int quality)
{
    var query = GetBananasByWeight(weight);
    var filteredBananas = FilterByQuality(query, quality);
    return filteredBananas.ToList();
}
</code></pre>

