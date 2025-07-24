# Cache accessed values in JSP page
[Link to question](https://stackoverflow.com/questions/12447005/cache-accessed-values-in-jsp-page)
**Creation Date:** 1347799983
**Score:** 0
**Tags:** java, jsp, caching
## Question Body
<p>In my <strong>Java</strong> web application, I have my whole database structure covered by <strong>Model classes</strong>. It's really neat, because using those models I can very simply print anything from the database directly in the <strong>JSP page</strong>. See following example:</p>

<pre><code>&lt;c:if test="${fn:length(author.books) == 0}"&gt;The author has no books.&lt;/c:if&gt;

&lt;c:forEach items="${author.books}" var="book"&gt;
${book.name}
&lt;/c:forEach&gt;
</code></pre>

<p>Model <code>Author</code> has a method <code>getBooks()</code> which fetches related books from the database and returns a <strong>collection</strong> of models representing books. The problem is that in the example above the method is called actually twice which results in one redundant query.</p>

<p>I know that I can store the value using <code>&lt;c:set /&gt;</code> but firstly, I would have use that <em>a lot</em> (the example above is quite common in my app) and secondly, it doesn't always work. For example:</p>

<pre><code>&lt;c:forEach items="${books}" var="book"&gt;
${book.author.name}
&lt;/c:forEach&gt;
</code></pre>

<p>My database unfortunately <strong>doesn't support joins</strong> so that for each line I have to run a query to fetch the author from the database (it's actually pretty fast, because authors are stored in <code>memcache</code> by keys). And let's say I want to use this loop <strong>twice</strong> in one page (<em>big menu</em> and <em>small menu</em> or whatever...). So each author is fetched twice from database (or memcache) and that is really not desired.</p>

<p>How do I avoid that? Ideally, the JSP "renderer" should each acquired value store in a <strong>temporary cache</strong> (just for one request) and next time use this cached value instead of calling the method again. Another way would be to implement this cache directly in the model objects but I don't know how to do that efficiently without rewriting half of my code. Any ideas?</p>

## Answers
### Answer ID: 12574220
<p>The biggest problem was with the second described example - I wanted to avoid repetitive fetching of the same entities from the datastore (or memcache). Luckily, all entities are fetched in a completely separated layer. I updated this layer so that now every fetched entity is stored in a HashMap by its key. This HashMap is used as a simple cache - when one entity is demanded more than once, it is fetched only in the first case, after that cached value is used. This HashMap is cleared when the request is finished.</p>

<p>This is more likely a workaround than a real solution I am still interested in other ideas.</p>

### Answer ID: 12447040
<p>JSPs should not be doing any such thing.  They're for display only.</p>

<p>The usual idiom is called Model-2 MVC for the web: a servlet acts as a Front Controller and routes JSP requests to back end services.   It should marshal the values that the JSP needs to display.  It's the back end that executes all logic.  That includes where data comes from: caches, databases, or real time calculations.</p>

<p>Your model objects should not know or care whether or not they're cached.  (It's no less an Author or Book just because you've decided to cache or persist it.)  Keep the cache separate.  </p>

<p>Why are you thinking of writing such a thing when there are so many available to you?  Google for something like EhCache or Terracotta.</p>

