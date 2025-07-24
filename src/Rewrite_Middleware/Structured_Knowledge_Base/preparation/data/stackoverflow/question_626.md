# Making a Limit X,Y MySQL Query with Joins Run Faster
[Link to question](https://stackoverflow.com/questions/34045973/making-a-limit-x-y-mysql-query-with-joins-run-faster)
**Creation Date:** 1449068605
**Score:** 0
**Tags:** mysql, database, join, query-optimization
## Question Body
<p>I have a MySQL query with a particular structure that I want to rewrite so that it runs faster.   It currently runs very slow taking about 255 seconds to execute.  If I remove the join it runs in &lt; 10 seconds.  Its purpose is to get records from table A, 100 rows at a time, for as long as a user wants to see more rows.  </p>

<p>I suspect that the query is taking a long time because it's doing the join on more than just the first 100 rows it finds.  Is this true, and if so, is there a way to rewrite the query to do the joining after it gets the rows from the main table?</p>

<p>The data comes from a 'main' table A which has a datetime field (START_TIME) and several foreign keys to tables with string values (tables, B,C,D).</p>

<p>Table A has 2.5 million rows.  Table B has 600K rows.
Table A has an index on START_TIME.  Table B has an index on its ID value.</p>

<p>Here's a basic form of the query.  I do not want to put an upper limit on START_TIME because I ALWAYS want to get 100 records back from the query. I use a response which has less than 100 records to indicate that there`s no more records in the database.</p>

<pre><code>SELECT 
    A.START_TIME, A.F1, A.F2, B.STRING
FROM 
    A
     INNER JOIN B ON A.B_ID = B.ID
WHERE
    A.START_TIME &gt;= '2015-03-22 05:23:44'
LIMIT 0, 100;
</code></pre>

<p>Here`s the EXPLAIN. Sorry for the format:</p>

<pre><code># id, select_type, table, type, possible_keys, key, key_len, ref, rows, Extra
1, SIMPLE, B, index, PRIMARY, FSN, 95, , 1, Using index; Using temporary; Using filesort
1, SIMPLE, A, ref, A_ix_B_ID,A_ix_C, A_ix_B_ID, 4, ag100_a$$burnaby.B.ID, 2, Using where
</code></pre>

## Answers
### Answer ID: 34169239
<pre><code>SELECT  A.START_TIME, A.F1, A.F2, 
      ( SELECT  STRING
            FROM  B
            WHERE  A.B_ID = B.ID 
      ) AS String
    FROM  A
    WHERE  A.START_TIME &gt;= '2015-03-22 05:23:44'
    ORDER BY START_TIME
    LIMIT  0, 100; 
</code></pre>

<p>will probably run faster.  It is 'forced' to use <code>INDEX(START_TIME)</code> from <code>A</code>.</p>

<p>Please provide <code>SHOW CREATE TABLE</code> for both tables; I want to check the datatypes, etc.</p>

### Answer ID: 34046137
<p>You have to provide explain plan so we can help you better.</p>

<p><a href="https://dev.mysql.com/doc/refman/5.5/en/execution-plan-information.html" rel="nofollow">https://dev.mysql.com/doc/refman/5.5/en/execution-plan-information.html</a></p>

<p>But for your description you still need index.</p>

<p>TableA beside <code>START_TIME</code> need index for each join field <code>B_id, C_id and D_id</code> and maybe using a composite index for all 4 variable would be better</p>

<pre><code> CREATE INDEX A_Bid_idx ON A (B_id);
 CREATE INDEX A_Cid_idx ON A (C_id);
 CREATE INDEX A_Did_idx ON A (D_id);

 OR

 CREATE INDEX A_Full_idx ON A (B_id,C_id, D_id, START_TIME);
</code></pre>

<p>Table C and D also need index for <code>C.ID and D.ID</code>. And would be even better if they use a composite index </p>

<pre><code>  (C.ID, C.STRING)  and
  (D.ID, D.STRING)

  CREATE INDEX C_id_idx ON C (ID);
  CREATE INDEX D_id_idx ON D (ID);

  OR

  CREATE INDEX C_id_string_idx ON C (ID, STRING);
  CREATE INDEX D_id_string_idx ON C (ID, STRING);
</code></pre>

<p>That way db doesnt have to make a lookup to find the string value asociated to the ID</p>

