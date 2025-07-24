# Will it be faster to use several threads to update the same database?
[Link to question](https://stackoverflow.com/questions/119157/will-it-be-faster-to-use-several-threads-to-update-the-same-database)
**Creation Date:** 1222144603
**Score:** 2
**Tags:** sql, database, multithreading
## Question Body
<p>I wrote a Java program to add and retrieve data from an MS Access. At present it goes sequentially through ~200K insert queries in ~3 minutes, which I think is slow. I plan to rewrite it using threads with 3-4 threads handling different parts of the hundred thousands records. I have a compound question:</p>

<ul>
<li><p>Will this help speed up the program because of the divided workload or would it be the same because the threads still have to access the database sequentially? </p></li>
<li><p>What strategy do you think would speed up this process (except for query optimization which I already did in addition to using Java's preparedStatement)</p></li>
</ul>

## Answers
### Answer ID: 130446
<p>IIRC access don't allow for multiple connections to te same file because of the locking policy it uses. </p>

<p>And I agree totally about dumping access for sql.</p>

### Answer ID: 130439
<p>I would agree that dumping Access would be the best first step. Having said that...</p>

<p>In a .NET and SQL environment I have definitely seen threads aid in maximizing INSERT throughputs.</p>

<p>I have an application that accepts asynchronous file drops and then processes them into tables in a database. </p>

<p>I created a loader that parsed the file and placed the data into a queue. The queue was served by one or more threads whose max I could tune with a parameter. I found that even on a single core CPU with your typical 7200RPM drive, the ideal number of worker threads was 3. It shortened the load time an almost proportional amount. The key is to balance it such that the CPU bottleneck and the Disk I/O bottleneck are balanced.</p>

<p>So in cases where a bulk copy is not an option, threads should be considered.</p>

### Answer ID: 120897
<p>First, don't use Access.  Move your data anywhere else -- SQL/Server -- MySQL -- anything.  The DB engine inside access (called Jet) is pitifully slow.  It's not a real database; it's for personal projects that involve small amounts of data.  It doesn't scale at all.</p>

<p>Second, threads rarely help.</p>

<p>The JDBC-to-Database connection is a process-wide resource.  All threads share the one connection.  </p>

<p>"But wait," you say, "I'll create a unique Connection object in each thread."</p>

<p>Noble, but <em>sometimes</em> doomed to failure.  Why?  Operating System processing between your JVM and the database may involve a socket that's a single, process-wide resource, shared by all your threads.</p>

<p>If you have a single OS-level I/O resource that's shared across all threads, you won't see much improvement.  In this case, the ODBC connection is one bottleneck.  And MS-Access is the other.</p>

### Answer ID: 119241
<p>Stimms bulk load approach will probably be your best bet but everything is worth trying once.  Note that your bottle neck is going to be disk IO and multiple threads may slow things down.  MS access can also fall apart when multiple users are banging on the file and that is exactly what your multi-threaded approach will act like (make a backup!).  If performance continues to be an issue consider upgrading to <a href="http://www.microsoft.com/sql/editions/express/default.mspx" rel="nofollow noreferrer">SQL express</a>.</p>

<p><a href="http://www.microsoft.com/sql/solutions/migration/access/default.mspx" rel="nofollow noreferrer">MS Access to SQL Server Migrations docs.</a></p>

<p>Good luck.</p>

### Answer ID: 119172
<p>Just try it and see if it helps. I would guess not because the bottleneck is likely to be in the disk access and locking of the tables, unless you can figure out a way to split the load across multiple tables and/or disks.</p>

### Answer ID: 119171
<p>With MSAccess as the backend database, you'll probably get better insert performance if you do an import from within MSAccess.  Another option (since you're using Java) is to directly manipulate the MDB file (if you're creating it from scratch and there are no other concurrent users - which MS Access doesn't handle very well) with a library like <a href="http://jackcess.sourceforge.net/" rel="nofollow noreferrer">Jackess</a>.</p>

<p>If none of these are solutions for you, then I'd recommend using a profiler on your Java application and see if it is spending most of its time waiting for the database (in which case adding threads probably won't help much) or if it is doing processing and parallelizing will help.</p>

### Answer ID: 119166
<p>On modern multi-core machines, using multiple threads to populate a database can make a difference. It depends on the database and its hardware. Try it and see.</p>

### Answer ID: 119163
<ol>
<li><p>Don't know.  Without knowing more about what the bottle neck is I can't comment if it will make it faster.  If the database is the limiter then chances are more threads will slow it down.</p></li>
<li><p>I would dump the access database to a flat file and then bulk load that file.  Bulk loading allows for optimzations which are far, far faster than running multiple insert queries.  </p></li>
</ol>

