# Possible linq bug/issue
[Link to question](https://stackoverflow.com/questions/5069154/possible-linq-bug-issue)
**Creation Date:** 1298309212
**Score:** 2
**Tags:** asp.net, linq, linq-to-sql
## Question Body
<p>I was having an issue with a LINQ query today and after some debugging I was able to resolve the issue but it seems like a bug to me in the way LINQ works. Here is what I had:</p>

<pre><code>var myitem = context
.items
.OrderByDescending(x =&gt; x.DateEdited)
.FirstOrDefault(x =&gt; x.fkId == myFkId &amp;&amp; x.DateEdited &lt; someDate);
</code></pre>

<p>In my database I have a table with some records and I want to retrieve the most recent record that is older than "someDate" and who has a particular foreign key in a column. The above query did not work however. It was returning the oldest record with the matching foreign key. I ended up having to rewrite my query like this to get it to work:</p>

<pre><code>var myitem = context
.items
.Where(x =&gt; x.fkId == myFkId &amp;&amp; x.DateEdited &lt; someDate)
.OrderByDescending(x =&gt; x.DateEdited)
.FirstOrDefault();
</code></pre>

<p>In my debugging I found out that the "x.DateEdited &lt; someDate" was re-ordering the IEnumerable so I ended up having to put my OrderByDescending clause after the date check.</p>

<p>Has anybody else run into this issue? Is it a bug or expected functionality?</p>

## Answers
### Answer ID: 5069303
<p>Even though <code>.OrderByDescending()</code> returns an <code>IOrderedEnumerable</code>, the <code>.FirstOrDefault()</code> is a shortcut to .<code>Where()</code> which only returns an <code>IEnumerable</code> which does not guarantee order.</p>

<p>Basically, adding a filter does not guarantee the order of the data.  If you look at the generated SQL from the first, you will get a nested subresult from the orderby that is then filtered again.</p>

### Answer ID: 5069215
<p>Generally, if an operation does not explicitly define the output order, you can't depend on the result being in any particular order until you specify/apply it yourself.</p>

<p>Unless you know that ordering an intermediate result will yield performance improvements in the next step of an algorithm, there's no reason to so. Just apply the ordering as a final processing step. </p>

