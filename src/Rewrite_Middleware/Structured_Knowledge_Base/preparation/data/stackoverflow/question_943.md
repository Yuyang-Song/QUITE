# Sequelize migrate failing due to dialect object Object not supported error
[Link to question](https://stackoverflow.com/questions/51177425/sequelize-migrate-failing-due-to-dialect-object-object-not-supported-error)
**Creation Date:** 1530719781
**Score:** 0
**Tags:** node.js, express, sequelize.js, node-postgres, sequelize-cli
## Question Body
<p><strong>Background</strong></p>

<p>I am creating a boilerplate express application. I have configured a database connection using pg and sequelize. When I add the cli and try to run <code>sequlize db:migrate</code> I get this error,</p>

<blockquote>
  <p>ERROR: The dialect [object Object] is not supported. Supported
  dialects: mssql, mysql, postgres, and sqlite.</p>
</blockquote>

<p><strong>Replicate</strong></p>

<p>Generate a new express application. Install pg, pg-hstore, sequelize and sequelize-cli. </p>

<p>Run <code>sequelize init</code>.</p>

<p>Add a config.js file to the /config path that was created from sequelize init. </p>

<p>Create the connection in the config.js file. </p>

<p>Update the config.json file created by sequelize-cli. </p>

<p>Run <code>sequelize db:migrate</code> </p>

<p><strong>Example</strong> </p>

<p><em>/config/config.js</em></p>

<pre><code>const Sequelize = require('sequelize');
const { username, host, database, password, port } = require('../secrets/db');

const sequelize = new Sequelize(database, username, password, {
  host,
  port,
  dialect: 'postgres',
  operatorsAliases: false,
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
});

module.exports = sequelize;
</code></pre>

<p><em>/config/config.js</em></p>

<pre><code>{
  "development": {
    "username": "user",
    "password": "pass",
    "database": "db",
    "host": "host",
    "dialect": "postgres"
  },
  "test": {
    "username": "user",
    "password": "pass",
    "database": "db",
    "host": "host",
    "dialect": "postgres"
  },
  "production": {
    "username": "user",
    "password": "pass",
    "database": "db",
    "host": "host",
    "dialect": "postgres"
  }
}
</code></pre>

<p><strong>Problem</strong></p>

<p>I expect the initial migrations to run but instead get an error,</p>

<blockquote>
  <p>ERROR: The dialect [object Object] is not supported. Supported
  dialects: mssql, mysql, postgres, and sqlite.</p>
</blockquote>

<p><strong>Versions</strong></p>

<pre><code>Dialect: postgres 
Dialect version: "pg":7.4.3 
Sequelize version: 4.38.0
Sequelize-Cli version: 4.0.0
</code></pre>

<p><em>Package Json</em></p>

<pre><code>"pg": "^7.4.3",
"pg-hstore": "^2.3.2",
"sequelize": "^4.38.0"
</code></pre>

<p><em>Installed globally</em></p>

<pre><code>npm install -g sequelize-cli
</code></pre>

<p><strong>Question</strong></p>

<p>Now that the major rewrite has been released for sequelize, what is the proper way to add the dialect so the migrations will run?</p>

<p>It is important to note that my connection is working fine. I can query the database without problems, only <code>sequelize-cli</code> will not work when running migrations.</p>

## Answers
### Answer ID: 76970219
<p>Hi Wuno and Hi everyone,</p>
<p>I've had the same problem recently and this was very annoying.</p>
<p>The problem:
<code>ERROR: The dialect [object Object] is not supported. Supported dialects: mssql, mysql, postgres, and sqlite.</code></p>
<p>First we need to know that: sequelize needs one type of connection and our program needs another.</p>
<p>For sequelize I have .sequelizerc:</p>
<pre><code>const path = require('path');

module.exports = {
    config: path.resolve(__dirname, 'src', 'config', 'database.js'),
    'migrations-path': path.resolve(__dirname, 'src', 'database', 'migrations'),
    'seeders-path': path.resolve(__dirname, 'src', 'database', 'seeders'),
    'models-path': path.resolve(__dirname, 'src', 'api', 'models')
}
</code></pre>
<p>And the connection in my database.js:</p>
<pre><code>const dotenv = require('dotenv');
dotenv.config();

module.exports = {
    dialect: process.env.DB_DIALECT,
    host: process.env.DB_HOST,
    username: process.env.DB_USER,
    password: process.env.DB_PWD,
    database: process.env.DB_NAME,
    define: {
        timestamps: true,
        underscored: true
    }
}
</code></pre>
<p>For sequelize is this, now you can run your db:migrate without problem, but if you try to use your app will start to message that Error...</p>
<p>After this you will have other errors, problably in your models when you try to run your code <em>(npm start or nodemon...)</em>. So, now you'll need to solve this with another connection, like I said before.</p>
<p>The new connection will I gave the name database_app.js:</p>
<pre><code>const dotenv = require('dotenv');
dotenv.config();
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USER,
    process.env.DB_PWD,
    {
        host: process.env.DB_HOST,
        dialect: process.env.DB_DIALECT,
        logging: false
    }
);
//console.log(sequelize);


module.exports = sequelize;
</code></pre>
<p>After this you need to change the configuration of your code, remember for sequelize is one and for run the code is another.</p>
<p>Regards.</p>

### Answer ID: 57066755
<p>i ran into same problem. there is a few thing that you need to change. first, i am not sure why you had 2 <code>config/config.js</code> file. i assumed the second file is <code>config.json</code>. the reason run into this problem is that </p>

<pre><code>const sequelize = new Sequelize(database, username, password, {
  host,
  port,
  dialect: 'postgres',
  operatorsAliases: false,
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000
  }
});
</code></pre>

<p>these lines of code is used for the node server to access db, not for sequlize-cli to migrate. you need to follow exact the sequlize-cli instruction. here is the link:  <a href="http://docs.sequelizejs.com/manual/migrations.html#dynamic-configuration" rel="nofollow noreferrer">instruction</a></p>

<p>my code:
<code>config/db.js</code></p>

<pre><code>const {sequlize_cli} = require('../config.json');

module.exports = sequlize_cli;
</code></pre>

<p><code>config.json</code></p>

<pre><code>{
    "sequlize_cli":{
        "development":{
            "username":"root",
            "password":"passowrd",
            "database":"monitor",
            "host":"127.0.0.1",
            "dialect": "postgres"
        },
        "test": {
            "username":"root",
            "password":"passowrd",
            "database":"monitor",
            "host":"127.0.0.1",
            "dialect": "postgres"
          },
          "production": {
            "username":"root",
            "password":"passowrd",
            "database":"monitor",
            "host":"127.0.0.1",
            "dialect": "postgres"
          }
    }
}
</code></pre>

<p>the main point i guess is to export the json object directly instead of exporting a <code>sequelize</code> object. In addition, this is only the problem with <code>postges</code> , i tested with mysql, your code works perfectly with mysql.</p>

