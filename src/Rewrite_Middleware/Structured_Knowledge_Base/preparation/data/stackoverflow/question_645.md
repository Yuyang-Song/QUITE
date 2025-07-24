# Can I modify this query using a WITH clause?
[Link to question](https://stackoverflow.com/questions/34948374/can-i-modify-this-query-using-a-with-clause)
**Creation Date:** 1453470884
**Score:** 0
**Tags:** sql, database, oracle-database, plsql
## Question Body
<p>I have written the following query in order to achieve the following:</p>

<p>1) Select all regulatory languages that do not have a specified <code>ID</code>.</p>

<p>2) Link those regulatory languages based on a hierarchy field (<code>RL_ID_DEFINED</code> - this field is the <code>ID</code> of the parent regulatory language).</p>

<p>My first variation used <code>NOT IN</code>, but after looking into it I decided that <code>NOT EXISTS</code> would be a more efficient approach.  Additionally, I was thinking that adding a <code>WITH</code> clause might make it run a bit faster, since in my current code it is running the nested <code>SELECT</code> statement for each <code>ID</code> in the iteration.  Would it be possible to rewrite with using a <code>WITH</code> clause for that nested <code>SELECT</code>?</p>

<pre><code>SELECT
    T1.ID 
FROM
    REGULATORY_LANGUAGES T1
WHERE
    T1.INACTIVE_DATE IS NULL 
    AND NOT EXISTS (
        SELECT
            NULL
        FROM
            REGULATORY_LANGUAGES T2,
            REVIEW_REGULATIONS T3
        WHERE
            T3.RVWTYPYR_ID = ? 
            AND T3.RL_ID = T2.ID
            AND T1.ID = T2.ID)
START WITH
    RL_ID_DEFINED IS NULL
    AND INACTIVE_DATE IS NULL
CONNECT BY
    PRIOR ID = RL_ID_DEFINED
</code></pre>

<p>The problem I'm running into is that when I look at the structure of a <code>WITH</code> clause, I would be creating it prior to my main <code>SELECT</code>.  However, that would require me to have defined my <code>T1</code> table already.  Any thoughts?</p>

<p>(Note - this is being called in a java method, hence the <code>?</code> in the line <code>T3.RVWTYPYR_ID = ?</code>.  When I test this in the database editor via Toad, I just hard code a value for the <code>?</code>).</p>

## Answers
### Answer ID: 34950042
<p>Much thanks to Tom H for his insight.  I've rewritten the query using <code>JOIN</code>:</p>

<pre><code>SELECT
    T1.ID
FROM
    REGULATORY_LANGUAGES T1
LEFT JOIN (      
    SELECT
        T2.ID ID
    FROM
        REGULATORY_LANGUAGES T2
    INNER JOIN    
        REVIEW_REGULATIONS T3
    ON
        T3.RVWTYPYR_ID = ?
        AND T3.RL_ID = T2.ID) T_JOIN
ON T1.ID = T_JOIN.ID             
WHERE
    T1.INACTIVE_DATE IS NULL
    AND T_JOIN.ID IS NULL
START WITH
    T1.RL_ID_DEFINED IS NULL
    AND T1.INACTIVE_DATE IS NULL 
CONNECT BY
    PRIOR T1.ID = T1.RL_ID_DEFINED
</code></pre>

### Answer ID: 34949538
<p>While speed is important, so is accuracy.  You mentioned that you switched from <code>not in</code> to <code>not exists</code> for efficiency.  They do different things.  There is another way to speed up the logic of <code>not in</code>.  Instead of this:</p>

<pre><code>where someField not in 
(select someField
from etc
)
</code></pre>

<p>Do this</p>

<pre><code>where someField in 
(select someField
from etc
where whatever
minus
select someField
from etc
where whatever
and more filters that identify records to exclude
)
</code></pre>

<p>Now for the <code>with</code> keyword.  It speeds up performance when you want to run the exact same subquery more than once.  So, instead of this:</p>

<pre><code>where field1 in 
(sql for subquery)
and field 2 in 
(exact same sql as above)
</code></pre>

<p>you do this:</p>

<pre><code>with temp as (sql for subquery)
select etc
where field1 in 
(select something from temp)
and field 2 in 
(select something from temp)
</code></pre>

<p>However, that's not your situation.  What you probably want to do is to investigate ways to send a list of parameters from java so that your query looks like this:</p>

<pre><code>T3.RVWTYPYR_ID in (?,?,etc)
</code></pre>

<p>Then you wouldn't have to repeat the subquery.</p>

