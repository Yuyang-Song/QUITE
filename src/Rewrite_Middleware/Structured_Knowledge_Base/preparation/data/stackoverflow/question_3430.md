# Cant connect to mysql database via JS... Error: getaddrinfo ENOTFOUND
[Link to question](https://stackoverflow.com/questions/79350809/cant-connect-to-mysql-database-via-js-error-getaddrinfo-enotfound)
**Creation Date:** 1736720118
**Score:** 1
**Tags:** javascript, node.js, error-handling, database-connection, nodemon
## Question Body
<p>Moving to an online database hosted by IONOS from localhost and having trouble connecting to the database via JS, but when I use php and the same database information I can connect and query perfectly fine.</p>
<p>Why am I getting error connecting to DB using JS code?</p>
<p>I do not want to rewrite my files in php as I am very unfamiliar and I already have tons of my files written in JS already when it ran fine with localhost.</p>
<p><strong>JS Code:</strong></p>
<pre class="lang-js prettyprint-override"><code>import mysql from 'mysql';
import env from &quot;dotenv&quot;;

env.config();

// Create a connection \
const connection = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT
});

// Test the connection
connection.connect()

connection.query('SELECT * FROM unit', (err, rows) =&gt; {
  if (err) throw err;
  console.log('Data received from Db:',rows[0].soluition);
});
</code></pre>
<p><strong>Error:</strong> <a href="https://i.sstatic.net/oYgNl5A4.png" rel="nofollow noreferrer">Error Snapshot</a></p>
<blockquote>
<p>file:///C:/Users/nunzi/Desktop/VFM/vfm-backend/src/db.js:19
if (err) throw err;
^</p>
<p>Error: getaddrinfo ENOTFOUND XXXXXXXXXXXXXXX
at GetAddrInfoReqWrap.onlookupall [as oncomplete] (node:dns:120:26)
--------------------
at Protocol._enqueue (C:\Users\nunzi\Desktop\VFM\vfm-backend\node_modules\mysql\lib\protocol\Protocol.js:144:48)
at Protocol.handshake (C:\Users\nunzi\Desktop\VFM\vfm-backend\node_modules\mysql\lib\protocol\Protocol.js:51:23)
at Connection.connect (C:\Users\nunzi\Desktop\VFM\vfm-backend\node_modules\mysql\lib\Connection.js:116:18)
at file:///C:/Users/nunzi/Desktop/VFM/vfm-backend/src/db.js:16:12
at ModuleJob.run (node:internal/modules/esm/module_job:271:25)
at async onImport.tracePromise.<strong>proto</strong> (node:internal/modules/esm/loader:547:26)
at async asyncRunEntryPointWithESMLoader (node:internal/modules/run_main:116:5) {
errno: -3008,
code: 'ENOTFOUND',
syscall: 'getaddrinfo',
hostname: 'XXXXXXXXXXXXXX',
fatal: true
}</p>
<p>Node.js v22.12.0</p>
</blockquote>
<p>Note: I changed hostname to X's just for example.</p>

