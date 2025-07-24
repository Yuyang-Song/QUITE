# How to configure C3p0.properties file in a jar file&#39;s classpath to read C3P0-config.xml outside the classpath
[Link to question](https://stackoverflow.com/questions/21736376/how-to-configure-c3p0-properties-file-in-a-jar-files-classpath-to-read-c3p0-con)
**Creation Date:** 1392229315
**Score:** 2
**Tags:** java, c3p0
## Question Body
<p>May be I have phrased the question wrongly but here's the issue. I have a library called util, inside util we have a database class that will be using C3P0 for database connectivity. This util library is used by different devs within the team . </p>

<p>To make life easier for everyone since we have a modular system, each module in the system can specify it's own database connection and properties as it sees fit for their module. The only reason we are doing this is because the methods for calling executing queries are all defined in this libraries and so instead of everyone rewriting the same code over and over it's much efficient to use a shared lib with that functionality.</p>

<p>The current set up is that I have the C3P0.properties file inside my util library classpath and inside it I have defined the path of the C3P0-config.xml file like this.</p>

<p>com.mchange.v2.c3p0.cfg.xml=./conf/c3p0-config.xml</p>

<p>I then build and the jar and give it to the rest of the devs . They then create a conf directory in their application and add the c3p0-config.xml.
The Strucuture of the Directory looks like this</p>

<pre><code>Parent directory - module name {

Sub directories

-lib  -&gt; {Util.jar &amp; other jars}

-conf -&gt; {c3p0-config.xml &amp; other config files}

-logs

-modulename.jar

}
</code></pre>

<p>On executing the jar file we get the error</p>

<pre><code>2014-02-12 20:50:59 INFO  MLog:124 - MLog clients using log4j logging.
2014-02-12 20:50:59 DEBUG MLog:101 - Could not find resource path text file for path '/com/mchange/v2/cfg/vmConfigResourcePaths.txt'. Skipping.
2014-02-12 20:50:59 DEBUG MLog:101 - Added paths from resource path text file at '/mchange-config-resource-paths.txt'
2014-02-12 20:50:59 DEBUG MLog:101 - Reading VM config for path list /com/mchange/v2/log/default-mchange-log.properties, /mchange-commons.properties, /c3p0.properties, hocon:/reference,/application,/c3p0,/, /mchange-log.properties, /
2014-02-12 20:50:59 DEBUG MLog:101 - The configuration file for resource identifier '/mchange-commons.properties' could not be found. Skipping.
java.io.FileNotFoundException: Resource not found at path '/mchange-commons.properties'.
    at com.mchange.v2.cfg.BasicPropertiesConfigSource.propertiesFromSource(BasicPropertiesConfigSource.java:64)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.firstInit(BasicMultiPropertiesConfig.java:185)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.&lt;init&gt;(BasicMultiPropertiesConfig.java:110)
    at com.mchange.v2.cfg.ConfigUtils.read(ConfigUtils.java:63)
    at com.mchange.v2.cfg.ConfigUtils.readVmConfig(ConfigUtils.java:115)
    at com.mchange.v2.cfg.MLogConfigSource.readVmConfig(MLogConfigSource.java:46)
    at com.mchange.v2.log.MLogConfig.refresh(MLogConfig.java:59)
    at com.mchange.v2.log.MLog.refreshConfig(MLog.java:59)
    at com.mchange.v2.log.MLog.&lt;clinit&gt;(MLog.java:51)
    at com.mchange.v2.naming.JavaBeanReferenceMaker.&lt;clinit&gt;(JavaBeanReferenceMaker.java:51)
    at com.mchange.v2.c3p0.impl.PoolBackedDataSourceBase.&lt;clinit&gt;(PoolBackedDataSourceBase.java:260)
    2014-02-12 20:50:59 DEBUG MLog:101 - The configuration file for resource identifier 'hocon:/reference,/application,/c3p0,/' could not be found. Skipping.
java.io.FileNotFoundException: HOCON lib (typesafe-config) is not available. Also, no resource available at '/reference,/application,/c3p0,/' for HOCON identifier 'hocon:/reference,/application,/c3p0,/'.
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.configSource(BasicMultiPropertiesConfig.java:86)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.firstInit(BasicMultiPropertiesConfig.java:184)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.&lt;init&gt;(BasicMultiPropertiesConfig.java:110)
    at com.mchange.v2.cfg.ConfigUtils.read(ConfigUtils.java:63)
    at com.mchange.v2.cfg.ConfigUtils.readVmConfig(ConfigUtils.java:115)
    at com.mchange.v2.cfg.MLogConfigSource.readVmConfig(MLogConfigSource.java:46)
    at com.mchange.v2.log.MLogConfig.refresh(MLogConfig.java:59)
    at com.mchange.v2.log.MLog.refreshConfig(MLog.java:59)
    at com.mchange.v2.log.MLog.&lt;clinit&gt;(MLog.java:51)
    at com.mchange.v2.naming.JavaBeanReferenceMaker.&lt;clinit&gt;(JavaBeanReferenceMaker.java:51)
    at com.mchange.v2.c3p0.impl.PoolBackedDataSourceBase.&lt;clinit&gt;(PoolBackedDataSourceBase.java:260)
2014-02-12 20:50:59 DEBUG MLog:101 - The configuration file for resource identifier '/mchange-log.properties' could not be found. Skipping.
java.io.FileNotFoundException: Resource not found at path '/mchange-log.properties'.
    at com.mchange.v2.cfg.BasicPropertiesConfigSource.propertiesFromSource(BasicPropertiesConfigSource.java:64)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.firstInit(BasicMultiPropertiesConfig.java:185)
    at com.mchange.v2.cfg.BasicMultiPropertiesConfig.&lt;init&gt;(BasicMultiPropertiesConfig.java:110)
    at com.mchange.v2.cfg.ConfigUtils.read(ConfigUtils.java:63)
    at com.mchange.v2.cfg.ConfigUtils.readVmConfig(ConfigUtils.java:115)
    at com.mchange.v2.cfg.MLogConfigSource.readVmConfig(MLogConfigSource.java:46)
    at com.mchange.v2.log.MLogConfig.refresh(MLogConfig.java:59)
    at com.mchange.v2.log.MLog.refreshConfig(MLog.java:59)
    at com.mchange.v2.log.MLog.&lt;clinit&gt;(MLog.java:51)
    at com.mchange.v2.naming.JavaBeanReferenceMaker.&lt;clinit&gt;(JavaBeanReferenceMaker.java:51)
    at com.mchange.v2.c3p0.impl.PoolBackedDataSourceBase.&lt;clinit&gt;(PoolBackedDataSourceBase.java:260)
</code></pre>

<p>What could be the problem ? What I'm I doing wrong ? </p>

## Answers
### Answer ID: 21738021
<p>In the log messages and stack traces that you've shown, there is nothing wrong at all. These are all <code>DEBUG</code> level messages. (<code>c3p0</code> &amp; <code>com.mchange</code> libraries should usually be logged at <code>INFO</code>.)</p>

<p><code>c3p0</code> &amp; <code>mchange-commons-java</code> check for potential config information in lots of different places. In many of those places, they find nothing, and so move on. Logging at <code>DEBUG</code>, you are watching the process of libraries checking for, e.g., <code>/mchange-log.properties</code>, in the <code>CLASSPATH</code> and failing to find it. At <code>DEBUG</code>, the libraries log that they looked, that they did not find, and the Exception that went along with not finding.</p>

<p>None of this is of concern at all. It is normal.</p>

<p>The main question is whether the config users put in <code>c3p0-config.xml</code> is taking. You are using a relative directory for the file, rather than an absolute filesystem location. I presume that will work, with relative being interpreted relative to the working directory of the process, but I'm not sure it will work, and even if it does, are you sure that it won't be fragile, depend on how users start up your process? Will users run a script that will ensure the proper working directory?</p>

