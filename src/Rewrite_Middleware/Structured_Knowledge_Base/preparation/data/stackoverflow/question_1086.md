# How to use my own methods or write a DbFunction for EF Core querying (EF Core 3.0)
[Link to question](https://stackoverflow.com/questions/58428949/how-to-use-my-own-methods-or-write-a-dbfunction-for-ef-core-querying-ef-core-3)
**Creation Date:** 1571303476
**Score:** 1
**Tags:** c#, entity-framework, linq, entity-framework-core
## Question Body
<p>I previously had the following set up:</p>

<pre><code>public static bool BlogIsLive(BlogPost b)
{
    return b.Status == (int)ItemStatus.Active &amp;&amp; b.PublishDate &lt; DateTime.Now ;
}

/// Database query

var blogs = (from b in db.BlogPost 
             where BlogIsLive(b) // &lt;--- super useful, used in multiple places
             select b
             ).ToList()
</code></pre>

<p>But after updating to EF Core 3.0, it throws the following error</p>

<pre><code>/// The LINQ expression ... could not be translated. Either rewrite the query in a form 
/// that can be translated, or switch to client evaluation explicitly by inserting a 
/// call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync().
</code></pre>

<p>I understand this is part of the breaking changes in EF Core 3.0</p>

<p>Now I have to write the query manually in all the places where <code>BlogsIsLive()</code> was before.</p>

<pre><code>var blogs = from b in db.BlogPost 
            where b.Status == (int)ItemStatus.Active  //&lt;--- Annoying repetition of code
            &amp;&amp; b.PublishDate &lt; DateTime.Now           //&lt;---
            select b
</code></pre>

<p>This is highly  annoying. Is there no way I can write a method that slots into there? </p>

<p>I know EF has DbFunctions which, for example, can ease the process of comparing <code>Date</code> values, so I see no reason why it would not be possible to write something of my own that does similar involving <code>Int</code>, <code>string</code> or <code>bool</code>. </p>

<p>Something like: </p>

<pre><code>public static DbFunction BlogIsLive(BlogPost b)
{
    //Example
    return DbFunction(b.Status == (int)ItemStatus.Active &amp;&amp; b.PublishDate &lt; DateTime.Now);
}

/// Database query

var blogs = (from b in db.BlogPost 
             where MyDbFunctions.BlogIsLive(b)
             select b
             ).ToList();
</code></pre>

<p>I've tried a few variations on the above, but no luck.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 58429355
<p>The original code has a serious bug that would throw in any non-Core version of EF too - it's a local function, it can't be translated to SQL. <code>Where</code> accepts <em>expressions</em> as arguments, not functions. You don't need that function anyway. </p>

<p>LINQ works with IQueryable and expressions. Each operator takes one IQueryable and returns another. That's how <code>Where</code> and <code>Select</code> work already. This means you can create your own function that adds the <code>Where</code> condition you want :</p>

<pre><code>public static IQueryable&lt;BlogPost&gt; WhereActive(this IQueryable&lt;BlogPost&gt; query)
{
    return query.Where(b=&gt;b.Status == (int)ItemStatus.Active &amp;&amp; b.PublishDate &lt; DateTime.Now);
}
</code></pre>

<p>And use it with any <code>IQueryable&lt;BlogPost&gt;</code>, eg :</p>

<pre><code>var finalQuery = query.WhereActive();
var posts=finalQuery.ToList();
</code></pre>

<p>Another, more cumbersome option is to construct the <code>Expression&lt;Func&lt;&gt;&gt;</code> call in code, and pass that to <code>Where</code> - essentially creating the WHERE condition dynamically. In this case it's not needed though.</p>

<p>EF Core 1.0 added a very unfortunate feature (more like a <code>what-were-they-thinking!</code> kind of feature), client-side evaluation. If something can't be translated, just load everything in memory and try to filter stuff without the benefit of indexing, execution plans, matching algorithms, RAM and CPUs found in a database server.</p>

<p>This may not be noticed if only 100 rows are loaded by only 1 client at a time, it's a perf-killer for any application with even small amounts of data and concurrent users.</p>

<p>In a web application, this translates to more servers to handle the same traffic.</p>

<p>That's why client-side evaluation was <em>removed</em> when EF 1.0 was introduced back in 2008.</p>

### Answer ID: 58429198
<p>Instead of using <code>db.BlogPost</code> as the base of the query, you can use a DbSet that already has that filter on it.</p>

<pre><code>DbSet&lt;BlogPost&gt; _allBlogs {get;set;}

IQueryable&lt;BlogPost&gt; ActiveBlogs { get =&gt; _allBlogs.Where(b=&gt; b.Status == (int)ItemStatus.Active); }

var blogs = from b in db.ActiveBlogs
        select b
</code></pre>

