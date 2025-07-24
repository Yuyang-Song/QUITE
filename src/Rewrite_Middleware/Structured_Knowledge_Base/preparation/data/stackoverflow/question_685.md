# SQL: Can&#39;t understand how to select from my tables
[Link to question](https://stackoverflow.com/questions/37061772/sql-cant-understand-how-to-select-from-my-tables)
**Creation Date:** 1462490068
**Score:** 0
**Tags:** mysql, sql
## Question Body
<p>I need help with a data extraction. I'm an sql noob and I think I have a serious issue with my data design skills. DB system is MYSQL running on Linux.</p>

<p>Table A is structured like this one:</p>

<pre><code>TYPE    SUBTYPE ID
-------------------
xyz     aaa     0001
xyz     aab     0001
xyz     aac     0001
xyz     aad     0001
xyz     aaa     0002
xyz     aaj     0002
xyz     aac     0002
xyz     aav     0002
</code></pre>

<p>Table B is:</p>

<pre><code>TYPE1   SUBTYPE1    TYPE2   SUBTYPE2    
-------------------------------------
xyz     aaa         xyz     aab
xyz     aac         xyz     aad
</code></pre>

<p>Looking at whole table A, I need to extract all rows where both type and subtype are present as columns in a single table B row. Of course this condition is never met since A.subtype can't be at same time equal to B.subtype1 AND B.subtype2 ... </p>

<p>In the example the result set for id should be:</p>

<pre><code>xyz     aaa     0001
xyz     aab     0001
xyz     aac     0001
xyz     aad     0001
</code></pre>

<p>I m trying to use a join with 2 AND conditions, but of course I got an empty set.</p>

<p>EDIT:</p>

<p>@Barmar thank you for your support. It seems that I m really near the final solution. Just to keep things clear, I opened this thread with a shortened and simplified data structure, just to highlight the point where I was stuck.
I thought about your solution, and is acceptable to have both result on a single row. Now, I need to reduce execution time. </p>

<p>First join takes about 2 minutes to complete, and it produce around 23Million of rows. The second join (table B) is probably taking longer.
In fact, I need 3 hours to have the final set of 10 millions of rows. How can we impove things a bit? I noticed that mysql engine is not threaded, and the query is only using a single CPU. I indexed all fields used by join, but I m not sure its the right thing to do...since I m not a DBA 
I suppose also having to rely on VARCHAR comparison for such a big join is not the best solution. Probably I should rewrite things using numerical ID that should be faster.. </p>

<p>Probably split things into different query will help parallelism. thanks for a feedback</p>

## Answers
### Answer ID: 37062424
<p>You can join Table A with itself to find all combinations of types and subtypes with the same ID, then compare them with the values in Table B.</p>

<pre><code>SELECT t1.type AS type1, t1.subtype AS subtype1, t2.type AS type2, t2.subtype AS subtype2, t1.id
FROM TableA AS t1
JOIN TableA AS t2 ON t1.id = t2.id AND NOT (t1.type = t2.type AND t1.subtype = t2.subtype)
JOIN TableB AS b ON t1.type = b.type1 AND t1.subtype = b.subtype1 AND t2.type = b.type2 AND t2.subtype = b.subtype2
</code></pre>

<p>This returns the two rows from Table A as a single row in the result, rather than as separate rows, I hope that's OK. If you need to split them up, you can move this into a subquery and join it back with the original table A to return each row.</p>

<pre><code>SELECT a.*
FROM TableA AS a
JOIN (the above query) AS x
ON a.id = x.id AND
    ((a.type = x.type1 AND a.subtype = x.subtype1)
    OR
     (a.type = x.type2 AND a.subtype = x.subtype2))
</code></pre>

<p><a href="http://www.sqlfiddle.com/#!9/00d407/4" rel="nofollow">DEMO</a></p>

### Answer ID: 37062033
<p>You can use Join like this :</p>

<pre><code>Select A.Type, A.SubType, A.ID from a_table A JOIN b_table B
ON (A.Type = B.Type1 AND A.SubType = B.SubType1) OR
   (A.Type = B.Type2 AND A.SubType = B.SubType2)
</code></pre>

<p>But I think there is a problem in your design, you have same values in Table A with different ID and there is no any condition on ID !</p>

<p>Instead of storing Type and SubType in Table B, you can store an unique ID of each record of Table A to Table B, then you can think about better ways to get results you want ...</p>

<p><strong>Edit</strong> :</p>

<p>With UNION of two joins you can get that result :</p>

<pre><code>Select A.Type, A.SubType, A.ID from A_table A
JOIN b_table B1 ON A.Type = B1.Type1 AND A.SubType = B1.SubType1
WHERE (B1.Type2, B1.SubType2) IN (SELECT Type, SubType FROM A_table) AND ID = '0001'

UNION

Select A.Type, A.SubType, A.ID from A_table A
JOIN b_table B2 ON A.Type = B2.Type2 AND A.SubType = B2.SubType2
WHERE (B2.Type1, B2.SubType1) IN (SELECT Type, SubType FROM A_table) AND ID = '0001'
</code></pre>

<p>But as I say, I think there is a design problem, it seems better that each type and subtype have an unique ID in Table A and work with this ID on Table B</p>

### Answer ID: 37061841
<p>You can use <code>EXISTS</code>:</p>

<pre><code>SELECT a.*
FROM TableA a
WHERE EXISTS(
    SELECT 1
    FROM TableB b
    WHERE
        (b.Type1 = a.Type AND b.SubType1 = a.SubType)
        OR (b.Type2 = a.Type AND b.SubType2 = a.SubType)
)
AND a.ID = '0001'
</code></pre>

<p><kbd><a href="http://sqlfiddle.com/#!9/1beb45/1/0" rel="nofollow"><strong>ONLINE DEMO</strong></a></kbd></p>

