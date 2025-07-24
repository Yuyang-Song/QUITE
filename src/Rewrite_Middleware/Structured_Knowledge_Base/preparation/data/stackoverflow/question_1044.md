# Lookup using an ID array with pipeline
[Link to question](https://stackoverflow.com/questions/56272507/lookup-using-an-id-array-with-pipeline)
**Creation Date:** 1558604949
**Score:** 1
**Tags:** javascript, arrays, mongodb, object
## Question Body
<p>I was trying to write a lookup function that takes an array with object ids and timestamps of object y. This worked flawlessly with <code>localflied</code> and <code>foreignfield</code> but I cannot reproduce the same result using pipeline.</p>

<p>(Names like <code>y</code> are made up to keep it general)</p>

<p>Working version:</p>

<pre><code>$lookup: {
   from: 'y',
   localField: 'ys.object_id',
   foreignField: '_id',
   as: 'docs',
},
</code></pre>

<p><code>ys</code> is an array of objects structured like this:</p>

<pre><code>{
  object_id: ObjectID(),
  timestamp: Date(),
}
</code></pre>

<p>I would like to rewrite this expression to use pipeline because I already want to filter some of the objects looked up out using their timestamp attribute.</p>

<p>What I have tried:</p>

<pre><code>$lookup: {
   from: 'y',
   let: { ys: '$ys' },
   pipeline: [
     {
       $match: { $expr: { $eq: ['$_id', '$$ys.object_id'] } },
     },
   ],
   as: 'docs',
},
</code></pre>

<p>Database size: <strong>20.4GB</strong></p>

<p>Full Query:</p>

<pre><code>const query = [
  {
    $match: { 'ys.timestamp': { $lte: date, $gt: previousMonth } },  // I have shorten this part a little (It's not the same but the logic was flawed anyway)
  },
  {
    $limit: 100,
  },
  {
    $lookup: {
      from: 'y',
      let: { ys: '$ys' },
      pipeline: [
        {
          $match: { $expr: { $in: ['$_id', '$$ys.object_id'] } },
        },
        {
          $sort: { timestamp: -1 },
        },
        {
          $limit: 1,
        },
      ],
      as: 'doc',
    },
  },
];
</code></pre>

<p>The above solution doesn't work it seems to get stuck and never actually return anything. (Times out after some time)</p>

<p>Is there a proper way of rewriting the working solution to a pipeline solution?</p>

<p><strong>IMPORTANT</strong>:
I have changed the query to look for one specific element by ID and then perform the lookup. This action did work but took about 20 seconds. I am pretty certain this is why my query times out when I run it with my usual query. Can anyone explain why there is a performance difference between the 2 approaches and if I can somehow bypass that?</p>

## Answers
### Answer ID: 56272673
<p>Very close - use <a href="https://docs.mongodb.com/manual/reference/operator/query/in" rel="nofollow noreferrer"><code>$in</code></a> instead of <a href="https://docs.mongodb.com/manual/reference/operator/query/eq" rel="nofollow noreferrer"><code>$eq</code></a>:</p>

<pre><code>$lookup: {
   from: 'y',
   let: { ys: '$ys' },
   pipeline: [
     {
       $match: { $expr: { $in: ['$_id', '$$ys.object_id'] } },
     },
   ],
   as: 'docs',
},
</code></pre>

<p>If you use <code>$eq</code> you're looking for a value that is equal to that array. Using <code>$in</code> means you're looking for a value that is contained within that array (like <code>includes</code>).</p>

