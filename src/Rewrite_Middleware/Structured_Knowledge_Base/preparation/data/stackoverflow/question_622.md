# How can I optimise an extremely slow MySQL query that uses COUNT DISTINCT
[Link to question](https://stackoverflow.com/questions/33943140/how-can-i-optimise-an-extremely-slow-mysql-query-that-uses-count-distinct)
**Creation Date:** 1448554821
**Score:** 0
**Tags:** mysql, sql, database
## Question Body
<p>I have a very slow MySQL query that I would like to optimise. </p>

<p>The query is taking <strong>66.2070 seconds</strong> to return 5 results from tables containing around 200 rows.</p>

<p>The database tables store <code>users</code>, <code>experiments</code> (A/B tests), <code>goals</code> (page URLs), <code>visits</code> (page visits) and <code>conversions</code> (clicks a goal's URL). The <code>visit</code> and <code>conversion</code> tables both have a <code>combination</code> column that records if version A or B of a page was visited or a conversion came from version A or B. Combinations are stored in the db as <code>1</code> or <code>2</code>.</p>

<p>I'm trying to get a list of a user's experiments with the number of visits and conversions for each combination.</p>

<p>For some relationships I'm using composite primary keys, which does make the joins more complicated. I doubt it but could this be the cause of the problem?</p>

<p>How can I rewrite this query to make it run in a reasonable time, at least less than a second?</p>

<p>Here's my database schema:</p>

<p><a href="https://i.sstatic.net/QPtqT.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/QPtqT.png" alt="Database schema diagram"></a> </p>

<p>and her's my query:</p>

<pre><code>SELECT e.id                  AS id, 
       e.name                AS name, 
       e.status              AS status, 
       e.created             AS created, 
       Count(DISTINCT v1.id) AS visits1, 
       Count(DISTINCT v2.id) AS visits2, 
       Count(DISTINCT c1.id) AS conversions1, 
       Count(DISTINCT c2.id) AS conversions2 
FROM   experiment e 
       LEFT JOIN visit v1 
              ON ( v1.experiment_id = e.id 
                   AND v1.user_id = e.user_id 
                   AND v1.combination = 1 ) 
       LEFT JOIN visit v2 
              ON ( v2.experiment_id = e.id 
                   AND v2.user_id = e.user_id 
                   AND v2.combination = 2 ) 
       LEFT JOIN goal g 
              ON ( g.experiment_id = e.id 
                   AND g.user_id = e.user_id 
                   AND g.principal = 1 ) 
       LEFT JOIN conversion c1 
              ON ( c1.experiment_id = e.id 
                   AND c1.user_id = e.user_id 
                   AND c1.goal_id = g.id 
                   AND c1.combination = 1 ) 
       LEFT JOIN conversion c2 
              ON ( c2.experiment_id = e.id 
                   AND c2.user_id = e.user_id 
                   AND c2.goal_id = g.id 
                   AND c2.combination = 2 ) 
WHERE  e.user_id = 25 
GROUP  BY e.id 
ORDER  BY e.created DESC 
LIMIT  5 
</code></pre>

<p>The resulting table should look something like this:</p>

<p><a href="https://i.sstatic.net/sTmVs.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/sTmVs.png" alt="Results table"></a></p>

## Answers
### Answer ID: 33943346
<p>For your question about the drawback of using composite keys I found this:</p>

<p><a href="https://stackoverflow.com/a/1460629/5605294">Drawback of composite keys</a></p>

<p>I can't currently test ur database but use the <code>EXPLAIN</code> syntax in mysql to find out what is wrong with the perfomance of ur query:</p>

<p><a href="http://dev.mysql.com/doc/refman/5.7/en/using-explain.html" rel="nofollow noreferrer">MySQL docs about EXPLAIN and optimizing ur query with EXPLAIN</a></p>

### Answer ID: 33943316
<p>You should do the aggregations before doing the joins, to avoid getting large intermediate results.  I think the logic is</p>

<pre><code>SELECT e.id, e.name, e.status, e.created, 
       v.visits1, v.visits2, g.conversions1, g.conversions2 
FROM experiment e LEFT JOIN
     (SELECT experiment_id, user_id, 
             SUM(combination = 1) as visits1,
             SUM(combination = 2) as visits2
      FROM visits
      WHERE combination IN (1, 2)
      GROUP BY experiment_id, user_id
     ) v
     ON v.experiment_id = e.id AND
        v.user_id = e.user_id LEFT JOIN
     (SELECT g.experiment_id, g.user_id, 
             SUM(c.combination = 1) as conversions1,
             SUM(c.combination = 2) as conversions2
      FROM goal g LEFT JOIN
           conversion c
           ON c.experiment_id = g.experiment_id AND
              c.user_id = g.user_id AND
              c.goal_id = g.id
      WHERE g.principal = 1
      GROUP BY g.experiment_id, g.user_id
     ) g
     ON g.experiment_id = e.id AND
        g.user_id = e.user_id LEFT JOIN
WHERE e.user_id = 25 
ORDER BY e.created DESC 
LIMIT 5 ;
</code></pre>

<p>There are further optimizations for this.  For instance, an index on <code>experiment(user_id, created, id)</code>.</p>

