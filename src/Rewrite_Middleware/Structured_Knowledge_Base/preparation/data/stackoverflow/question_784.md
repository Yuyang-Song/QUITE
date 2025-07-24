# Creating Spring Data Aggregation of multiple MongoDB queries
[Link to question](https://stackoverflow.com/questions/42055477/creating-spring-data-aggregation-of-multiple-mongodb-queries)
**Creation Date:** 1486318092
**Score:** 1
**Tags:** java, spring, mongodb
## Question Body
<p>The database MongoDB I have stored documents in the format:</p>

<pre><code>    {
      "achievement": [
        {
          "userFromId":"max",
          "userToId":"peter",
          "date":"2016-01-25",
          "pointCount":1,
          "description":"good work",
          "type":"THANKS"
        }
      ]
    }
</code></pre>

<p>How to get the number of records in the database (if any) for the a certain date, in which people are thanking the other people.
I created a query to retrieve data:</p>

<pre><code>    DBObject clause1 = new BasicDBObject("userFromId", userFromId);
    DBObject clause2 = new BasicDBObject("userToId", userToId);
    DBObject clause3 = new BasicDBObject("sendDate", localDate);
    DBObject clause4 = new BasicDBObject("type", Thanks);
    BasicDBList or = new BasicDBList();
    or.add(clause1);
    or.add(clause2);
    or.add(clause3);
    or.add(clause4);
    DBObject query = new BasicDBObject("$or", or);
</code></pre>

<p>But I do not know how to get the number of records and how can rewrite the query using aggregation?
For example:</p>

<pre><code>        Aggregation aggregation = Aggregation.newAggregation(
            Aggregation.group("userFromId")
                .first("userFromId").as("userFromId")
                .sum("pointCount").as("pointCount"));
</code></pre>

<p>I do not know how to add a few more parameters.
What the return request if the data to the database does not exist?</p>

<p>Thanks for any help</p>

## Answers
### Answer ID: 42056261
<p>You can use something like this. This will count all the number of documents matching the below criteria.   </p>

<p>Regular Query</p>

<pre><code>db.collection.count({ $or: [ { "userFromId": userFromId }, { "userToId": userToId } ] });
</code></pre>

<p>Using Aggregation</p>

<pre><code>db.collection.aggregate( [
  { $match: { $or: [ { "userFromId": userFromId }, { "userToId": userToId } ] } },
  { $group: { _id: null, count: { $sum: 1 } } }
] );
</code></pre>

