# query extremely slow after migration to mysql 5.7
[Link to question](https://stackoverflow.com/questions/37733946/query-extremely-slow-after-migration-to-mysql-5-7)
**Creation Date:** 1465498114
**Score:** 10
**Tags:** mysql, database, performance, migration
## Question Body
<p>I have a MySQL database with InnoDB tables summing up over 10 ten GB of data that I want to migrate from MySQL 5.5 to MySQL 5.7. And I have a query that looks a bit like:</p>

<pre><code>SELECT dates.date, count(mySub2.myColumn1), sum(mySub2.myColumn2)
FROM (
    SELECT date
    FROM dates -- just a table containing all possible dates next 5 years
    WHERE date BETWEEN '2016-06-01' AND '2016-09-03'
) AS dates
LEFT JOIN (
    SELECT o.id, time_start, time_end
    FROM order AS o
    INNER JOIN order_items AS oi on oi.order_id = o.id
    WHERE time_start BETWEEN '2016-06-01' AND '2016-09-03'
) AS mySub1 ON dates.date &gt;= mySub1.time_start AND dates.date &lt; mySub1.time_end
LEFT JOIN (
    SELECT o.id, time_start, time_end
    FROM order AS o
    INNER JOIN order_items AS oi on oi.order_id = o.id
    WHERE o.shop_id = 50 AND time_start BETWEEN '2016-06-01' AND '2016-09-03'
) AS mySub2 ON dates.date &gt;= mySub2.time_start AND dates.date &lt; mySub2.time_end
GROUP BY dates.date;
</code></pre>

<p>My problem is that this query is performing fast in MySQL 5.5 but extremely slow in MySQL 5.7.</p>

<p>In MySQL 5.5 it is taking over 1 second at first and &lt; 0.001 seconds every recurring execution without restarting MySQL.<br>
In MySQL 5.7 it is taking over 11.5 seconds at first and 1.4 seconds every recurring execution without restarting MySQL.<br>
And the more LEFT JOINs I add to the query, the slower the query becomes in MySQL 5.7.</p>

<p>Both instances now run on the same machine, on the same hard drive and with the same my.ini settings. So it isn't hardware.<br>
The execution plans do differ, though and I don't know what to make from it.</p>

<p>This is the EXPLAIN EXTENDED on MySQL 5.5:</p>

<pre><code>| id | select_type | table      | type  | possible_keys | key         | key_len | ref       | rows  | filtered | extra                           |
|----|-------------|------------|-------|---------------|-------------|---------|-----------|-------|----------|---------------------------------|
| 1  | PRIMARY     | dates      | ALL   |               |             |         |           | 95    | 100.00   | Using temporary; Using filesort |
| 1  | PRIMARY     | &lt;derived2&gt; | ALL   |               |             |         |           | 281   | 100.00   | ''                              |
| 1  | PRIMARY     | &lt;derived3&gt; | ALL   |               |             |         |           | 100   | 100.00   | ''                              |
| 3  | DERIVED     | o          | ref   | xxxxxx        | shop_id_fk  | 4       | ''        | 1736  | 100.00   | ''                              |
| 3  | DERIVED     | oc         | ref   | xxxxx         | order_id_fk | 4       | myDb.o.id | 1     | 100.00   | Using index                     |
| 2  | DERIVED     | o          | range | xxxx          | date_start  | 3       |           | 17938 | 100.00   | Using where                     |
| 2  | DERIVED     | oc         | ref   | xxx           | order_id_fk | 4       | myDb.o.id | 1     | 100.00   | Using where                     |
</code></pre>

<p>This is the EXPLAIN EXTENDED on MySQL 5.7:</p>

<pre><code>| id | select_type | table | type   | possible_keys | key         | key_len | ref              | rows | filtered | extra          |
|----|-------------|-------|--------|---------------|-------------|---------|------------------|------|----------|----------------|
| 1  | SIMPLE      | dates | ALL    |               |             |         |                  | 95   | 100.00   | Using filesort |
| 1  | SIMPLE      | oi    | ref    | xxxxxx        | order_id_fk | 4       | const            | 228  | 100.00   |                |
| 1  | SIMPLE      | o     | eq_ref | xxxxx         | PRIMARY     | 4       | myDb.oi.order_id | 1    | 100.00   | Using where    |
| 1  | SIMPLE      | o     | ref    | xxxx          | shop_id_fk  | 4       | const            | 65   | 100.00   | Using where    |
| 1  | SIMPLE      | oi    | ref    | xxx           | order_id_fk | 4       | myDb.o.id        | 1    | 100.00   | Using where    |
</code></pre>

<p>I want to understand why the MySQLs treat the same query that much different, and how I can tweak MySQL 5.7 to be faster?<br>
I'm not looking for help on rewriting the query to be faster, as that is something I am already doing on my own.</p>

## Answers
### Answer ID: 61142750
<p>I too faced slow query execution issue after migrating to mysql 5.7 and in my case, even setting session optimizer_switch to 'derived_merge=off'; didn't help. </p>

<p>Then, I followed this link: <a href="https://www.saotn.org/mysql-innodb-performance-improvement/" rel="nofollow noreferrer">https://www.saotn.org/mysql-innodb-performance-improvement/</a> and the query's speed became normal. </p>

<p>To be specific my change was just setting these four parameters in my.ini as described in the link:</p>

<p>innodb_buffer_pool_size</p>

<p>innodb_buffer_pool_instances</p>

<p>innodb_write_io_threads</p>

<p>innodb_read_io_threads</p>

### Answer ID: 38016228
<p>Building and maintaining a "Summary Table" would make this query run much faster than even 1 second.</p>

<p>Such a table would probably include <code>shop_id</code>, <code>date</code>, and some count.</p>

<p><a href="http://mysql.rjweb.org/doc.php/summarytables" rel="nofollow">More on summary tables</a>.</p>

### Answer ID: 37743777
<p>As can be read in the comments, @wchiquito has suggested to look at the <code>optimizer_switch</code>. In here I found that the switch <code>derived_merge</code> could be set to off, to fix this new, and in this specific case undesired, behaviour.</p>

<p><code>set session optimizer_switch='derived_merge=off';</code> fixes the problem.<br>
(This can also be done with <code>set global ...</code> or be put in the my.cnf / my.ini)</p>

