# Database with high throughput, efficient random access and queries on secondary index
[Link to question](https://stackoverflow.com/questions/34950144/database-with-high-throughput-efficient-random-access-and-queries-on-secondary)
**Creation Date:** 1453476332
**Score:** 2
**Tags:** database, high-load, bigdata
## Question Body
<p>We have ~1Tb of user profiles and need to perform two types operations on them:</p>

<ul>
<li><strong>random reads and writes</strong> (~20k profile updates per second)</li>
<li><strong>queries on predefined dimensions</strong> (e.g. for reporting)</li>
</ul>

<p>For example, if we encounter user in a transaction, we want to update his profile with a URL he came from. At the end of the day we want to see all users who visited particular URL. We don't need joins, aggregations, etc., only filtering by one or several fields. </p>

<p>We don't really care about <em>latency</em>, but need high <strong>throughput</strong>. </p>

<hr>

<p>Most databases we looked at belong to one of two categories - key-value DBs with fast random access or batch DBs optimized for querying and analytics.</p>

<h2>Key-value storages</h2>

<p><strong>Aerospike</strong> can store terabyte-scale data and is very well-optimized for fast key-based lookup. However, queries on secondary index are deadly slow, which makes it unsuitable for our purposes. </p>

<p><strong>MongoDB</strong> is pretty flexible, but requires too much hardware to handle our load. In addition, we encountered particular issues with massive exports from it. </p>

<p><strong>HBase</strong> looks attractive since we already have Hadoop cluster. Yet, it's not really clear how to create secondary index for it and what its performance will be. </p>

<p><strong>Cassandra</strong> - may be an option, but we don't have experience with it (if you do, please share it)</p>

<p><strong>Couchbase</strong> - may be an option, but we don't have experience with it (if you do, please share it)</p>

<h2>Analytic storages</h2>

<p><strong>Relational DBMS (e.g. Oracle, PostreSQL)</strong> provide both - random access and efficient queries, but we have doubts that they can handle terabyte data.</p>

<p><strong>HDFS / Hive / SparkSQL</strong> - excellent for batch processing, but doesn't support indexing. The closest thing is partitioning, but it's not applicable given many-to-many relations (e.g. many users visited many URLs). Also, to our knowledge none of HDFS-backed tools except for HBase support updates, so you can only append new data and read latest version, which is not very convenient. </p>

<p><strong>Vertica</strong> has very efficient queries, but updates boil down to rewriting the whole file, so are terribly slow. </p>

<p>(Because of limited experience some of information above may be subjective or wrong, please feel free to comment about it)</p>

<hr>

<ol>
<li>Do any of the mentioned databases have useful options that we missed?</li>
<li>Is there any other database(s) optimized for your use case? If not, how  would you address this task? </li>
</ol>

