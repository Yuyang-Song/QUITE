# How can improve this SQL query?
[Link to question](https://stackoverflow.com/questions/13937948/how-can-improve-this-sql-query)
**Creation Date:** 1355850189
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<p>I believe this is a SQL query running on Oracle:</p>

<pre><code>SELECT ID, DEVICE_TYPE, S3_KEY, TO_CHAR(CREATION_DATE, 'YYYY-MM-DD HH24:MI:SS') AS CREATION_DAT
FROM KASE_DDL.ARCHIVED_LOG 
WHERE 
    CREATION_DATE &gt;= TO_DATE('{DIST_YYYY/MM/DD HH24:MI:SS_UTC}', 'YYYY/MM/DD HH24:MI:SS') 
    AND CREATION_DATE &lt;= TO_DATE('{DIET_YYYY/MM/DD HH24:MI:SS_UTC}', 'YYYY/MM/DD HH24:MI:SS')
</code></pre>

<p>It is running slow and I wonder how can I rewrite it to improve its efficiency. For example, can this query utilize indexing if there is an index built on CREATION_DATE? I remember reading books saying that if there is computation around a column, Oracle may not be able to use any index built on it. Is my query falling into this case? Any other suggestion? Thank you.</p>

<p>UPDATE:</p>

<p>In my problem, CREATION_DATE has an index built in. I am curious about whether this query enables the database to utilize the index or not.</p>

## Answers
### Answer ID: 13951514
<p>For an additional performance gain you can try to use covering indexes.
In your case there is </p>

<pre><code>create index ndxCovering on KASE_DDL.ARCHIVED_LOG(CREATION_DATE, ID, DEVICE_TYPE, S3_KEY);
</code></pre>

<p>It allows to read data only from index pages without seeking of data pages.</p>

### Answer ID: 13951614
<p>You can check the probable effectiveness of the index by comparing the clustering_factor in the user_indexes table with the number of rows and the number of blocks for the table. The clustering factor will be between the number of blocks and the number of rows, which represent the theoretical minimum and maximum values respectively.</p>

<p>If the clustering factor is closer to the number of blocks (ie. it's relatively small) then the index will be more likely to be chosen and the selection of block from the table based on accessing the index will be require less work by the system.</p>

<p>It's always worth checking if you have any doubts about the performance improvements you're seeing when the index is used to access the table.</p>

### Answer ID: 13938007
<p>Add an index on <code>CREATION_DATE</code>. </p>

<p>I would also use the <a href="http://docs.oracle.com/cd/B28359_01/server.111/b28286/conditions011.htm" rel="nofollow"><code>BETWEEN</code></a> operator for the dates, but I like to read it that way. </p>

