# Complex MySQL query still using filesort although indexes exist
[Link to question](https://stackoverflow.com/questions/9207091/complex-mysql-query-still-using-filesort-although-indexes-exist)
**Creation Date:** 1328773380
**Score:** 11
**Tags:** mysql, optimization, indexing, filesort
## Question Body
<p>I have a Joomla table with thousands of rows of content (approx 3million). I'm having a bit of trouble rewriting the database queries to be as fast as possible when querying the tables.</p>

<p>Here is my full query:</p>

<pre><code>SELECT cc.title AS category, a.id, a.title, a.alias, a.title_alias, a.introtext, a.fulltext, a.sectionid, a.state, a.catid, a.created, a.created_by, a.created_by_alias, a.modified, a.modified_by, a.checked_out, a.checked_out_time, a.publish_up, a.publish_down, a.attribs, a.hits, a.images, a.urls, a.ordering, a.metakey, a.metadesc, a.access, CASE WHEN CHAR_LENGTH(a.alias) THEN CONCAT_WS(":", a.id, a.alias) ELSE a.id END AS slug, CASE WHEN CHAR_LENGTH(cc.alias) THEN CONCAT_WS(":", cc.id, cc.alias) ELSE cc.id END AS catslug, CHAR_LENGTH( a.`fulltext` ) AS readmore, u.name AS author, u.usertype, g.name AS groups, u.email AS author_email
FROM j15_content AS a
LEFT JOIN j15_categories AS cc
ON a.catid = cc.id
LEFT JOIN j15_users AS u
ON u.id = a.created_by
LEFT JOIN j15_groups AS g
ON a.access = g.id
WHERE 1
AND a.access &lt;= 0
AND a.catid = 108
AND a.state = 1
AND ( publish_up = '0000-00-00 00:00:00' OR publish_up &lt;= '2012-02-08 00:16:26' )
AND ( publish_down = '0000-00-00 00:00:00' OR publish_down &gt;= '2012-02-08 00:16:26' )
ORDER BY a.title, a.created DESC
LIMIT 0, 10
</code></pre>

<p>Here is the output from an EXPLAIN:</p>

<pre><code> +----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-----------------------------+
| id | select_type | table | type   | possible_keys                                         | key       | key_len | ref                       | rows    | Extra                       |
+----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-----------------------------+
|  1 | SIMPLE      | a     | ref    | idx_access,idx_state,idx_catid,idx_access_state_catid | idx_catid | 4       | const                     | 3108187 | Using where; Using filesort |
|  1 | SIMPLE      | cc    | const  | PRIMARY                                               | PRIMARY   | 4       | const                     |       1 |                             |
|  1 | SIMPLE      | u     | eq_ref | PRIMARY                                               | PRIMARY   | 4       | database.a.created_by     |       1 |                             |
|  1 | SIMPLE      | g     | eq_ref | PRIMARY                                               | PRIMARY   | 1       | database.a.access         |       1 |                             |
+----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-----------------------------+
</code></pre>

<p>And to show what indexes exist, SHOW INDEX FROM j15_content:</p>

<pre><code>+-------------+------------+------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+
| Table       | Non_unique | Key_name               | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment |
+-------------+------------+------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+
| j15_content |          0 | PRIMARY                |            1 | id          | A         |     3228356 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_section            |            1 | sectionid   | A         |           2 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_access             |            1 | access      | A         |           1 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_checkout           |            1 | checked_out | A         |           2 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_state              |            1 | state       | A         |           2 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_catid              |            1 | catid       | A         |           6 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_createdby          |            1 | created_by  | A         |           1 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | title                  |            1 | title       | A         |      201772 |        4 | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_access_state_catid |            1 | access      | A         |           1 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_access_state_catid |            2 | state       | A         |           2 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_access_state_catid |            3 | catid       | A         |           7 |     NULL | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_title_created      |            1 | title       | A         |     3228356 |        8 | NULL   |      | BTREE      |         |
| j15_content |          1 | idx_title_created      |            2 | created     | A         |     3228356 |     NULL | NULL   |      | BTREE      |         |
+-------------+------------+------------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+
</code></pre>

<p>As you can see there are a few pieces of data being taken from the database. Now I have tested by simplifying the query that the real issue lies with the ORDER BY clause. Without ordering the results, the query is quite responsive, here is an explanation:</p>

<pre><code>+----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-------------+
| id | select_type | table | type   | possible_keys                                         | key       | key_len | ref                       | rows    | Extra       |
+----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-------------+
|  1 | SIMPLE      | a     | ref    | idx_access,idx_state,idx_catid,idx_access_state_catid | idx_catid | 4       | const                     | 3108187 | Using where |
|  1 | SIMPLE      | cc    | const  | PRIMARY                                               | PRIMARY   | 4       | const                     |       1 |             |
|  1 | SIMPLE      | u     | eq_ref | PRIMARY                                               | PRIMARY   | 4       | database.a.created_by     |       1 |             |
|  1 | SIMPLE      | g     | eq_ref | PRIMARY                                               | PRIMARY   | 1       | database.a.access         |       1 |             |
+----+-------------+-------+--------+-------------------------------------------------------+-----------+---------+---------------------------+---------+-------------+
</code></pre>

<p>As you can see it's the fatal filesort that's killing the server. With this many rows, I'm doing my best to optimize everything through indexes but something still isn't right with this. Any input would be greatly appreciated.</p>

<p>Tried using FORCE INDEX to no avail:</p>

<pre><code>explain     SELECT cc.title AS category, a.id, a.title, a.alias, a.title_alias, a.introtext, a.fulltext, a.sectionid, a.state, a.catid, a.created, a.created_by, a.created_by_alias, a.modified, a.modified_by, a.checked_out, a.checked_out_time, a.publish_up, a.publish_down, a.attribs, a.hits, a.images, a.urls, a.ordering, a.metakey, a.metadesc, a.access, CASE WHEN CHAR_LENGTH(a.alias) THEN CONCAT_WS(":", a.id, a.alias) ELSE a.id END AS slug, CASE WHEN CHAR_LENGTH(cc.alias) THEN CONCAT_WS(":", cc.id, cc.alias) ELSE cc.id END AS catslug, CHAR_LENGTH( a.`fulltext` ) AS readmore, u.name AS author, u.usertype, g.name AS groups, u.email AS author_email
    -&gt;     FROM bak_content AS a
    -&gt;     FORCE INDEX (idx_title_created)
    -&gt;     LEFT JOIN bak_categories AS cc
    -&gt;     ON a.catid = cc.id
    -&gt;     LEFT JOIN bak_users AS u
    -&gt;     ON u.id = a.created_by
    -&gt;     LEFT JOIN bak_groups AS g
    -&gt;     ON a.access = g.id
    -&gt;     WHERE 1
    -&gt;     AND a.access &lt;= 0
    -&gt;     AND a.catid = 108
    -&gt;     AND a.state = 1
    -&gt;     AND ( publish_up = '0000-00-00 00:00:00' OR publish_up &lt;= '2012-02-08
    -&gt;     AND ( publish_down = '0000-00-00 00:00:00' OR publish_down &gt;= '2012-0
    -&gt;     ORDER BY a.title, a.created DESC
    -&gt;     LIMIT 0, 10;
</code></pre>

<p>Produces:</p>

<pre><code>+----+-------------+-------+--------+---------------+---------+---------+-------
| id | select_type | table | type   | possible_keys | key     | key_len | ref
+----+-------------+-------+--------+---------------+---------+---------+-------
|  1 | SIMPLE      | a     | ALL    | NULL          | NULL    | NULL    | NULL
|  1 | SIMPLE      | cc    | const  | PRIMARY       | PRIMARY | 4       | const
|  1 | SIMPLE      | u     | eq_ref | PRIMARY       | PRIMARY | 4       | database
|  1 | SIMPLE      | g     | eq_ref | PRIMARY       | PRIMARY | 1       | database
+----+-------------+-------+--------+---------------+---------+---------+-------
</code></pre>

## Answers
### Answer ID: 9306402
<p>I hope this is syntactically correct</p>

<pre><code>SELECT
    cc.title AS category,
    a.id, a.title, a.alias, a.title_alias,
    a.introtext, a.fulltext, a.sectionid,
    a.state, a.catid, a.created, a.created_by,
    a.created_by_alias, a.modified, a.modified_by,
    a.checked_out, a.checked_out_time,
    a.publish_up, a.publish_down, a.attribs,
    a.hits, a.images, a.urls, a.ordering, a.metakey,
    a.metadesc, a.access,
    CASE WHEN CHAR_LENGTH(a.alias) THEN CONCAT_WS(":", a.id, a.alias) ELSE a.id END AS slug,
    CASE WHEN CHAR_LENGTH(cc.alias) THEN CONCAT_WS(":", cc.id, cc.alias) ELSE cc.id END AS catslug, CHAR_LENGTH( a.`fulltext` ) AS readmore,
    u.name AS author, u.usertype, g.name AS groups, u.email AS author_email 
FROM
(
    SELECT aa.*
    FROM 
    (
        SELECT id FROM 
        FROM j15_content
        WHERE catid=108 AND state=1
        AND a.access &lt;= 0 
        AND (publish_up   = '0000-00-00 00:00:00' OR   publish_up &lt;= '2012-02-08 00:16:26')
        AND (publish_down = '0000-00-00 00:00:00' OR publish_down &gt;= '2012-02-08 00:16:26')
        ORDER BY title,created DESC
        LIMIT 0,10
    ) needed_keys
    LEFT JOIN j15_content aa USING (id)
) a
LEFT JOIN j15_categories AS cc ON a.catid = cc.id 
LEFT JOIN j15_users AS u ON a.created_by = u.id
LEFT JOIN j15_groups AS g ON a.access = g.id;
</code></pre>

<p>You will need a supporting index for subquery needed_keys</p>

<pre><code>ALTER TABLE j15_content ADD INDEX subquery_ndx (catid,state,access,title,created);
</code></pre>

<p>Give it a Try !!!</p>

### Answer ID: 9253997
<p>Have you tried increasing these values tmp_table_size and max_heap_table_size:</p>

<p>There is a short explanation <a href="http://dev.mysql.com/doc/refman/5.6/en/internal-temporary-tables.html" rel="nofollow">here</a> and also links to the detail of each of them.</p>

<p>Hope this helps!</p>

### Answer ID: 9240583
<p>AFAIK this can't be reasonably solved using an index, hints or restructuring of the query itself.</p>

<p>The reason this is slow is the fact that it requires a filesort of 2M rows which does actually take a long time. If you zoom in on the order by it's specified as <code>ORDER BY a.title, a.created DESC</code>. The problem is the combination of sorting on more than 1 column and having a DESC part. Mysql does not support descending indexes (the keyword DESC is supported in the <a href="http://dev.mysql.com/doc/refman/5.0/en/create-index.html" rel="nofollow">CREATE INDEX statement</a> but only for future use).</p>

<p>The suggested workaround is to create an extra column 'reverse_created' that gets automatically populated in such a way that your query can use <code>ORDER BY a.title, a.reverse_created</code>. So you fill it with <code>max_time - created_time</code>. Then create an index on that combination and (if needed) specify that index as a hint.</p>

<p>There are a couple of really good blog articles about this topic that explain this a lot better and with examples:</p>

<ul>
<li><a href="http://www.mysqlperformanceblog.com/2006/05/09/descending-indexing-and-loose-index-scan/" rel="nofollow">http://www.mysqlperformanceblog.com/2006/05/09/descending-indexing-and-loose-index-scan/</a></li>
<li><a href="http://www.mysqlperformanceblog.com/2007/02/16/using-index-for-order-by-vs-restricting-number-of-rows/" rel="nofollow">http://www.mysqlperformanceblog.com/2007/02/16/using-index-for-order-by-vs-restricting-number-of-rows/</a></li>
</ul>

<p>-Update- You should be able to do a quick test on this by removing the "DESC" part from the order by in your query. The results will be functionally wrong but it should use the existing index you have (or otherwise the force should work).</p>

### Answer ID: 9239923
<p>Perhaps trying this might help:</p>

<pre class="lang-sql prettyprint-override"><code>CREATE INDEX idx_catid_title_created ON j15_content (catid,title(8),created);
DROP INDEX idx_catid ON j15_content;
</code></pre>

### Answer ID: 9221076
<p>Can you try this variation:</p>

<pre><code>SELECT cc.title AS category, ...
FROM 
    ( SELECT *
      FROM j15_content AS a 
               USE INDEX (title)             --- with and without the hint
      WHERE 1
        AND a.access &lt;= 0
        AND a.catid = 108
        AND a.state = 1
        AND ( publish_up = '0000-00-00 00:00:00' 
           OR publish_up &lt;= '2012-02-08 00:16:26' )
        AND ( publish_down = '0000-00-00 00:00:00' 
           OR publish_down &gt;= '2012-02-08 00:16:26' )
      ORDER BY a.title, a.created DESC
      LIMIT 0, 10
    ) AS a
  LEFT JOIN j15_categories AS cc
    ON a.catid = cc.id
  LEFT JOIN j15_users AS u
    ON u.id = a.created_by
  LEFT JOIN j15_groups AS g
    ON a.access = g.id
</code></pre>

<p>An index on <code>(catid, state, title)</code> would be even better I think.</p>

### Answer ID: 9207376
<p>Sometimes MySQL has trouble finding the proper index. You can resolve this by hinting to the proper index. </p>

<p>Hint syntax:
<a href="http://dev.mysql.com/doc/refman/4.1/en/index-hints.html" rel="nofollow">http://dev.mysql.com/doc/refman/4.1/en/index-hints.html</a></p>

<p>Make sure you have the right index and tune it's performance by experimenting.</p>

<p>Cheers!</p>

