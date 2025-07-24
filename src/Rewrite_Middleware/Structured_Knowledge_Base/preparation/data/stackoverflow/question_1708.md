# Queries within queries: Is there a better way?
[Link to question](https://stackoverflow.com/questions/4665348/queries-within-queries-is-there-a-better-way)
**Creation Date:** 1294806672
**Score:** 1
**Tags:** sql, postgresql, join, query-optimization, subquery
## Question Body
<p>As I build bigger, more advanced web applications, I'm finding myself writing extremely long and complex queries. I tend to write queries within queries a lot because I feel making one call to the database from PHP is better than making several and correlating the data.</p>

<p>However, anyone who knows anything about SQL knows about <code>JOIN</code>s. Personally, I've used a <code>JOIN</code> or two before, but quickly stopped when I discovered using subqueries because it felt easier and quicker for me to write and maintain.</p>

<p>Commonly, I'll do subqueries that may contain one or more subqueries from relative tables.<br>
Consider this example:</p>

<pre><code>SELECT 
  (SELECT username FROM users WHERE records.user_id = user_id) AS username,
  (SELECT last_name||', '||first_name FROM users WHERE records.user_id = user_id) AS name,
  in_timestamp,
  out_timestamp
FROM records
ORDER BY in_timestamp
</code></pre>

<p>Rarely, I'll do subqueries after the <code>WHERE</code> clause.<br>
Consider this example:</p>

<pre><code>SELECT
  user_id,
  (SELECT name FROM organizations WHERE (SELECT organization FROM locations WHERE records.location = location_id) = organization_id) AS organization_name
FROM records
ORDER BY in_timestamp
</code></pre>

<p>In these two cases, would I see any sort of improvement if I decided to rewrite the queries using a <code>JOIN</code>?</p>

<p>As more of a blanket question, what are the advantages/disadvantages of using subqueries or a <code>JOIN</code>? Is one way more correct or accepted than the other?</p>

## Answers
### Answer ID: 4665455
<p>a) I'd start by pointing out that the two are not necessarily interchangable.  Nesting as you have requires there to be 0 or 1 matching value otherwise you will get an error.  A join puts no such requirement and may exclude the record or introduce more depending on your data and type of join.</p>

<p>b) In terms of performance, you will need to check the query plans but your nested examples are unlikely to be more efficient than a table join.  Typically sub-queries are executed once per row but that very much depends on your database, unique constraints, foriegn keys, not null etc.  Maybe the DB can rewrite more efficiently but joins can use a wider variety of techniques, drive the data from different tables etc because they do different things (though you may not observe any difference in your output depending on your data).  </p>

<p>c) Most DB aware programmers I know would look at your nested queries and rewrite using joins, subject to the data being suitably 'clean'.</p>

<p>d) Regarding "correctness" - I would favour joins backed up with proper constraints on your data where necessary (e.g. a unique user ID).  You as a human may make certain assumptions but the DB engine cannot unless you tell it.  The more it knows, the better job it (and you) can do.</p>

### Answer ID: 4665414
<p>JOINs are preferable to separate [sub]queries.<br>
If the subselect (AKA subquery) is not correlated to the outer query, it's very likely the optimizer will scan the table(s) in the subselect once because the value isn't likely to change.  When you have correlation, like in the example provided, the likelihood of single pass optimization becomes very unlikely.  In the past, it's been believed that correlated subqueries execute, RBAR -- Row By Agonizing Row.  With a JOIN, the same result can be achieved while ensuring a single pass over the table.  </p>

<p>This is a proper re-write of the query provided:</p>

<pre><code>   SELECT u.username,
          u.last_name||', '|| u.first_name AS name,
          r.in_timestamp,
          r.out_timestamp
     FROM RECORDS r 
LEFT JOIN USERS u ON u.user_id = r.user_id
 ORDER BY r.in_timestamp
</code></pre>

<p>...because the subselect can return NULL if the user_id doesn't exist in the <code>USERS</code> table.  Otherwise, you could use an INNER JOIN:</p>

<pre><code>  SELECT u.username,
         u.last_name ||', '|| u.first_name AS name,
         r.in_timestamp,
         r.out_timestamp
    FROM RECORDS r 
    JOIN USERS u ON u.user_id = r.user_id
ORDER BY r.in_timestamp
</code></pre>

<p>Derived tables/inline views are also possible using JOIN syntax.</p>

### Answer ID: 4665398
<p>Joins in most cases will be much more faster.</p>

<p>Lets take this with an example.</p>

<p>Lets use your first query:</p>

<pre><code>SELECT 
(SELECT username FROM users WHERE records.user_id = user_id) AS username,
  (SELECT last_name||', '||first_name FROM users WHERE records.user_id = user_id) AS name,
  in_timestamp,
  out_timestamp
FROM records
ORDER BY in_timestamp
</code></pre>

<p>Now consider we have 100 records in records and 100 records in user.(Assuming we dont have index on user_id)</p>

<p>So if we understand your algorithm it says:
For each record
   Scan all 100 records in users to find out username
   Scan all 100 records in users to find out last name and first name</p>

<p>So its like we scanned users table 100*100*2 time. Is it really worth. If we consider index on user_id it will make thing better, but is it still worth.</p>

<p>Now consider a join (nested loop will almost produce same result as above, but consider a hash join):
Its like.
Make a hash map of user.
For each record
   Find a mapping record in Hashmap. Which will be certainly much more faster then looping and finding a record.</p>

<p>So clearly, joins should be favorable.</p>

<p>NOTE: Example used of 100 record may produce identical plan, but the idea is to analyze how it can effect the performance.</p>

### Answer ID: 4665358
<p>In simple cases, the query optimiser should be able to produce identical plans for a simple join versus a simple sub-select.</p>

<p>But in general (and where appropriate), you should favour joins over sub-selects.</p>

<p>Plus, you should avoid correlated subqueries (a query in which the inner expression refer to the outer), as they are effectively a for loop within a for loop). In most cases a correlated subquery can be written as a join.</p>

