# Configuring Quartz for database servers
[Link to question](https://stackoverflow.com/questions/12904653/configuring-quartz-for-database-servers)
**Creation Date:** 1350338221
**Score:** 0
**Tags:** mysql, sql-server, postgresql, quartz-scheduler
## Question Body
<p>I am using Quartz scheduler version 1.5.2, the schedules are stored on a MSSQL database. Quartz is running in a cluster mode with the property -</p>

<pre><code>org.quartz.jobStore.selectWithLockSQL = select lock_name from qrtz_locks with (updlock,rowlock) where lock_name=?
</code></pre>

<p>Works fine.. so far!! 
If I need to make functionality available across different database - Postgres, MySQL,Oracle; the above property needs to change. </p>

<p>How would I rewrite the query to run across all databases? Or is there any other way to achieve easy portability?</p>

## Answers
### Answer ID: 12919990
<p>Check out <a href="http://quartz-scheduler.org/documentation/quartz-2.1.x/configuration/ConfigJobStoreTX" rel="nofollow"><code>org.quartz.jobStore.driverDelegateClass</code></a> property:</p>

<blockquote>
  <p>Driver delegates understand the particular 'dialects' of varies database systems. [...]</p>
</blockquote>

<p>Quartz supports out-of-the box the following database (dialects): </p>

<ul>
<li><p>MSSQL</p></li>
<li><p>PostgreSQL</p></li>
<li><p>WebLogic</p></li>
<li><p>Oracle</p></li>
<li><p>Cloudscape</p></li>
<li><p>DB2 (v6, v7, v8)</p></li>
<li><p>HSQLDB</p></li>
<li><p>Pointbase</p></li>
<li><p>Sybase</p></li>
</ul>

<p>I know also successfully used it with H2 and MySQL.</p>

