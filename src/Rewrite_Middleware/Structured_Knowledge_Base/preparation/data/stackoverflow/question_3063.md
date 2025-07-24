# How to maintain mongo client in NodeJS
[Link to question](https://stackoverflow.com/questions/64442904/how-to-maintain-mongo-client-in-nodejs)
**Creation Date:** 1603188498
**Score:** 0
**Tags:** node.js, mongodb, express, connection
## Question Body
<p>I'm trying to understand how to maintain the mongo client in node application. The first thought I had is to create a client on every single collection retrieval. Something like this:</p>
<pre><code>const getCollection = (collectionName) =&gt; {
return MongoClient.connect(url, {useNewUrlParser: true, useUnifiedTopology: true})
    .then((client) =&gt; {
        const database = client.db(databaseName);
        return database.collection(collectionName);
    })
    .catch((err) =&gt; {
        console.log(err);
    });
};
</code></pre>
<p>And then use the returned promise for queries. Like this:</p>
<pre><code>const executeFind = (collectionName, query, projection, skip, limit) =&gt; {
    return getCollection(collectionName)
        .then(collection =&gt; {
            return collection.find(query, {projection: projection})
                .skip(skip)
                .limit(limit)
                .toArray();
        })
        .catch((err) =&gt; {
            console.log(err);
        });
};
</code></pre>
<p>The problem with this approach is that number of open connections to mongo increases rapidly when running the application resulting in problems with the database operations and lot of alerts.</p>
<p>Possible causes of connection increase I considered:</p>
<ul>
<li>Large pool size - I tried adding <code>maxPoolSize=5</code> to URL. Also adding <code>poolSize: 5</code> to <code>options</code> (second parameter of <strong>MongoClient</strong>'s <code>connect</code> function. The number connections still bursts.</li>
<li>Missing connection close  - I can't find the doc now but I read somewhere that connections are managed by client itself so there is not need to thinking about <code>close()</code> ing them. But anyway, I tried to rewrite the code to <code>close()</code> the client after <code>collection.find()</code> returns the result. I am getting <code>Cannot use a session that has ended</code></li>
</ul>
<p>Other than these, I don't have any other thoughts in mind to maintain the mongo client in a way that will be efficient in terms of resource allocation/running. I'd like to hear the answer on both:</p>
<ul>
<li><strong>1. What exactly can be done in this very approach to avoid open connection increase?</strong></li>
<li><strong>2. What is more general/optimal/best practiced way of maintaining mongo client.</strong></li>
</ul>

## Answers
### Answer ID: 64447203
<p>I can partially answer my question.
I was able to solve the connection increase problem with <code>client.close()</code>. The main problem seemed to be that the promises were missing <code>await</code> so <code>close()</code> was resulting in unexpected behavior (<code>close()</code> sometimes happened before the actual invoking of the query, and resulted in <code>session already closed</code> error).</p>
<p>The problem with above approach (open and close connection on every call) is that it's quite slow.</p>
<p><strong>Still looking for general answer about optimally maintaining the client.</strong></p>
<p><strong>Update</strong></p>
<p>I was finally able to find solution which doesn't open absurdly high amount of connections and is also optimal.</p>
<p>The trick here is to declare and invoke async function in data access layer (Or wherever the database code is located) that will set the database object. Something like this:</p>
<pre><code>let database;

(async () =&gt; {
    const client = await MongoClient.connect(url, {poolSize: 150, useNewUrlParser: true, useUnifiedTopology: true});
    database = client.db(databaseName);
})();
</code></pre>
<p>And then just reuse the database object everywhere, like this:</p>
<pre><code>database.collection(collectionName).insertMany(documents);
</code></pre>
<p>Pooling and connection open/close is handled by <code>client</code>. In terms of optimality it's way faster (As expected). Not sure if having global database or immediate function invoke in dao (Though, as the file is imported with <code>require</code> it shouldn't be invoked more than once) is the best practice but it definitely does the trick.</p>

### Answer ID: 64444087
<ul>
<li>Check the below snippet for the mongo db pool connection.</li>
</ul>
<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>MongoClient.connect(url, {
  poolSize: 10
  // other options can go here
}, function(err, db) {
  global.mongodb = db;
});</code></pre>
</div>
</div>
</p>
<ul>
<li>For handling the connection, we need to write the custom code, like checking connection is exist or not, if not create a new connection.</li>
</ul>

