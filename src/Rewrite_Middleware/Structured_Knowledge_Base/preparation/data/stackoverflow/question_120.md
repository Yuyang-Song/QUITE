# Entity framework. Counting database hits
[Link to question](https://stackoverflow.com/questions/13676398/entity-framework-counting-database-hits)
**Creation Date:** 1354501942
**Score:** 4
**Tags:** c#, entity-framework
## Question Body
<p>When working with NHibernate I was able to count, in a test, how many times I hit the database which was great (guards from unintentional mistakes when rewriting queries).</p>

<p>Is it possible count/detect when a query is executed when using the Enitity Framerwork?</p>

<p>An example test would look like this:</p>

<pre><code>int currentSqlCounter = EntityFrameWork.QueryCount();
MyMethodBeingTested();
Assert.AreEqual( 2, EntityFrameWork.QueryCount() - currentSqlCounter);
</code></pre>

## Answers
### Answer ID: 13680004
<p>Support for logging in EntityFramework is quite weak and I don't know of any in-the-box solution for this. </p>

<p>I used the Tracing capabilities of the  EFProviderWrappers  <a href="http://code.msdn.microsoft.com/EFProviderWrappers" rel="nofollow">http://code.msdn.microsoft.com/EFProviderWrappers</a> to do something similar in a previous project.</p>

