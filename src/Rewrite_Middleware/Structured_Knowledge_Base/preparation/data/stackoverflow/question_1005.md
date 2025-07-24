# How to transform an UNWIND query to FOREACH in Neo4J Cypher?
[Link to question](https://stackoverflow.com/questions/54309379/how-to-transform-an-unwind-query-to-foreach-in-neo4j-cypher)
**Creation Date:** 1548163731
**Score:** 0
**Tags:** foreach, neo4j, cypher
## Question Body
<p>I have the following Neo4J Cypher query:</p>

<pre><code>UNWIND $mentionsRelations as mention 
MATCH (u:User{name:mention.from}) 
RETURN u.uid;
</code></pre>

<p>The params are: </p>

<pre><code>{
  "mentionsRelations": [
    {
      "from": "a",
      "to": "b"
    },
    {
      "from": "c",
      "to": "d"
    }
  ]
}
</code></pre>

<p>Is it possible to rewrite it to get the same results using the <code>FOREACH</code> query?</p>

<p>I know it doesn't accept the <code>MATCH</code> parameter, but I'm just curious if there's a workaround to get the same results?</p>

<p>Basically what I want is to reiterate through the <code>mentionsRelations</code> using <code>FOREACH</code> and to then output any matches in the database it uncovers.</p>

<p>Thanks!</p>

## Answers
### Answer ID: 54313758
<p>Not currently possible, FOREACH is only for write operations and can't be used for just matching to nodes.</p>

<p>Is there some reason UNWIND won't work for you?</p>

<p>You can also do a match based upon list membership, which should work similarly, though you'd have to extract out the values to use for the property match:</p>

<pre><code>WITH [mention in $mentionsRelationships | mention.from] as froms
MATCH (u:User) 
WHERE u.name in froms
RETURN u.uid;
</code></pre>

