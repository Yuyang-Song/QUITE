# Batching stores transparently
[Link to question](https://stackoverflow.com/questions/64027819/batching-stores-transparently)
**Creation Date:** 1600863534
**Score:** 1
**Tags:** spring, spring-boot, spring-jdbc, jooq
## Question Body
<p>We are using the following frameworks and versions:</p>
<ul>
<li><code>jOOQ 3.11.1</code></li>
<li><code>Spring Boot 2.3.1.RELEASE</code></li>
<li><code>Spring 5.2.7.RELEASE</code></li>
</ul>
<p>I have an issue where some of our business logic is divided into logical units that look as follows:</p>
<ul>
<li>Request containing a user transaction is received</li>
<li>This request contains various information, such as the type of transaction, which products are part of this transaction, what kind of payments were done, etc.</li>
<li>These attributes are then stored individually in the database.</li>
</ul>
<p>In code, this looks approximately as follows:</p>
<pre class="lang-java prettyprint-override"><code>TransactionRecord transaction = transactionRepository.create();
transaction.create(creationCommand);`
</code></pre>
<p>In <code>Transaction#create</code> (which runs transactionally), something like the following occurs:</p>
<pre class="lang-java prettyprint-override"><code>storeTransaction();
storePayments();
storeProducts();
// ... other relevant information
</code></pre>
<p>A given transaction can have many different types of products and attributes, all of which are stored. Many of these attributes result in <code>UPDATE</code> statements, while some may result in <code>INSERT</code> statements - it is difficult to fully know in advance.</p>
<p>For example, the <code>storeProducts</code> method looks approximately as follows:</p>
<pre class="lang-java prettyprint-override"><code>products.forEach(product -&gt; {
    ProductRecord record = productRepository.findProductByX(...);
    if (record == null) {
        record = productRepository.create();
        record.setX(...);
        record.store();
    } else {
      // do something else
    }
});
</code></pre>
<p>If the products are new, they are <code>INSERT</code>ed. Otherwise, other calculations may take place. Depending on the size of the transaction, this single user transaction could obviously result in up to <code>O(n)</code> database calls/roundtrips, and even more depending on what other attributes are present. In transactions where a large number of attributes are present, this may result in upwards of hundreds of database calls for a single request (!). I would like to bring this down as close as possible to <code>O(1)</code> so as to have more predictable load on our database.</p>
<p>Naturally, batch and bulk inserts/updates come to mind here. What I would like to do is to batch all of these statements into a single batch using <code>jOOQ</code>, and execute after successful method invocation prior to commit. I have found several (<a href="https://stackoverflow.com/questions/45274242/jooq-batch-record-insert">SO Post</a>, <a href="https://www.jooq.org/javadoc/latest/org.jooq/org/jooq/DSLContext.html#batchStore%28java.util.Collection%29" rel="nofollow noreferrer">jOOQ API</a>, <a href="https://github.com/jOOQ/jOOQ/issues/3419" rel="nofollow noreferrer">jOOQ GitHub Feature Request</a>) posts where this topic is implicitly mentioned, and <a href="https://groups.google.com/forum/#!topic/jooq-user/RRAYf2OUO8U" rel="nofollow noreferrer">one user groups post</a> that seemed explicitly related to my issue.</p>
<p>Since I am using <code>Spring</code> together with <code>jOOQ</code>, I believe my ideal solution (preferably declarative) would look something like the following:</p>
<pre class="lang-java prettyprint-override"><code>@Batched(100) // batch size as parameter, potentially
@Transactional
public void createTransaction(CreationCommand creationCommand) {
    // all inserts/updates above are added to a batch and executed on successful invocation
}
</code></pre>
<p>For this to work, I imagine I'd need to manage a scoped (<code>ThreadLocal</code>/<code>Transactional</code>/<code>Session</code> scope) resource which can keep track of the current batch such that:</p>
<ol>
<li>Prior to entering the method, an empty batch is created if the method is <code>@Batched</code>,</li>
<li>A custom <code>DSLContext</code> (perhaps extending <code>DefaultDSLContext</code>) that is made available via DI has a <code>ThreadLocal</code> flag which keeps track of whether any current statements should be batched or not, and if so</li>
<li>Intercept the calls and add them to the current batch instead of executing them immediatelly.</li>
</ol>
<p>However, step 3 would necessitate having to rewrite a large portion of our code from the (IMO) relatively readable:</p>
<pre class="lang-java prettyprint-override"><code>records.forEach(record -&gt; {
    record.setX(...);
    // ...
    record.store();
}
</code></pre>
<p>to:</p>
<pre class="lang-java prettyprint-override"><code>userObjects.forEach(userObject -&gt; {
    dslContext.insertInto(...).values(userObject.getX(), ...).execute();
}
</code></pre>
<p>which would defeat the purpose of having this abstraction in the first place, since the second form can also be rewritten using <code>DSLContext#batchStore</code> or <code>DSLContext#batchInsert</code>. IMO however, batching and bulk insertion should not be up to the individual developer and should be able to be handled transparently at a higher level (e.g. by the framework).</p>
<p>I find the readability of the <code>jOOQ</code> API to be an amazing benefit of using it, however it seems that it does not lend itself (as far as I can tell) to interception/extension very well for cases such as these. Is it possible, with the <code>jOOQ 3.11.1</code> (or even current) API, to get behaviour similar to the former with transparent batch/bulk handling? What would this entail?</p>
<hr />
<p>EDIT:</p>
<p>One possible but extremely hacky solution that comes to mind for enabling transparent batching of stores would be something like the following:</p>
<ol>
<li>Create a <code>RecordListener</code> and add it as a default to the <code>Configuration</code> whenever batching is enabled.</li>
<li>In <code>RecordListener#storeStart</code>, add the query to the current Transaction's batch (e.g. in a <code>ThreadLocal&lt;List&gt;</code>)</li>
<li>The <code>AbstractRecord</code> has a <code>changed</code> flag which is checked (<code>org.jooq.impl.UpdatableRecordImpl#store0</code>, <code>org.jooq.impl.TableRecordImpl#addChangedValues</code>) prior to storing. Resetting this (and saving it for later use) makes the store operation a no-op.</li>
<li>Lastly, upon successful method invocation but prior to commit:</li>
</ol>
<ul>
<li>Reset the <code>changes</code> flags of the respective records to the correct values</li>
<li>Invoke <code>org.jooq.UpdatableRecord#store</code>, this time without the <code>RecordListener</code> or while skipping the <code>storeStart</code> method (perhaps using another <code>ThreadLocal</code> flag to check whether batching has already been performed).</li>
</ul>
<p>As far as I can tell, this approach <em>should</em> work, in theory. Obviously, it's extremely hacky and prone to breaking as the library internals may change at any time if the code depends on Reflection to work.</p>
<p>Does anyone know of a better way, using only the public <code>jOOQ</code> API?</p>

## Answers
### Answer ID: 64046687
<h3>jOOQ 3.14 solution</h3>
<p>You've already discovered the relevant <a href="https://github.com/jOOQ/jOOQ/issues/3419" rel="nofollow noreferrer">feature request #3419</a>, which will solve this on the JDBC level starting from jOOQ 3.14. You can either use the <code>BatchedConnection</code> directly, wrapping your own connection to implement the below, or use this API:</p>
<pre class="lang-java prettyprint-override"><code>ctx.batched(c -&gt; {

    // Make sure all records are attached to c, not ctx, e.g. by fetching from c.dsl()
    records.forEach(record -&gt; {
        record.setX(...);
        // ...
        record.store();
    }
});
</code></pre>
<h3>jOOQ 3.13 and before solution</h3>
<p>For the time being, until #3419 is implemented (it will be, in jOOQ 3.14), you can implement this yourself as a workaround. You'd have to proxy a JDBC <code>Connection</code> and <code>PreparedStatement</code> and ...</p>
<p><strong>... intercept all:</strong></p>
<ul>
<li>Calls to <code>Connection.prepareStatement(String)</code>, returning a cached proxy statement if the SQL string is the same as for the last prepared statement, or batch execute the last prepared statement and create a new one.</li>
<li>Calls to <code>PreparedStatement.executeUpdate()</code> and <code>execute()</code>, and replace those by calls to <code>PreparedStatement.addBatch()</code></li>
</ul>
<p><strong>... delegate all:</strong></p>
<ul>
<li>Calls to other API, such as e.g. <code>Connection.createStatement()</code>, which should flush the above buffered batches, and then call the delegate API instead.</li>
</ul>
<p>I wouldn't recommend hacking your way around jOOQ's <code>RecordListener</code> and other SPIs, I think that's the wrong abstraction level to buffer database interactions. Also, you will want to batch other statement types as well.</p>
<p>Do note that by default, jOOQ's <code>UpdatableRecord</code> tries to fetch generated identity values (see <code>Settings.returnIdentityOnUpdatableRecord</code>), which is something that prevents batching. Such <code>store()</code> calls must be executed immediately, because you might expect the identity value to be available.</p>

