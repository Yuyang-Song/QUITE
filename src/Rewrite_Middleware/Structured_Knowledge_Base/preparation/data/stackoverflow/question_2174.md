# How to receive a value from this JavaScript function?
[Link to question](https://stackoverflow.com/questions/21917027/how-to-receive-a-value-from-this-javascript-function)
**Creation Date:** 1392922603
**Score:** 0
**Tags:** javascript, node.js, callback
## Question Body
<p>I know it's quite a typical question and I should look into callback functions, but as much as I've tried, I couldn't solve this one. Maybe you can help?</p>

<p>The problem is very simple. At a certain point of my code I've got the following function that queries Neo4J database (through node.js node-neo4j library) and gets the results into <code>statements.data</code> variable.</p>

<pre><code>   dbneo.cypherQuery(rangeQuery, function(err, statements){

            if(err) {
                err.type = 'neo4j';
                return fn(err);
             }

            console.log(statements);

            fn(null,statements.data);

     });

     var results = statements.data; // THIS DOESN'T WORK! HOW TO CHANGE IT?
</code></pre>

<p>What I need is that another variable <code>results</code> gets the <code>statements.data</code> from that DB request and the script continues.</p>

<p>How would I need to rewrite this code in order to do that?</p>

<p>I'm not very familiar with JavaScript, so I tried different syntax but it didn't work.
For example, when I wrap the dbneo.cypherQuery function into another function and call its results, I still can't pass the value I need to the parameter.</p>

<p>Thank you and sorry if this question is irritating in my inability to solve such a simple problem. </p>

## Answers
### Answer ID: 21917771
<p>You are facing the situation why javascript is often said to lead to callback hell. You cannot do <code>var results = statements.data</code> this because at the time that line is executed, the async callback function <code>function(err, statements){...</code> may not yet be executed and thus your <code>results</code> will be <code>undefined</code>. </p>

<p>If you want your code to behave synchronously you need to use something called promises.</p>

<p>One good post about promises is here:</p>

<p><a href="http://domenic.me/2012/10/14/youre-missing-the-point-of-promises/" rel="nofollow">http://domenic.me/2012/10/14/youre-missing-the-point-of-promises/</a></p>

<p>To solve your problem with the excellent Q library ( <a href="https://github.com/kriskowal/q" rel="nofollow">https://github.com/kriskowal/q</a> ) you could write your function for example like this:</p>

<pre><code>function cypherQuery() {
    var deferred = Q.defer();

    dbneo.cypherQuery(rangeQuery, function(err, statements){
        if(err) {
            err.type = 'neo4j';
            deferred.reject(err);
        } else {
            deferred.resolve(statements.data);
        }

        return deferred.promise;
 });
}
</code></pre>

<p>then you can call your function like this:</p>

<pre><code>cypherQuery().then(function(result) {
    console.log(result);
})
</code></pre>

### Answer ID: 21917309
<p>I think that the problem is that you shouldn't <code>return</code> values when using asynchronous javascript.</p>

<p>Callbacks are the most common implementation for asynchronous behaviour, whereas returning values is a common synchronous operation.</p>

<p>You can solve your problem by passing as a parameter the function that needs statements.data and invoke it inside your function like this:</p>

<pre><code>var functionThatRequireData = function (data) { .... }

dbneo.cypherQuery(rangeQuery, function(err, statements, functionThatRequireData){

            console.log(statements);

            functionThatRequireData(statements.data);

     });
</code></pre>

<p>That way you can have the data you need, without using <code>return</code>.</p>

<p>As an alternative, if storing the definition of the function <code>functionThatRequireData</code> in a variable doesn't seem to work, you can still do something like:</p>

<pre><code>var auxiliarFunction = function(data){
    functionThatRequireData(data);
}
</code></pre>

<p>And call <code>auxiliarFunction</code> function instead of <code>functionThatRequireData</code> (just in case you have problems with the scope or something similar).</p>

<p>Hope this helps.</p>

### Answer ID: 21917354
<p>Your problem is that you're trying to use <code>statements.data</code> and that object is only defined inside your anonymous function.</p>

<p>Try this way:</p>

<pre><code>var results;
dbneo.cypherQuery(rangeQuery, function(err, statements){
    if(err) {
        err.type = 'neo4j';
        return fn(err);
    }

    console.log(statements);

    fn(null,statements.data);

    results = statements.data;
});
</code></pre>

