# Ordering a sequence of writes to MongoDB v4.0 / DocumentDB
[Link to question](https://stackoverflow.com/questions/71620208/ordering-a-sequence-of-writes-to-mongodb-v4-0-documentdb)
**Creation Date:** 1648225667
**Score:** 0
**Tags:** mongodb, pymongo, aws-documentdb
## Question Body
<h2>Problem</h2>
<p>I need to establish write consistency for a sequence of queries using <code>updateMany</code>, against a DocumentDB cluster with only a single primary instance. I am not sure which approach to use, between Transactions, <em>ordered</em> BulkWrites, or simply setting a <em>Majority</em> write concern for each <code>updateMany</code> query.</p>
<h2>Environment</h2>
<p>AWS DocumentDB cluster, which maps to MongoDB v4.0, via pymongo 3.12.0 .</p>
<p>Note: the cluster has a single primary instance, and no other instances. In practice, AWS will have us connect to the cluster in replica set mode. I am not sure whether this means we need to still think about this problem in terms of replica sets.</p>
<h2>Description</h2>
<p>I have a sequence of documents <code>D</code> , each of which is an array of records. Each record is of the form <code>{field: MyField, from_id: A, to_id: B}</code>.</p>
<p>To process a record, I need to look in my DB for all fields <code>MyField</code> that have value <code>A</code>, and then set that value to <code>B</code>. The actual query I use to do this is <code>updateMany</code>. The code looks something like:</p>
<pre class="lang-py prettyprint-override"><code>for doc in Documents:
  for record in doc: 
    doWriteUpdate(record)

def doWriteUpdate(record):
  query = ... # format the query based on record's information
  db.updateMany(query)
</code></pre>
<p><strong>I need the update operations to happen such that the writes have actually been applied, and are visible, before the next <code>doWriteUpdate</code> query runs.</strong></p>
<p>This is because I expect to encounter a situation where I can have a record <code>{field: MyField, from_id: A, to_id: B}</code>, and then a subsequent record (whether in the same document, or a following document) <code>{field: MyField, from_id: B, to_id: C}</code>. Being able to properly apply the latter record operation, depends on the former record operation having been committed to the database.</p>
<h2>Possible Approaches</h2>
<h5>Transactions</h5>
<p>I have tried wrapping my <code>updateMany</code> operation in a Transaction. If this had worked, I would have called it a day; but I exceed the size allowed: <code>Total size of all transaction operations must be less than 33554432</code>. Without rewriting the queries, this cannot be worked around, because the <code>updateMany</code> has several layers of array-filtering, and digs through a lot of documents. I am not even sure if transactions are appropriate in this case, because I am not using any replica sets, and they seem to be intended for ACID with regard to replication.</p>
<h4>Ordered Bulk Writes</h4>
<p><a href="https://www.mongodb.com/docs/v4.0/reference/method/db.collection.bulkWrite/#bulkwrite-write-operations-updateonemany" rel="nofollow noreferrer">BulkWrite.updateMany</a> would appear to guarantee execution order of a sequence of writes. So, one approach could be, to generate the update query strings for each record <code>r</code> in a document <code>D</code>, and then send those through (preserving order) as a BulkWrite. While this would seem to &quot;preserve order&quot; of execution, I don't know if a) the preservation of execution order, also guarantees write consistency (everything executed serially is applied serially), and, more important, b) whether the <em>following</em> BulkWrites, for the other documents, will interleave with this one.</p>
<h4>WriteConcern</h4>
<p><a href="https://pymongo.readthedocs.io/en/3.12.0/api/pymongo/write_concern.html#pymongo.write_concern.WriteConcern" rel="nofollow noreferrer">Pymongo</a> states that writes will block given a desired WriteConcern. My session is single-threaded, so this should give the desired behavior. However, <a href="https://www.mongodb.com/docs/v4.0/reference/write-concern/#acknowledgment-behavior" rel="nofollow noreferrer">MongoDB</a> says</p>
<blockquote>
<p>For multi-document transactions, you set the write concern at the transaction level, not at the individual operation level. Do not explicitly set the write concern for individual write operations in a transaction.</p>
</blockquote>
<p>I am not clear on whether this pertains to &quot;transactions&quot; as in the general sense, or MongoDB Transactions set up through session objects. If it means the latter, then it shouldn't apply to my use case. If the former, then I don't know what other approach to use.</p>

## Answers
### Answer ID: 71634192
<p>The proper write concern is majority, and with a read concern that uses the <a href="https://www.mongodb.com/docs/manual/reference/read-concern-linearizable/#mongodb-readconcern-readconcern.-linearizable-" rel="nofollow noreferrer">linearizable</a></p>
<blockquote>
<p><strong>Real Time Order Combined</strong> with &quot;majority&quot; write concern, &quot;linearizable&quot;
read concern enables multiple threads to perform reads and writes on a
single document as if a single thread performed these operations in
real time; that is, the corresponding schedule for these reads and
writes is considered linearizable.</p>
</blockquote>

