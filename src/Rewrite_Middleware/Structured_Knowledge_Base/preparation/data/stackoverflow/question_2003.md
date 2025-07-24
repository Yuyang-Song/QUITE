# Mysql Join on range of time values (no exact relation)
[Link to question](https://stackoverflow.com/questions/15337155/mysql-join-on-range-of-time-values-no-exact-relation)
**Creation Date:** 1363000356
**Score:** 1
**Tags:** mysql, performance, join, range
## Question Body
<p>I am evaluating logfiles for a research project and inserted them to a MySQL database.
Now I have a query where I need to join data from other tables without having an exact matching value.</p>

<p>The "logdata" table contains the data of mobile units I have to analyze, "basepositions" holds the GPS coordinates of base stations. In two of the data fields of "logdata" the sender position of the corresponding base station is logged. The problem there is: the position of the base station varies slightly over time (GPS fluctuation, just some degrees), so I have to look for the right entry by using the BETWEEN operation as seen in the query below. This is not perfect, but there are only about 100 base stations, so the cost is tolerable here.</p>

<p>The same problem exists in the second join. There I have to get a validity flag out of another table. The problem here is: both logs are written approximately every second, but are not synchronized. So i have to scan for the corresponding row, again by using BETWEEN and the time range of 1 second.</p>

<p>Because of the number of rows, this second scan lets my execution time explode.
I think the diffuse correlation is the problem here.</p>

<p>The two tables both have the indexes given in the overview below.</p>

<p>Is there a way to speed up the query? Because of the performance problems it now takes 30 hours to complete in my database setup to return around 20000 rows.</p>

<p>I appreciate any help.</p>

<p>logdata (~ 300.000.000 entries):</p>

<pre><code>+-----------+---------------------+------+-----+---------+----------------+
| Field     | Type                | Null | Key | Default | Extra          |
+-----------+---------------------+------+-----+---------+----------------+
| id        | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| unit      | tinytext            | YES  | MUL | NULL    |                |
| timestamp | bigint(20)          | YES  |     | NULL    |                |
| logid     | int(11)             | YES  |     | NULL    |                |
| d1        | bigint(20)          | YES  |     | NULL    |                |
| d2        | bigint(20)          | YES  |     | NULL    |                |
| d3        | bigint(20)          | YES  |     | NULL    |                |
| d4        | bigint(20)          | YES  |     | NULL    |                |
| d5        | bigint(20)          | YES  |     | NULL    |                |
| d6        | bigint(20)          | YES  |     | NULL    |                |
| d7        | bigint(20)          | YES  |     | NULL    |                |
| d8        | bigint(20)          | YES  |     | NULL    |                |
| d9        | bigint(20)          | YES  |     | NULL    |                |
| d10       | bigint(20)          | YES  |     | NULL    |                |
+-----------+---------------------+------+-----+---------+----------------+
</code></pre>

<p>basepositions (~100 entries):</p>

<pre><code>+----------------------------+--------------+------+-----+---------+-------+
| Field                      | Type         | Null | Key | Default | Extra |
+----------------------------+--------------+------+-----+---------+-------+
| ID                         | int(11)      | NO   | PRI | NULL    |       |
| GPSLONGITUDE               | varchar(50)  | YES  |     | NULL    |       |
| LOCATION                   | varchar(100) | YES  |     | NULL    |       |
| GPSLATITUDE                | varchar(50)  | YES  |     | NULL    |       |
| GPSALTITUDE                | varchar(50)  | YES  |     | NULL    |       |
| ISUNDERTEST                | tinyint(1)   | YES  |     | 0       |       |
+----------------------------+--------------+------+-----+---------+-------+
</code></pre>

<p>validity (~200.000.000 entries):</p>

<pre><code>+-----------+---------------------+------+-----+---------+----------------+
| Field     | Type                | Null | Key | Default | Extra          |
+-----------+---------------------+------+-----+---------+----------------+
| id        | bigint(20) unsigned | NO   | PRI | NULL    | auto_increment |
| unit      | tinytext            | YES  | MUL | NULL    |                |
| timestamp | bigint(20)          | YES  |     | NULL    |                |
| logid     | int(11)             | YES  |     | NULL    |                |
| d1        | bigint(20)          | YES  |     | NULL    |                |
+-----------+---------------------+------+-----+---------+----------------+
</code></pre>

<p>my query so far:</p>

<pre><code>SELECT
    logdata.unit,
    logdata.timestamp,
    logdata.d1,
    logdata.d2,
    cast(logdata.d3/10000000 as decimal(15, 10)),
    cast(logdata.d4/10000000 as decimal(15, 10)),
    logdata.d5,
    logdata.d6,
    logdata.d7,
    logdata.d8,
    cast(logdata.d9/10000000 as decimal(15, 10)),
    cast(logdata.d10/10000000 as decimal(15, 10)),
    BASEID,
    validity.d1
FROM
    logdata
JOIN
    basepositions
ON
    cast(GPSLATITUDE / 10000000 as decimal(15,10)) BETWEEN cast(d3 / 10000000 as decimal(15,10)) - 0.0001 AND cast(d3 / 10000000 as decimal(15,10)) + 0.0001
    AND
    cast(GPSLONGITUDE / 10000000 as decimal(15,10)) BETWEEN cast(d4 / 10000000 as decimal(15,10)) - 0.0001 AND cast(d4 / 10000000 as decimal(15,10)) + 0.0001
JOIN
    validity
ON
    validity.unit = logdata.unit 
    AND
    validity.logid = 12345
    AND
    validity.timestamp BETWEEN logdata.timestamp - 500 AND logdata.timestamp + 499

WHERE
    logdata.unit = "IVS${IVS}"
    AND
    logdata.logid = 111222
    AND 
    BASEID = 012;
</code></pre>

<p>indeces:</p>

<pre><code>+-------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table             | Non_unique | Key_name             | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+-------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| logdata           |          0 | PRIMARY              |            1 | id          | A         |   301433830 |     NULL | NULL   |      | BTREE      |         |               |
| logdata           |          1 | unit_logid_timestamp |            1 | unit        | A         |          18 |        6 | NULL   | YES  | BTREE      |         |               |
| logdata           |          1 | unit_logid_timestamp |            2 | logid       | A         |          18 |     NULL | NULL   | YES  | BTREE      |         |               |
| logdata           |          1 | unit_logid_timestamp |            3 | timestamp   | A         |   301433830 |     NULL | NULL   | YES  | BTREE      |         |               |
+-------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
</code></pre>

<p><strong>EDIT (Comment field was to small):</strong>
I think the problem is the join that is constructed. EXPLAIN EXTENDED shows, that the query optimizer is joining all three tables together, which means 300.000.000 * 200.000.000 * 100 rows to look through.
When I rewrite the join with "validity" to a subquery mysql is just joining  "logdata" and "basepositions".
I think data type changes could be a factor in later optimizing but first i think i have to get down a few runtime classes by optimizing the query plan.
I'm not experienced enough to know what i can do to further optimize this query.
The single query for a timestamp on "validity" returns in no time at all.
The single query for the Basestation position is also very fast.
I don't know how I can convince mysql to first filter and the join my query.</p>

<p><strong>EDIT 2:</strong></p>

<p>here are the idexes you asked for. I got them using "SHOW INDEXES FROM"</p>

<p>indexes for "validity":</p>

<pre><code>+-------------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table                   | Non_unique | Key_name             | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+-------------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| validity                |          0 | PRIMARY              |            1 | id          | A         |   194863653 |     NULL | NULL   |      | BTREE      |         |               |
| validity                |          1 | unit_logid_timestamp |            1 | unit        | A         |          18 |        6 | NULL   | YES  | BTREE      |         |               |
| validity                |          1 | unit_logid_timestamp |            2 | logid       | A         |          18 |     NULL | NULL   | YES  | BTREE      |         |               |
| validity                |          1 | unit_logid_timestamp |            3 | timestamp   | A         |   194863653 |     NULL | NULL   | YES  | BTREE      |         |               |
+-------------------------+------------+----------------------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
</code></pre>

<p>indexes for "basepositions":</p>

<pre><code>+----------------------+------------+---------------------------------------+--------------+----------------------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| Table                | Non_unique | Key_name                              | Seq_in_index | Column_name                | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment |
+----------------------+------------+---------------------------------------+--------------+----------------------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
| basepositions        |          0 | PRIMARY                               |            1 | ID                         | A         |         109 |     NULL | NULL   |      | BTREE      |         |               |
+----------------------+------------+---------------------------------------+--------------+----------------------------+-----------+-------------+----------+--------+------+------------+---------+---------------+
</code></pre>

<p>EXPLAIN of the query above:</p>

<pre><code>id      select_type     table           type    possible_keys           key                     key_len     ref         rows        filtered    Extra
1       SIMPLE          basepositions   const   PRIMARY                 PRIMARY                 4           const       1           100.00  
1       SIMPLE          logdata         ref     unit_logid_timestamp    unit_logid_timestamp    14          const,const 4150932     100.00      Using where
1       SIMPLE          validity        ref     unit_logid_timestamp    unit_logid_timestamp    14          const,const 3294136     100.00      Using where
</code></pre>

<p>EXPLAIN (after adding indexes for lat/lon):</p>

<pre><code>id      select_type     table         type    possible_keys            key                     key_len  ref             rows    filtered    Extra
1       SIMPLE          basepositions const   PRIMARY,lat_lon,lat,lon  PRIMARY                 4        const           1       100.00
1       SIMPLE          logdata       ref     unit_logid_timestamp     unit_logid_timestamp    14       const,const     4150932 100.00      Using where
1       SIMPLE          validity      ref     unit_logid_timestamp     unit_logid_timestamp    14       const,const     3294136 100.00      Using where
</code></pre>

