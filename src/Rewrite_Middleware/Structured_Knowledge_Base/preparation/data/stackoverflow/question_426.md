# Neo4j: MERGE with comma in pattern throws &#39;Invalid syntax&#39;, unlike MATCH or CREATE
[Link to question](https://stackoverflow.com/questions/25601380/neo4j-merge-with-comma-in-pattern-throws-invalid-syntax-unlike-match-or-crea)
**Creation Date:** 1409558735
**Score:** 2
**Tags:** neo4j, cypher
## Question Body
<p>Good morning,</p>

<p>To achieve idempotence I use Neo4j's <code>MERGE</code> keyword to insert patterns into my database. For example, I might insert a user and his friends like this:</p>

<pre><code>MERGE (friend:User)&lt;-[:FRIEND]-(me:User)-[:FRIEND]-&gt;(anotherfriend:User);
</code></pre>

<p>I thought I could rewrite the same statement like this:</p>

<pre><code>MERGE (me:User)-[:FRIEND]-&gt;(friend:User), (me)-[:FRIEND]-&gt;(anotherfriend:User);
</code></pre>

<p>But this results in this error:</p>

<pre><code>Invalid input ',': expected whitespace, a relationship pattern, ON, LOAD CSV, START, MATCH, UNWIND, MERGE, CREATE, SET, DELETE, REMOVE, FOREACH, WITH, RETURN, UNION, ';' or end of input (line 1, column 41)
"MERGE (me:User)-[:FRIEND]-&gt;(friend:User), (me)-[:FRIEND]-&gt;(anotherfriend:User);"
</code></pre>

<p><code>MATCH</code> and <code>CREATE</code> do support this syntax. Is there any reason why <code>MERGE</code> doesn't? Is it simply something that hasn't been implemented yet?</p>

<p>Note: this is not an actual query I'm using in my application but just something simple to illustrate my point.</p>

<p>Thanks,
Jan</p>

## Answers
### Answer ID: 25613430
<p>I consider this being a imperfection of the cypher implementation. Please file a github issue at <a href="https://github.com/neo4j/neo4j/issues" rel="nofollow">https://github.com/neo4j/neo4j/issues</a> for this.</p>

