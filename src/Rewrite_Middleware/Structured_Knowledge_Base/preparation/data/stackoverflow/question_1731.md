# Any reference for good Datamining tools in Java?
[Link to question](https://stackoverflow.com/questions/5446094/any-reference-for-good-datamining-tools-in-java)
**Creation Date:** 1301181889
**Score:** 0
**Tags:** java, database, data-mining
## Question Body
<p>We are working on an internship project for company. The project itself consists of Datamining. Let's say the structure of database we have to work is huge (in Gigabytes). </p>

<p>Sad to say that DB itself is very poorly structured with inconsistent values and most importantly <strong>no primary or foreign keys</strong>. So in our simple Servlet modules to extract and show the inconsistent data, it takes forever for queries to perform and show up on servlet.</p>

<p>As n00b programmers we do not know about Join and such things in DB. Also we are using MySQL as our DB server. The DB is composed of real-time data from telecom towers.</p>

<p>To find sample inconsistency in table values we are using combination of multiple queries, output of one query serving as input to another query like:</p>

<p><code>"SELECT distinct(tow_id) FROM  'tower_data' WHERE TIME_STAMP LIKE ? ";</code> </p>

<p>//query for finding tower-id.</p>

<pre><code>"SELECT time_stamp FROM tower_data WHERE 'TIME_STAMP' LIKE ? AND 'PARAM_CODE' = ? AND 'TOW_ID'=? GROUP BY time_stamp HAVING count( * ) &gt;1";
</code></pre>

<p>//query for finding time stamps with duplicate data.</p>

<p>And so on.</p>

<p>Also there are some 10 tables in the database. We need to combine 2-3 tables to get values for custom queries.</p>

<p>After finding all the inconsistent values for multiple factors, we have to do data cleansing, removal of noise, data prediction and such tasks in the next stage.</p>

<p>So we thought we can apply some Java Data Mining tools which would in turn apply some algorithm to speed up the data retrieval. </p>

<p>Please guide us towards some good datamining tools. Any guidance towards optimizing/rewriting the queries would also be highly appreciated. </p>

## Answers
### Answer ID: 5447919
<p>Since you seem to have a lot of badly structured data, I do not think data-mining will help.
You may consider using <a href="http://hadoop.apache.org/" rel="nofollow">Apache Hadoop</a> for going over all this data and finding inconsistencies. You can use <a href="http://wiki.apache.org/hadoop/AmazonEC2" rel="nofollow">Amazon EC2</a> for a simple and relatively cheap way to run Hadoop. You can also use Hadoop to port the databases to a better schema, provided that you can build one.</p>

<p>EDIT: I guess you can also do some things within MySQL. Use <a href="http://dev.mysql.com/doc/refman/5.0/en/explain.html" rel="nofollow">query explanation</a> to find the slow parts of your query - I believe 'LIKE' is usually slow, and maybe you can reformulate the query to something faster. Maybe you can first sort your schema by timestamp and then look at sub-ranges. Again, you first have to have an efficient way to get the data, and then you can try to mine it. Good luck.  </p>

### Answer ID: 5447883
<p>I'm not 100% sure it will help in your case, but have a look at <a href="http://code.google.com/p/google-refine/" rel="nofollow">google-refine</a>...</p>

