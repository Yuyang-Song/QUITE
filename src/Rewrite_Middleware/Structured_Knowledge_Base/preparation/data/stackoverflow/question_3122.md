# AWS proxy: RDS connection throttling while using sequelize in lambda
[Link to question](https://stackoverflow.com/questions/67470222/aws-proxy-rds-connection-throttling-while-using-sequelize-in-lambda)
**Creation Date:** 1620648762
**Score:** 2
**Tags:** aws-lambda, sequelize.js, amazon-rds, amazon-rds-proxy
## Question Body
<p>I am leveraging the use of AWS services for a functionality</p>
<p>Summary: I have a lambda that accesses a Postgres DB in RDS. Instead of directly connecting to DB, the proxy endpoint is accessed as it is architecturally advised. I have no problem generating IAM token and it is used as the password while creating the Sequelize connection.</p>
<p>Problem: Initially I was not using rds-proxy. In this scenario, I was making use of the execution context of lambda to reuse connections. Here I didn't close connections in lambda(It worked fine - was directly connecting to the database here). But on proxy implementation, without closing connections, there is a big spike in connections that proxy makes to the database and it is testing the limits on load. with 10req/sec I'm seeing 90 connections</p>
<p>On closing the connections in lambda the connections get substantially reduced to &lt;20.</p>
<p>But I have nested database queries during a single lambda execution and it will be difficult to rewrite these functionalities.</p>
<p>Below is the Sequelize connection object written to create connection</p>
<pre><code>const { Sequelize } = require('sequelize');
let proxyToken = '***latest iam token with 15min validity***';
let additionalConnectionDetails = {
host: process.env.PROXY_ENDPOINT,
schema: 'schemaname',
searchPath: 'searchpath',
dialect: 'postgres',
dialectOptions: {
    prependSearchPath: true,
    ssl: {
    require: true,
    rejectUnauthorized: false 
    }
},
// pool: {
//     max: 2,
//     min: 1,
//     acquire: 3000,
//     idle: 0,
//     evict: 120000
// },
// // maxConcurrentQueries: 100
}

sequelize_connection = new Sequelize(dbCreds.app, dbCreds.userName, proxyToken, additionalConnectionDetails);
console.log('sequelize', sequelize_connection)
return sequelize_connection
</code></pre>
<p>I tried using the connection pool, but it didn't make much of a difference in lambda.</p>
<p>How can I reduce the number of connections established without closing connections. Any suggestions are appreciated. Thanks in advance.</p>

