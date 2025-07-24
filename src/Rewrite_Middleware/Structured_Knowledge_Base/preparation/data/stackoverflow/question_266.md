# Is there something like Redis DB, but not limited with RAM size?
[Link to question](https://stackoverflow.com/questions/18447380/is-there-something-like-redis-db-but-not-limited-with-ram-size)
**Creation Date:** 1377529921
**Score:** 44
**Tags:** database, redis, nosql, bigdata
## Question Body
<p>I'm looking for a database matching these criteria:</p>

<ul>
<li>May be non-persistent;</li>
<li>Almost all keys of DB need to be updated once in 3-6 hours (100M+ keys with total size of 100Gb)</li>
<li>Ability to quickly select data by key (or Primary Key)</li>
<li>This needs to be a DBMS (so LevelDB doesn't fit)</li>
<li>When data is written, DB cluster must be able to serve queries (single nodes can be blocked though)</li>
<li>Not in-memory – our dataset will exceed the RAM limits</li>
<li>Horizontal scaling and replication</li>
<li>Support full rewrite of all data (MongoDB doesn't clear space after deleting data)</li>
<li>C# and Java support</li>
</ul>

<p>Here's my process of working with such database:
We've got an analytics cluster that produces 100M records (50GB) of data every 4-6 hours. The data is a "key - array[20]". This data needs to be distributed to users through a front-end system with a rate of 1-10k requests per second. In average, only ~15% of the data is requested, the rest of it will be rewritten in 4-6 hours when the next data set is generated.</p>

<p>What i tried:</p>

<ol>
<li>MongoDB. Datastorage overhead, high defragmentation costs.</li>
<li>Redis. Looks perfect, but it's limited with RAM and our data exceeds it.</li>
</ol>

<p>So the question is: is there anything like Redis, but not limited with RAM size?</p>

## Answers
### Answer ID: 18460597
<p><strong>Yes, there are two alternatives to Redis that are not limited by RAM size while remaining compatible with Redis protocol:</strong></p>

<p>Ardb (C++), replication(Master-Slave/Master-Master): <a href="https://github.com/yinqiwen/ardb" rel="nofollow noreferrer">https://github.com/yinqiwen/ardb</a></p>

<blockquote>
  <p>A redis-protocol compatible persistent storage server, support
  LevelDB/KyotoCabinet/LMDB as storage engine.</p>
</blockquote>

<p>Edis (Erlang): <a href="https://github.com/cbd/edis" rel="nofollow noreferrer">https://github.com/cbd/edis</a> </p>

<blockquote>
  <p>Edis is a protocol-compatible Server replacement for Redis, written in
  Erlang. Edis's goal is to be a drop-in replacement for Redis when
  persistence is more important than holding the dataset in-memory. Edis
  (currently) uses Google's leveldb as a backend.</p>
</blockquote>

<p><strong>And for completeness here is another data-structures database:</strong></p>

<p>Hyperdex (Strings, Integers, Floats, Lists, Sets, Maps): <a href="http://hyperdex.org/doc/latest/DataTypes/#chap:data-types" rel="nofollow noreferrer">http://hyperdex.org/doc/latest/DataTypes/#chap:data-types</a></p>

<blockquote>
  <p>HyperDex is:</p>
  
  <ul>
  <li>Fast: HyperDex has lower latency, higher throughput, and lower
  variance than other key-value stores. </li>
  <li>Scalable: HyperDex scales as
  more machines are added to the system. </li>
  <li>Consistent: HyperDex guarantees
  linearizability for key-based operations. Thus, a read always returns
  the latest value inserted into the system. Not just “eventually,” but
  immediately and always. </li>
  <li>Fault Tolerant: HyperDex automatically
  replicates data on multiple machines so that concurrent failures, up
  to an application-determined limit, will not cause data loss.
  Searchable: </li>
  <li>HyperDex enables efficient lookups of secondary data
  attributes. </li>
  <li>Easy-to-Use: HyperDex provides APIs for a variety of
  scripting and native languages. </li>
  <li>Self-Maintaining: A HyperDex is
  self-maintaining and requires little user maintenance.</li>
  </ul>
</blockquote>

### Answer ID: 18489138
<p>Yes, SSDB(<a href="https://github.com/ideawu/ssdb" rel="noreferrer">https://github.com/ideawu/ssdb</a>), it has very similar APIs to Redis: <a href="http://www.ideawu.com/ssdb/docs/php/" rel="noreferrer">http://www.ideawu.com/ssdb/docs/php/</a></p>

<p>SSDB supports hash, zset. It use leveldb as storage engine, most data is stored on disk, RAM is used for cache. On our SSDB instance with 300GB data, it only uses 800MB RAM.</p>

### Answer ID: 18448901
<p>These days you can easily find servers with more than 100 GB of RAM to host a single instance, or you can shard your data and use several servers with less RAM. Storing 100 GB with Redis (in RAM) is not really a problem.</p>

<p>Now if you really want to try a bleeding-edge clone of Redis not limited by RAM size, there is NDS (by Matt Palmer):</p>

<ul>
<li><p><a href="http://www.anchor.com.au/blog/2013/04/redis-rethought-exciting-extremes-with-larger-than-memory-datasets/" rel="nofollow noreferrer">http://www.anchor.com.au/blog/2013/04/redis-rethought-exciting-extremes-with-larger-than-memory-datasets/</a></p></li>
<li><p><a href="https://github.com/mpalmer/redis/tree/nds-2.6" rel="nofollow noreferrer">https://github.com/mpalmer/redis/tree/nds-2.6</a></p></li>
</ul>

<p>Note that the storage backend of NDS has moved from Kyoto Cabinet to LMDB (a very good package, which also powers OpenLDAP), precisely because of space reclaim issues following deleted keys.</p>

<p>Other solutions - not compatible with Redis - may also suit your needs: Couchbase, and Aerospike, for instance could easily support your throughput. Cassandra and Riak would probably work as well provided you have enough nodes.</p>

