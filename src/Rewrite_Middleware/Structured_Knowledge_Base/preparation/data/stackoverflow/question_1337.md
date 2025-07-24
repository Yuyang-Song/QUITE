# MySQL High CPU Consumption (600%)
[Link to question](https://stackoverflow.com/questions/71163591/mysql-high-cpu-consumption-600)
**Creation Date:** 1645122710
**Score:** 2
**Tags:** mysql, performance, caching, cpu
## Question Body
<p>We have a high traffic server running mysql. This database has run fine for years with no significant spikes in traffic or changes to the database but recently Mysql CPU consumption has spiked to a consistent 600%.</p>
<p>We don't see any slow queries being logged but we get the following recommendations.</p>
<p>We're not very knowledgeable with MySQL and everything we've tried to fix the CPU consumption has not worked.</p>
<p>If anyone can provide some recommended settings that would be appreciated.</p>
<pre><code>top - 08:08:59 up 313 days, 12:47,  2 users,  load average: 7.21, 6.48, 6.08
Tasks: 294 total,   1 running, 293 sleeping,   0 stopped,   0 zombie
Cpu(s): 29.9%us, 10.6%sy,  3.9%ni, 47.1%id,  3.1%wa,  0.0%hi,  5.5%si,  0.0%st
Mem:   8018016k total,  7869300k used,   148716k free,   587632k buffers
Swap:        0k total,        0k used,        0k free,  5894136k cached

[mysqld]
# skip-networking
#tmpdir=/dev/shm
general_log = 1
slow_query_log = 1
log-slow-queries = /var/log/mysql-slow.log
slow-query_log_file = /var/log/mysql-slow.log
long_query_time = 2
sort_buffer_size = 4M
max_connections = 151
max_allowed_packet = 100M
query_cache_size = 128M
query_cache_limit = 5M
join_buffer_size = 10M
tmp_table_size = 64M
max_heap_table_size = 64M
thread_cache_size = 4
table_cache = 20k
innodb_buffer_pool_size = 512M
key_buffer_size = 128M
local-infile=0
open_files_limit=2058
wait_timeout = 500
connect_timeout = 500
interactive_timeout = 500
performance_schema = on


 &gt;&gt;  MySQLTuner 1.4.0 - Major Hayden &lt;major@mhtx.net&gt;
 &gt;&gt;  Bug reports, feature requests, and downloads at http://mysqltuner.com/
 &gt;&gt;  Run with '--help' for additional options and output filtering
[OK] Logged in using credentials passed on the command line
[OK] Currently running supported MySQL version 5.5.50-log
[OK] Operating on 64-bit architecture

-------- Storage Engine Statistics -------------------------------------------
[--] Status: +ARCHIVE +BLACKHOLE +CSV -FEDERATED +InnoDB +MRG_MYISAM 
[--] Data in MyISAM tables: 453M (Tables: 169)
[--] Data in PERFORMANCE_SCHEMA tables: 0B (Tables: 17)
[!!] InnoDB is enabled but isn't being used
[!!] Total fragmented tables: 5

-------- Security Recommendations  -------------------------------------------
[OK] All database users have passwords assigned

-------- Performance Metrics -------------------------------------------------
[--] Up for: 22m 39s (763K q [561.834 qps], 22K conn, TX: 506M, RX: 95M)
[--] Reads / Writes: 71% / 29%
[--] Total buffers: 848.0M global + 14.6M per thread (151 max threads)
[OK] Maximum possible memory usage: 3.0G (39% of installed RAM)
[OK] Slow queries: 0% (1/763K)
[OK] Highest usage of available connections: 52% (80/151)
[OK] Key buffer size / total MyISAM indexes: 128.0M/273.3M
[OK] Key buffer hit rate: 100.0% (72M cached / 29K reads)
[OK] Query cache efficiency: 79.1% (472K cached / 596K selects)
[OK] Query cache prunes per day: 0
[OK] Sorts requiring temporary tables: 0% (8 temp sorts / 43K sorts)
[OK] Temporary tables created on disk: 0% (37 on disk / 10K total)
[!!] Thread cache hit rate: 47% (12K created / 22K connections)
[OK] Table cache hit rate: 97% (249 open / 256 opened)
[OK] Open file limit used: 0% (277/41K)
[!!] Table locks acquired immediately: 53%

-------- Recommendations -----------------------------------------------------
General recommendations:
    Add skip-innodb to MySQL configuration to disable InnoDB
    Run OPTIMIZE TABLE to defragment tables for better performance
    MySQL started within last 24 hours - recommendations may be inaccurate
    Optimize queries and/or use InnoDB to reduce lock wait
Variables to adjust:
    thread_cache_size (&gt; 4)
</code></pre>
<p><strong>Suboptimal caching method.</strong></p>
<p>You are using the MySQL Query cache with a fairly high traffic database. It might be worth considering to use memcached instead of the MySQL Query cache, especially if you have multiple slaves.</p>
<p><strong>Less than 80% of the query cache is being utilized.</strong></p>
<p>This might be caused by query_cache_limit being too low. Flushing the query cache might help as well.</p>
<p><strong>The query cache is considerably fragmented.</strong></p>
<p>Severe fragmentation is likely to (further) increase Qcache_lowmem_prunes. This might be caused by many Query cache low memory prunes due to query_cache_size being too small. For a immediate but short lived fix you can flush the query cache (might lock the query cache for a long time). Carefully adjusting query_cache_min_res_unit to a lower value might help too, e.g. you can set it to the average size of your queries in the cache using this formula: (query_cache_size - qcache_free_memory) / qcache_queries_in_cache</p>
<p><strong>There are lots of rows being sorted.</strong></p>
<p>While there is nothing wrong with a high amount of row sorting, you might want to make sure that the queries which require a lot of sorting use indexed columns in the ORDER BY clause, as this will result in much faster sorting</p>
<p><strong>There are too many joins without indexes.</strong></p>
<p>This means that joins are doing full table scans. Adding indexes for the columns being used in the join conditions will greatly speed up table joins</p>
<p><strong>The rate of reading the first index entry is high.</strong></p>
<p>This usually indicates frequent full index scans. Full index scans are faster than table scans but require lots of CPU cycles in big tables, if those tables that have or had high volumes of UPDATEs and DELETEs, running 'OPTIMIZE TABLE' might reduce the amount of and/or speed up full index scans. Other than that full index scans can only be reduced by rewriting queries.</p>
<p><strong>The rate of reading data from a fixed position is high.</strong></p>
<p>This indicates that many queries need to sort results and/or do a full table scan, including join queries that do not use indexes. Add indexes where applicable.</p>
<p><strong>The rate of reading the next table row is high.</strong></p>
<p>This indicates that many queries are doing full table scans. Add indexes where applicable.</p>
<p><strong>Many temporary tables are being written to disk instead of being kept in memory.</strong></p>
<p>Increasing max_heap_table_size and tmp_table_size might help. However some temporary tables are always being written to disk, independent of the value of these variables. To eliminate these you will have to rewrite your queries to avoid those conditions (Within a temporary table: Presence of a BLOB or TEXT column or presence of a column bigger than 512 bytes) as mentioned in the MySQL Documentation</p>
<p><strong>MyISAM key buffer (index cache) % used is low.</strong></p>
<p>You may need to decrease the size of key_buffer_size, re-examine your tables to see if indexes have been removed, or examine queries and expectations about what indexes are being used.</p>
<p><strong>The rate of opening tables is high.</strong></p>
<p>Opening tables requires disk I/O which is costly. Increasing table_open_cache might avoid this.</p>
<p><strong>The rate of opening files is high.</strong></p>
<p>Consider increasing open_files_limit, and check the error log when restarting after changing open_files_limit.</p>
<p><strong>Too many table locks were not granted immediately.</strong></p>
<p>Optimize queries and/or use InnoDB to reduce lock wait.</p>
<p><strong>Too many table locks were not granted immediately.</strong></p>
<p>Optimize queries and/or use InnoDB to reduce lock wait.</p>
<p><strong>Too many connections are aborted.</strong></p>
<p>Connections are usually aborted when they cannot be authorized. This article might help you track down the source.</p>
<p><strong>The InnoDB log file size is not an appropriate size, in relation to the InnoDB buffer pool.</strong></p>
<p>Especially on a system with a lot of writes to InnoDB tables you should set innodb_log_file_size to 25% of innodb_buffer_pool_size. However the bigger this value, the longer the recovery time will be when database crashes, so this value should not be set much higher than 256 MiB. Please note however that you cannot simply change the value of this variable. You need to shutdown the server, remove the InnoDB log files, set the new value in my.cnf, start the server, then check the error logs if everything went fine. See also this blog entry</p>
<p>EDIT</p>
<pre><code>    -------- Storage Engine Statistics -------------------------------------------
[--] Status: +ARCHIVE +BLACKHOLE +CSV -FEDERATED +InnoDB +MRG_MYISAM 
[--] Data in MyISAM tables: 461M (Tables: 168)
[--] Data in InnoDB tables: 16K (Tables: 1)
[--] Data in PERFORMANCE_SCHEMA tables: 0B (Tables: 17)
[!!] Total fragmented tables: 8

-------- Security Recommendations  -------------------------------------------
[OK] All database users have passwords assigned

-------- Performance Metrics -------------------------------------------------
[--] Up for: 25d 22h 33m 27s (1B q [533.080 qps], 35M conn, TX: 801B, RX: 148B)
[--] Reads / Writes: 71% / 29%
[--] Total buffers: 1020.0M global + 14.6M per thread (151 max threads)
[OK] Maximum possible memory usage: 3.2G (41% of installed RAM)
[OK] Slow queries: 0% (7/1B)
[OK] Highest usage of available connections: 55% (84/151)
[OK] Key buffer size / total MyISAM indexes: 300.0M/317.3M
[OK] Key buffer hit rate: 100.0% (35B cached / 18K reads)
[OK] Query cache efficiency: 79.6% (743M cached / 933M selects)
[!!] Query cache prunes per day: 34376
[OK] Sorts requiring temporary tables: 0% (48K temp sorts / 68M sorts)
[OK] Temporary tables created on disk: 0% (1K on disk / 17M total)
[OK] Thread cache hit rate: 76% (8M created / 35M connections)
[OK] Table cache hit rate: 98% (504 open / 511 opened)
[OK] Open file limit used: 1% (678/41K)
[!!] Table locks acquired immediately: 74%
[OK] InnoDB buffer pool / data size: 512.0M/16.0K
[OK] InnoDB log waits: 0
-------- Recommendations -----------------------------------------------------
General recommendations:
    Run OPTIMIZE TABLE to defragment tables for better performance
    Optimize queries and/or use InnoDB to reduce lock wait
Variables to adjust:
    query_cache_size (&gt; 128M)
</code></pre>

## Answers
### Answer ID: 71180703
<p>Master00, since you need and want to stay with MyISAM, consider the following suggestions to IMPROVE your response time with MyISAM.</p>
<p>Corrected variable name to key_cache_age_threshold - my humble apologies. Wilson</p>
<pre><code>key_cache_block_size=16384  # from 1024 to reduce overhead managing key_buffer data
key_cache_division_limit=50  # from 100 percent to enable Hot / Warm cache separation
key_cache_age_threshold=7200  # from 300 seconds before AGE_OUT causes another READ
</code></pre>
<p>and the these three changes will reduce your key_reads Rate Per Second significantly.</p>
<p>For additional useful tips, view my profile for contact info and get in touch.</p>

### Answer ID: 71165721
<p>Before I get started, I'll mention that everything in the recommended list is worth looking at and I agree strongly with the other answer that 5.5 is crazy-old — to the point of not even getting security patches. Upgrading is a very good idea.</p>
<hr />
<p>That out of the way, I want to focus on this:</p>
<blockquote>
<p>This database has run fine for years with no significant spikes in traffic or changes to the database</p>
</blockquote>
<p>With that in mind, I know two common reasons you can see a sudden drop in performance like this:</p>
<ol>
<li><p>The disks are on the verge of failing, such that some disk I/O operations are slow or repeating. If this is your issue, you'll likely find other evidence of it in the core server (not MySql) logs... <em>but not always!</em></p>
</li>
<li><p>As you see data growth — not just over time but in terms of business growth (hopefully the business has more customers than it did when the server was installed) — it takes more memory to keep active records buffered in RAM instead of frequently reading from the (much slower) disks than it used to. You can hit a tipping point, where suddenly many of your queries that used to finish entirely in RAM now need to spill out to disk.</p>
</li>
</ol>
<p>Yes, yes, I know both of these are disk issues, while the problem presents as CPU use. However, disk I/O problems often show up as CPU load issues, with processes waiting on disk to complete.</p>
<p>The solution to both of these usually involves hardware upgrades... but you can delay this if it's the second reason by working the list of recommendations in your question.</p>

### Answer ID: 71164746
<p>Upgrade -- Support of 5.5 ended about 7 years ago.</p>
<p>Tip-top recommendation:  Switch your tables from MyISAM to InnoDB.  And be sure to adjust <code>key_buffer_size</code> down to 20M and <code>innodb_buffer_pool_size</code> higher, but not so high that it causes swapping.</p>
<p>Top recommendation:  Use the <a href="http://mysql.rjweb.org/doc.php/mysql_analysis#slow_queries_and_slowlog" rel="nofollow noreferrer"><em>SlowLog</em></a> that you have been capturing.  Digest it and let's discuss the 'worst' couple of queries.</p>
<p>Well, maybe there is nothing much in the slowlog (&quot;Slow queries: 0% (1/763K)&quot;).  So lower <code>long_query_time</code> to <code>0.4</code></p>
<p>The query cache <em>may</em> be hurting more than it is helping.  It is hard to say.</p>
<p>Not much of the 8MB is taken up by MySQL; do you have other apps running on the same machine?  Changing memory size will not relieve CPU issues.  Using a little more memory to raise <code>table_open_cache</code>, <code>open_files_limit</code>, etc, <em>may</em> help with the CPU.</p>
<p>If you are not using MyISAM, lower <code>key_buffer_size</code> to <code>20M</code>.</p>
<p>Ignore the note about &quot;fragmented tables&quot;.</p>
<p>Turn off the <code>general_log</code>; it rapidly fills the disk.  (Not much CPU impact.)</p>
<p>&quot;Up for: 22m 39s&quot; -- The analysis is mostly focused on &quot;startup&quot; activity; hence does not adequately address your question.  Wait 24 hours.</p>
<p>Deeper analysis:  <a href="http://mysql.rjweb.org/doc.php/mysql_analysis#tuning" rel="nofollow noreferrer">http://mysql.rjweb.org/doc.php/mysql_analysis#tuning</a></p>

