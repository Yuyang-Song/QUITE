# MySql .NET connector usage in heavy load C# netcore async process
[Link to question](https://stackoverflow.com/questions/58516993/mysql-net-connector-usage-in-heavy-load-c-netcore-async-process)
**Creation Date:** 1571813450
**Score:** 0
**Tags:** c#, .net-core, async-await, mysql-connector
## Question Body
<p>MySql .NET connector usage in heavy load async process</p>

<p>I am rewriting from scratch a C# .NET Core multithreaded tcp server (for a IoT project) which is serving across multiple nodes >5k long lived tcp client connections per node, migrating to an async version of it (I expect to get at least 10k connections per node using async patterns without noticeable load on the cpu).</p>

<p>Each connection needs to read/write from a MySQL database on a regular basis (at minimum 1 write every 3 minutes when idle, much more when there is activity).</p>

<p>So far I've been using the .NET Connector connection pooling feature, and I declared a <code>[ThreadStatic]</code> static Connection object, which ensures that each thread is given a different thread-safe connection.</p>

<p>I acquire the connection from the connector's pool and put it into the thread-static Connection instance, then I release it as soon as I can.</p>

<p>By using an additional spin count mechanism, I avoid to acquire/release the instance if I need to run multiple sql statements in nested function calls.</p>

<p>Unfortunately this method, apart from the obvious not-so-good performance (to say the least) of the multithreaded approach, tends to keep in the pool an increasing number of open and idle connections.</p>

<p>With 5k tcp connections on a single node, the sql query execution rate per second on that node is about at 50 q/s, which is not a huge value per se, but keeps all connections in the pool "live" thus preventing the connector pool manager to actually release idle connections in its background thread (approximately 1000 connections per node).</p>

<p>Now the real question.</p>

<p>It is unclear to me how to deal with this situation in an async environment.
I've been using also the alternative MySqlConnector which claims to be truly async, but still my doubts remain.</p>

<p>How should I replace the <code>[ThreadStatic]</code> instance if I switch to async/await pattern?</p>

<p>How can I make sure that each async context flow is using its own Connection instance in a thread-safe fashion (especially considering that no other statements can run over a connection until all its cursors have been closed)?</p>

<p>How can I have parallel queries running when needed?</p>

<p>How can I deal with the connector pool manager?</p>

<p>I am really confused at this.</p>

<p>I've read about <code>AsyncLocal&lt;&gt;</code> class but I could not make much out of it. Is this the right path to follow?</p>

