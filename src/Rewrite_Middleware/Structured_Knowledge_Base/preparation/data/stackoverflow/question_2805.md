# MongoDB index strategy for BSON `_id` vs String `id`?
[Link to question](https://stackoverflow.com/questions/53231202/mongodb-index-strategy-for-bson-id-vs-string-id)
**Creation Date:** 1541786981
**Score:** 0
**Tags:** mongodb, mongoid
## Question Body
<p>I have a question for the scholars.</p>

<pre><code>2018-11-09T19:01:39.896+0100 [conn1851] query database.collection 
  query: { 
    $query: { 
      id: "5bb79a18293609212200cbe2" 
    }, 
    $orderby: { 
      _id: 1 
    } 
  } 
planSummary: IXSCAN { _id: 1 } 
ntoskip:0 
nscanned:138476 
nscannedObjects:138476 
keyUpdates:0 
numYields:0 
locks(micros) 
r:127627 
nreturned:1 
reslen:497 
127ms
</code></pre>

<p>To me it looks like because I am not querying the <code>_id</code> with BSON then the index isn't used properly. Do I really have to create additional indexes for querying the database on the string value of the <code>_id</code> namely <code>id</code> or is it just the type mismatch or something?</p>

<p>These are the current indexes I have </p>

<pre><code>&gt; db.collection.getIndexes()
[
    {
        "v" : 1,
        "key" : {
            "_id" : 1
        },
        "name" : "_id_",
        "ns" : "database.collection"
    },
    {
        "v" : 1,
        "key" : {
            "sport_id" : 1
        },
        "name" : "sport_id_1",
        "ns" : "database.collection"
    },
    {
        "v" : 1,
        "key" : {
            "sport_id" : 1,
            "updated_at" : -1
        },
        "name" : "sport_id_1_updated_at_-1",
        "ns" : "database.collection"
    },
    {
        "v" : 1,
        "key" : {
            "external_ids.id" : 1
        },
        "name" : "external_ids.id_1",
        "ns" : "database.collection"
    }
]
</code></pre>

<p>I am currently on mongodb 2.6.12 and using mongoid v 2.5 i think.</p>

<p>This is part of what a document looks like:</p>

<pre><code>{ 
  "_id" : ObjectId("593a61de2936093a460004ca"), 
  "sport_id" : ObjectId("592eefe3293609345c000867")
  "id" : "593a61de2936093a460004ca", 
  "created_at" : ISODate("2017-06-09T08:52:46Z") 
}
</code></pre>

<p>Looks like all our documents are also saving the string representation of the <code>_id</code>. This is just horribly wrongly modeled huh?</p>

<p>I didn't create this mess but I will have to fix it. Any suggestions how to proceed from this? Looks like we are for unknown reasons duplicating the <code>_id</code> into an <code>id</code>. Should I just index that or is there a better fix? I might have to rewrite this question come to think of it...</p>

