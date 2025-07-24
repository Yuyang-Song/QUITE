# Linq query throws NullReferenceException when pulling data from SQLite, why?
[Link to question](https://stackoverflow.com/questions/44099730/linq-query-throws-nullreferenceexception-when-pulling-data-from-sqlite-why)
**Creation Date:** 1495387359
**Score:** 1
**Tags:** c#, asp.net, linq, linq-to-sql
## Question Body
<p>I'm trying to pull data from SQLite database with following query:</p>

<pre><code>DateTime Dzien = new DateTime(ticks ?? 0);
    var assinged = Data.Tasks.ToList();
    var assign =  assinged.Where(t =&gt; t.AssignedId ==
                              Data.AssignedTasks.FirstOrDefault(d =&gt; d.Date.Date == Dzien.Date).Id).ToList();
</code></pre>

<p>But it throws an exception:</p>

<p>NullReferenceException: Object reference not set to an instance of an object.
PiCoreSQLite.Controllers.HomeController+&lt;>c__DisplayClass3_0.b__0(Tasks t) in HomeController.cs, line 37</p>

<p>Data object is a databese contex and Tasks is a DbSet containing Tasks objects.</p>

<p>I tried removing ToList() but then query doesn't return anything. However it does work and returns data when using similiar query in asp.net .cshtml view:</p>

<pre><code> @{
    var zrobione =
        from completed in Model.Item1.Where(t =&gt; t.AssignedId == 
        Model.Item3.FirstOrDefault(d =&gt; d.Date.Date == DateTime.Today).Id)
        group completed by completed.Categories;
}
</code></pre>

<p>I tried rewriting query in fluent syntax and it still throws an exception.</p>

<p>My question is: Why is exception thrown and how to fix it?</p>

## Answers
### Answer ID: 44099875
<blockquote>
  <p>Why this exception is thrown?</p>
</blockquote>

<p>The problem is caused by the following statement:</p>

<pre><code>Data.AssignedTasks.FirstOrDefault(d =&gt; d.Date.Date == Dzien.Date)
</code></pre>

<p>The <code>FirstOrDefault</code> method returns the first item in the sequence you apply this method that fulfills the predicate you pass in this method in this case, the predicate is the following:</p>

<pre><code>d =&gt; d.Date.Date == Dzien.Date
</code></pre>

<p>In case of <strong>not found</strong> any such an item a <code>null</code> is returned (more generally is returned the default value of the type of the object you are looking for. So if you were looking for an <code>int</code> the default value would be the 0. In case of <em>reference type</em> the default value is <code>null</code>). </p>

<p>That being said is pretty evident that a <code>null</code> is returned and then you try to access the <code>Id</code> property of a null reference...Hence you get this error message.</p>

<blockquote>
  <p>How can we handle this?</p>
</blockquote>

<p>One approach it could be the following:</p>

<pre><code>var assign =  assinged.Where(t =&gt; t.AssignedId ==
                                (Data.AssignedTasks
                                     .FirstOrDefault(d =&gt; d.Date.Date == Dzien.Date)?.Id ?? -1))
                      .ToList();
</code></pre>

<p>In the above code <em>I have made the assumption</em> that <code>AssignedId</code> takes only positive or zero values. You could handle this appropriately, if that is not the case.</p>

<blockquote>
  <p>How the above works?</p>
</blockquote>

<p>As we have already mentioned <code>FirstOrDefault</code> would return a reference to the first found object that fulfills the predicate you pass or <code>null</code>. So in order we be safe we use the null conditional operator, <code>?.</code>. If you get any reference other than null you can read safely the <code>Id</code>, otherwise it is meaningless to do so and the result is <code>null</code>. Then you apply the null coalescing operator <code>??</code>. This operator returns the left hand value when it is different from null otherwise it returns the right hand value.</p>

### Answer ID: 44099868
<p>First of all, you need to determine what exactly throws an exception. Divide your code into small simple steps and debug it. What fails will tell you how to handle it appropriately.</p>

<p>Also, it is worth noting that the first sample of your code is not a LINQ to SQL at all, while the second sample is. This is the difference and one of the reasons why they work differently. BTW, it should be expected.</p>

<p>Most probably <code>Data.AssignedTasks.FirstOrDefault(d =&gt; d.Date.Date == Dzien.Date)</code> returns null and then pulling <code>Id</code> out of it throws an exception. In the second sample this whole expression is translated to SQL query which is why it works just fine.</p>

