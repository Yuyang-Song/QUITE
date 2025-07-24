# Function won&#39;t return an array of items created from MySQL Query (async/Await)
[Link to question](https://stackoverflow.com/questions/55972993/function-wont-return-an-array-of-items-created-from-mysql-query-async-await)
**Creation Date:** 1556897548
**Score:** 0
**Tags:** mysql, node.js, async-await
## Question Body
<p>I'm trying to create an array of items from a MySQL query to return from an async function but the returns are empty.</p>

<p>Things I've tried:</p>

<ul>
<li>Read up to the latest info about async/await</li>
<li>Stack overflow</li>
<li>Numerous test around changing code, replacing return calls, rewriting functions.</li>
</ul>

<p>This is for a new webservice (nodejs) that needs to initialize values from a MySQL database and after that fast access to the values to compare them against values pulled from the internet. To limit the amount of database calls I'm planning to have the values in an array (in-memory) and whenever they change enough (based on calculations) write them to the DB. </p>

<p>All is Linux based using Node 11</p>

<pre><code>require('dotenv').config()

var mysql = require('mysql')
var dbconnection = mysql.createConnection({
  host: 'localhost',
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PW,
  database: process.env.MYSQL_DB
})
dbconnection.connect(function (err) {
  if (err) {
    console.error('error connecting: ' + err.stack)
  }
})
async function ReadDB () {
  var ArrBuyPrice = []
  var query = 'SELECT * FROM pricing'
  var items = await dbconnection.query(query, function (err, rows, result) {
    if (err) throw err
    for (var i in rows) {
      ArrBuyPrice.push(rows[i].price_buy.toFixed(8))
    }
    return ArrBuyPrice
  })
  return items
}

async function InitialProcess () {
  var DbResult = await ReadDB()
  console.log(DbResult)
}

InitialProcess()
</code></pre>

<p>I would expect the <code>console.log</code> output to be <code>[ '0.00000925', '0.00000012' ]</code></p>

## Answers
### Answer ID: 55973401
<pre><code>// https://stackoverflow.com/questions/44004418

var mysql = require('mysql')
var dbconnection = mysql.createConnection({
    host: 'localhost',
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PW,
    database: process.env.MYSQL_DB
})

const util = require('util');

async function ReadDB() {
    var ArrBuyPrice = []

    const query = util.promisify(dbconnection.query).bind(dbconnection);

    try {
        const rows = await query('select * from pricing');
        for (var i in rows) {
            ArrBuyPrice.push(rows[i].price_buy.toFixed(8))
        }
        return ArrBuyPrice;
    } catch (error) {
        console.log(error)
        return [];
    } finally {
        dbconnection.end();
    }
}

async function InitialProcess() {
    var DbResult = await ReadDB()
    console.log(DbResult)
}

InitialProcess();
</code></pre>

<hr>

<p><strong>What is Problem:</strong>  </p>

<pre><code>async function ReadDB() {
  var ArrBuyPrice = []
  var query = 'SELECT * FROM pricing';

  var items = await dbconnection.query(query, function (err, rows, result) {
    if (err) throw err
    for (var i in rows) {
      ArrBuyPrice.push(rows[i].price_buy.toFixed(8))
    }
    return ArrBuyPrice
  });
  return items
}
</code></pre>

<p>At <code>await dbconnection.query</code>, <code>await</code> is not working, and it is unnecessary, because <code>dbconnection.query()</code> function is not <code>Promise</code> function.</p>

<p>So, the <code>rows</code> which  query result will arrive after <code>return items</code>;
And <code>return ArrBuyPrice</code> function is not running.</p>

