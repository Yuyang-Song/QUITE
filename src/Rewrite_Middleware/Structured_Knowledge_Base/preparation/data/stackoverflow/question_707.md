# MongoDb Aggregation (SQL UNION style)
[Link to question](https://stackoverflow.com/questions/38255279/mongodb-aggregation-sql-union-style)
**Creation Date:** 1467925674
**Score:** 0
**Tags:** mongodb, mongodb-query, aggregation-framework, union
## Question Body
<p>I need some help/advice on how to replicate some SQL behaviour in MongoDB.
Specifically, given this collection:</p>

<pre><code>{
  "_id" : ObjectId("577ebc0660084921141a7857"),
  "tournament" : "Wimbledon",
  "player1" : "Agassi",
  "player2" : "Lendl",
  "sets" : [{
      "score1" : 6,
      "score2" : 4,
      "tiebreak" : false
    }, {
      "score1" : 7,
      "score2" : 6,
      "tiebreak" : true
    }, {
      "score1" : 7,
      "score2" : 6,
      "tiebreak" : true
    }]
}
{
  "_id" : ObjectId("577ebc3560084921141a7858"),
  "tournament" : "Wimbledon",
  "player1" : "Ivanisevic",
  "player2" : "McEnroe",
  "sets" : [{
      "score1" : 4,
      "score2" : 6,
      "tiebreak" : false
    }, {
      "score1" : 3,
      "score2" : 6,
      "tiebreak" : false
    }, {
      "score1" : 6,
      "score2" : 4,
      "tiebreak" : false
    }]
}
{
  "_id" : ObjectId("577ebc7560084921141a7859"),
  "tournament" : "Roland Garros",
  "player1" : "Navratilova",
  "player2" : "Graf",
  "sets" : [{
      "score1" : 5,
      "score2" : 7,
      "tiebreak" : false
    }, {
      "score1" : 6,
      "score2" : 3,
      "tiebreak" : false
    }, {
      "score1" : 7,
      "score2" : 7,
      "tiebreak" : true
    }, {
      "score1" : 7,
      "score2" : 5,
      "tiebreak" : false
    }]
}
</code></pre>

<p>And these two distinct aggregations:</p>

<p><strong>1) Aggregation ALFA</strong>: this aggregation is purposely strange, in the sense that it is designed to find all matches where <strong>at least 1 tiebreak is true</strong> but <strong>only show sets where tiebreak is false</strong>. Please don't consider the logic of it, it is crafted to allow full freedom to the user.</p>

<pre><code>{
    $match: {
        "tournament": "Wimbledon",
        "sets.tiebreak": true
    }
},
{
    $project: {
        "tournament": 1,
        "player1": 1,
        "sets": {
            $filter: {
                input: "$sets",
                as: "set",
                cond: {
                    $eq: ["$$set.tiebreak", false]
                }
            }
        }
    }
}
</code></pre>

<p><strong>2) Aggregation BETA</strong>: this aggregation is purposely strange, in the sense that it is designed to find all matches where <strong>at least 1 tiebreak is false</strong> but <strong>only show sets where tiebreak is true</strong>. Please don't consider the logic of it, it is crafted to allow full freedom to the user. Please note that <strong>player1</strong> is hidden from the results.</p>

<pre><code>{
    $match: {
        "tournament": "Roland Garros",
        "sets.tiebreak": false
    }
},
{
    $project: {
        "tournament": 1,
        "sets": {
            $filter: {
                input: "$sets",
                as: "set",
                cond: {
                    $eq: ["$$set.tiebreak", true]
                }
            }
        }
    }
}
</code></pre>

<p>Now suppose that these two aggregations purpose is to delimit what part of the database a user can see, in the sense that those two queries delimit all the documents (and details) that are visible to the user. This is similar to 2 sql views that user has rights to access.</p>

<p><strong>I need/want to try to rewrite the previous distinct aggregations in only one. Can this be achieved?</strong></p>

<p>It is mandatory to keep all restriction that were set in Aggregation A &amp; B, without loosing any control on data and without leaking and data that was not available in query A or B.</p>

<p>Specifically, matches in Wimbledon can only be seen if they had at least one set which ended with a tiebreak. Player1 field CAN be seen. Single sets must be hidden if they did not end with a tiebreak and hidden otherwise. <em>If needed, it is acceptable, but not desirable, to not see player1 at all.</em></p>

<p>Conversely, matches in Roland Garros can be seen only if they had at least one set which ended without a tie break. Player1 field MUST be hidden. Single sets must be seen if they ended with a tiebreak and hidden otherwise.</p>

<p>Again, the purpose is to UNION the two aggregations while keeping the limits imposed by the two aggregations.</p>

<p>MongoDB is version 3.5, can be upgraded to unstable releases if needed.</p>

## Answers
### Answer ID: 38616574
<p>here's my two cents for the issue:<br>
if you wish to avoid empty sets when </p>

<ul>
<li>a "<em>Wimbledon</em>" doc has <strong>all</strong> <code>true</code> tibreaks,</li>
<li>or "<em>Roland Garros</em>" has <strong>all</strong> <code>false</code> tiebreaks</li>
</ul>

<p>you may reshape the query: </p>

<pre><code>...
 {
   $and: [{
     "sets.tiebreak": true,
   }, {
     "sets.tiebreak": false
   }],
   $or: [{
     "tournament": "Wimbledon"
   }, {
     "tournament": "Roland Garros"
   }]
 }
...
</code></pre>

<p>and use it in:  </p>

<ul>
<li>aggregate pipeline <a href="http://pastebin.com/cM6mNsuC" rel="nofollow">http://pastebin.com/cM6mNsuC</a>  </li>
<li>mapReduce (if performance is no a big issue..) <a href="http://pastebin.com/MShihSQL" rel="nofollow">http://pastebin.com/MShihSQL</a></li>
</ul>

