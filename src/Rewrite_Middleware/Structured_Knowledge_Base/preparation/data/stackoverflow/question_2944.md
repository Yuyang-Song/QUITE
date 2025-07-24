# Google Cloud SQL connection in NodeJS app (Express) --&gt; Error: connect ENOENT
[Link to question](https://stackoverflow.com/questions/59584987/google-cloud-sql-connection-in-nodejs-app-express-error-connect-enoent)
**Creation Date:** 1578083517
**Score:** 0
**Tags:** mysql, sql, node.js, google-app-engine, google-cloud-sql
## Question Body
<p>I'm trying to deploy my NodeJS app on Google Cloud services and getting the following error hen I try to call a database query using Postman through localhost/8080, which is where my server is listening: <code>connect ENOENT /cloudsql/&lt;MY_CONNECTION_NAME&gt;</code>. Here's my database connection file, <code>config.js</code>:</p>

<pre><code>
const mysql = require('mysql');
const dotenv = require('dotenv');

dotenv.config();

const {
  DB_PASS,
  DB_USER,
  DB_NAME,
} = process.env;

const config = {
  user: DB_USER,
  password: DB_PASS,
  database: DB_NAME,
  socketPath: `/cloudsql/${process.env.CLOUD_SQL_CONNECTION_NAME}`,
};

const connection = mysql.createConnection(config);

// create connection
connection.connect((err) =&gt; {
  if (err) throw err;
  console.log(`Connected to database ${DB_NAME}`);
});

module.exports.connection = connection;
</code></pre>

<p>I know that Google recommends using a pool to connect, but I'm afraid that doing that will require me rewriting all my database queries, and I'm on a tight deadline.</p>

<p>I've been able to successfully shell into the database with MYSQL using the terminal.</p>

## Answers
### Answer ID: 63871277
<p>this is happen if you are using flex as env in <code>app.yaml</code> to run without errors remove the <code>env:flex</code> from your <code>app.yaml</code>,
your app.yaml need to look like this
<a href="https://i.sstatic.net/o5hES.png" rel="nofollow noreferrer">app.yaml</a></p>
<p>and you will successfully connected to the cloud sql without causing errors
<a href="https://i.sstatic.net/QIzjL.png" rel="nofollow noreferrer">console log</a></p>

### Answer ID: 59587832
<p>Take a look at the <a href="https://cloud.google.com/sql/docs/mysql/connect-app-engine" rel="nofollow noreferrer">Connecting to App Engine</a> page. In particular, here are some things you should check if the socket isn't present:</p>

<ol>
<li>For GAE Flex, make sure you have the following in your <code>app.yaml</code>:</li>
</ol>

<pre><code>beta_settings:
  cloud_sql_instances: &lt;INSTANCE_CONNECTION_NAME&gt;
</code></pre>

<ol start="2">
<li><p>Ensure the SQL Admin API is enabled and make sure you have the correct IAM permissions (<code>Cloud SQL Client1 or higher) on your service account (</code>service-PROJECT_NUMBER@gae-api-prod.google.com.iam.gserviceaccount.com`). If between projects, make sure you have the</p></li>
<li><p>Make sure you are spelling  <code>&lt;INSTANCE_CONNECTION_NAME&gt;</code> correctly. It should be in the format <code>&lt;PROJECT&gt;:&lt;REGION&gt;:&lt;INSTANCE&gt;</code> - you can copy it exactly from the "Instance Details" page for your instance.</p></li>
</ol>

<p>Additionally, using a connection pool will have no effect on your queries. Using a pool only means that when you "open" a connection, it is actually reusing an existing connection, and when you "close" a connection it puts it back in the pool for your application to use elsewhere. The queries you perform using the pool should be exactly the same. </p>

