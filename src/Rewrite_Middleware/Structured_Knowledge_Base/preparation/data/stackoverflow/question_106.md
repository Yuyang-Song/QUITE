# Trying to use connection pooling outside servlet engine
[Link to question](https://stackoverflow.com/questions/13018780/trying-to-use-connection-pooling-outside-servlet-engine)
**Creation Date:** 1350935624
**Score:** 0
**Tags:** java, tomcat, jdbc, connection-pooling
## Question Body
<p>I've a series of methods running within a servlet engine (Tomcat in this case), using connection pooling to access the database written in this way:</p>
<pre><code>// Gets an RSS_Feed.
public static RSS_Feed get(int rssFeedNo) {
    ConnectionPool_DB pool = ConnectionPool_DB.getInstance();
    Connection connection = pool.getConnection();
    PreparedStatement ps = null;
    ResultSet rs = null;

    String query = (&quot;SELECT * &quot; +
                    &quot;FROM RSS_Feed &quot; +
                    &quot;WHERE RSSFeedNo = ?;&quot;);

    try {
        ps = connection.prepareStatement(query);
        ps.setInt(1, rssFeedNo);
        rs = ps.executeQuery();
        if (rs.next()) {
            return mapRSSFeed(rs);
        }
        else {
            return null;
        }
    }
    catch(Exception ex) {
        logger.error(&quot;Error getting RSS_Feed &quot; + rssFeedNo + &quot;\n&quot;, ex);
        return null;
    }
    finally {
        Database_Utils.closeResultSet(rs);
        Database_Utils.closeStatement(ps);
        pool.freeConnection(connection);
    }
}
</code></pre>
<p>Is it possible to call such a method outside of the servlet engine at all? I would like to do this in a batch process executed from the command line instead of within the servlet engine. I know I could simply rewrite the query without connection pooling but this is one of many queries involved in the process.</p>
<p>The connection pooling is implemented via Apache Common DBCP.</p>
<p><strong><code>ConnectionPool_DB.getInstance();</code> reads:</strong></p>
<pre><code>private ConnectionPool_DB() {
    try {
        InitialContext ic = new InitialContext();
        dataSource = (DataSource) ic.lookup(PropertiesFile.getProperty(&quot;myApp&quot;, &quot;DATASOURCE&quot;));
        // dataSource = (DataSource) ic.lookup(&quot;java:/comp/env/jdbc/myApp&quot;);
    }
    catch(Exception ex) {
        logger.error(&quot;Error getting a connection pool's datasource\n&quot;, ex);
    }
}
</code></pre>

## Answers
### Answer ID: 13018885
<p>I have something like this in a project: </p>

<pre><code>Context ctx = new InitialContext(); 
DataSource ds = (DataSource) ctx.lookup("DbConnection");
ConnectionPool connectionPool = new ConnectionPool(ds)
</code></pre>

<p>And inside context xml I define the resouce like this</p>

<pre><code>&lt;Resource name="DbConnection" 
auth="SERVLET" 
type="javax.sql.DataSource"  
scope="Shareable"            
driverClassName="**driverClassName**" 
url="**url**" 
username="**username**" 
password="**password**" 
maxActive="10" 
maxIdle="10" 
maxWait="1000"
/&gt;
</code></pre>

<p>So I assume you have something similar
If so you need to write code to create the DataSource yourself.</p>

<p>This should help you with that
<a href="http://docs.oracle.com/javase/tutorial/jdbc/basics/sqldatasources.html" rel="nofollow">http://docs.oracle.com/javase/tutorial/jdbc/basics/sqldatasources.html</a></p>

### Answer ID: 13018959
<p>Do you mean that you want to share a connection pool between your servlet engine and a batch job? Or that you want to use connection pooling within a batch job?</p>

<p>As to sharing a pool between Tomcat and a batch job: Hmm, I don't see how you'd do it. Tomcat and the batch job would each have their own instance of the Java Virtual Machine. They're not sharing memory, classes, etc, so I don't know where such a common pool would live.</p>

<p>If you mean within a batch job: Sure. I think such a thing is rarely necessary. In batch jobs I normally open a connection at the start of the program and close it at the end. There's not much value to creating a connection pool. Desktop apps are a little trickier. I often create a connection when the app starts and close it when they exit, but arguably this ties up a connection when the user is just staring blindly at the screen (like I often do for the hour or so before lunch), so other times I open a connection every time the user clicks a key that causes something to happen, then release it before going back to "wait" mode. Again, there's little point pooling because in a desktop app, there are no other users to share the pool with.</p>

<p>But can it be done? Sure. I've done it in desktop apps where many things could happen at various times and so it was awkward to pass a single connection around.</p>

