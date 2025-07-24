# TypeError: Cannot read properties of undefined (reading &#39;postgresClient&#39;)
[Link to question](https://stackoverflow.com/questions/77248422/typeerror-cannot-read-properties-of-undefined-reading-postgresclient)
**Creation Date:** 1696654821
**Score:** 0
**Tags:** node.js, typescript, database, postgresql
## Question Body
<p>I'm trying to make an API that uses PostgreSQL to store shortened links. However, when trying to execute a query to the database, <code>postgreClient</code> is undefined every time.</p>
<p>short.controller.ts:</p>
<pre class="lang-js prettyprint-override"><code>import { Request, Response, NextFunction } from &quot;express&quot;;
import client from &quot;../Database&quot;;

export default class ShortController {
    private postgreClient;

    constructor() {
        this.postgreClient = client;
    }

    async post(request: Request, response: Response, next: NextFunction) {
        const url = request.query.url;
        const randomString = Math.random().toString(36).substring(2, 7);

        const shortUrl = `${process.env.API_URL}/api/short/${randomString}`;

        try {
            const sql = &quot;INSERT INTO short (short_url, url) VALUES ($1, $2)&quot;;
            await this.postgreClient.query(sql, [shortUrl, url]);
            await response.json({ shortUrl });
        } catch (exception) {
            console.error(exception);
            await response.json({ message: &quot;Error&quot; });
        }
    }
}
</code></pre>
<p>Database.ts:</p>
<pre class="lang-js prettyprint-override"><code>import { Client } from &quot;pg&quot;;
import * as dotenv from &quot;dotenv&quot;;

dotenv.config();

const dbHost = process.env.DB_HOST || &quot;localhost&quot;;
const dbPort = process.env.DB_PORT || 5432;
const dbUser = process.env.DB_USER || &quot;postgres&quot;;
const dbPassword = process.env.DB_PASSWORD || &quot;password&quot;;
const dbDatabase = process.env.DB_DATABASE || &quot;kyowakoku&quot;;

const connectionString = `postgres://${dbUser}:${dbPassword}@${dbHost}:${dbPort}/${dbDatabase}`;

const client = new Client({ connectionString });

export default client;
</code></pre>
<p>I tried rewriting to a especially class thinking it would do something, but without result.</p>

## Answers
### Answer ID: 77250978
<p>I assume that the <code>TypeError: Cannot read properties of undefined (reading 'postgresClient')</code> error occurs around these lines:</p>
<pre class="lang-js prettyprint-override"><code>// short.controller.ts
        try {
            const sql = &quot;INSERT INTO short (short_url, url) VALUES ($1, $2)&quot;;
            await this.postgreClient.query(sql, [shortUrl, url]); &lt;- error occurs because of this line
            await response.json({ shortUrl });
</code></pre>
<p>That means that <code>this</code> refers to an <code>undefined</code> value, in other words, the context of the function has been lost. So i'd suggest you to check where and how the method <code>ShortController#post</code> is being called.</p>
<p>I can assume that the method was called without it's context. Maybe somewhere in your code you passed the method to the express instance in such a manner:</p>
<pre class="lang-js prettyprint-override"><code>app.post('/', shortControllerInstance.post) &lt;- here the context is lost. Any reference to `this` inside the method `post` will most likely refer to `undefined`
</code></pre>
<p>To fix this you need to explicitly bind the function to the correct context:</p>
<pre class="lang-js prettyprint-override"><code>app.post('/', shortControllerInstance.post.bind(shortControllerInstance)) &lt;- now the context is bound to the function
</code></pre>
<p>This probably will fix the issue with lost function's context, but for further checks see @big-bob-little's <a href="https://stackoverflow.com/a/77248527/8507883">answer</a> also.</p>
<p>Note that it is just an assumption based on the amount of code provided by you. It is always better to post the whole reproduction code. Also the entire error message with the stack trace is also helpful.</p>

### Answer ID: 77248527
<p>The only issue I see is that you did not call <strong>connect()</strong> on the postgres client . This means you've built a connection string and failed to do the actual connection to the DB.</p>
<p>There are 2 ways you can solve this.</p>
<ol>
<li><strong>Calling the connect method in your database.ts file</strong></li>
</ol>
<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>import {
  Client
} from "pg";
import * as dotenv from "dotenv";

dotenv.config();

const dbHost = process.env.DB_HOST || "localhost";
const dbPort = process.env.DB_PORT || 5432;
const dbUser = process.env.DB_USER || "postgres";
const dbPassword = process.env.DB_PASSWORD || "password";
const dbDatabase = process.env.DB_DATABASE || "kyowakoku";

// i'm editing this code as response to your follow up comment. 
// if the client is having issues on multiple connections, switch to using a pool. 
// he pool is initially created empty and will create new clients lazily as they are needed


const client = new Pool({
  host: dbHost,
  user: dbUser,
  //add password , port etc 
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

// const connectionString = //`postgres://${dbUser}:${dbPassword}@${dbHost}:${dbPort}/${dbDatabase}`;
//const client = new Client({
//  connectionString
// });

// call the connect() to initialize the actual db connection before exporting it 
//client.connect()

export default client;</code></pre>
</div>
</div>
</p>
<ol start="2">
<li>Leave the database.ts file as it is, and initiate the connection from your  controller.ts file</li>
</ol>
<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>import {
  Request,
  Response,
  NextFunction
} from "express";
import client from "../Database";

export default class ShortController {
  private postgreClient;

  constructor() {
    this.postgreClient = client;
    this.connectToDatabase(); // Call a method to connect to the database
  }

  // method to connect to the database 
  private async connectToDatabase() {
    try {
      await this.postgreClient.connect(); // Connect to the database
      console.log("Connected to PostgreSQL database");
    } catch (error) {
      console.error("Error connecting to PostgreSQL database:", error);
    }
  }

  async post(request: Request, response: Response, next: NextFunction) {
    const url = request.query.url;
    const randomString = Math.random().toString(36).substring(2, 7);

    const shortUrl = `${process.env.API_URL}/api/short/${randomString}`;

    try {
      const sql = "INSERT INTO short (short_url, url) VALUES ($1, $2)";
      await this.postgreClient.query(sql, [shortUrl, url]);
      await response.json({
        shortUrl
      });
    } catch (exception) {
      console.error(exception);
      await response.json({
        message: "Error"
      });
    }
  }
}</code></pre>
</div>
</div>
</p>
<p>Other general rules</p>
<ol>
<li>Ensure your .env file is loaded correctly and contains the specified env variables for the DB_HOST, DB_USER, DB_PORT etc</li>
<li>Ensure you have postgres running on your machine and can be accessed from the specified DB_PORT stated in your env file</li>
<li>Ensure the database specified exist or can be created</li>
</ol>

