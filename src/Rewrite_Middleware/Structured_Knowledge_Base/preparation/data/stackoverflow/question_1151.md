# Mysql - High number of questions?
[Link to question](https://stackoverflow.com/questions/61079136/mysql-high-number-of-questions)
**Creation Date:** 1586259304
**Score:** 1
**Tags:** mysql, performance, phpmyadmin
## Question Body
<p>I have monitored Mysql via the Phpmyadmin interface and it seems to me that the number of questions is very high.</p>

<p>I don't think I generate more than 10 queries per second on average from a few different connections (Apache + a game server)</p>

<p>But the number of questions showed in the Phpmyadmin interface seems very high to me. Is this normal? Are there more questions than queries? Is it not the same thing?</p>

<p><img src="https://i.sstatic.net/o4MUq.jpg" alt="Too many questions?"> </p>

<p>I looked at the mysql logs and I can't seem to see any unexpected queries that I would not be aware of. So all this is a bit of a mystery.</p>

<p>My game server often needs 1 or 2 seconds to get a response from the database (for simple queries) and I wonder if this is related.</p>

<p>Thanks for your precious help!</p>

<p>EDIT: some more information</p>

<p>All status variable page from Phpmyadmin (some are in red)</p>

<pre><code>Variable    Value   Description
Aborted clientsDocumentation    245     The number of connections that were aborted because the client died without closing the connection properly.
Aborted connectsDocumentation   275.9 k The number of failed attempts to connect to the MySQL server.
Binlog cache disk useDocumentation  0   The number of transactions that used the temporary binary log cache but that exceeded the value of binlog_cache_size and used a temporary file to store statements from the transaction.
Binlog cache useDocumentation   0   The number of transactions that used the temporary binary log cache.
Binlog stmt cache disk useDocumentation 0   
Binlog stmt cache useDocumentation  0   
Bytes receivedDocumentation 47.4 G  
Bytes sentDocumentation 491.8 G 
Com admin commandsDocumentation 124     
Com alter dbDocumentation   0   
Com alter db upgradeDocumentation   0   
Com alter eventDocumentation    0   
Com alter functionDocumentation 0   
Com alter procedureDocumentation    0   
Com alter serverDocumentation   0   
Com alter tableDocumentation    4   
Com alter tablespaceDocumentation   0   
Com analyzeDocumentation    0   
Com assign to keycacheDocumentation 0   
Com beginDocumentation  203     
Com binlogDocumentation 0   
Com call procedureDocumentation 0   
Com change dbDocumentation  6.6 M   
Com change masterDocumentation  0   
Com checkDocumentation  0   
Com checksumDocumentation   0   
Com commitDocumentation 309     
Com create dbDocumentation  0   
Com create eventDocumentation   0   
Com create functionDocumentation    0   
Com create indexDocumentation   0   
Com create procedureDocumentation   0   
Com create serverDocumentation  0   
Com create tableDocumentation   50  
Com create triggerDocumentation 0   
Com create udfDocumentation 0   
Com create userDocumentation    0   
Com create viewDocumentation    0   
Com deleteDocumentation 3 M 
Com delete multiDocumentation   149     
Com doDocumentation 0   
Com drop dbDocumentation    0   
Com drop eventDocumentation 0   
Com drop functionDocumentation  0   
Com drop indexDocumentation 0   
Com drop procedureDocumentation 0   
Com drop serverDocumentation    0   
Com drop tableDocumentation 50  
Com drop triggerDocumentation   0   
Com drop userDocumentation  0   
Com drop viewDocumentation  0   
Com empty queryDocumentation    0   
Com flushDocumentation  111     
Com grantDocumentation  0   
Com ha closeDocumentation   0   
Com ha openDocumentation    0   
Com ha readDocumentation    0   
Com helpDocumentation   0   
Com insertDocumentation 8.3 M   
Com insert selectDocumentation  67 k    
Com install pluginDocumentation 0   
Com killDocumentation   0   
Com loadDocumentation   0   
Com lock tablesDocumentation    3.8 k   
Com optimizeDocumentation   1.1 k   
Com preload keysDocumentation   0   
Com purgeDocumentation  0   
Com purge before dateDocumentation  0   
Com release savepointDocumentation  0   
Com rename tableDocumentation   0   
Com rename userDocumentation    0   
Com repairDocumentation 0   
Com replaceDocumentation    297.4 k 
Com replace selectDocumentation 0   
Com resetDocumentation  0   
Com resignalDocumentation   0   
Com revokeDocumentation 0   
Com revoke allDocumentation 0   
Com rollbackDocumentation   3   
Com rollback to savepointDocumentation  0   
Com savepointDocumentation  0   
Com selectDocumentation 41.4 M  
Com set optionDocumentation 13.5 M  
Com show authorsDocumentation   0   
Com show binlog eventsDocumentation 0   
Com show binlogsDocumentation   68.1 k  
Com show charsetsDocumentation  0   
Com show collationsDocumentation    0   
Com show contributorsDocumentation  0   
Com show create dbDocumentation 1.7 k   
Com show create eventDocumentation  0   
Com show create funcDocumentation   0   
Com show create procDocumentation   0   
Com show create tableDocumentation  86 k    
Com show create triggerDocumentation    0   
Com show databasesDocumentation 978     
Com show engine logsDocumentation   0   
Com show engine mutexDocumentation  0   
Com show engine statusDocumentation 0   
Com show errorsDocumentation    0   
Com show eventsDocumentation    50  
Com show fieldsDocumentation    86.2 k  
Com show function statusDocumentation   1.7 k   
Com show grantsDocumentation    26  
Com show keysDocumentation  415     
Com show master statusDocumentation 67.7 k  
Com show open tablesDocumentation   0   
Com show pluginsDocumentation   0   
Com show privilegesDocumentation    0   
Com show procedure statusDocumentation  1.7 k   
Com show processlistDocumentation   67.7 k  
Com show profileDocumentation   0   
Com show profilesDocumentation  0   
Com show relaylog eventsDocumentation   0   
Com show slave hostsDocumentation   0   
Com show slave statusDocumentation  67.7 k  
Com show statusDocumentation    67.7 k  
Com show storage enginesDocumentation   6   
Com show table statusDocumentation  88.3 k  
Com show tablesDocumentation    2.6 k   
Com show triggersDocumentation  85.2 k  
Com show variablesDocumentation 320     
Com show warningsDocumentation  8   
Com signalDocumentation 0   
Com slave startDocumentation    0   
Com slave stopDocumentation 0   
Com stmt closeDocumentation 0   
Com stmt executeDocumentation   0   
Com stmt fetchDocumentation 0   
Com stmt prepareDocumentation   0   
Com stmt reprepareDocumentation 0   
Com stmt resetDocumentation 0   
Com stmt send long dataDocumentation    0   
Com truncateDocumentation   0   
Com uninstall pluginDocumentation   0   
Com unlock tablesDocumentation  3.8 k   
Com updateDocumentation 15 M    
Com update multiDocumentation   127.8 k 
Com xa commitDocumentation  0   
Com xa endDocumentation 0   
Com xa prepareDocumentation 0   
Com xa recoverDocumentation 0   
Com xa rollbackDocumentation    0   
Com xa startDocumentation   0   
CompressionDocumentation    OFF 
ConnectionsDocumentation    7 M The number of connection attempts (successful or not) to the MySQL server.
Created tmp disk tablesDocumentation    326.7 k The number of temporary tables on disk created automatically by the server while executing statements. If Created_tmp_disk_tables is big, you may want to increase the tmp_table_size value to cause temporary tables to be memory-based instead of disk-based.
Created tmp filesDocumentation  255.8 k How many temporary files mysqld has created.
Created tmp tablesDocumentation 16.3 M  The number of in-memory temporary tables created automatically by the server while executing statements.
Delayed errorsDocumentation 0   The number of rows written with INSERT DELAYED for which some error occurred (probably duplicate key).
Delayed insert threadsDocumentation 0   The number of INSERT DELAYED handler threads in use. Every different table on which one uses INSERT DELAYED gets its own thread.
Delayed writesDocumentation 0   The number of INSERT DELAYED rows written.
Flush commandsDocumentation 1   The number of executed FLUSH statements.
Handler commitDocumentation 869.5 k The number of internal COMMIT statements.
Handler deleteDocumentation 120.1 M The number of times a row was deleted from a table.
Handler discoverDocumentation   0   The MySQL server can ask the NDB Cluster storage engine if it knows about a table with a given name. This is called discovery. Handler_discover indicates the number of time tables have been discovered.
Handler prepareDocumentation    0   
Handler read firstDocumentation 6.2 M   The number of times the first entry was read from an index. If this is high, it suggests that the server is doing a lot of full index scans; for example, SELECT col1 FROM foo, assuming that col1 is indexed.
Handler read keyDocumentation   73.5 G  The number of requests to read a row based on a key. If this is high, it is a good indication that your queries and tables are properly indexed.
Handler read lastDocumentation  962.7 k 
Handler read nextDocumentation  94.8 G  The number of requests to read the next row in key order. This is incremented if you are querying an index column with a range constraint or if you are doing an index scan.
Handler read prevDocumentation  100 G   The number of requests to read the previous row in key order. This read method is mainly used to optimize ORDER BY … DESC.
Handler read rndDocumentation   22.1 G  The number of requests to read a row based on a fixed position. This is high if you are doing a lot of queries that require sorting of the result. You probably have a lot of queries that require MySQL to scan whole tables or you have joins that don't use keys properly.
Handler read rnd nextDocumentation  207.2 G The number of requests to read the next row in the data file. This is high if you are doing a lot of table scans. Generally this suggests that your tables are not properly indexed or that your queries are not written to take advantage of the indexes you have.
Handler rollbackDocumentation   2   The number of internal ROLLBACK statements.
Handler savepointDocumentation  0   
Handler savepoint rollbackDocumentation 0   
Handler updateDocumentation 13.4 G  The number of requests to update a row in a table.
Handler writeDocumentation  32.7 G  The number of requests to insert a row in a table.
Innodb buffer pool bytes dataDocumentation  43.8 M  
Innodb buffer pool bytes dirtyDocumentation 49.2 k  
Innodb buffer pool pages dataDocumentation  2.7 k   The number of pages containing data (dirty or clean).
Innodb buffer pool pages dirtyDocumentation 3   The number of pages currently dirty.
Innodb buffer pool pages flushedDocumentation   577.5 k The number of buffer pool pages that have been requested to be flushed.
Innodb buffer pool pages freeDocumentation  5.4 k   The number of free pages.
Innodb buffer pool pages miscDocumentation  112     The number of pages busy because they have been allocated for administrative overhead such as row locks or the adaptive hash index. This value can also be calculated as Innodb_buffer_pool_pages_total - Innodb_buffer_pool_pages_free - Innodb_buffer_pool_pages_data.
Innodb buffer pool pages totalDocumentation 8.2 k   Total size of buffer pool, in pages.
Innodb buffer pool read aheadDocumentation  633     
Innodb buffer pool read ahead evictedDocumentation  0   
Innodb buffer pool read ahead rndDocumentation  0   The number of "random" read-aheads InnoDB initiated. This happens when a query is to scan a large portion of a table but in random order.
Innodb buffer pool read requestsDocumentation   614.7 M The number of logical read requests InnoDB has done.
Innodb buffer pool readsDocumentation   1.7 k   The number of logical reads that InnoDB could not satisfy from buffer pool and had to do a single-page read.
Innodb buffer pool wait freeDocumentation   0   Normally, writes to the InnoDB buffer pool happen in the background. However, if it's necessary to read or create a page and no clean pages are available, it's necessary to wait for pages to be flushed first. This counter counts instances of these waits. If the buffer pool size was set properly, this value should be small.
Innodb buffer pool write requestsDocumentation  1.8 M   The number writes done to the InnoDB buffer pool.
Innodb data fsyncsDocumentation 861.2 k The number of fsync() operations so far.
Innodb data pending fsyncsDocumentation 0   The current number of pending fsync() operations.
Innodb data pending readsDocumentation  0   The current number of pending reads.
Innodb data pending writesDocumentation 0   The current number of pending writes.
Innodb data readDocumentation   42.8 M  The amount of data read so far, in bytes.
Innodb data readsDocumentation  2.5 k   The total number of data reads.
Innodb data writesDocumentation 1.1 M   The total number of data writes.
Innodb data writtenDocumentation    19.2 G  The amount of data written so far, in bytes.
Innodb dblwr pages writtenDocumentation 577.5 k The number of pages that have been written for doublewrite operations.
Innodb dblwr writesDocumentation    165.4 k The number of doublewrite operations that have been performed.
Innodb have atomic builtinsDocumentation    ON  
Innodb log waitsDocumentation   0   The number of waits we had because log buffer was too small and we had to wait for it to be flushed before continuing.
Innodb log write requestsDocumentation  192.2 k The number of log write requests.
Innodb log writesDocumentation  204.7 k The number of physical writes to the log file.
Innodb os log fsyncsDocumentation   368.4 k The number of fsync() writes done to the log file.
Innodb os log pending fsyncsDocumentation   0   The number of pending log file fsyncs.
Innodb os log pending writesDocumentation   0   Pending log file writes.
Innodb os log writtenDocumentation  201.6 M The number of bytes written to the log file.
Innodb page sizeDocumentation   16.4 k  The compiled-in InnoDB page size (default 16KB). Many values are counted in pages; the page size allows them to be easily converted to bytes.
Innodb pages createdDocumentation   324     The number of pages created.
Innodb pages readDocumentation  2.4 k   The number of pages read.
Innodb pages writtenDocumentation   577.5 k The number of pages written.
Innodb row lock current waitsDocumentation  0   The number of row locks currently being waited for.
Innodb row lock timeDocumentation   0   The total time spent in acquiring row locks, in milliseconds.
Innodb row lock time avgDocumentation   0   The average time to acquire a row lock, in milliseconds.
Innodb row lock time maxDocumentation   0   The maximum time to acquire a row lock, in milliseconds.
Innodb row lock waitsDocumentation  0   The number of times a row lock had to be waited for.
Innodb rows deletedDocumentation    232     The number of rows deleted from InnoDB tables.
Innodb rows insertedDocumentation   37.7 k  The number of rows inserted in InnoDB tables.
Innodb rows readDocumentation   1.8 G   The number of rows read from InnoDB tables.
Innodb rows updatedDocumentation    518.5 k The number of rows updated in InnoDB tables.
Innodb truncated status writesDocumentation 0   
Key blocks not flushedDocumentation 0   The number of key blocks in the key cache that have changed but haven't yet been flushed to disk. It used to be known as Not_flushed_key_blocks.
Key blocks unusedDocumentation  0   The number of unused blocks in the key cache. You can use this value to determine how much of the key cache is in use.
Key blocks usedDocumentation    13.4 k  The number of used blocks in the key cache. This value is a high-water mark that indicates the maximum number of blocks that have ever been in use at one time.
Key buffer fraction %   100.00 %    Percentage of used key cache (calculated value)
Key read ratio %    13.69 % Key cache miss calculated as rate of physical reads compared to read requests (calculated value)
Key read requestsDocumentation  226.1 G The number of requests to read a key block from the cache.
Key readsDocumentation  30.9 G  The number of physical reads of a key block from disk. If Key_reads is big, then your key_buffer_size value is probably too small. The cache miss rate can be calculated as Key_reads/Key_read_requests.
Key write ratio %   28.09 % Percentage of physical writes compared to write requests (calculated value)
Key write requestsDocumentation 945.8 M The number of requests to write a key block to the cache.
Key writesDocumentation 265.7 M The number of physical writes of a key block to disk.
Last query costDocumentation    0   The total cost of the last compiled query as computed by the query optimizer. Useful for comparing the cost of different query plans for the same query. The default value of 0 means that no query has been compiled yet.
Max used connectionsDocumentation   152     The maximum number of connections that have been in use simultaneously since the server started.
Not flushed delayed rowsDocumentation   0   The number of rows waiting to be written in INSERT DELAYED queues.
Open filesDocumentation 567     The number of files that are open.
Open streamsDocumentation   0   The number of streams that are open (used mainly for logging).
Open table definitionsDocumentation 301     
Open tablesDocumentation    400     The number of tables that are open.
Opened filesDocumentation   4.6 M   
Opened table definitionsDocumentation   1.6 k   
Opened tablesDocumentation  126.3 k The number of tables that have been opened. If opened tables is big, your table cache value is probably too small.
Performance schema cond classes lostDocumentation   0   
Performance schema cond instances lostDocumentation 0   
Performance schema file classes lostDocumentation   0   
Performance schema file handles lostDocumentation   0   
Performance schema file instances lostDocumentation 0   
Performance schema locker lostDocumentation 0   
Performance schema mutex classes lostDocumentation  0   
Performance schema mutex instances lostDocumentation    0   
Performance schema rwlock classes lostDocumentation 0   
Performance schema rwlock instances lostDocumentation   0   
Performance schema table handles lostDocumentation  0   
Performance schema table instances lostDocumentation    0   
Performance schema thread classes lostDocumentation 0   
Performance schema thread instances lostDocumentation   0   
Prepared stmt countDocumentation    0   
Qcache free blocksDocumentation 2.8 k   The number of free memory blocks in query cache. High numbers can indicate fragmentation issues, which may be solved by issuing a FLUSH QUERY CACHE statement.
Qcache free memoryDocumentation 8.4 M   The amount of free memory for query cache.
Qcache hitsDocumentation    35 M    The number of cache hits.
Qcache insertsDocumentation 31.5 M  The number of queries added to the cache.
Qcache lowmem prunesDocumentation   4.2 M   The number of queries that have been removed from the cache to free up memory for caching new queries. This information can help you tune the query cache size. The query cache uses a least recently used (LRU) strategy to decide which queries to remove from the cache.
Qcache not cachedDocumentation  9.8 M   The number of non-cached queries (not cachable, or not cached due to the query_cache_type setting).
Qcache queries in cacheDocumentation    4.8 k   The number of queries registered in the cache.
Qcache total blocksDocumentation    12.5 k  The total number of blocks in the query cache.
QueriesDocumentation    130.7 M 
QuestionsDocumentation  130.7 M 
Rpl statusDocumentation AUTH_MASTER The status of failsafe replication (not yet implemented).
Select full joinDocumentation   674 k   The number of joins that do not use indexes. If this value is not 0, you should carefully check the indexes of your tables.
Select full range joinDocumentation 32.9 k  The number of joins that used a range search on a reference table.
Select rangeDocumentation   6.7 M   The number of joins that used ranges on the first table. (It's normally not critical even if this is big.)
Select range checkDocumentation 0   The number of joins without keys that check for key usage after each row. (If this is not 0, you should carefully check the indexes of your tables.)
Select scanDocumentation    10.3 M  The number of joins that did a full scan of the first table.
Slave heartbeat periodDocumentation 0   
Slave open temp tablesDocumentation 0   The number of temporary tables currently open by the slave SQL thread.
Slave received heartbeatsDocumentation  0   
Slave retried transactionsDocumentation 0   Total (since startup) number of times the replication slave SQL thread has retried transactions.
Slave runningDocumentation  OFF This is ON if this server is a slave that is connected to a master.
Slow launch threadsDocumentation    0   The number of threads that have taken more than slow_launch_time seconds to create.
Slow queriesDocumentation   4.1 M   The number of queries that have taken more than long_query_time seconds.Documentation
Sort merge passesDocumentation  130 k   The number of merge passes the sort algorithm has had to do. If this value is large, you should consider increasing the value of the sort_buffer_size system variable.
Sort rangeDocumentation 1.6 M   The number of sorts that were done with ranges.
Sort rowsDocumentation  9.3 G   The number of sorted rows.
Sort scanDocumentation  10.1 M  The number of sorts that were done by scanning the table.
Ssl accept renegotiatesDocumentation    0   
Ssl acceptsDocumentation    0   
Ssl callback cache hitsDocumentation    0   
Ssl cipherDocumentation     
Ssl cipher listDocumentation        
Ssl client connectsDocumentation    0   
Ssl connect renegotiatesDocumentation   0   
Ssl ctx verify depthDocumentation   0   
Ssl ctx verify modeDocumentation    0   
Ssl default timeoutDocumentation    0   
Ssl finished acceptsDocumentation   0   
Ssl finished connectsDocumentation  0   
Ssl session cache hitsDocumentation 0   
Ssl session cache missesDocumentation   0   
Ssl session cache modeDocumentation NONE    
Ssl session cache overflowsDocumentation    0   
Ssl session cache sizeDocumentation 0   
Ssl session cache timeoutsDocumentation 0   
Ssl sessions reusedDocumentation    0   
Ssl used session cache entriesDocumentation 0   
Ssl verify depthDocumentation   0   
Ssl verify modeDocumentation    0   
Ssl versionDocumentation        
Table locks immediateDocumentation  95.8 M  The number of times that a table lock was acquired immediately.
Table locks waitedDocumentation 105.3 k The number of times that a table lock could not be acquired immediately and a wait was needed. If this is high, and you have performance problems, you should first optimize your queries, and then either split your table or tables or use replication.
Tc log max pages usedDocumentation  0   
Tc log page sizeDocumentation   0   
Tc log page waitsDocumentation  0   
Threads cache hitrate % 99.99 % Thread cache hit rate (calculated value)
Threads cachedDocumentation 7   The number of threads in the thread cache. The cache hit rate can be calculated as Threads_created/Connections. If this value is red you should raise your thread_cache_size.
Threads connectedDocumentation  4   The number of currently open connections.
Threads createdDocumentation    551     The number of threads created to handle connections. If Threads_created is big, you may want to increase the thread_cache_size value. (Normally this doesn't give a notable performance improvement if you have a good thread implementation.)
Threads runningDocumentation    1   The number of threads that are not sleeping.
UptimeDocumentation 110 days, 23 hours, 42 minutes and 38 seconds   
Uptime since flush statusDocumentation  110 days, 23 hours, 42 minutes and 38 seconds   
</code></pre>

<p>Open new phpMyAdmin window</p>

<p>Possible performance issues from Phpmyadmin:
There are so many recommandations. It is difficult to know where to start.</p>

<p>Possible performance issues</p>

<pre><code>Issue   Recommendation
Less than 80% of the query cache is being utilized. This might be caused by query_cache_limit being too low. Flushing the query cache might help as well.
The query cache is considerably fragmented. Severe fragmentation is likely to (further) increase Qcache_lowmem_prunes. This might be caused by many Query cache low memory prunes due to query_cache_size being too small. For a immediate but short lived fix you can flush the query cache (might lock the query cache for a long time). Carefully adjusting query_cache_min_res_unit to a lower value might help too, e.g. you can set it to the average size of your queries in the cache using this formula: (query_cache_size - qcache_free_memory) / qcache_queries_in_cache
Cached queries are removed due to low query cache memory from the query cache.  You might want to increase query_cache_size, however keep in mind that the overhead of maintaining the cache is likely to increase with its size, so do this in small increments and monitor the results.
The max size of the result set in the query cache is the default of 1 MiB.  Changing query_cache_limit (usually by increasing) may increase efficiency. This variable determines the maximum size a query result may have to be inserted into the query cache. If there are many query results above 1 MiB that are well cacheable (many reads, little writes) then increasing query_cache_limit will increase efficiency. Whereas in the case of many query results being above 1 MiB that are not very well cacheable (often invalidated due to table updates) increasing query_cache_limit might reduce efficiency.
Too many sorts are causing temporary tables.    Consider increasing sort_buffer_size and/or read_rnd_buffer_size, depending on your system memory limits
There are lots of rows being sorted.    While there is nothing wrong with a high amount of row sorting, you might want to make sure that the queries which require a lot of sorting use indexed columns in the ORDER BY clause, as this will result in much faster sorting
There are too many joins without indexes.   This means that joins are doing full table scans. Adding indexes for the columns being used in the join conditions will greatly speed up table joins
The rate of reading the first index entry is high.  This usually indicates frequent full index scans. Full index scans are faster than table scans but require lots of CPU cycles in big tables, if those tables that have or had high volumes of UPDATEs and DELETEs, running 'OPTIMIZE TABLE' might reduce the amount of and/or speed up full index scans. Other than that full index scans can only be reduced by rewriting queries.
The rate of reading data from a fixed position is high. This indicates that many queries need to sort results and/or do a full table scan, including join queries that do not use indexes. Add indexes where applicable.
The rate of reading the next table row is high. This indicates that many queries are doing full table scans. Add indexes where applicable.
Many temporary tables are being written to disk instead of being kept in memory.    Increasing max_heap_table_size and tmp_table_size might help. However some temporary tables are always being written to disk, independent of the value of these variables. To eliminate these you will have to rewrite your queries to avoid those conditions (Within a temporary table: Presence of a BLOB or TEXT column or presence of a column bigger than 512 bytes) as mentioned in the MySQL Documentation
MyISAM key buffer (index cache) % used is low.  You may need to decrease the size of key_buffer_size, re-examine your tables to see if indexes have been removed, or examine queries and expectations about what indexes are being used.
The % of indexes that use the MyISAM key buffer is low. You may need to increase key_buffer_size.
The rate of opening tables is high. Opening tables requires disk I/O which is costly. Increasing table_open_cache might avoid this.
Too many table locks were not granted immediately.  Optimize queries and/or use InnoDB to reduce lock wait.
The maximum amount of used connections is getting close to the value of {max_connections}.  Increase max_connections, or decrease wait_timeout so that connections that do not close database handlers properly get killed sooner. Make sure the code closes database handlers properly.
Too many connections are aborted.   Connections are usually aborted when they cannot be authorized. This article might help you track down the source.
Too many connections are aborted.   Connections are usually aborted when they cannot be authorized. This article might help you track down the source.
The InnoDB log file size is not an appropriate size, in relation to the InnoDB buffer pool. Especially on a system with a lot of writes to InnoDB tables you should set innodb_log_file_size to 25% of innodb_buffer_pool_size. However the bigger this value, the longer the recovery time will be when database crashes, so this value should not be set much higher than 256 MiB. Please note however that you cannot simply change the value of this variable. You need to shutdown the server, remove the InnoDB log files, set the new value in my.cnf, start the server, then check the error logs if everything went fine. See also this blog entry
</code></pre>

<p>SHOW STATUS in 2nd message. See below.</p>

## Answers
### Answer ID: 61131103
<p>Rate Per Second = RPS</p>

<p>Suggestions to consider for your my.cnf [mysqld] section</p>

<pre><code>innodb_io_capacity=500  # from 200 to improve IOPS
read_rnd_buffer_size=128K  # from 256K to reduce handler_read_rnd_next RPS of 21,885
read_buffer_size=256K  # from 128K to reduce handler_read_next RPS of 9,909
key_cache_age_threshold=7200  # from 300 (seconds) to reduce key_reads RPS of 3,234
</code></pre>

<p>You should find these configuration changes reduce CPU BUSY significantly.</p>

<p>There are many other areas to reduce the workload on your server, slow queries 1,541 per hour for starters, can likely be corrected with appropriate indexes.</p>

<p>Please view my profile, Network profile for free downloadable Utility Scripts to assist with performance tuning including monitoring RPS of items mentioned.</p>

