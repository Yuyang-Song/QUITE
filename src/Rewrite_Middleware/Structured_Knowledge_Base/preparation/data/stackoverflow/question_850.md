# Storing microseconds in a MySQL database
[Link to question](https://stackoverflow.com/questions/45648866/storing-microseconds-in-a-mysql-database)
**Creation Date:** 1502531407
**Score:** 0
**Tags:** java, mysql, datetime, playframework, playframework-2.0
## Question Body
<p>I have a Play Framework application with ebeans.To synchronise between the main system and an offline system I use an addDate field to identify unique records.</p>

<p>This works perfect while developing and initial testing (development with jdbc:h2:mem:play;MODE=MYSQL) and testing with a limited dataset.</p>

<p>But in production, with concurrent users I discovered that in the MySQL database milliseconds are not stored. I have the fields created as datetime(6), but a query like:</p>

<pre><code>SELECT UNIX_TIMESTAMP(add_date) FROM `user` WHERE 1 
</code></pre>

<p>returns:</p>

<pre><code>1499722493.000000
1499772800.000000
1499777225.000000
1499790922.000000
1499875868.000000
1499954855.000000
1499977124.000000
1499981148.000000
1499986822.000000
</code></pre>

<p>(ps. just selecting the add_date field in MySQL return 2015-12-17 16:15:50.000000, showing the precision is there)</p>

<p>So milliseconds are not stored. In Java I use the normal Date class, so they are in there (and so in the H2 men test database).</p>

<pre><code>protected Date addDate;
</code></pre>

<p>How can I have the milliseconds stored in the Database with my current configuration without, hopefully, having to rewrite too much code?</p>

<p>[Edit:]</p>

<pre><code>I am using MySQL on Debian: Ver 14.14 Distrib 5.6.35
sbt.version=0.13.11
addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.5.16")
addSbtPlugin("com.typesafe.sbt" % "sbt-play-ebean" % "3.0.2")
mysql-connector-java % 5.1.43
</code></pre>

## Answers
### Answer ID: 45656980
<h1>java.time</h1>

<p>The troublesome <code>java.util.Date</code> class is now supplanted by the <a href="https://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html" rel="nofollow noreferrer">java.time</a> classes. </p>

<p>The <a href="http://docs.oracle.com/javase/8/docs/api/java/time/Instant.html" rel="nofollow noreferrer"><code>Instant</code></a> class represents a moment on the timeline in <a href="https://en.wikipedia.org/wiki/Coordinated_Universal_Time" rel="nofollow noreferrer">UTC</a> with a resolution of <a href="https://en.wikipedia.org/wiki/Nanosecond" rel="nofollow noreferrer">nanoseconds</a> (up to nine (9) digits of a decimal fraction). </p>

<p>Capturing the current moment is limited to <a href="https://en.wikipedia.org/wiki/Millisecond" rel="nofollow noreferrer">milliseconds</a> in Java 8 but expanded to up to nanoseconds in Java 9 and later with a <a href="https://bugs.openjdk.java.net/browse/JDK-8068730" rel="nofollow noreferrer">new implementation</a> of <a href="https://docs.oracle.com/javase/8/docs/api/java/time/Clock.html" rel="nofollow noreferrer"><code>Clock</code></a>. To be clear, I'll repeat: Both Java 8 and Java 9 can <em>store</em> a value with nanoseconds, but only Java 9 and later can <em>capture</em> the current moment in finer than milliseconds resolution.</p>

<pre><code>Instant instant = Instant.now() ;  // Captures milliseconds in Java 8 but nanoseconds in Java 9+.
</code></pre>

<p>Use a JDBC driver that complies with JDBC 4.2 or later, to work directly with the java.time types rather than the hacked java.sql types. Call the <code>PreparedStatement::setObject</code> and <code>ResultSet::getObject</code> methods.</p>

<pre><code>myPreparedStatement.setObject( … , instant ) ;
</code></pre>

<p>…and…</p>

<pre><code>Instant instant = myResultSet.getObject( … , Instant.class ) ; // Transfers a value with nanoseconds if present.
</code></pre>

<hr>

<h1>About java.time</h1>

<p>The <a href="http://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html" rel="nofollow noreferrer">java.time</a> framework is built into Java 8 and later. These classes supplant the troublesome old <a href="https://en.wikipedia.org/wiki/Legacy_system" rel="nofollow noreferrer">legacy</a> date-time classes such as <a href="https://docs.oracle.com/javase/8/docs/api/java/util/Date.html" rel="nofollow noreferrer"><code>java.util.Date</code></a>, <a href="https://docs.oracle.com/javase/8/docs/api/java/util/Calendar.html" rel="nofollow noreferrer"><code>Calendar</code></a>, &amp; <a href="http://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html" rel="nofollow noreferrer"><code>SimpleDateFormat</code></a>.</p>

<p>The <a href="http://www.joda.org/joda-time/" rel="nofollow noreferrer">Joda-Time</a> project, now in <a href="https://en.wikipedia.org/wiki/Maintenance_mode" rel="nofollow noreferrer">maintenance mode</a>, advises migration to the <a href="http://docs.oracle.com/javase/8/docs/api/java/time/package-summary.html" rel="nofollow noreferrer">java.time</a> classes.</p>

<p>To learn more, see the <a href="http://docs.oracle.com/javase/tutorial/datetime/TOC.html" rel="nofollow noreferrer">Oracle Tutorial</a>. And search Stack Overflow for many examples and explanations. Specification is <a href="https://jcp.org/en/jsr/detail?id=310" rel="nofollow noreferrer">JSR 310</a>.</p>

<p>Where to obtain the java.time classes? </p>

<ul>
<li><a href="https://en.wikipedia.org/wiki/Java_version_history#Java_SE_8" rel="nofollow noreferrer"><strong>Java SE 8</strong></a>, <a href="https://en.wikipedia.org/wiki/Java_version_history#Java_SE_9" rel="nofollow noreferrer"><strong>Java SE 9</strong></a>, and later

<ul>
<li>Built-in. </li>
<li>Part of the standard Java API with a bundled implementation.</li>
<li>Java 9 adds some minor features and fixes.</li>
</ul></li>
<li><a href="https://en.wikipedia.org/wiki/Java_version_history#Java_SE_6" rel="nofollow noreferrer"><strong>Java SE 6</strong></a> and <a href="https://en.wikipedia.org/wiki/Java_version_history#Java_SE_7" rel="nofollow noreferrer"><strong>Java SE 7</strong></a>

<ul>
<li>Much of the java.time functionality is back-ported to Java 6 &amp; 7 in <a href="http://www.threeten.org/threetenbp/" rel="nofollow noreferrer"><strong><em>ThreeTen-Backport</em></strong></a>.</li>
</ul></li>
<li><a href="https://en.wikipedia.org/wiki/Android_(operating_system)" rel="nofollow noreferrer"><strong>Android</strong></a>

<ul>
<li>The <a href="https://github.com/JakeWharton/ThreeTenABP" rel="nofollow noreferrer"><strong><em>ThreeTenABP</em></strong></a> project adapts <em>ThreeTen-Backport</em> (mentioned above) for Android specifically.</li>
<li>See <a href="http://stackoverflow.com/q/38922754/642706"><em>How to use ThreeTenABP…</em></a>.</li>
</ul></li>
</ul>

<p>The <a href="http://www.threeten.org/threeten-extra/" rel="nofollow noreferrer"><strong>ThreeTen-Extra</strong></a> project extends java.time with additional classes. This project is a proving ground for possible future additions to java.time. You may find some useful classes here such as <a href="http://www.threeten.org/threeten-extra/apidocs/org/threeten/extra/Interval.html" rel="nofollow noreferrer"><code>Interval</code></a>, <a href="http://www.threeten.org/threeten-extra/apidocs/org/threeten/extra/YearWeek.html" rel="nofollow noreferrer"><code>YearWeek</code></a>, <a href="http://www.threeten.org/threeten-extra/apidocs/org/threeten/extra/YearQuarter.html" rel="nofollow noreferrer"><code>YearQuarter</code></a>, and <a href="http://www.threeten.org/threeten-extra/apidocs/index.html" rel="nofollow noreferrer">more</a>.</p>

### Answer ID: 45650257
<p>In java you can not accurate to the microsecond (nanosecond) without taking a lot of system resources. Your date is inserted in milliseconds because java does it in milliseconds.</p>

<p>If you want to use microseconds from SQL you must use the SQL NOW() on insertion. </p>

