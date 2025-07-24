# Problems with converting List to IQueryable in Linq
[Link to question](https://stackoverflow.com/questions/63248249/problems-with-converting-list-to-iqueryable-in-linq)
**Creation Date:** 1596548683
**Score:** -3
**Tags:** c#, linq, iqueryable
## Question Body
<p><strong>EDIT</strong></p>
<p>Actually this question should be more general: <strong>How to modify query to DB if Linq with <code>IQueryable</code> gives errors?</strong></p>
<p>The correct answer is as far as I understand — to get as much of the query done at the database level. Because in this particular case my complicate query just can not be transform from Linq to sql.</p>
<p>So I just wrote a raw sql query with <code>FromSqlRaw()</code> method and errors have gone. Moreover I wrote query in the way that does not take all entries (with filtering) as opposed to <code>ToList()</code> method, so I have less doubt about performance (though I did not measure it).</p>
<hr />
<p>Need some help with understanding how to use linq with converting <code>List</code> to <code>IQueryable</code>.</p>
<p>What I had:
A three tables in DB with IQueryable-based queries to one of them.</p>
<p>What I need:
To create a query that combine data from three tables by Linq and give me resulting specific column with data for every element of one of table with function of filtering by this column.</p>
<p>What I try:
Supplement IQueryable-based query. But I found problems with <code>List</code> to <code>IQueryable</code> converting. Method <code>AsQueryable()</code> gives errors.</p>
<p>What I achieve:
I rewrite queries with List-based logic in Linq and it gives me what I need. But I do not understand:</p>
<ul>
<li>Is this practice good?</li>
<li>Why should I often must make <code>ToList()</code> conversion for avoiding errors?</li>
<li>Is the speed of my solution worse than IQueryable-based approach?</li>
</ul>
<p>Here is fiddle with my exercises: <a href="https://dotnetfiddle.net/BAKi6r" rel="nofollow noreferrer">https://dotnetfiddle.net/BAKi6r</a></p>
<p>What I need I get in <code>listF</code> var.</p>
<p>I totally replace <code>CreateAsync</code> method in it with <code>Create</code> method for <code>List</code>. Is it good?
I also try to use hardcoded Lists with <code>CreateAsync</code> method /<code>items2moq</code>, <code>items3moq</code>/, but they with filtered List-based query give <code>The provider for the source IQueryable doesn't implement IAsyncQueryProvider</code> error. Also I got <code>Argument types do not match</code> error when I use <code>IQueryable</code> for <code>NamesIQ</code> instead of <code>List</code> for <code>NamesList</code>. What exactly the source of this errors?</p>

## Answers
### Answer ID: 63248537
<blockquote>
<p>Why should I often must make ToList() conversion for avoiding errors?</p>
</blockquote>
<p>I often think about Linq queries in three &quot;levels&quot;:</p>
<ol>
<li><p><code>IQueryable</code> - there are designed to translate a Linq query into an equivalent database (or whatever data source you're using) query. Many Linq and non-Linq operations just can't be translated into its SQL or other equivalent, so this layer would throw an error. Even operations that <em>seem</em> simple (like splitting a string) are difficult if not impossible to do in SQL</p>
</li>
<li><p><code>IEnumerable</code> - in this layer, Linq queries are done <em>in memory</em>, so there's much more flexibility to do custom operations. To get from the <code>IQueryable</code> layer to the <code>IEnumerable</code> layer, the <code>AsEnumerable()</code> call is the most straightforward. That separates the part of the query that gets raw data from the part that can create custom objects, do more complex filtering and aggregations, etc. Note that <code>IEnumerable</code> still uses &quot;deferred execution&quot;, meaning that at this stage, the query is <em>just a query</em> - the results don;t actually get computed until you <em>enumerate</em> it, either with a <code>foreach</code> loop or by advancing to the next layer:</p>
</li>
<li><p><code>List</code>/<code>Array</code>/etc. This is where queries are executed and turned into concrete collections. Some of the benefits of this layer are serializability (you can't &quot;serialize&quot; an enumerator) and  eager-loading (as opposed to deferred execution described above).</p>
</li>
</ol>
<p>So you're <em>probably</em> getting an error because you have some part of your query that can't be translated by the underlying <code>Queryable</code> provider, and using <code>ToList</code> is a convenient way to materialize the raw data into a list, which allows you to do more complex operations. Note that <code>AsEnumerable()</code> would do the same thing but would maintain deferred execution.</p>
<blockquote>
<p>Is this practice good?</p>
</blockquote>
<p>It can be, but you might easily be getting more data than you <em>need</em> by doing filtering at the list level rather than at the database level. My general practice is to get as much of the query done at the database level, and only moving to the enumerable/list level when there's no known way to translate the rest of the query to SQL.</p>
<blockquote>
<p>Is the speed of my solution worse than IQueryable-based approach?</p>
</blockquote>
<p>The only way to know is to try it both ways and measure the difference. But it's a pretty safe bet that if you get more raw data than you need and filter in memory that you'll have worse performance.</p>

