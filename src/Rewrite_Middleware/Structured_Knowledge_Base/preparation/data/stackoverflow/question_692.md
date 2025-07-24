# Slow MongoDB queries with Sails.js
[Link to question](https://stackoverflow.com/questions/37421228/slow-mongodb-queries-with-sails-js)
**Creation Date:** 1464114510
**Score:** 0
**Tags:** javascript, node.js, mongodb, sails.js, sails-mongo
## Question Body
<p>I wrote an app using Sails.js with mongoDb(sails-mongo).</p>

<p>Firstly, I decided to write all to a single document...
And database slowed on 5GB of data.. 
"Slowed" means that basic find query executed in 30-50s..  </p>

<p>Than I rewrite all in an multiple collections and add indexing..
example of my models:</p>

<p>Markets.js</p>

<pre><code>  module.exports = {
      attributes: {
        name: {
          type: 'string',
          index: true
        },
        pairs: {
         collection: 'Exchanges',
         via: 'source',
        }
      }
    };
</code></pre>

<p>and Exchanges.js</p>

<pre><code>module.exports = {

  attributes: {
    s1: {
      type: "string"
    },
    source:{
      model: "Maklers",
      index: true
    },
    s2: {
      type: "string"
    },
    p: {
      type: 'float'
    },
    v1: {
      type: 'float'
    },
    v2: {
      type: 'float'
    },
    vb: {
      type: 'float'
    }
  }
};
</code></pre>

<p>and example of slow query </p>

<pre><code>Markets.findOne({
          name: info,
          sort: 'createdAt DESC',
          limit: 1,
          createdAt: {
            '&lt;=': aft
          }
        }).populateAll().exec(function(err, items) {
          callback(err, items);
        });
</code></pre>

<p>result of db.stats</p>

<pre><code>&gt; db.stats()
{
    "db" : "stats222",
    "collections" : 8,
    "objects" : 36620661,
    "avgObjSize" : 238.26556139988844,
    "dataSize" : 8725442352,
    "storageSize" : 10033258480,
    "numExtents" : 63,
    "indexes" : 13,
    "indexSize" : 2940024192,
    "fileSize" : 14958985216,
    "nsSizeMB" : 16,
    "extentFreeList" : {
        "num" : 0,
        "totalSize" : 0
    },
    "dataFileVersion" : {
        "major" : 4,
        "minor" : 22
    },
    "ok" : 1
}
</code></pre>

<p>What you can advice me?
It`s about 2000 of records every minute..</p>

<p>How to increase perfomance?
Change db config? Change indexes? Change DB? Change models/collections config?</p>

<p>I using 2-core server with 2GB of Virtual Memory..
Sorry for bad english..</p>

## Answers
### Answer ID: 42207973
<p>There is a drawback in the 0.12 version of Waterline when using mongodb. By default waterline is not case sensitive, and mongodb is!</p>

<p>Your queries are slow, because when searching strings, it is being used a REGEX to find any case, so your indexes are useless. But you can change it, by disabling the case sensitiveness with the wlnex attribute:</p>

<pre><code>someMongodbServer: {
    adapter: 'sails-mongo',
    host: 'mongodb',
    port: 27017,
    user: 'username',
    password: 'password',
    database: 'databaseCoolName',
    wlNext: {
      caseSensitive: true
    }   
},
</code></pre>

<p>You can confirm this error by checking on the mongodb logs. And see what are the slow queries.</p>

