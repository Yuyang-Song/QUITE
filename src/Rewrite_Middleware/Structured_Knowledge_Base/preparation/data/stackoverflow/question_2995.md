# CassandraDataSource JDBC as a datasource
[Link to question](https://stackoverflow.com/questions/61560440/cassandradatasource-jdbc-as-a-datasource)
**Creation Date:** 1588427422
**Score:** 1
**Tags:** java, database, jdbc, cassandra
## Question Body
<p>I've used the Apache DBUtils library in my Java application, initially written in MySQL.  I'm looking at changing the database to Cassandra.  The only way I can run queries on it is to use a basic data source.</p>

<p>I've got the Datagrip fork  of the DBSchema library, available here:
<a href="https://dbschema.com/jdbc-driver/Cassandra.html" rel="nofollow noreferrer">https://dbschema.com/jdbc-driver/Cassandra.html</a></p>

<p>I've tried "twig", a cassandra JDBC driver but it's nowhere near complete.</p>

<p>I can't use the datastax driver as (AFAIK) it doesn't support data sources.
If I can't resolve this it's a full rewrite.</p>

<p>Here's my code, where am I going wrong?</p>

<pre><code>
import com.github.cassandra.jdbc.CassandraDriver;
import org.apache.commons.dbcp2.BasicDataSource;

import javax.sql.DataSource;

public class CustomDataSource {

CassandraDriver    cs = new CassandraDriver();


    final String DB_URL = "jdbc:cassandra://localhost:9160/queuie";
    final String JDBC_DRIVER = "com.github.cassandra.jdbcx.CassandraDataSource";

   private final BasicDataSource basicDataSource;
</code></pre>

<p>The error message I'm getting is: </p>

<pre><code>java.sql.SQLException: 
Cannot load JDBC driver class 'com.github.cassandra.jdbcx.CassandraDriver' 
at org.apache.commons.dbcp2.DriverFactory.createDriver(DriverFactory.java:54)
at org.apache.commons.dbcp2.BasicDataSource.createConnectionFactory(BasicDataSource.java:472)
at org.apache.commons.dbcp2.BasicDataSource.createDataSource(BasicDataSource.java:538)
at org.apache.commons.dbcp2.BasicDataSource.getConnection(BasicDataSource.java:753)
at org.apache.commons.dbutils.AbstractQueryRunner.prepareConnection(AbstractQueryRunner.java:319)
at org.apache.commons.dbutils.QueryRunner.query(QueryRunner.java:327)
at DoLogin.doPost(DoLogin.java:534)
at javax.servlet.http.HttpServlet.service(HttpServlet.java:660)
at javax.servlet.http.HttpServlet.service(HttpServlet.java:741)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:200)
at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:96)
at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:490)
at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:139)
at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
at org.apache.catalina.valves.AbstractAccessLogValve.invoke(AbstractAccessLogValve.java:668)
at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74)
at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:408)
at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:66)
at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:834)
at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1415)
at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
at java.base/java.lang.Thread.run(Thread.java:834) Caused by: java.lang.ClassNotFoundException: com.github.cassandra.jdbcx.CassandraDriver
at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1363)
at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1186)
at org.apache.commons.dbcp2.DriverFactory.createDriver(DriverFactory.java:49) ... 33 more java.sql.SQLException: Cannot load JDBC driver class 'com.github.cassandra.jdbcx.CassandraDriver'
at org.apache.commons.dbcp2.DriverFactory.createDriver(DriverFactory.java:54)
at org.apache.commons.dbcp2.BasicDataSource.createConnectionFactory(BasicDataSource.java:472)
at org.apache.commons.dbcp2.BasicDataSource.createDataSource(BasicDataSource.java:538)
at org.apache.commons.dbcp2.BasicDataSource.getConnection(BasicDataSource.java:753)
at org.apache.commons.dbutils.AbstractQueryRunner.prepareConnection(AbstractQueryRunner.java:319)
at org.apache.commons.dbutils.QueryRunner.query(QueryRunner.java:327)
at DoLogin.doPost(DoLogin.java:534)
at javax.servlet.http.HttpServlet.service(HttpServlet.java:660)
at javax.servlet.http.HttpServlet.service(HttpServlet.java:741)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.logging.log4j.web.Log4jServletFilter.doFilter(Log4jServletFilter.java:71)
at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:200)
at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:96)
at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:490)
at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:139)
at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
at org.apache.catalina.valves.AbstractAccessLogValve.invoke(AbstractAccessLogValve.java:668)
at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74)
at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:408)
at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:66)
at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:834)
at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1415)
at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
at java.base/java.lang.Thread.run(Thread.java:834) Caused by: java.lang.ClassNotFoundException: com.github.cassandra.jdbcx.CassandraDriver
at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1363)
at org.apache.catalina.loader.WebappClassLoaderBase.loadClass(WebappClassLoaderBase.java:1186)
at org.apache.commons.dbcp2.DriverFactory.createDriver(DriverFactory.java:49) ... 33 more

</code></pre>

<p>EDIT: I just realised I'm not resolving the com.dbschema package,  It's installed as a local file by Maven using mvn install, any ideas?</p>

