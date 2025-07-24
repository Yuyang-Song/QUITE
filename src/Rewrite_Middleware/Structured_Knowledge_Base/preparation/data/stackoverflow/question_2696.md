# Sliding window with cosmos db temporarily loses records
[Link to question](https://stackoverflow.com/questions/47950339/sliding-window-with-cosmos-db-temporarily-loses-records)
**Creation Date:** 1514010617
**Score:** 0
**Tags:** azure-cosmosdb, azure-stream-analytics
## Question Body
<p>I have what I figure is a pretty standard setup </p>

<pre><code>Event hubs -&gt; stream analytics -&gt;cosmosdb sql
</code></pre>

<p>As events come in I have a stream analytics query which adds up the values using a sliding window of 60 minutes and writes to cosmos. I'd expect at most 5000messages/hr which would update a particular record in cosmos. My problem is that records in cosmos seem to be deleted and rewritten instead of being updated. There is quite a long period (30 seconds+) when no record is visible even though one should be. Eventually, a record shows up with updated values. </p>

<p>I can only think that as events enter and exit the sliding window they're causing updates which rewrite the record rather than updating it and that I'm querying the database during that window. This is obviously a pretty irritating issue and I'm sure I must be doing something wrong to have this behaviour. Is there some setting or some diagnostics which might shed some light on the issue?</p>

<p>I've tried playing with the consistency levels in cosmos but they don't seem to have much impact on what I'm seeing. I'm running my cosmos collections at 5000RU but I'm only pumping through about 10RU's worth of data. So there are no scaling issues. </p>

<p>My query looks like </p>

<pre><code>SELECT
    concat(cast(groupid as nvarchar(max)), ':',  cast(IPV4_SRC_ADDR as nvarchar(max))) as partitionkey,
    concat(cast(L7_PROTO_NAME as nvarchar(max)), ':lastHour') as Id,
    System.timestamp as outputtime,
    groupid,
    IPV4_SRC_ADDR,
    L7_PROTO_NAME,
    sum(IN_BYTES + OUT_BYTES) as TOTAL_BYTES
INTO
    layer7sql
FROM
    source TIMESTAMP BY [timestamp]
Group by groupid,
         IPV4_SRC_ADDR,
         L7_PROTO_NAME,
         slidingwindow(Minute,60)
</code></pre>

<p>I'm happy to provide any other debugging information which could be useful in understanding my issue. </p>

<p><strong>Additional</strong>
The _rid of the records remains the same. These are the output settings I have </p>

<p><a href="https://i.sstatic.net/RLy9k.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/RLy9k.png" alt="enter image description here"></a></p>

<p>When I query I get back </p>

<pre><code>{
    "_rid": "glpSAPQhPgA=",
    "Documents": [
        {
            "partitionkey": "2587:10.1.2.194",
            "id": "SSL:lastHour",
            "outputtime": "2017-12-23T06:28:40.960916Z",
            "groupid": "2587",
            "ipv4_src_addr": "10.1.2.194",
            "l7_proto_name": "SSL",
            "total_bytes": 322,
            "_rid": "glpSAPQhPgAMAAAAAAAAAA==",
            "_self": "dbs/glpSAA==/colls/glpSAPQhPgA=/docs/glpSAPQhPgAMAAAAAAAAAA==/",
            "_etag": "\"02001fd6-0000-0000-0000-5a3df7cd0000\"",
            "_attachments": "attachments/",
            "_ts": 1514010573
        }
    ],
    "_count": 1
}
</code></pre>

<p>and the query I'm using via the REST api is </p>

<pre><code>{
    "query": "select * from root r where r.ipv4_src_addr='10.1.2.194' and r.id='SSL:lastHour' order by r.total_bytes desc",
    "parameters": []
} 
</code></pre>

<p>I am specifying a partition key there including the field IPV4_SRC_ADDR but I don't think this is actually a partitioned collection. As an experiment I updated my query to </p>

<pre><code>SELECT
    concat(cast(L7_PROTO_NAME as nvarchar(max)), ':lastHour') as Id,
    System.timestamp as outputtime,
    groupid,
    L7_PROTO_NAME,
    sum(IN_BYTES + OUT_BYTES) as TOTAL_BYTES
INTO
    layer7sql
FROM
    NProbe TIMESTAMP BY [timestamp]
Group by groupid,
         L7_PROTO_NAME,
         slidingwindow(Minute,60)
</code></pre>

<p>So far that appears to be working better. I wonder if maybe I had some conflicts were taking a while to resolve and during that time window the records weren't visible. </p>

