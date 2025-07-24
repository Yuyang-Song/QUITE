# Custom Comparer in LINQ query to sort strings/numerics
[Link to question](https://stackoverflow.com/questions/29733639/custom-comparer-in-linq-query-to-sort-strings-numerics)
**Creation Date:** 1429466224
**Score:** 1
**Tags:** c#, linq
## Question Body
<p>I've written a custom comparer that sorts strings and numeric. This all works fine.</p>

<p>However I'm rewriting my whole BLL to use LINQ where possible as I do like the syntax. Now i'm stumbling onto using my custom comparer. As LINQ syntax (query based) will not allow to use custom comparers Im now using method based LINQ.</p>

<p>But in order to make it to work, I need to do an intermediate ToList(), which again works fine, but looks somewhat weird to me?  </p>

<pre><code>        var areas = cc.Areas.Where(a =&gt; a.ProjectId == ProjectId).ToList()
                            .OrderBy(a =&gt; a.UnitNumber, new Common.Comparers.StringNumericComparer());
</code></pre>

<p>Now i'm unsure if this has to do with the SQL query to be executed first and then the results sorted in my C# code side, but this is beyond my knowledge.
Does ToList() force the first part of the linq query to be executed on the database?</p>

## Answers
### Answer ID: 29733665
<p>Yes your understanding is correct. Until the .ToList() it is an IQueryable. On ToList() a database query is fired and the results are fetched in memory and then a sort occurs on the List.</p>

<p>Your comparer cannot execute before this since it does not translate to an SQL query.</p>

### Answer ID: 29733663
<p>Yes, <code>.ToList()</code> forces your <code>Areas</code> to be loaded and the sorting occurs in memory.</p>

