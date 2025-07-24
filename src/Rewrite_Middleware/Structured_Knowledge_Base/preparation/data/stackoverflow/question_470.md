# Why does LINQ with LazyLoading randomly NOT load children?
[Link to question](https://stackoverflow.com/questions/27451367/why-does-linq-with-lazyloading-randomly-not-load-children)
**Creation Date:** 1418414986
**Score:** 0
**Tags:** c#, linq, linq-to-sql, entity-framework-4
## Question Body
<p>I am trying to load MyObject which has a series of MyObjectChild objects. LazyLoading is on by default for my context object, and I haven't disabled it. I have the following query in my code:</p>

<pre><code>    public MyObject GetMyObject(string objectNumber)
    {
        List&lt;MyObject&gt; query = (from obj in Context.MyObjects
                                where obj.ObjectNumber == objectNumber
                                orderby obj.LastUpdateDate descending
                                select obj).ToList();

        return query.FirstOrDefault();
    }
</code></pre>

<p>This returns the first item as an object. Yes, we want to disconnect the object returned from the database, so I expect this to return MyObject with all of the MyObjectChild objects attached. The awkward part is that the database has thouasands of <em>MyObjectChild</em>s, but once in a blue moon it decides NOT to load them.</p>

<p>Later in the code, I have:</p>

<pre><code>    MyObject myObject = GetMyObject("123456");

    foreach (MyObjectChild c in myObject.MyObjectChilds)
    {
        ... /* Do some stuff */
    }
</code></pre>

<p>Very randomly (one time in a hundred??) this foreach loop doesn't have any records to "foreach" over. Note that it doesn't throw an exception either!! It just bypasses this section of the code entirely as if the MyObjectChilds collection was empty.</p>

<p>1) <em>Can anyone explain why this happens?</em> 99% of the time, it works perfectly, but when it fails, it is very bad for us. I need to understand in what conditions this could fail so that I can code around it.</p>

<p>2) <em>What is the BEST way to prevent this situation/condition?</em> We do this kind of thing all over the place, and our database layout is HUGE, so I'd rather not turn lazy loading off and have to rewrite all of our underlying code to use thousands of .Include(...) statements all over the place. Is there a better/easier/faster solution that still guarantees that we get the information every time?</p>

<p><strong>UPDATE</strong></p>

<p>After doing much more digging, I've found two "semi-simple" solutions to this issue. One I knew about, but just overlooked: <code>ToList()</code>. Yes, I am doing a <code>ToList()</code> on the query, but I wasn't doing it on the <code>foreach</code>, thus it had a chance to no load the child objects.</p>

<pre><code>    foreach (MyObjectChild c in myObject.MyObjectChilds.ToList())
    {
</code></pre>

<p>Another solution that works <em>MUCH</em> like <code>.ToList()</code> is to force the loading of the child object before each use. This will be much more cumbersome for me to implement (based on my current code). However, (from what I can tell from other posts around SO) this is more likely to always have the result I'm looking for.</p>

<pre><code>    if (!obj.MyObjectChilds.IsLoaded)
    {
        obj.MyObjectChilds.Load();
    }
    foreach (MyObjectChild c in myObject.MyObjectChilds)
    {
        ...
</code></pre>

<p>For now, I'm going through my code to make sure that I've <code>ToList</code>-ed all of my foreach loops that loop over sub-database-objects. That seems to be the simplest fix, although I'm not sure it is the "most correct" fix.</p>

## Answers
### Answer ID: 27451851
<p>ToList() will execute query and create local copy of data which cannot load children. But to be 100% sure that children will be loaded use <a href="http://msdn.microsoft.com/en-us/library/bb738708(v=vs.110).aspx" rel="nofollow">Include</a> method. Also I recomend you to rewrite your query (use FirstOrDefault instead of ToList and copy your object manually (use Clone method)). To check if MyObjectChilds were loaded use IsLoaded and to manually load children use Load method.</p>

### Answer ID: 27451781
<p>So I have had this same issue before. The key though is detecting it as soon as you get your initial collection.</p>

<p>Once you have detected this then you need to reload the child collection.</p>

<p>Here is an extension method to help solve this problem. </p>

<pre><code>public static void RefreshChildCollections&lt;TEntity, TContext&gt;(this ICollection&lt;TEntity&gt; entityCollection, TContext content)
{
    ((IObjectContextAdapter)content).ObjectContext.Refresh(RefreshMode.StoreWins, entityCollection);
}
</code></pre>

<p>Usage</p>

<pre><code>collectionToReload.RefreshChildCollections(Context);
</code></pre>

