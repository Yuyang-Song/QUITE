# Unable to perform basic JOIN using LINQ Query syntax
[Link to question](https://stackoverflow.com/questions/74209574/unable-to-perform-basic-join-using-linq-query-syntax)
**Creation Date:** 1666794904
**Score:** 0
**Tags:** c#, entity-framework, linq, entity-framework-core, linq-to-entities
## Question Body
<p>I want to join another table using the query syntax. I am getting the following error:</p>
<blockquote>
<p>The LINQ expression 'DbSet()
.GroupJoin(
inner: DbSet(),
outerKeySelector: a =&gt; (int?)a.ID,
innerKeySelector: b =&gt; b.aID,
resultSelector: (a, b) =&gt; new {
// my properties here
})' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.</p>
</blockquote>
<p>My code looks along the lines of:</p>
<pre><code>var q =
    from a in As
    join b in Bs on a.ID equals b.aID into bs
    select new
    {
        // my properties here
    };
</code></pre>
<p>I want to join the Bs and access <code>bs</code> to perform <code>Count()</code> on it in my list of properpties.</p>
<p>EDIT: Here is an example using LINQPad 7 (default database).
<a href="https://i.sstatic.net/wrQjZ.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/wrQjZ.png" alt="enter image description here" /></a></p>

## Answers
### Answer ID: 74210740
<p>Do not use <code>GroupJoin</code> (<code>join</code> which ends with <code>into</code>) with EF Core, except situation when you need LEFT JOIN. It's translation is strictly limited.</p>
<pre class="lang-cs prettyprint-override"><code>var q =
    from a in As
    select new
    {
        ...
        TotalBCount = Bs.Count(b =&gt; b.aID == a.ID)
    };
</code></pre>

