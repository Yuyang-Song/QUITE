# what&#39;s the difference between SQL&#39;s
[Link to question](https://stackoverflow.com/questions/20233823/whats-the-difference-between-sqls)
**Creation Date:** 1385525971
**Score:** 0
**Tags:** sql, database
## Question Body
<p>I work with Databases not extensively but to the point where I can write Selects, update's ,small joins etc..
I can get my work done with my current knowledge. I have encountered some difficulty while trying to complete a task, I got the task completed but would like to understand why some of the SQL's that I have written in process did not work.</p>

<p>Task at hand: I have a table "TESTTABLE" that has 5 columns and the 6th is the sum of these 5 columns.
Currently table looks like below:</p>

<pre><code>ID  NAME SUB1 SUB2 SUB3 SUB4 SUB5 TOTAL
1   VA   10   20   30   40   50 
2   MI   20   40   60   80   10 
3   NC   10   30   50   70   90 
4   SC   10   20   30   40   50 
5   WA   20   40   60   80   15 
</code></pre>

<p>the last column 'Total' is currently empty.</p>

<p>Now,I need to update the total column in the table with the sum(sub1+sub2=sub3+sub4+sub5).</p>

<p>In this process I have written the following SQL's and it did work, would like to understand the difference.</p>

<p>Attempt1:</p>

<pre><code>UPDATE TESTTABLE T 
SET Total = 
           SELECT (sub1+sub2+sub3+sub4+sub5) 
           FROM TESTTABLE TB 
           WHERE T.ID = TB.ID);
</code></pre>

<p>Error encountered:--ERROR:  (2) This form of correlated query is not supported - consider rewriting;</p>

<p>Attempt2:</p>

<pre><code>CREATE TABLE TEMP_TESTTABLE AS( SELECT ID, SUM(sub1+sub2+sub3+sub4+sub5) AS SUB_TOTAL  FROM TESTTABLE ) 

 UPDATE TESTTABLE  A
 SET TOTAL = 
             (SELECT SUB_TOTAL 
              FROM TEMP_TESTTABLE B 
              WHERE B.ID=A.ID);
</code></pre>

<p>ERROR encountered: ERROR: (2) This form of correlated query is not supported - consider rewriting </p>

<p>Attempt3:</p>

<pre><code>UPDATE TESTTABLE  
SET TOTAL = SUM(sub1+sub2+sub3+sub4+sub5);
</code></pre>

<p>ERROR encountered: ERROR:  Aggregate functions not allowed in the set list of an UPDATE statement</p>

<p>Attempt4- Successful one;</p>

<pre><code>UPDATE TESTTABLE  A
SET TOTAL = B.SUB_TOTAL FROM TEMP_TESTTABLE B
WHERE A.ID=B.ID
</code></pre>

<p>Attempt 4 worked for me by using the temp table created in attempt2 [TEMP_TESTTABLE].</p>

<p>I need some detail explanation, and appreciate if anyone can provide me and let me know how my attempt4 is different than 1,2,3.</p>

<p>Help is greatly appreciated.</p>

<p>Thanks, </p>

## Answers
### Answer ID: 20233970
<p>Attempt1 failed because subqueries should be enclosed in parentheses.</p>

<pre><code>UPDATE TESTTABLE T 
SET Total = 
       (SELECT (sub1+sub2+sub3+sub4+sub5) 
        FROM TESTTABLE TB 
        WHERE T.ID = TB.ID);
</code></pre>

<p>Attempt2 failed because <code>SUM()</code> function is aggregate function, to sum values from multiple rows, not to sum values from multiple columns in one row.</p>

<p>You should redefine the column as a computed column, like this</p>

<pre><code>Alter table TESTTABLE 
add column Total as sub1+sub2+sub3+sub4+sub5
</code></pre>

### Answer ID: 20233871
<p>This is the cannonical Soluion.</p>

<pre><code>UPDATE
    TESTTABLE 

SET 
    Total = (sub1+sub2+sub3+sub4+sub5)
</code></pre>

<p>The reason the others failed is that you where doing subselects that returned multiple rows. You didn't tell the UPDATE how the different rows mapped from the select to the UPDATE.</p>

<p>In this version you are making it simple - one table - on each row set a value on that row based on the data in that row.</p>

<p>In your final version you're doing the same but in a redundant way (extra join that does nothing).</p>

