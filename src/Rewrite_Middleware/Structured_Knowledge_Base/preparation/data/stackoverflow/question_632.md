# Can I expect a significant performance boost by moving a large key value store from MySQL to a NoSQL DB?
[Link to question](https://stackoverflow.com/questions/3426587/can-i-expect-a-significant-performance-boost-by-moving-a-large-key-value-store-f)
**Creation Date:** 1281118815
**Score:** 7
**Tags:** mysql, nosql, cassandra, tokyo-cabinet
## Question Body
<p>I'm developing a database that holds large scientific datasets. Typical usage scenario is that on the order of 5GB of new data will be written to the database every day; 5GB will also be deleted each day. The total database size will be around 50GB. The server I'm running on will not be able to store the entire dataset in memory.</p>

<p>I've structured the database such that the main data table is just a key/value store consisting of a unique ID and a Value.</p>

<p>Queries are typically for around 100 consecutive values,
eg. <code>SELECT Value WHERE ID BETWEEN 7000000 AND 7000100;</code></p>

<p>I'm currently using MySQL / MyISAM, and these queries take on the order of 0.1 - 0.3 seconds, but recently I've come to realize that MySQL is probably not the optimal solution for what is basically a large key/value store.</p>

<p>Before I start doing lots of work installing the new software and rewriting the whole database I wanted to get a rough idea of whether I am likely to see a significant performance boost when using a NoSQL DB (e.g. Tokyo Tyrant, Cassandra, MongoDB) instead of MySQL for these types of retrievals.</p>

<p>Thanks</p>

## Answers
### Answer ID: 3469665
<p>Please consider also <a href="http://www.orientechnologies.com" rel="nofollow noreferrer">OrientDB</a>. It uses indexes with RB+Tree algorithm. In my tests with 100GB of database reads of 100 items took 0.001-0.015 seconds on my laptop, but it depends how the key/value are distributed inside the index.</p>

<p>To make your own test with it should take less than 1 hour.</p>

<p>One bad news is that OrientDB not supports a clustered configuration yet (planned for September 2010).</p>

### Answer ID: 3434226
<p>I would expect Cassandra to do better where the dataset does not fit in memory than a b-tree based system like TC, MySQL, or MongoDB.  Of course, Cassandra is also designed so that if you need more performance, it's trivial to add more machines to support your workload.</p>

### Answer ID: 3438883
<p>I use MongoDB in production for a write intensive operation where I do well over the rates you are referring to for both WRITE and READ operations, the size of the database is around 90GB and a single instance (amazon m1.xlarge) does 100QPS I can tell you that a typical key->value query takes about 1-15ms on a database with 150M entries, with query times reaching the 30-50ms time under heavy load.
at any rate 200ms is way too much for a key/value store.</p>

<p>If you only use a single commodity server I would suggest mongoDB as it quite efficient and easy to learn
if you are looking for a distributed solution you can try any Dynamo clone:
Cassandra (Facebook) or Project Volemort (LinkedIn) being the most popular.
keep in mind that looking for strong consistency slows down these systems quite a bit.</p>

