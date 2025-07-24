# Unexpected Linq Behavior - ToList()
[Link to question](https://stackoverflow.com/questions/14142328/unexpected-linq-behavior-tolist)
**Creation Date:** 1357228318
**Score:** 8
**Tags:** c#, .net, linq, linq-to-nhibernate
## Question Body
<p>I have two similar queries theoretically returning the same results:</p>

<pre><code>var requestNotWorking = SessionManagement.Db.Linq&lt;Item&gt;(false).Where(i =&gt; 
                        i.Group != null &amp;&amp; i.Group.Id == methodParameter)
                       .ToList();
</code></pre>

<p>This request returns 0 items, even though it is supposed to return one.
The following is a rewrite of the latter but with a call to the <code>ToList()</code> method. This request works and returns the item expected in the first query!</p>

<pre><code>var requestWorking = SessionManagement.Db.Linq&lt;Item&gt;(false).ToList().Where(i =&gt; 
                     i.Group != null &amp;&amp; i.Group.Id == methodParameter).ToList();
</code></pre>

<p>Note: <code>SessionManagement.Db.Linq&lt;Item&gt;(false)</code>is a generic Linq to Nhibernate method with the boolean attribute determining if the request must be executed in the cache (true) or the database (false). There is supposedly nothing wrong in this method as it works  normally in many other parts of the solution. The mapping of Item is nothing fancy: no bags and the following parameters:
<code>lazy="false" schema="dbo" mutable="false" polymorphism="explicit"</code></p>

<p>Why is this so?</p>

<p><strong>Edit</strong>:</p>

<p>The generated sql request of requestNoWorking ends with :</p>

<p><code>(Item.Group_ID is not null) and Item.Group_ID=@p0',N'@p0 int',@p0=11768</code> </p>

<p>The generated sql request of requestWorking is roughly a <code>select * from dbo.Items</code></p>

## Answers
### Answer ID: 14143704
<p>I was very interested by your theory on <code>c.Group.Id != null</code>, which I found logical even though it contradicted other pieces of code in my solution. However, removing it did not change anything. I found that removing <code>mutable="false"</code>property solved the problem. It seems a bit magical but it worked.</p>

<p>The requests I posted were in fact happening in methods checking the possibility of update/deletion. My conclusion is that somehow making Item immutable falted the results. But what I don't understand is why requestWorking worked then!</p>

### Answer ID: 14142478
<p>i'm assuming the nhibernate session thing you've got going on there returns a queryable.  if so, the evaluation of the first query is delayed until the <code>.ToList()</code> call, and the entire query is run on the server.  I would suggest that you run a trace on the sql server if possible, or perhaps download <a href="http://www.hibernatingrhinos.com/products/nhprof" rel="nofollow">NHProf</a> to see what the actual query being executed is.</p>

<p>the second query is evaluated as soon as you hit the first <code>.ToList()</code>, so you're pulling the whole table back from the db, and then filtering using .net.  i honestly can't tell you why they would be evaluating differently, but i assume there is something with the mapping/configuration that is causing the db query to be written slightly wrong.</p>

### Answer ID: 14142473
<p>All I can see is that in the 2nd version, your <code>Where</code> is executed by LINQ to Objects rather than LINQ to NHibernate. So the first version must do something that LINQ to NHibernate doesn't digest very well.</p>

<p>I'm <em>thinking</em> it's the <code>i.Group != null</code> that LINQ To NHibernate has a problem with, seeing that the use of <code>null</code> is CLR-specific. You may need to use another construct in LINQ to NHibernate to test for empty field values.</p>

