# SQLite - multiple calls in same transaction
[Link to question](https://stackoverflow.com/questions/69531523/sqlite-multiple-calls-in-same-transaction)
**Creation Date:** 1633980471
**Score:** 3
**Tags:** typescript, sqlite, capacitor
## Question Body
<p>Thanks for looking -
I'm writing a front end SPA in Typescript. I'm using capacitorJS for cross platform compatibility, and I'm using the @capacitor-community/sqlite plugin.
I'm new to SQLite, but not to databases in general.</p>
<p>This may be complicated by using a specific API over SQLite.<br />
The API is here: <a href="https://github.com/capacitor-community/sqlite#supported-methods" rel="nofollow noreferrer">https://github.com/capacitor-community/sqlite#supported-methods</a></p>
<p>Regardless, the API is not matching my expectations.</p>
<p>I want a pattern of being able to start a transaction, make multiple calls, and finally commit the transaction (or roll back in an error handler). It would be great if I can make calls to read within the same txn, or at least be able to read <em>outside</em> the txn while the write txn is open.</p>
<p>It looks like this (capacitor-community/sqlite) wrapper is adding a transaction around each call I make, by default, unless I override with a bool parameter. If I override, I'm responsible to include the transaction code in the sql statement block.</p>
<p>My first, naive approach was to issue a statement that would start a transaction, it would then make additional api calls that are supposed to be part of the txn, and finally run a sql statement that would <code>commit</code> the txn.<br />
e.g.</p>
<pre class="lang-js prettyprint-override"><code>async Transaction(actions: () =&gt; Promise&lt;void&gt;): Promise&lt;void&gt; {
    await SqliteService.Instance.db.execute('BEGIN TRANSACTION;', 
    try {
      await actions();
      await SqliteService.Instance.db.execute('COMMIT TRANSACTION;', false); //useTransaction = false
    } catch (e) {
      await SqliteService.Instance.db.execute('ROLLBACK TRANSACTION;', false); //useTransaction = false
      throw e;
    }

</code></pre>
<p>This didn't work at all. It appears state like that isn't kept between calls. I think some things (like having an open cursor) would cause the session to remain open, but normally the session would just open and shut with each call I make to the API.<br />
<em>I have not tried doing tricks with e.g. cursors to keep the transaction open, this seemed like an anti pattern</em></p>
<p>As I mulled it over, it seems I may have to send one big block of SQL within a transaction to get SQLite to do what I want.</p>
<p>So I'm considering rewriting my documentStore api to, instead of directly calling SQLite to run statements, instead when I want to do multiple things in a single transaction, to provide a sqlBuilder type class. Then I could glue multiple statements together.</p>
<p>...</p>
<p>But I like with the current interface, and rewriting the 'write' methods on my documentStore to have something of a sqlBuilder seems like a big step in a different direction.
e.g.</p>
<pre class="lang-js prettyprint-override"><code>async Transaction(sqlBuilder: (builder: WriteSqlBuilder&lt;T&gt;) =&gt; {statement: string, values: unknown[]} []) {
...
</code></pre>
<p>I'd like to know - how do people usually approach performing multiple actions (queries, writes) in SQLite within a single transaction?</p>
<p>Thanks!</p>

## Answers
### Answer ID: 69562943
<p>So, this ended up being some peculiar behavior in the wrapper I was using <code>capacitor-community/sqlite</code>.</p>
<p>When making calls to e.g. <code>executeSet({sql, params}[], transaction)</code> you can pass a boolean to use a transaction or not. This is a helper.
This <code>transaction</code> value defaults to true.  When it's set true, the wrapping library automatically adds <code>BEGIN TRANSACTION</code> and <code>COMMIT TRANSACTION</code> (and <code>ROLLBACK TRANSACTION</code> in case of error) around your sql items for you, all in the single call.</p>
<p>If you explicitly set <code>transaction</code> to false, it'll behave as vanilla SQLite would, starting an implicit transaction for the call, and when the call is finished, that's the last SQL statement, the implicit transaction is implicitly committed.</p>
<p>What tripped me up is I'm doing my dev work in a web browser (for this cross platform application), so I'm using <code>jeep-sqlite</code>. <code>jeep-sqlite</code> uses an in-memory sqlite db, and has a <code>saveToStore(dbName)</code> method to flush the SQLite bytes into an IndexedDb entry.</p>
<p>I think what was happening is I was flushing within the middle of the transaction. After flushing, there was no long an active transaction.</p>
<hr />
<p>In the end I'm using <code>async-lock</code> around my access to the SQLite db wrapper, and have my own <code>async Transaction(actions: () =&gt; Promise&lt;void&gt;)</code> method that handles the BEGIN/COMMIT/ROLLBACK itself, and some general purpose DocumentStore methods that make calls that are implicitly then included in the transaction.</p>

