# Insert multiple entries to SQL Server with Node.js
[Link to question](https://stackoverflow.com/questions/53714522/insert-multiple-entries-to-sql-server-with-node-js)
**Creation Date:** 1544480263
**Score:** 2
**Tags:** javascript, node.js, sql-server-2008, node-modules, node-mssql
## Question Body
<p>I am rewriting an old API for which I am trying to insert multiple values at once into a MSSQL-Server (2008) database using the node module <a href="https://www.npmjs.com/package/mssql" rel="nofollow noreferrer">mssql</a>. Now, I am capable of doing this <em>somehow</em>, but I want to this following <strong>best practices</strong>. I've done my research and tried a lot of things to accomplish my target. However, I was not able to find a single solution which works just right.</p>

<h1>Before</h1>

<p>You may wonder:</p>

<blockquote>
  <p>Well, you are <em>rewriting</em> this API, so there must be a way this has been done before and that was working?</p>
</blockquote>

<p>Sure, you're right, it was working before, but... not in a way I'd feel comfortable with using in the rewrite. Let me show you how it was done before (little bit of abstraction added of course):</p>

<pre><code>const request = new sql.Request(connection);
let query = "INSERT INTO tbl (col1, col2, col3, col4) VALUES ";
for (/*basic for loop w/ counter variable i*/) {
    query += "(1, @col2" + [i] + ", @col3" + [i] + ", (SELECT x FROM y WHERE z = @someParam" + [i] + "))";
    // a check whether to add a comma or not
    request.input("col2" + [i], sql.Int(), values[i]);
    // ...
}
request.query(query, function(err, recordset) {
    // ...
}
</code></pre>

<p>While this is working, again, I don't quite think this could be called anything like <strong>'best practice'</strong>. Also this shows the biggest problem: a subselect is used to insert a value.</p>

<h1>What I tried so far</h1>

<h2>The easy way</h2>

<p>At first I tried the probably easiest thing:</p>

<pre><code>// simplified
const sQuery = "INSERT INTO tbl (col1, col2, col3, col4) VALUES (1, @col2, @col3, (SELECT x FROM y WHERE z = @col4));";
oPool.request().then(oRequest =&gt; {
    return oRequest
        .input("col2", sql.Int(), aValues.map(oValue =&gt; oValue.col2))
        .input("col3", sql.Int(), aValues.map(oValue =&gt; oValue.col3))
        .input("col4", sql.Int(), aValues.map(oValue =&gt; oValue.col4))
        .query(sQuery);
});
</code></pre>

<p>I'd say, this was a pretty good guess and actually working relative fine.
Except for the part, that ignores every item after the first one... which makes this pretty useless. So, I tried...</p>

<h2>Request.multiple = true</h2>

<p>...and I thought, it would do the job. But - surprise - it doesn't, still only the first item is inserted.</p>

<h2>Using '?' for parameters</h2>

<p>At this point I really started the search for a solution, as the second one was only a quick search in the modules documentation.
I stumbled upon <a href="https://stackoverflow.com/a/50840662/6013079">this answer</a> and tried it immediately.
Didn't take long for my terminal to spit out a</p>

<blockquote>
  <p>RequestError: Incorrect syntax near '?'.</p>
</blockquote>

<p>So much for that.</p>

<h2>Bulk inserting</h2>

<p>Some further research led to <a href="https://stackoverflow.com/questions/43663017/bulk-inserting-with-node-mssql-package">bulk inserting</a>.
Pretty interesting, cool feature and excellent updating of the question with the solution by the OP!
I had some struggle getting started here, but eventually it looked really good: Multiple records were inserted and the values seemed okay.</p>

<p>Until I added the subquery. Using it as value for a column declared didn't cause any error, however when checking the values of the table, it simply displayed a <pre>0</pre> as value for this column. Not a big surprise at all, but everybody can dream, right?</p>

<h2>The lazy way</h2>

<p>I don't really know what to think about this:</p>

<pre><code>// simplified
Promise.all(aValues.map(oValue =&gt; {
    return oPool.request().then(oRequest =&gt; 
        oRequest
            .input("col2", sql.Int, oValue.col2)
            .input("col3", sql.Int, oValue.col3)
            .input("col4", sql.Int, oValue.col4)
            .query(sQuery);
    });
});
</code></pre>

<p>It does the job, but if any of the request fails for whichever reason, the other, non-failing inserts, will still be executed, even though this should <strong>not</strong> be possible.</p>

<h2>Lazy + Transaction</h2>

<p>As continuing even if some fail was the major problem with the last method, I tried building a transaction around it. All querys are successful? Good, commit. Any query has an errpr? Well, just rollback than. So I build a transaction, moved my Promise.all construct into it and tried again.
Aaand the next error pops up in my terminal:</p>

<pre><code>TransactionError: Can't acquire connection for the request. There is another request in progress.
</code></pre>

<p>If you came this far, I don't need to tell you what the problem is.</p>

<h1>Summary</h1>

<p>What I didn't try yet (and I don't think I will try this) is using the transaction way and calling the statements sequentially. I do not believe that this is be the way to go.</p>

<p>And I also don't think the lazy way is the one that should be used, as it uses single requests for every record to insert, when this could somehow be done using only one request. It's just that this <em>somehow</em> is, I don't know, not in my head right now. So please, if you have anything that could help me, tell me.</p>

<p>Also, if you see anything else that's wrong with my code, feel free to point it out. I am not considering myself as a beginner, but I also don't think that learning will ever end. :)</p>

## Answers
### Answer ID: 71039315
<p>The way I solved this was using PQueue library with concurrency 1. Its slow due to concurrency of one but it works with thousands of queries:</p>
<pre class="lang-js prettyprint-override"><code>    const transaction = sql.transaction();
    const request = transaction.request();
    const queue = new PQueue({ concurrency: 1 });

    // being transaction
    await transaction.begin();

    for (const query of queries) {
      queue.add(async () =&gt; {
        try {
          await request.query(query);
        } catch (err) {
          // stop pending transactions
          await queue.clear();
          await queue.onIdle();
          // rollback transaction
          await transaction.rollback();
          // throw error
          throw err;
        }
      });
    }
    // await queue
    await queue.onIdle();
    // comit transaction
    await transaction.commit();
</code></pre>

