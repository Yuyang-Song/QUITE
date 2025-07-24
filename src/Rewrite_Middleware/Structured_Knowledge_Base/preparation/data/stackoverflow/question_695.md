# SELECT Query in WebSQL in Safari is returning an error
[Link to question](https://stackoverflow.com/questions/37648885/select-query-in-websql-in-safari-is-returning-an-error)
**Creation Date:** 1465181106
**Score:** 1
**Tags:** javascript, sqlite, cordova, safari, web-sql
## Question Body
<p>This is the code in question. I've been trying to get working. </p>

<p>The issue, is that the variable result in the callback doesn't have any rows in it. 
But this is present only in Safari. Chrome works perfectly.<br>
The Database on Safari and Chrome is showing the correct values in the database.  </p>

<p>The result variable has an interesting property in it: </p>

<pre><code>SQLResultSet
insertId: Error: InvalidAccessError: DOM Exception 15
</code></pre>

<p>But the rows array is not present.  </p>

<pre><code>db.transaction(function (tx) {
        tx.executeSql("INSERT INTO QUIZZES (id,name,completed,icon) VALUES (coalesce((SELECT max(id) FROM QUIZZES),0)+1,?,0,?)", [json.name,json.icon],
            function (tx, result) {
                console.log('Inserted Quiz. Selecting Quiz');

                tx.executeSql("SELECT * FROM QUIZZES ", [],
                    function (tx, result) {
                        console.log(result);
                        var quizid = result.rows[0].id;
                        console.log(quizid);
                    },
                    errorCB);
            });

    },
errorCB);
</code></pre>

<p>What I've tried is re-working my code from one transaction to multiple separate calls to DB via the db.transaction(... in the callbacks.<br>
And I also tried rewriting the queries themselves, or writing queries that will return the correct result 100% of the time. Yet, got got nowhere.</p>

<p>Thank you for your help in advance</p>

## Answers
### Answer ID: 38245675
<p>The issue is that Chrome is much more lenient in how you structure your code.</p>

<p>Selecting the results from a query should be done: via</p>

<pre><code>results.rows.item(0).id;
</code></pre>

<p>rather than </p>

<pre><code>result.rows[0].id;
</code></pre>

<p>Note the item.</p>

<p>This solved the issue for me.</p>

