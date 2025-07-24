# Issue combining inner and outer joins in Oracle
[Link to question](https://stackoverflow.com/questions/67163291/issue-combining-inner-and-outer-joins-in-oracle)
**Creation Date:** 1618840108
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<p>I'm trying to simplify a query against an Oracle database that uses multiple inner joins against the same table. I know the multiple joins against the same table can be cleaned up with outer joins, but I'm failing to elicit the same results.</p>
<p>Below are the tables listing only the columns needed for the query. The &quot;link&quot; column in table X maps to the ID, ID2, and ID3 columns in tables A, B, and C respectively.</p>
<pre><code>**Table A**
id

**Table B**
id
id2
nm

**Table C**
id3
nm

**Table X**
cfgnum
link
</code></pre>
<p>Existing (working query):</p>
<pre><code>SELECT COUNT(*)
FROM A,
     X,
     X X1,
     X X2,
     B,
     C
WHERE X.cfgnum = 9999
AND A.id = X.link
AND X.cfgnum = X1.cfgnum
AND X.cfgnum = X2.cfgnum
AND B.id2 = X1.link
AND B.id = A.id
AND C.id3 = X2.link
AND C.nm = B.nm;
</code></pre>
<p>The below was my attempt to rewrite, but it returns substantially different results. With the comments in place it does return the right number of rows against the linking X table.</p>
<pre><code>SELECT COUNT(*)
FROM X
LEFT JOIN A ON X.link = A.id
LEFT JOIN B on X.link = B.id2 --AND A.id = B.id
LEFT JOIN C on X.link = C.id3 --AND B.nm = C.nm
WHERE cfgnum = 9999
AND COALESCE (A.id, B.id2, C.id3) IS NOT NULL;  
</code></pre>
<p>Any help is appreciated!</p>
<p><strong>UPDATE</strong></p>
<p>Apologies, new at this, and it appears I did not provide enough information. Table X groups rows from other tables under a &quot;cfgnum&quot;. Each &quot;cfgnum&quot; can link to numerous rows in numerous tables.</p>
<p>Hopefully the below sample data makes sense.</p>
<pre><code>**Table A**
id
1
2
7
    
**Table B**
id  id2  nm
3   1    name1
4   3    name2
    
**Table C**
id3  nm
5    name2
6    name3
    
**Table X**
cfgnum  link
9998    1
9998    2
9998    3
9999    1
9999    3
9999    4
9999    6
9999    7
9999    8
</code></pre>
<p>My thought was using left joins to X would minimize the number of joins required to X. Notice the &quot;working&quot; query has X three times in the from clause. If I'm offbase, please let me know.</p>
<p>Thanks again.</p>

## Answers
### Answer ID: 67164420
<p><strong>Updated:</strong>
If you have just one-to-one relationship, ie you have just 1 link to each of A,B,C for specific cfgnum, you can use aggregation:</p>
<pre><code>SELECT COUNT(*)
FROM (select cfgnum,
        max(decode(rownum,1,link)) link1,
        max(decode(rownum,2,link)) link2,
        max(decode(rownum,3,link)) link3
      from X
      WHERE cfgnum = 9999
      group by cfgnum -- just in case if you need to remove the predicate &quot;cfgnum=9999&quot;
    ) x1
    join A on A.id in (link1,link2,link3)
    join B on B.id2 in (link1,link2,link3) and B.id = A.id
    join C on C.id3 in (link1,link2,link3) and C.nm = B.nm;
</code></pre>

### Answer ID: 67164212
<p>There are no left joins in your previous query. So you can try this -</p>
<pre><code>SELECT COUNT(*)
  FROM A
  JOIN X ON A.id = X.link
  JOIN X1 ON X.cfgnum = X1.cfgnum
  JOIN X2 ON X.cfgnum = X2.cfgnum
  JOIN B ON B.id2 = X1.link
         AND B.id = A.id
  JOIN C ON C.id3 = X2.link
         AND C.nm = B.nm
WHERE X.cfgnum = 9999
</code></pre>

