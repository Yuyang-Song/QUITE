# ToListAsync() vs AsEnumerable() in terms of synchronicity
[Link to question](https://stackoverflow.com/questions/76649315/tolistasync-vs-asenumerable-in-terms-of-synchronicity)
**Creation Date:** 1688933333
**Score:** 4
**Tags:** c#, linq, asp.net-core, entity-framework-core
## Question Body
<p>Let's say I have the following method:</p>
<pre><code>var result = (await db.Students
                      .Where(s =&gt; s.Name == &quot;Foo&quot;)
                      .ToListAsync())
                      .Select(s =&gt; MySuperSmartMethod(s));
</code></pre>
<p><code>MySuperSmartMethod</code> here is a method that cannot be translated to SQL.</p>
<p>As I understood from this <a href="https://stackoverflow.com/a/17996264">answer</a>, calling the <code>ToList()</code> (and <code>ToListAsync()</code> as well) method to evaluate future methods on the client side has a problem: it immediately queries the database, iterates the result and puts it into memory.</p>
<p>So, it is better to call <code>AsEnumerable()</code> instead of <code>ToList()</code>, cause it does not create an unnecessary intermediate list. <code>AsEnumerable()</code> returns an <code>IEnumerable</code>, so when it comes to executing future methods, they will iterate over objects directly in the IEnumerable.</p>
<p>Therefore I conclude that I should rewrite the previous method to something something like this:</p>
<pre><code>var result = db.Students
               .Where(s =&gt; s.Name == &quot;Foo&quot;)
               .AsEnumerable()
               .Select(s =&gt; MySuperSmartMethod(s));
</code></pre>
<p>Ok, but now I have another problem: my method is not asynchronous anymore.</p>
<p>So, what should i do? Are there any other approaches? Does asynchronous querying database lead to any performance benefits in an ASP.NET Core application? Or should I rewrite my asynchronous MediatR queries and commands to synchronous replacing <code>ToListAsync()</code> with <code>AsEnumerable()</code> wherever it's possible?</p>

## Answers
### Answer ID: 76649806
<p>What you can do is keep it as a <code>IAsyncEnumerable</code>. This means that the query is not actually executed until you enumerate it using <code>ToListAsync</code></p>
<pre class="lang-cs prettyprint-override"><code>var result = db.Students
               .Where(s =&gt; s.Name == &quot;Foo&quot;)
               .AsAsyncEnumerable()
               .Select(s =&gt; MySuperSmartMethod(s));
// much later
var list = await result.ToListAsync(someCancellationToken);
</code></pre>
<p>For this to work, you need to install the <a href="https://www.nuget.org/packages/System.Linq.Async" rel="nofollow noreferrer"><code>System.Linq.Async</code> package</a>.</p>
<p>You can in theory roll your own <code>Select</code> extension, but be aware that simply doing <code>await (foreach</code> will begin the enumeration immediately.</p>

### Answer ID: 76649710
<p>Using an asynchronous method in EF is static &quot;hey, this might take a while, so if anyone else is waiting, you can go ahead&quot;. It does nothing (significant or positive) for execution time of the code that is in the queue awaiting it. So depending on whether this code can actually take a while or not it may be no issue at all to leave it synchronous. <code>async</code> isn't a silver bullet for performance, if anything it makes every query that slight bit <em>slower</em> than if they were left synchronous. It's great for stuff that might take a second or more to execute (typically I set a threshold of around 300-500ms) or are called by methods I expect to be executed very frequently.</p>
<p>The best solution IMHO is to avoid situations where you feel you need &quot;SuperSmartMethod&quot; in query expressions. Projection can help with this where &quot;SuperSmartMethod&quot; can be computational within the view model rather than the query, when &quot;SuperSmartMethod&quot; appears in a <code>Select</code>;</p>
<p>For instance if SuperSmartMethod requires values A, B, and C from one or more entities, load A, B, and C into your ViewModel and expose &quot;SuperSmart&quot; property or function in the ViewModel. The query remains pure, and <code>async</code> compatible.</p>
<p>Another solution if you need to keep &quot;SuperSmartMethod&quot; in the query expression is to wrap your querying method within a method using an <code>async IAsyncEnumerable</code> /w <code>yield</code>. <strong>Edit</strong> Removed this example until I can have a play with it. It doesn't look like that would work out of the box since it would expect something awaited inside the querying method...</p>

