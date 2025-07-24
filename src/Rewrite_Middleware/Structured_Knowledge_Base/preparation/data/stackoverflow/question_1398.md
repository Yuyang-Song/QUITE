# Handling &quot;Socket has unexpectedly been closed&quot; - MariaDB nodejs connector
[Link to question](https://stackoverflow.com/questions/74925498/handling-socket-has-unexpectedly-been-closed-mariadb-nodejs-connector)
**Creation Date:** 1672111985
**Score:** 2
**Tags:** node.js, express, mariadb
## Question Body
<p>I have an express server running in a docker container and a mariadb server both on a synology NAS. When the NAS backs up the database it says &quot;The application will be temporarily stopped during backup and will not run until backup ends.&quot;  I am using the mariadb nodejs connector and instantiating a pool that I require in other modules.
The problem I have is that when it does this, whether or not I am attempting to query the database, my express server will get a fatal error regarding socket unexpectedly being closed and crash.  The error log reads:</p>
<pre><code>[nodemon] starting `node ./server.js` 
listening on port 3001 
/Express/node_modules/mariadb/lib/connection.js:1158 
 if (!avoidThrowError &amp;&amp; !errorThrownByCmd) throw err; 
 ^ 
 
SqlError: (conn=42, no: 45009, SQLState: 08S01) socket has unexpectedly been clo 
sed 
 at module.exports.createFatalError (/Express/node_modules/mariadb/lib/misc/e 
rrors.js:81:10) 
 at Connection.socketErrorHandler (/Express/node_modules/mariadb/lib/connecti 
on.js:1098:20) 
 at Socket.emit (node:events:525:35) 
 at endReadableNT (node:internal/streams/readable:1359:12) 
 at process.processTicksAndRejections (node:internal/process/task_queues:82:2 
1) { 
 text: 'socket has unexpectedly been closed', 
 sql: null, 
 fatal: true, 
 errno: 45009, 
 sqlState: '08S01', 
 code: 'ER_SOCKET_UNEXPECTED_CLOSE'
</code></pre>
<p>This is what my db connection file looks like:</p>
<pre><code>const mariaDB=require('mariadb');
const pool=mariaDB.createPool({
    host: host,
    port: port,
    user: user,
    password: password,
   
    connectionLimit: 5,
    database: database
})
module.exports =  pool;
</code></pre>
<p>and in other modules I am doing something similar to the following:</p>
<pre><code>const pool=require('../models/databaseConnection')

async function submitNewQuote(quote){
    let conn;
    let newQuote
    try{
        conn=await pool.getConnection();
        let sqlString=...;
        let valArray=...;
        const results=await conn.query(sqlString,valArray)
        newQuote=results;
    } catch(e){
        console.log(e)
    } finally{
        if(conn)await conn.end();
        return newQuote.insertId;
    }
}

</code></pre>
<p>There is not much documentation on handling fatal pool errors that I can find on the mariadb knowledgedb
<a href="https://mariadb.com/kb/en/connector-nodejs-promise-api/#pool-api" rel="nofollow noreferrer">https://mariadb.com/kb/en/connector-nodejs-promise-api/#pool-api</a></p>
<p>I've tried switching to the mysql node connector but its not as simple as just changing the connector (the format of my queries is not in the .query(sql,callback) format so I would have to rewrite queries to even try it, I think).  I am hoping there is some kind of error handling I can perform on the created pool to catch the fatal socket closing and redo the pool.</p>

## Answers
### Answer ID: 74950644
<p>See <a href="https://github.com/mariadb-corporation/mariadb-connector-nodejs/blob/master/documentation/promise-api.md#pool-options" rel="nofollow noreferrer">pool options</a> documentation.</p>
<p>Pool cannot detect all socket issue. The problem is that most of the time, network error will be detected only when trying to write to the socket. In order to better detect socket error, here is what you can do:</p>
<p>By default, pool doesn't validate connection when it has been use recently (option <code>minDelayValidation</code>). If you want to ensure that the connection is always ok, you can set this option to value 0: pool will then validate the connection each time it's borrowed. If that validation fails having a socket error for example, the connection will be discarded and another connection will be used (after being validate) or a new connection will be created.</p>
<p>Btw, pool has some shortcut <code>query</code> option that permits to borrow a connection, execute a single query then release connection:</p>
<pre><code>  async function submitNewQuote(quote){
    let sqlString = ...;
    let valArray = ...;
    try {
      const newQuote = await pool.query(sqlString, valArray);
      return newQuote.insertId;
    } catch(e){
      console.log(e)
    }
  }
</code></pre>
<p>This permits easier code to read, and ensure connection to be released to pool.</p>

