# Finding ID of mongo documents with duplicated elements in nested array
[Link to question](https://stackoverflow.com/questions/69235217/finding-id-of-mongo-documents-with-duplicated-elements-in-nested-array)
**Creation Date:** 1631972652
**Score:** 1
**Tags:** database, mongodb, mongodb-query, nosql, nosql-aggregation
## Question Body
<p>I would like to extract from the collection the IDs of documents that have duplicate IDs of &quot;drives&quot; objects that are nested in the array that is in &quot;streetModel&quot;.<br />
This is my typical document :</p>
<pre><code>  {
    &quot;_id&quot;: {
        &quot;$oid&quot;: &quot;61375bec4fa522001b608568&quot;
    },
    &quot;name&quot;: &quot;Streetz&quot;,
    &quot;statusDetail&quot;: {},
    &quot;streetModel&quot;: {
        &quot;_id&quot;: &quot;3.7389-51.0566&quot;,
        &quot;name&quot;: &quot;Kosheen - Darude - Swedish - Trynidad - Maui&quot;,
        &quot;countryCode&quot;: &quot;DEN&quot;,
        &quot;drives&quot;: [{
            &quot;_id&quot;: -903500698,
            &quot;direction&quot;: &quot;WEST&quot;
            }, {
            &quot;_id&quot;: 1915399546,
            &quot;direction&quot;: &quot;EAST&quot;
            }, {
            &quot;_id&quot;: 1294835467,
            &quot;direction&quot;: &quot;NORTH&quot;
            }, {
            &quot;_id&quot;: 1248969937,
            &quot;direction&quot;: &quot;EAST&quot;
            }, {
            &quot;_id&quot;: 1248969937,
            &quot;direction&quot;: &quot;EAST&quot;
            }, {
            &quot;_id&quot;: 1492411786,
            &quot;direction&quot;: &quot;SOUTH&quot;
                }]
    },
    &quot;createdAt&quot;: {
            &quot;$date&quot;: &quot;2021-09-07T12:32:44.238Z&quot;
        }
    }
</code></pre>
<p>In this particular document with the ID 61375bec4fa522001b608568, in &quot;streetModel&quot;, in &quot;drives&quot; array I have got duplicated drives objects with id 1248969937.<br />
I would like to create a query to the database that will return the ID of all documents with such a problem (duplicate &quot;drives&quot;).<br />
Right now I have got this:</p>
<pre><code>db.streets.aggregate([
  {
    $unwind: &quot;$streetModel&quot;
  },
  {
    $unwind: &quot;$drives&quot;
  },
  {
    $group: {
      _id: {
        id: &quot;$_id&quot;
      },
      sum: {
        $sum: 1
      },

    }
  },
  {
    $match: {
      sum: {
        $gt: 1
      }
    }
  },
  {
    $project: {
      _id: &quot;$_id._id&quot;,
      duplicates: {
        drives: &quot;$_id&quot;
      }
    }
  }
])
</code></pre>
<p>but that's not it.<br />
I try in many ways to rewrite this query, but unfortunately it doesn't work.</p>

## Answers
### Answer ID: 69236064
<p>Query</p>
<ul>
<li>unwind</li>
<li>group by document id + driverid</li>
<li>keep only those that had more than one time same driveid</li>
<li>replace-root is to make the document better looking, you could $project also instead</li>
<li>if you need any more stage i think you can add it, for examplpe to get the documents that have this problem project only the docid's</li>
</ul>
<p><a href="https://mongoplayground.net/p/hhvQNzUlaJk" rel="nofollow noreferrer">Test code here</a></p>
<pre class="lang-js prettyprint-override"><code>db.collection.aggregate([
  {
    &quot;$unwind&quot;: {
      &quot;path&quot;: &quot;$streetModel.drives&quot;
    }
  },
  {
    &quot;$group&quot;: {
      &quot;_id&quot;: {
        &quot;docid&quot;: &quot;$_id&quot;,
        &quot;driveid&quot;: &quot;$streetModel.drives._id&quot;
      },
      &quot;duplicates&quot;: {
        &quot;$push&quot;: &quot;$streetModel.drives.direction&quot;
      }
    }
  },
  {
    &quot;$match&quot;: {
      &quot;$expr&quot;: {
        &quot;$gt&quot;: [
          {
            &quot;$size&quot;: &quot;$duplicates&quot;
          },
          1
        ]
      }
    }
  },
  {
    &quot;$replaceRoot&quot;: {
      &quot;newRoot&quot;: {
        &quot;$mergeObjects&quot;: [
          &quot;$_id&quot;,
          &quot;$$ROOT&quot;
        ]
      }
    }
  },
  {
    &quot;$project&quot;: {
      &quot;_id&quot;: 0
    }
  }
])
</code></pre>

