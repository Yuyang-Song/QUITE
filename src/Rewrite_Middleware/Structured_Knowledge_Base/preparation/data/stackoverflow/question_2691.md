# Using MongoDB Atlas in Vertx
[Link to question](https://stackoverflow.com/questions/47768675/using-mongodb-atlas-in-vertx)
**Creation Date:** 1513069310
**Score:** 1
**Tags:** mongodb, vert.x, mongodb-atlas
## Question Body
<p>Has anyone tried to use MongoDB Atlas Database as a service (<a href="https://www.mongodb.com" rel="nofollow noreferrer">https://www.mongodb.com</a>) with Vertx?</p>

<p>I've tried to connect but I keep getting the following error:</p>

<pre><code>INFO: Exception in monitor thread while connecting to server socie-shard-00-01-zeymc.mongodb.net:27017
com.mongodb.MongoSocketReadException: Prematurely reached end of stream
    at com.mongodb.connection.AsynchronousSocketChannelStream$BasicCompletionHandler.completed(AsynchronousSocketChannelStream.java:215)
    at com.mongodb.connection.AsynchronousSocketChannelStream$BasicCompletionHandler.completed(AsynchronousSocketChannelStream.java:201)
    at sun.nio.ch.Invoker.invokeUnchecked(Invoker.java:126)
    at sun.nio.ch.Invoker.invokeUnchecked(Invoker.java:281)
    at sun.nio.ch.WindowsAsynchronousSocketChannelImpl$ReadTask.completed(WindowsAsynchronousSocketChannelImpl.java:579)
    at sun.nio.ch.Iocp$EventHandlerTask.run(Iocp.java:397)
    at sun.nio.ch.AsynchronousChannelGroupImpl$1.run(AsynchronousChannelGroupImpl.java:112)
    at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
    at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
    at java.lang.Thread.run(Thread.java:745)
</code></pre>

<p>I used the following:</p>

<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;io.vertx&lt;/groupId&gt;
    &lt;artifactId&gt;vertx-mongo-client&lt;/artifactId&gt;
    &lt;version&gt;3.5.0&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>

<p>Than I tried to used their Java Mongo driver:</p>

<pre><code>&lt;dependency&gt;
    &lt;groupId&gt;org.mongodb&lt;/groupId&gt;
    &lt;artifactId&gt;mongo-java-driver&lt;/artifactId&gt;
    &lt;version&gt;3.6.0&lt;/version&gt;
&lt;/dependency&gt;
</code></pre>

<p>This works. Only this takes a big rewrite on all my queries. And I'm not sure if this is a good driver in combination with Vertx. </p>

<p>Does anyone know how to fix the error above or does anyone know if it's safe to use the org.mongodb java driver.</p>

<p>Many thanks in advance!</p>

<p><strong>My solution</strong></p>

<p>Thanks to Daniel, I managed to get it working with the vertx-mongo-client!</p>

<p>I added to my Json config</p>

<pre><code>config.put("ssl", true);
</code></pre>

<p>And I added the following line before creating the MongoClient.</p>

<pre><code>System.setProperty("org.mongodb.async.type", "netty");
</code></pre>

## Answers
### Answer ID: 47776719
<p>Had a similar problem a while ago, but got it working with the official vertx mongo client. I only had to be sure to provide all the connection info. 
Example:</p>

<pre><code>{
hosts: [
    {
        host: "xpto-shard-00-00-aaa.mongodb.net",
        port: 27017
    },
    {
        host: "xpto-shard-00-01-aaa.mongodb.net",
        port: 27017
    },
    {
        host: "xpto-shard-00-02-aaa.mongodb.net",
        port: 27017
    }
],
replicaSet: "xpto-shard-0",
db_name: "db_name",
username: "username",
password: "password",
ssl: true,
authSource: "admin",
maxPoolSize: 30,
minPoolSize: 5,
waitQueueMultiple : 100
</code></pre>

<p>}</p>

<p>Also, I had to be sure to set a system property:</p>

<pre><code>var System = Java.type("java.lang.System");
System.setProperty("org.mongodb.async.type", "netty");
</code></pre>

<p>(This verticle is in Javascript but it's pretty much the same in Java)</p>

