# php mysqli persistent connection not being shared in App Engine
[Link to question](https://stackoverflow.com/questions/52886612/php-mysqli-persistent-connection-not-being-shared-in-app-engine)
**Creation Date:** 1539928688
**Score:** 1
**Tags:** php, google-app-engine, mysqli, google-cloud-sql, persistent-connection
## Question Body
<p>We have an application written in php using mysqli running on Google App Engine and connecting to Google Cloud SQL. We have a file connection.php that instantiate </p>

<p><code>$connection = new mysqli(...);</code> </p>

<p>and this script is included in all the scripts that needs to connect to database.</p>

<p>We have been getting more and more traffic and we started to see problems with queries queuing up very badly causing MySQL has gone away errors. We realized the problem was because we created a new Active Connection for each request coming in, which was crazy. We do realize that we need to use connection pooling but at this point of time we do not have the time to rewrite the whole thing. So we want to use php mysqli persistent connection until we are able to rewrite the application into Java or something that can use connection pooling.</p>

<p>Theoretically, with persistent connection implemented, we should be getting as much Active Connections in Cloud SQL as Instances in App Engine (with documents saying one persistent connection is shared within one process). This is how to use persistent connection :</p>

<pre><code>$connection = new mysqli('p:localhost',...)
</code></pre>

<p>In our php.ini :</p>

<pre><code>mysqli.allow_persistent = "1"
mysqli.max_persistent = "-1"
mysqli.max_links = "-1"
</code></pre>

<p>However, we see that each time a new request comes in, one new Active Connection is still created in Cloud SQL. Even worse, these connections are not closed and queries are queuing up faster. We see 8 instances with 40 Active Connections at times.</p>

<p>My question is are we missing something when implementing persistent connections? Why is it not working the way we anticipated? Thanks in advance!</p>

## Answers
### Answer ID: 52906324
<p>You have to make sure your connection.php is a Singleton. If not, each time a connection to the DB is made, a new mysqli connection will be created with params defined in the php.ini.</p>

