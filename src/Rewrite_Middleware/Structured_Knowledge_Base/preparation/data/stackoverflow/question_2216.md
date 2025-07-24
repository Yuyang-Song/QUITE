# MongoDB Array matching 6 from 10
[Link to question](https://stackoverflow.com/questions/24329493/mongodb-array-matching-6-from-10)
**Creation Date:** 1403274193
**Score:** 0
**Tags:** javascript, mongodb, meteor
## Question Body
<p>I have a collection in mongodb with thousand documents like this : </p>

<pre><code>{
    "numbers" : [
            31,
            12,
            19,
            41,
            2,
            15
    ],
    "date" : ISODate("2014-06-18T09:37:59.164Z"),
    "string" : "31,12,19,41,2,15",
    "_id" : "Eg38tNEZFtTZTmxjx"
}
</code></pre>

<p>I also have an match array like [1,2,3,4,5,6,7,8,10]</p>

<p>How can I query documents that match 6 numbers from the match array;</p>

<p>I know this: db.collection.find({ numbers: { $all: [ 1 , 2, 3, 4, 5, 6 ] } });</p>

<p>but this limits me to checking a match array with only 6 numbers, i want the match array be with 10 numbers and only return the documents that have 6 numbers from those 10.</p>

<p>p.s. I can change the form of document if it's needed to add any field to it. To make the match perform faster. I can rewrite the whole database it's not a problem.</p>

## Answers
### Answer ID: 24330125
<p>I would say your best starting point is investigating the mongodb $where operator:</p>

<p><a href="http://docs.mongodb.org/manual/reference/operator/query/where/" rel="nofollow">http://docs.mongodb.org/manual/reference/operator/query/where/</a></p>

<p>That gives you the opportunity to write a custom function for the comparison.  However, if performance is a concern you may have to revisit your model design to allow for better indexing.</p>

<p>Example code for reducing an array to matches:</p>

<pre><code>var numbers = [31,12,19,41,2,15,1,4,3,7,5];
var matchArray = [1,2,3,4,5,6,7,8,9,10];
function isInList() {
    var reducedNums = numbers.filter(function(num) {
        return matchArray.indexOf(num) !== -1
    });

    console.log(reducedNums);
}
</code></pre>

<p>With the <code>reducedNums</code> you'll be able to check the length to make sure it's >= 6.</p>

<p>To use that in a query you can do something like:</p>

<pre><code>var matchArray = [1,2,3,4,5,6,7,8,9,10];

function isInList() {
    // `this` contains each object in the mongo query.
    var reducedNums = this.numbers.filter(function(num) {
        return matchArray.indexOf(num) !== -1
    });
    return reducedNums.length &gt;= 6;
}

db.myDocuments.find({ $where: isInList });
</code></pre>

<p>That code is untested, fyi.</p>

