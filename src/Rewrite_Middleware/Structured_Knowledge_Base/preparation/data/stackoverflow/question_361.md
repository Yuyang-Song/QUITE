# Eclipse giving me XML junk in console instead of running program
[Link to question](https://stackoverflow.com/questions/22626920/eclipse-giving-me-xml-junk-in-console-instead-of-running-program)
**Creation Date:** 1395728849
**Score:** 1
**Tags:** java, eclipse
## Question Body
<p>Note: I am running Eclipse ADT Build: v22.2.1-833290</p>

<p>Example:  I have the java code:</p>

<p>File: HelloWorld.java</p>

<pre><code>public class HelloWorld
{
    public static void main(String[] args)
    {
        System.out.println("Hello World!");
    }
}
</code></pre>

<p>Works just fine if a compile and run at the console.  However, when I run this file in Eclipse, I get the garbage shown below.  I trust computers enough to know that Eclipse is giving me exactly what I am asking it to give me, meaning that I've got some switch set somewhere.  The question is, how do I get Eclipse to stop giving me what I asked for and actually give me what I want?</p>

<p><em><strong>Update</em></strong>
I was using the "Run" button on the toolbar, as per usual, but I found that if I used the context menu Run As --> Java Application, it would run fine, and then run fine after that with just the button.  I must have something messed up about the default run configuration. Is there a way to set that properly?  Really, just a small annoyance at this point.</p>

<pre><code>&lt;ConnectionProperties&gt;
 &lt;PropertyCategory name="Connection/Authentication"&gt;
  &lt;Property name="user" required="No" default="" sortOrder="-2147483647" since="all versions"&gt;
    The user to connect as
  &lt;/Property&gt;
  &lt;Property name="password" required="No" default="" sortOrder="-2147483646" since="all versions"&gt;
    The password to use when connecting
  &lt;/Property&gt;
  &lt;Property name="socketFactory" required="No" default="com.mysql.jdbc.StandardSocketFactory" sortOrder="4" since="3.0.3"&gt;
    The name of the class that the driver should use for creating socket connections to the server. This class must implement the interface 'com.mysql.jdbc.SocketFactory' and have public no-args constructor.
  &lt;/Property&gt;
  &lt;Property name="connectTimeout" required="No" default="0" sortOrder="9" since="3.0.1"&gt;
    Timeout for socket connect (in milliseconds), with 0 being no timeout. Only works on JDK-1.4 or newer. Defaults to '0'.
  &lt;/Property&gt;
  &lt;Property name="socketTimeout" required="No" default="0" sortOrder="10" since="3.0.1"&gt;
    Timeout on network socket operations (0, the default means no timeout).
  &lt;/Property&gt;
  &lt;Property name="connectionLifecycleInterceptors" required="No" default="" sortOrder="2147483647" since="5.1.4"&gt;
    A comma-delimited list of classes that implement "com.mysql.jdbc.ConnectionLifecycleInterceptor" that should notified of connection lifecycle events (creation, destruction, commit, rollback, setCatalog and setAutoCommit) and potentially alter the execution of these commands. ConnectionLifecycleInterceptors are "stackable", more than one interceptor may be specified via the configuration property as a comma-delimited list, with the interceptors executed in order from left to right.
  &lt;/Property&gt;
  &lt;Property name="useConfigs" required="No" default="" sortOrder="2147483647" since="3.1.5"&gt;
    Load the comma-delimited list of configuration properties before parsing the URL or applying user-specified properties. These configurations are explained in the 'Configurations' of the documentation.
  &lt;/Property&gt;
  &lt;Property name="authenticationPlugins" required="No" default="" sortOrder="alpha" since="5.1.19"&gt;
    Comma-delimited list of classes that implement com.mysql.jdbc.AuthenticationPlugin and which will be used for authentication unless disabled by "disabledAuthenticationPlugins" property.
  &lt;/Property&gt;
  &lt;Property name="defaultAuthenticationPlugin" required="No" default="com.mysql.jdbc.authentication.MysqlNativePasswordPlugin" sortOrder="alpha" since="5.1.19"&gt;
    Name of a class implementing com.mysql.jdbc.AuthenticationPlugin which will be used as the default authentication plugin (see below). It is an error to use a class which is not listed in "authenticationPlugins" nor it is one of the built-in plugins. It is an error to set as default a plugin which was disabled with "disabledAuthenticationPlugins" property. It is an error to set this value to null or the empty string (i.e. there must be at least a valid default authentication plugin specified for the connection, meeting all constraints listed above).
  &lt;/Property&gt;
  &lt;Property name="disabledAuthenticationPlugins" required="No" default="" sortOrder="alpha" since="5.1.19"&gt;
    Comma-delimited list of classes implementing com.mysql.jdbc.AuthenticationPlugin or mechanisms, i.e. "mysql_native_password". The authentication plugins or mechanisms listed will not be used for authentication which will fail if it requires one of them. It is an error to disable the default authentication plugin (either the one named by "defaultAuthenticationPlugin" property or the hard-coded one if "defaultAuthenticationPlugin" property is not set).
  &lt;/Property&gt;
  &lt;Property name="disconnectOnExpiredPasswords" required="No" default="true" sortOrder="alpha" since="5.1.23"&gt;
    If "disconnectOnExpiredPasswords" is set to "false" and password is expired then server enters "sandbox" mode and sends ERR(08001, ER_MUST_CHANGE_PASSWORD) for all commands that are not needed to set a new password until a new password is set.
  &lt;/Property&gt;
  &lt;Property name="interactiveClient" required="No" default="false" sortOrder="alpha" since="3.1.0"&gt;
    Set the CLIENT_INTERACTIVE flag, which tells MySQL to timeout connections based on INTERACTIVE_TIMEOUT instead of WAIT_TIMEOUT
  &lt;/Property&gt;
  &lt;Property name="localSocketAddress" required="No" default="" sortOrder="alpha" since="5.0.5"&gt;
    Hostname or IP address given to explicitly configure the interface that the driver will bind the client side of the TCP/IP connection to when connecting.
  &lt;/Property&gt;
  &lt;Property name="propertiesTransform" required="No" default="" sortOrder="alpha" since="3.1.4"&gt;
    An implementation of com.mysql.jdbc.ConnectionPropertiesTransform that the driver will use to modify URL properties passed to the driver before attempting a connection
  &lt;/Property&gt;
  &lt;Property name="useCompression" required="No" default="false" sortOrder="alpha" since="3.0.17"&gt;
    Use zlib compression when communicating with the server (true/false)? Defaults to 'false'.
  &lt;/Property&gt;
 &lt;/PropertyCategory&gt;
 &lt;PropertyCategory name="Networking"&gt;
  &lt;Property name="maxAllowedPacket" required="No" default="-1" sortOrder="alpha" since="5.1.8"&gt;
    Maximum allowed packet size to send to server. If not set, the value of system variable 'max_allowed_packet' will be used to initialize this upon connecting. This value will not take effect if set larger than the value of 'max_allowed_packet'. Also, due to an internal dependency with the property "blobSendChunkSize", this setting has a minimum value of "8203" if "useServerPrepStmts" is set to "true".
  &lt;/Property&gt;
  &lt;Property name="tcpKeepAlive" required="No" default="true" sortOrder="alpha" since="5.0.7"&gt;
    If connecting using TCP/IP, should the driver set SO_KEEPALIVE?
  &lt;/Property&gt;
  &lt;Property name="tcpNoDelay" required="No" default="true" sortOrder="alpha" since="5.0.7"&gt;
    If connecting using TCP/IP, should the driver set SO_TCP_NODELAY (disabling the Nagle Algorithm)?
  &lt;/Property&gt;
  &lt;Property name="tcpRcvBuf" required="No" default="0" sortOrder="alpha" since="5.0.7"&gt;
    If connecting using TCP/IP, should the driver set SO_RCV_BUF to the given value? The default value of '0', means use the platform default value for this property)
  &lt;/Property&gt;
  &lt;Property name="tcpSndBuf" required="No" default="0" sortOrder="alpha" since="5.0.7"&gt;
    If connecting using TCP/IP, should the driver set SO_SND_BUF to the given value? The default value of '0', means use the platform default value for this property)
  &lt;/Property&gt;
  &lt;Property name="tcpTrafficClass" required="No" default="0" sortOrder="alpha" since="5.0.7"&gt;
    If connecting using TCP/IP, should the driver set traffic class or type-of-service fields ?See the documentation for java.net.Socket.setTrafficClass() for more information.
  &lt;/Property&gt;
 &lt;/PropertyCategory&gt;
 &lt;PropertyCategory name="High Availability and Clustering"&gt;
  &lt;Property name="autoReconnect" required="No" default="false" sortOrder="0" since="1.1"&gt;
    Should the driver try to re-establish stale and/or dead connections? If enabled the driver will throw an exception for a queries issued on a stale or dead connection, which belong to the current transaction, but will attempt reconnect before the next query issued on the connection in a new transaction. The use of this feature is not recommended, because it has side effects related to session state and data consistency when applications don't handle SQLExceptions properly, and is only designed to be used when you are unable to configure your application to handle SQLExceptions resulting from dead and stale connections properly. Alternatively, as a last option, investigate setting the MySQL server variable "wait_timeout" to a high value, rather than the default of 8 hours.
  &lt;/Property&gt;
  &lt;Property name="autoReconnectForPools" required="No" default="false" sortOrder="1" since="3.1.3"&gt;
    Use a reconnection strategy appropriate for connection pools (defaults to 'false')
  &lt;/Property&gt;
  &lt;Property name="failOverReadOnly" required="No" default="true" sortOrder="2" since="3.0.12"&gt;
    When failing over in autoReconnect mode, should the connection be set to 'read-only'?
  &lt;/Property&gt;
  &lt;Property name="maxReconnects" required="No" default="3" sortOrder="4" since="1.1"&gt;
    Maximum number of reconnects to attempt if autoReconnect is true, default is '3'.
  &lt;/Property&gt;
  &lt;Property name="reconnectAtTxEnd" required="No" default="false" sortOrder="4" since="3.0.10"&gt;
    If autoReconnect is set to true, should the driver attempt reconnections at the end of every transaction?
  &lt;/Property&gt;
  &lt;Property name="retriesAllDown" required="No" default="120" sortOrder="4" since="5.1.6"&gt;
    When using loadbalancing, the number of times the driver should cycle through available hosts, attempting to connect.  Between cycles, the driver will pause for 250ms if no servers are available.
  &lt;/Property&gt;
  &lt;Property name="initialTimeout" required="No" default="2" sortOrder="5" since="1.1"&gt;
    If autoReconnect is enabled, the initial time to wait between re-connect attempts (in seconds, defaults to '2').
  &lt;/Property&gt;
  &lt;Property name="roundRobinLoadBalance" required="No" default="false" sortOrder="5" since="3.1.2"&gt;
    When autoReconnect is enabled, and failoverReadonly is false, should we pick hosts to connect to on a round-robin basis?
  &lt;/Property&gt;
  &lt;Property name="queriesBeforeRetryMaster" required="No" default="50" sortOrder="7" since="3.0.2"&gt;
    Number of queries to issue before falling back to master when failed over (when using multi-host failover). Whichever condition is met first, 'queriesBeforeRetryMaster' or 'secondsBeforeRetryMaster' will cause an attempt to be made to reconnect to the master. Defaults to 50.
  &lt;/Property&gt;
  &lt;Property name="secondsBeforeRetryMaster" required="No" default="30" sortOrder="8" since="3.0.2"&gt;
    How long should the driver wait, when failed over, before attempting 
  &lt;/Property&gt;
  &lt;Property name="allowMasterDownConnections" required="No" default="false" sortOrder="2147483647" since="5.1.27"&gt;
    Should replication-aware driver establish connections to slaves when connection to master servers cannot be established at initial connection?  Defaults to 'false', which will cause SQLException when configured master hosts are all unavailable when establishing a new replication-aware Connection.
  &lt;/Property&gt;
  &lt;Property name="replicationEnableJMX" required="No" default="false" sortOrder="2147483647" since="5.1.27"&gt;
    Enables JMX-based management of load-balanced connection groups, including live addition/removal of hosts from load-balancing pool.
  &lt;/Property&gt;
  &lt;Property name="selfDestructOnPingMaxOperations" required="No" default="0" sortOrder="2147483647" since="5.1.6"&gt;
    =If set to a non-zero value, the driver will report close the connection and report failure when Connection.ping() or Connection.isValid(int) is called if the connection's count of commands sent to the server exceeds this value.
  &lt;/Property&gt;
  &lt;Property name="selfDestructOnPingSecondsLifetime" required="No" default="0" sortOrder="2147483647" since="5.1.6"&gt;
    If set to a non-zero value, the driver will report close the connection and report failure when Connection.ping() or Connection.isValid(int) is called if the connection's lifetime exceeds this value.
  &lt;/Property&gt;
  &lt;Property name="resourceId" required="No" default="" sortOrder="alpha" since="5.0.1"&gt;
    A globally unique name that identifies the resource that this datasource or connection is connected to, used for XAResource.isSameRM() when the driver can't determine this value based on hostnames used in the URL
  &lt;/Property&gt;
 &lt;/PropertyCategory&gt;
 &lt;PropertyCategory name="Security"&gt;
  &lt;Property name="allowMultiQueries" required="No" default="false" sortOrder="1" since="3.1.1"&gt;
    Allow the use of ';' to delimit multiple queries during one statement (true/false), defaults to 'false', and does not affect the addBatch() and executeBatch() methods, which instead rely on rewriteBatchStatements.
  &lt;/Property&gt;
  &lt;Property name="useSSL" required="No" default="false" sortOrder="2" since="3.0.2"&gt;
    Use SSL when communicating with the server (true/false), defaults to 'false'
  &lt;/Property&gt;
  &lt;Property name="requireSSL" required="No" default="false" sortOrder="3" since="3.1.0"&gt;
    Require SSL connection if useSSL=true? (defaults to 'false').
  &lt;/Property&gt;
  &lt;Property name="verifyServerCertificate" required="No" default="true" sortOrder="4" since="5.1.6"&gt;
    If "useSSL" is set to "true", should the driver verify the server's certificate? When using this feature, the keystore parameters should be specified by the "clientCertificateKeyStore*" properties, rather than system properties.
  &lt;/Property&gt;
  &lt;Property name="clientCertificateKeyStoreUrl" required="No" default="" sortOrder="5" since="5.1.0"&gt;
    URL to the client certificate KeyStore (if not specified, use defaults)
  &lt;/Property&gt;
  &lt;Property name="clientCertificateKeyStoreType" required="No" default="JKS" sortOrder="6" since="5.1.0"&gt;
    KeyStore type for client certificates (NULL or empty means use the default, which is "JKS". Standard keystore types supported by the JVM are "JKS" and "PKCS12", your environment may have more available depending on what security products are installed and available to the JVM.
  &lt;/Property&gt;
  &lt;Property name="clientCertificateKeyStorePassword" required="No" default="" sortOrder="7" since="5.1.0"&gt;
    Password for the client certificates KeyStore
  &lt;/Property&gt;
  &lt;Property name="trustCertificateKeyStoreUrl" required="No" default="" sortOrder="8" since="5.1.0"&gt;
    URL to the trusted root certificate KeyStore (if not specified, use defaults)
  &lt;/Property&gt;
  &lt;Property name="trustCertificateKeyStoreType" required="No" default="JKS" sortOrder="9" since="5.1.0"&gt;
    KeyStore type for trusted root certificates (NULL or empty means use the default, which is "JKS". Standard keystore types supported by the JVM are "JKS" and "PKCS12", your environment may have more available depending on what security products are installed and available to the JVM.
  &lt;/Property&gt;
  &lt;Property name="trustCertificateKeyStorePassword" required="No" default="" sortOrder="10" since="5.1.0"&gt;
    Password for the trusted root certificates KeyStore
  &lt;/Property&gt;
  &lt;Property name="allowLoadLocalInfile" required="No" default="true" sortOrder="2147483647" since="3.0.3"&gt;
    Should the driver allow use of 'LOAD DATA LOCAL INFILE...' (defaults to 'true').
  &lt;/Property&gt;
  &lt;Property name="allowUrlInLocalInfile" required="No" default="false" sortOrder="2147483647" since="3.1.4"&gt;
    Should the driver allow URLs in 'LOAD DATA LOCAL INFILE' statements?
  &lt;/Property&gt;
  &lt;Property name="paranoid" required="No" default="false" sortOrder="alpha" since="3.0.1"&gt;
    Take measures to prevent exposure sensitive information in error messages and clear data structures holding sensitive data when possible? (defaults to 'false')
  &lt;/Property&gt;
  &lt;Property name="passwordCharacterEncoding" required="No" default="" sortOrder="alpha" since="5.1.7"&gt;
    What character encoding is used for passwords? Leaving this set to the default value (null), uses the platform character set, which works for ISO8859_1 (i.e. "latin1") passwords. For passwords in other character encodings, the encoding will have to be specified with this property, as it's not possible for the driver to auto-detect this.
  &lt;/Property&gt;
 &lt;/PropertyCategory&gt;
 &lt;PropertyCategory name="Performance Extensions"&gt;
  &lt;Property name="callableStmtCacheSize" required="No" default="100" sortOrder="5" since="3.1.2"&gt;
    If 'cacheCallableStmts' is enabled, how many callable statements should be cached?
  &lt;/Property&gt;
  &lt;Property name="metadataCacheSize" required="No" default="50" sortOrder="5" since="3.1.1"&gt;
    The number of queries to cache ResultSetMetadata for if cacheResultSetMetaData is set to 'true' (default 50)
  &lt;/Property&gt;
  &lt;Property name="useLocalSessionState" required="No" default="false" sortOrder="5" since="3.1.7"&gt;
    Should the driver refer to the internal values of autocommit and transaction isolation that are set by Connection.setAutoCommit() and Connection.setTransactionIsolation() and transaction state as maintained by the protocol, rather than querying the database or blindly sending commands to the database for commit() or rollback() method calls?
  &lt;/Property&gt;
  &lt;Property name="useLocalTransactionState" required="No" default="false" sortOrder="6" since="5.1.7"&gt;
    Should the driver use the in-transaction state provided by the MySQL protocol to determine if a commit() or rollback() should actually be sent to the database?
  &lt;/Property&gt;
  &lt;Property name="prepStmtCacheSize" required="No" default="25" sortOrder="10" since="3.0.10"&gt;
    If prepared statement caching is enabled, how many prepared statements should be cached?
  &lt;/Property&gt;
  &lt;Property name="prepStmtCacheSqlLimit" required="No" default="256" sortOrder="11" since="3.0.10"&gt;
    If prepared statement caching is enabled, what's the largest SQL the driver will cache the parsing for?
  &lt;/Property&gt;
  &lt;Property name="parseInfoCacheFactory" required="No" default="com.mysql.jdbc.PerConnectionLRUFactory" sortOrder="12" since="5.1.1"&gt;
    Name of a class implementing com.mysql.jdbc.CacheAdapterFactory, which will be used to create caches for the parsed representation of client-side prepared statements.
  &lt;/Property&gt;
  &lt;Property name="serverConfigCacheFactory" required="No" default="com.mysql.jdbc.PerVmServerConfigCacheFactory" sortOrder="12" since="5.1.1"&gt;
    Name of a class implementing com.mysql.jdbc.CacheAdapterFactory&amp;lt;String, Map&amp;lt;String, String&amp;gt;&amp;gt;, which will be used to create caches for MySQL server configuration values
  &lt;/Property&gt;
  &lt;Property name="alwaysSendSetIsolation" required="No" default="true" sortOrder="2147483647" since="3.1.7"&gt;
    Should the driver always communicate with the database when Connection.setTransactionIsolation() is called? If set to false, the driver will only communicate with the database when the requested transaction isolation is different than the whichever is newer, the last value that was set via Connection.setTransactionIsolation(), or the value that was read from the server when the connection was established.  Note that useLocalSessionState=true will force the same behavior as alwaysSendSetIsolation=false, regardless of how alwaysSendSetIsolation is set.
  &lt;/Property&gt;
  &lt;Property name="maintainTimeStats" required="No" default="true" sortOrder="2147483647" since="3.1.9"&gt;
    Should the driver maintain various internal timers to enable idle time calculations as well as more verbose error messages when the connection to the server fails? Setting this property to false removes at least two calls to System.getCurrentTimeMillis() per query.
  &lt;/Property&gt;
  &lt;Property name="useCursorFetch" required="No" default="false" sortOrder="2147483647" since="5.0.0"&gt;
    If connected to MySQL &amp;gt; 5.0.2, and setFetchSize() &amp;gt; 0 on a statement, should that statement use cursor-based fetching to retrieve rows?
  &lt;/Property&gt;
  &lt;Property name="blobSendChunkSize" required="No" default="1048576" sortOrder="alpha" since="3.1.9"&gt;
    Chunk size to use when sending BLOB/CLOBs via ServerPreparedStatements. Note that this value cannot exceed the value of "maxAllowedPacket" and, if that is the case, then this value will be corrected automatically.
  &lt;/Property&gt;
  &lt;Property name="cacheCallableStmts" required="No" default="false" sortOrder="alpha" since="3.1.2"&gt;
    Should the driver cache the parsing stage of CallableStatements
  &lt;/Property&gt;
  &lt;Property name="cachePrepStmts" required="No" default="false" sortOrder="alpha" since="3.0.10"&gt;
    Should the driver cache the parsing stage of PreparedStatements of client-side prepared statements, the "check" for suitability of server-side prepared and server-side prepared statements themselves?
  &lt;/Property&gt;
  &lt;Property name="cacheResultSetMetadata" required="No" default="false" sortOrder="alpha" since="3.1.1"&gt;
    Should the driver cache ResultSetMetaData for Statements and PreparedStatements? (Req. JDK-1.4+, true/false, default 'false')
  &lt;/Property&gt;
  &lt;Property name="cacheServerConfiguration" required="No" default="false" sortOrder="alpha" since="3.1.5"&gt;
    Should the driver cache the results of 'SHOW VARIABLES' and 'SHOW COLLATION' on a per-URL basis?
  &lt;/Property&gt;
  &lt;Property name="defaultFetchSize" required="No" default="0" sortOrder="alpha" since="3.1.9"&gt;
    The driver will call setFetchSize(n) with this value on all newly-created Statements
  &lt;/Property&gt;
  &lt;Property name="dontTrackOpenResources" required="No" default="false" sortOrder="alpha" since="3.1.7"&gt;
    The JDBC specification requires the driver to automatically track and close resources, however if your application doesn't do a good job of explicitly calling close() on statements or result sets, this can cause memory leakage. Setting this property to true relaxes this constraint, and can be more memory efficient for some applications. Also the automatic closing of the Statement and current ResultSet in Statement.closeOnCompletion() and Statement.getMoreResults ([Statement.CLOSE_CURRENT_RESULT | Statement.CLOSE_ALL_RESULTS]), respectively, ceases to happen. This property automatically sets holdResultsOpenOverStatementClose=true.
  &lt;/Property&gt;
  &lt;Property name="dynamicCalendars" required="No" default="false" sortOrder="alpha" since="3.1.5"&gt;
    Should the driver retrieve the default calendar when required, or cache it per connection/session?
  &lt;/Property&gt;
  &lt;Property name="elideSetAutoCommits" required="No" default="false" sortOrder="alpha" since="3.1.3"&gt;
    If using MySQL-4.1 or newer, should the driver only issue 'set autocommit=n' queries when the server's state doesn't match the requested state by Connection.setAutoCommit(boolean)?
  &lt;/Property&gt;
  &lt;Property name="enableQueryTimeouts" required="No" default="true" sortOrder="alpha" since="5.0.6"&gt;
    When enabled, query timeouts set via Statement.setQueryTimeout() use a shared java.util.Timer instance for scheduling. Even if the timeout doesn't expire before the query is processed, there will be memory used by the TimerTask for the given timeout which won't be reclaimed until the time the timeout would have expired if it hadn't been cancelled by the driver. High-load environments might want to consider disabling this functionality.
  &lt;/Property&gt;
  &lt;Property name="holdResultsOpenOverStatementClose" required="No" default="false" sortOrder="alpha" since="3.1.7"&gt;
    Should the driver close result sets on Statement.close() as required by the JDBC specification?
  &lt;/Property&gt;
  &lt;Property name="largeRowSizeThreshold" required="No" default="2048" sortOrder="alpha" since="5.1.1"&gt;
    What size result set row should the JDBC driver consider "large", and thus use a more memory-efficient way of representing the row internally?
  &lt;/Property&gt;
  &lt;Property name="loadBalanceStrategy" required="No" default="random" sortOrder="alpha" since="5.0.6"&gt;
    If using a load-balanced connection to connect to SQL nodes in a MySQL Cluster/NDB configuration (by using the URL prefix "jdbc:mysql:loadbalance://"), which load balancing algorithm should the driver use: (1) "random" - the driver will pick a random host for each request. This tends to work better than round-robin, as the randomness will somewhat account for spreading loads where requests vary in response time, while round-robin can sometimes lead to overloaded nodes if there are variations in response times across the workload. (2) "bestResponseTime" - the driver will route the request to the host that had the best response time for the previous transaction.
  &lt;/Property&gt;
  &lt;Property name="locatorFetchBufferSize" required="No" default="1048576" sortOrder="alpha" since="3.2.1"&gt;
    If 'emulateLocators' is configured to 'true', what size buffer should be used when fetching BLOB data for getBinaryInputStream?
  &lt;/Property&gt;
  &lt;Property name="rewriteBatchedStatements" required="No" default="false" sortOrder="alpha" since="3.1.13"&gt;
    Should the driver use multiqueries (irregardless of the setting of "allowMultiQueries") as well as rewriting of prepared statements for INSERT into multi-value inserts when executeBatch() is called? Notice that this has the potential for SQL injection if using plain java.sql.Statements and your code doesn't sanitize input correctly. Notice that for prepared statements, server-side prepared statements can not currently take advantage of this rewrite option, and that if you don't specify stream lengths when using PreparedStatement.set*Stream(), the driver won't be able to determine the optimum number of parameters per batch and you might receive an error from the driver that the resultant packet is too large. Statement.getGeneratedKeys() for these rewritten statements only works when the entire batch includes INSERT statements. Please be aware using rewriteBatchedStatements=true with INSERT .. ON DUPLICATE KEY UPDATE that for rewritten statement server returns only one value as sum of all affected (or found) rows in batch and it isn't possible to map it correctly to initial statements; in this case driver returns the total result as a result of each batch statement, i.e. the only unambiguous result is 0.
  &lt;/Property&gt;
  &lt;Property name="useDirectRowUnpack" required="No" default="true" sortOrder="alpha" since="5.1.1"&gt;
    Use newer result set row unpacking code that skips a copy from network buffers  to a MySQL packet instance and instead reads directly into the result set row data buffers.
  &lt;/Property&gt;
  &lt;Property name="useDynamicCharsetInfo" required="No" default="true" sortOrder="alpha" since="5.0.6"&gt;
    Should the driver use a per-connection cache of character set information queried from the server when necessary, or use a built-in static mapping that is more efficient, but isn't aware of custom character sets or character sets implemented after the release of the JDBC driver?
  &lt;/Property&gt;
  &lt;Property name="useFastDateParsing" required="No" default="true" sortOrder="alpha" since="5.0.5"&gt;
    Use internal String-&gt;Date/Time/Timestamp conversion routines to avoid excessive object creation?
  &lt;/Property&gt;
  &lt;Property name="useFastIntParsing" required="No" default="true" sortOrder="alpha" since="3.1.4"&gt;
    Use internal String-&gt;Integer conversion routines to avoid excessive object creation?
  &lt;/Property&gt;
  &lt;Property name="useJvmCharsetConverters" required="No" default="false" sortOrder="alpha" since="5.0.1"&gt;
    Always use the character encoding routines built into the JVM, rather than using lookup tables for single-byte character sets?
  &lt;/Property&gt;
  &lt;Property name="useReadAheadInput" required="No" default="true" sortOrder="alpha" since="3.1.5"&gt;
    Use newer, optimized non-blocking, buffered input stream when reading from the server?
  &lt;/Property&gt;
 &lt;/PropertyCategory&gt;
 &lt;PropertyCategory name="Debugging/Profiling"&gt;
  &lt;Property name="logger" required="No" default="com.mysql.jdbc.log.StandardLogger" sortOrder="0" since="3.1.1"&gt;
    The name of a class that implements "com.mysql.jdbc.log.Log"  that will be used to log messages to. (default is "com.mysql.jdbc.log.StandardLogger", which logs to STDERR)
  &lt;/Property&gt;
  &lt;Property name="gatherPerfMetrics" required="No" default="false" sortOrder="1" since="3.1.2"&gt;
    Should the driver gather performance metrics, and report them via the configured logger every 'reportMetricsIntervalMillis' milliseconds?
  &lt;/Property&gt;
</code></pre>

<p>etc. etc. etc. </p>

## Answers
### Answer ID: 22644154
<p>Expanding on my comment.</p>

<p>Since you have MySQL jars in <code>lib\ext</code> looks like Eclipse is trying to load up these jars .
Try removing these jars and try running your program again. Putting jars in <code>lib\ext</code> is considered a bad <a href="https://stackoverflow.com/questions/2068961/is-putting-external-jars-in-the-java-home-lib-ext-directory-a-bad-thing">practice</a>.</p>

<p>Related thread on MySQL - <a href="https://stackoverflow.com/questions/12220161/issue-accessing-mysql-from-java">here</a></p>

