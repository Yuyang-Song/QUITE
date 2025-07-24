# SQL Server SELECT WITH (NOLOCK) causing exclusive lock in tempdb
[Link to question](https://stackoverflow.com/questions/78169798/sql-server-select-with-nolock-causing-exclusive-lock-in-tempdb)
**Creation Date:** 1710539075
**Score:** 1
**Tags:** php, sql-server, locking, sqlsrv
## Question Body
<p>I've got a php application that hangs indefinitely waiting on a Microsoft SQL Server 2019 lock.  The script is using the SQLSRV driver.  There are two SELECT queries accessing a local temp table, both of which attempt to acquire an exclusive lock on an object.  The first lock is granted but the process hangs forever in a suspended state.  The second query does likewise, waiting for the lock granted to the first query.  The odd thing is both queries are using WITH (NOLOCK).</p>
<p>Here's the first query:</p>
<pre><code>SELECT * FROM #ids_temp WITH (NOLOCK) WHERE backupid = N'4dd31554df67d8503fba000945fbe02a' AND itemname = N'user'
</code></pre>
<p>sys.dm_os_waiting_tasks says it's waiting type is ASYNC_NETWORK_IO.
The second query is like the first:</p>
<pre><code>SELECT 'x' FROM #ids_temp WITH (NOLOCK) WHERE backupid = N'4dd31554df67d8503fba000945fbe02a' AND itemname = N'userfinal' AND itemid = '3' ORDER BY 1 OFFSET 0 ROWS  FETCH NEXT 1 ROWS ONLY
</code></pre>
<p>It's wait type is LCK_M_X.  From all the documentation I've been able to find, neither of these queries should be requesting an exclusive lock.  Is there some database setting that could be requiring exclusive locks for select queries?  How can I keep these queries from requesting exclusive locks?</p>
<p>I tried rewriting the PHP script to call sqlsrv_free_stmt after the first query and before the second one starts in order to release the lock on the temp table.  However, I noticed the same problem happening in other areas of the code.  The PHP application was originally written for a MySQL database and it works fine in such an environment.  So instead of trying to find every instance of code designed to run with no locks on the temp tables, it seems better to adjust the behavior of the database to accommodate the code.</p>
<p><strong>Update:</strong> The two queries use the same connection and are reading from the same temporary table.  The exclusive-locked object is an instance of the  #ids_temp table in the tempdb database.  The application also hold a Sch-S lock on a table in another database.  That table was previously referenced by another query using the same connection.  That previous query looks like this:</p>
<pre><code>    SELECT ggh.*
        FROM grade_grades_history ggh
        JOIN #ids_temp bi WITH (NOLOCK) ON ggh.itemid = bi.itemid
        WHERE bi.backupid = N'4dd31554df67d8503fba000945fbe02a'
        AND bi.itemname = 'grade_item'
</code></pre>
<p>The Sch-S lock is granted on the table grade_grades_history.  I don't think this should interfere with reading from the #ids_temp table though since this is also just a SELECT query. The PHP application is keeping the SQL transactions open as it iterates over the results.  That's the reason why the initial transactions never finish.</p>
<p>Other users have supposedly run this application in a MSSQL Server setup successfully.  That's why I suspect the issue lies in my database configuration instead of the application code.  If the database would stop putting the exclusive locks in place then the application should work as-is.</p>

