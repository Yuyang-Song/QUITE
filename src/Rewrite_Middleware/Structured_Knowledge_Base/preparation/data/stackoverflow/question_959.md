# How can I create a generic implementation that lists data from my database?
[Link to question](https://stackoverflow.com/questions/51947064/how-can-i-create-a-generic-implementation-that-lists-data-from-my-database)
**Creation Date:** 1534848715
**Score:** 0
**Tags:** c#, generics, abstract-class
## Question Body
<p>I've got a large number of tables in my database that are essentially supporting data. These tables list nationalities, genders, languages, etc. and are all based on the same data model:</p>

<pre><code>public class SupportDataModel
{
    public int Id { get; set; }
    public string Name { get; set; }
    public bool Deleted { get; set; }
}
public class Gender : SupportDataModel
{
}
</code></pre>

<p>This data is presented in DropDownList controls mostly so I need to query each table to get a list. Since I don't want to have to rewrite this query every time I need to access the data, I've written it as a helper class:</p>

<pre><code>public class GendersHelper : IAlternateHelper&lt;Gender&gt;
{
    public List&lt;Gender&gt; ListItems()
    {
        using (var db = new ApplicationDbContext())
        {
            return db.Genders.Where(x =&gt; !x.Deleted).ToList();
        }
    }
}
</code></pre>

<p>For each of these classes, this function is identical except in the table it queries. That's why I'd like to write a single class that uses the type that I pass in to it as the determining factor for which table I'm querying, but I don't know how to do this.</p>

<p>Here's what I've got so far...</p>

<pre><code>public abstract class SupportingDataHelper&lt;T&gt;
{
    public List&lt;T&gt; ListItems()
    {
        // Logic to determine which table gets queried,
        // as well as the query itself should go here.
    }
}
</code></pre>

<p>How do I get this method to determine from the type passed in which table to query and then return a list of those items?</p>

## Answers
### Answer ID: 51947145
<p>You can just use <a href="https://msdn.microsoft.com/en-us/library/gg696521(v=vs.113).aspx" rel="nofollow noreferrer"><code>DbContext.Set&lt;T&gt;</code></a> which returns a set for selected type:</p>

<pre><code>public class SupportDataRepository&lt;T&gt; where T : SupportDataModel
{
    public List&lt;T&gt; ListItems()
    {
        using (var db = new ApplicationDbContext())
        {
            return db.Set&lt;T&gt;().Where(x =&gt; !x.Deleted).ToList();
        }
    }
}
</code></pre>

<p>However, I wouldn't call this class <code>Helper</code>, because it looks more like a repository. </p>

<p>Another thing to consider is that you definitely don't want to create an empty class like:</p>

<pre><code>public class Gender : SupportDataModel
{
}
</code></pre>

<p>because it doesn't make much sense. Perhaps, you may want to use <code>enum</code> property to define a type of <code>SupportDataModel</code>. In this case, you will have only one table (with more rows though), one simple class with simple repository class and no inheritance or generics. </p>

