# Get data from MySQL query for use in nodejs
[Link to question](https://stackoverflow.com/questions/59666792/get-data-from-mysql-query-for-use-in-nodejs)
**Creation Date:** 1578582245
**Score:** 0
**Tags:** javascript, mysql, node.js
## Question Body
<p>Trying to query my database and each time I do, it runs all the queries at the end instead of when I need them in nodejs. </p>

<pre><code>var mysql = require('mysql');

var con = mysql.createConnection({
  host: database.host,
  user: database.user,
  password: database.password,
  database: database.database
});
</code></pre>

<p>The connection data I am pulling from a json file.</p>

<pre><code>function getSymbol(id){
var s = "";
con.query("SELECT * FROM Symbol WHERE PlayerID = '" + id + "'", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
    if (result.length &lt; 1) {
        console.log(result);
        s = result[0].Symbol;
    }
    else {
        s = "!";
    }
});
console.log(s);
return s;
</code></pre>

<p>}</p>

<p>It all runs at the end of the program wondering if there is a fix or if I should switch to python (seriously considering rewriting all of it at this point).</p>

## Answers
### Answer ID: 59667049
<p>As mentioned, the method is NOT sync. Your result will be on the callback you pass.</p>

<pre><code>con.query(sql, function (err, result) {
    if (err) throw err;
    console.log("The Data: " + result);
});
</code></pre>

<p>More Info: <a href="https://www.w3schools.com/nodejs/nodejs_mysql.asp" rel="nofollow noreferrer">https://www.w3schools.com/nodejs/nodejs_mysql.asp</a> </p>

<p>Moreover, you need to connect first with <code>con.connect( &lt;callback-here&gt; )</code>.</p>

<p>The best way to work with this is to avoid the callbacks for async/wait syntax.</p>

### Answer ID: 59666914
<p>The problem is what you have written comes under NIO and it wont wait for executing the next statement unless you ask it to. Try the below code:</p>

<pre><code>async function getSymbol(id){
   var s = "";
   try {
    let result = await con.query("SELECT * FROM Symbol WHERE PlayerID = '" + id + "'")
    if (result.length &lt; 1) {
        console.log(result);
        s = result[0].Symbol;
    }
    else {
        s = "!";
    }
   }catch(error){
        console.log(error);
        throw new error;
   }
    console.log(s);
   return s;
 }
</code></pre>

<p>Note: I have used async/await. You can also use <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise" rel="nofollow noreferrer">Promises</a></p>

