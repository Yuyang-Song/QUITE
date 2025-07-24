# Data is loss when I use the UNWIND
[Link to question](https://stackoverflow.com/questions/45707750/data-is-loss-when-i-use-the-unwind)
**Creation Date:** 1502869211
**Score:** -1
**Tags:** database, neo4j, cypher, neo4j-ogm
## Question Body
<pre><code>MATCH (ORG:ORG)-[ORGHASPROBLEM:HAS]-&gt;(PROBLEM:PROBLEM) WITH PROBLEM,

extract(NUM IN filter( V IN collect({ PROB1:PROBLEM.PROB_ID, PROB2:PROBLEM.REGION}) where V.PROB2= 'LONDON') | NUM.PROB1) AS MEASURES1,

extract(NUM IN filter( V IN collect({ PROB1:PROBLEM.PROB_ID, PROB2:PROBLEM.REGION}) where V.PROB2= 'PARIS') | NUM.PROB1) AS MEASURES2

unwind MEASURES1 AS RESULT1
unwind MEASURES2 AS RESULT2

RETURN DISTINCT PROBLEM.SLAB AS DIMENSION,count(RESULT1) AS  MEASURES1,count(RESULT2) AS MEASURES2
</code></pre>

<hr>

<p>I am uploading the image of the database and expected output. Can anybody rewrite the query or tell me where I am going wrong?</p>

<p>My question is that MEASURES1 and MEASURES2 have my required data. When I am using the unwind <code>MEASURES1 AS RESULT1</code> it give the output as required, but in case of the 2nd unwind (unwind <code>MEASURES2 AS RESULT2</code>) it removes the entire data from <code>MEASURES1</code> and <code>MEASURES2</code>.</p>

<p>Please, see the attached image to understand the scenario more clearly.</p>

<p><a href="https://i.sstatic.net/hztsC.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/hztsC.png" alt="Data model, expected output"></a></p>

## Answers
### Answer ID: 45718973
<p>The follow query will get the data out of the database in a way that will allow you to build your report. As a bonus it will also work if you add a new region :</p>

<pre><code>MATCH (p:PROBLEM)
WITH count(*) AS ct, p.REGION AS pregion, p.SLAB AS slab
RETURN slab, collect({region: pregion,  count: ct}) as result;
</code></pre>

<p>Hope this helps.</p>

<p>Regards,
Tom</p>

