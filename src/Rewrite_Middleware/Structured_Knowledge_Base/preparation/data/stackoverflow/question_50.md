# Oracle - using multiple exists to check record availability
[Link to question](https://stackoverflow.com/questions/11151484/oracle-using-multiple-exists-to-check-record-availability)
**Creation Date:** 1340348162
**Score:** 0
**Tags:** performance, oracle-database, query-optimization, exists
## Question Body
<p>I have a situation in my application for displaying the count of data which match different criterion. Since the performance of counting is degrading with respect to the growth of database, we decided to show only the availability information using the exists clause.</p>

<p>Below is my table structure </p>

<pre><code>Table: DocInfo
---------------------------------------
DocId       number
DocName     varchar(250)
DocStatus   number
SignedBy    number
ForwardedBy number
ForwardCount    number
DocOwner    number
MgrID       number
ProjectId   number
</code></pre>

<p>The current query which does the counting is like this</p>

<pre><code>SELECT NVL(SUM(CASE
                 WHEN (DocStatus IN (1150,1155,1170,1182,1190) AND
                       DocOwner=56366 AND
                       ForwardCount=0)
                   THEN 1
                   ELSE 0
               END), 0) "ForReview",
       NVL(SUM(CASE
                 WHEN (DocStatus IN (1200) And
                       MgrID = 56366 AND
                       ForwardCount = 0 )
                   THEN 1
                   ELSE 0
               END), 0) "Accepted" , 
       NVL(SUM(CASE
                 WHEN (DocStatus IN (1150,1155,1170,1182,1190) AND
                       DocOwner=56366 AND
                       MgrID = 0 )
                   THEN 1
                   ELSE 0
               END), 0) "Waiting"
  FROM DocInfo 
  WHERE ProjectId = 313 and
        (DocOwner = 56366 or MgrID = 56366)
</code></pre>

<p>I need to change the counting to an <code>exists</code> clause so that i can show whether documents are available or not in each category.</p>

<p>Since this change is to improve the performance, running this as different queries is also not advisable. Please help me, I have ran out of my limited knowledge.</p>

<p>Sorry to miss the part which i have already tried.</p>

<p>I have changed the above query to a union with exists clause in each like below.</p>

<pre><code>SELECT 'ForReview' AS A
  FROM DUAL
  WHERE EXISTS (SELECT NULL
                  FROM DocInfo 
                  WHERE ProjectId = 313 and
                        (DocOwner = 56366 or MgrID = 56366)  and
                        (DocStatus IN (1150,1155,1170,1182,1190) AND
                         DocOwner=56366 AND
                         ForwardCount=0)) 
UNION 
  SELECT 'Accepted' AS A
    FROM DUAL
    WHERE EXISTS (SELECT NULL
                    FROM DocInfo
                    WHERE ProjectId = 313 and
                          (DocOwner = 56366 or MgrID = 56366) and
                          (DocStatus IN (1200) And
                           MgrID = 56366 AND
                           ForwardCount = 0 )) 
UNION
  SELECT 'Waiting' AS A
    FROM DUAL
    WHERE EXISTS (SELECT NULL
                    FROM DocInfo
                    WHERE ProjectId = 313 and
                          (DocOwner = 56366 or MgrID = 56366) and
                          (DocStatus IN (1150,1155,1170,1182,1190) AND
                           DocOwner=56366 AND
                           MgrID = 0)) 
</code></pre>

<p>I have mentioned only 3 conditions, whereas my actual application has 8 different criteria to be added into this query. so when i have 8 Exists clauses, it runs internally as 8 different queries, and in effect it takes more time - single segment in the entire union query takes only 560 ms whereas all queries together takes around 7 seconds to generate the output.</p>

<p>Since my requirement is only to identify the <strong>Availability</strong> of any such record i do not want to navigate through the entire recordset and count it.</p>

<p>Is there anyway to optimize/rewrite this query</p>

<p>Thank You</p>

## Answers
### Answer ID: 11155700
<blockquote>
  <p>"so when i have 8 Exists clauses, it runs internally as 8 different
  queries, and in effect it takes more time - single segment in the
  entire union query takes only 560 ms whereas all queries together
  takes around 7 seconds to generate the output."</p>
</blockquote>

<p>Surprise, surprise.  Running what amounts to the same query <em>eight</em> times will not be faster than running that query once.  </p>

<p>Now it is true that EXISTS can be faster, because it only needs to find a single row which matches the given criteria, rather than retrieving an entire data set.  However you have just shifted the retrieved data into the WHERE clause so the database still has to do the same amount of work.  In fact, it is apparently doing a lot more work, because <code>7s &gt; (560ms * 8)</code>.  </p>

<p>To solve your problem properly you need to understand how the database works and how to tune it.  <a href="http://docs.oracle.com/cd/B19306_01/server.102/b14211/optimops.htm" rel="nofollow">Find out more</a>. </p>

<p>For a start, define a tuning goal.  Your original query takes half a second to run: that's not lightning fast but it is pretty quick.  Why is this a problem?  How quickly do you want it to run?</p>

<p>Next, run an <a href="http://docs.oracle.com/cd/B19306_01/server.102/b14200/statements_9010.htm" rel="nofollow">EXPLAIN PLAN</a>.  Is the query using indexes?  How efficiently is its index usage>  What percentage of the rows are being selected?  </p>

<p>Now you also need to undersatnd your data. Is the selected data evenly distributed throughout the table or are there clusters?  Do some projects, owners or managers have more records than others?  How does that distribution effect performance?</p>

<p>Please bear in mind, tuning is a science and it is complicated: there are whole books on the subject and some people make very fine livings as performance troubleshooters.  It requires a lot of information about your system, both knowledge of what your application does and low-level information on which activities your database is doing.  We can help you in your quest to find a more performant solution but we cannot just look at a shonky query and tell you how to re-write so it runs quicker.   </p>

