# Index to search in multiple tables
[Link to question](https://stackoverflow.com/questions/73430247/index-to-search-in-multiple-tables)
**Creation Date:** 1661030759
**Score:** 1
**Tags:** mysql, sql, mysql-8.0
## Question Body
<h2>Problem</h2>
<p>TL;DR
My query is slow.</p>
<p>Im trying to find multiple <code>customer</code> by a given search-term &quot;J&quot;. The fields im scanning are distributed among 2 tables <code>customer</code> and <code>company_customer</code>:</p>
<ul>
<li><code>firstname</code> begins with</li>
<li><code>lastname</code> begins with</li>
<li><code>number</code> begins with (this is the specific customer-number for a company/custumer combination)</li>
</ul>
<p>I'm having a hard time optimizing the database and query (running mysql-8).</p>
<p>I've tested this with 10 companies and 100k customers each. The search took <strong>close to half a second</strong> - there has to be a way to get this faster.</p>
<h2>The query</h2>
<pre><code>SELECT
    cc.number,
    c.firstname,
    c.lastname
FROM
    customer c
    JOIN company_customer cc
        ON cc.customer_id = c.id
WHERE
    cc.company_id = 1
    AND (
           c.lastname LIKE 'J%'
        OR c.firstname LIKE 'J%'
        OR cc.number LIKE 'J%'
    )
ORDER BY
    lastname,
    firstname
LIMIT 20;
</code></pre>
<h2>The schema (simplyfied)</h2>
<ul>
<li>company (id, ...)</li>
<li>customer (id, ...)</li>
<li>company_customer (company_id, customer_id, number)</li>
</ul>
<p><a href="https://www.db-fiddle.com/f/82KBeQ2yT3BFyAhpoyc6BA/2" rel="nofollow noreferrer">Fiddle</a></p>
<h2>What I've tried</h2>
<ul>
<li>remove the actual search part to pinpoint the problem (every <code>like</code>) - still slow</li>
<li>get a list of <code>customer.id</code> via subselect - even slower</li>
<li>split the search - but when i search for <code>customer</code>s i only want to search for those associated with a specific <code>company_cusomer.company_id</code> - so i cant get around the join right?</li>
<li>Find possible index by using <code>EXPLAIN</code></li>
</ul>
<h2>What I've found out</h2>
<p>I think the problem is the index for <code>lastname, firstname</code> is not being used since the <code>JOIN</code> occupies the index usage - since only one may be used.</p>
<h2>The question</h2>
<p>Is there a way to set an index to get the data faster?
Or a way to rewrite the sql to get the data faster?</p>
<h2>Edit</h2>
<p>the explain (before with 1M rows in customers):</p>
<pre><code>+----+-------------+-------+------------+--------+-------------------------+---------+---------+---------------------+--------+----------+---------------------------------+
| id | select_type | table | partitions | type   | possible_keys           | key     | key_len | ref                 | rows   | filtered | Extra                           |
+----+-------------+-------+------------+--------+-------------------------+---------+---------+---------------------+--------+----------+---------------------------------+
|  1 | SIMPLE      | cc    | NULL       | ref    | PRIMARY,IDX_co,IDX_cu   | PRIMARY | 4       | const               | 204966 |   100.00 | Using temporary; Using filesort |
|  1 | SIMPLE      | c     | NULL       | eq_ref | PRIMARY                 | PRIMARY | 4       | test.cc.customer_id |      1 |   100.00 | NULL                            |
+----+-------------+-------+------------+--------+-------------------------+---------+---------+---------------------+--------+----------+---------------------------------+
</code></pre>
<p>the explain (before 1M rows):</p>
<pre><code>+----+-------------+-------+------------+--------+-----------------------+---------+---------+-----------------+------+----------+-------------+
| id | select_type | table | partitions | type   | possible_keys         | key     | key_len | ref             | rows | filtered | Extra       |
+----+-------------+-------+------------+--------+-----------------------+---------+---------+-----------------+------+----------+-------------+
|  1 | SIMPLE      | c     | NULL       | index  | PRIMARY               | IDX_lf  | 804     | NULL            |   20 |   100.00 | Using index |
|  1 | SIMPLE      | cc    | NULL       | eq_ref | PRIMARY,IDX_co,IDX_cu | PRIMARY | 8       | const,test.c.id |    1 |   100.00 | NULL        |
+----+-------------+-------+------------+--------+-----------------------+---------+---------+-----------------+------+----------+-------------+
</code></pre>

## Answers
### Answer ID: 73431253
<p>The <code>OR</code>, especially since it touches more than one table, is especially hard to optimize.</p>
<p>These may help:</p>
<pre><code>cc:  INDEX(company_id, number, customer_id)
c:  INDEX(lastname, firstname, id)
</code></pre>
<p>The best optimization (especially for huge tables) would be to switch to <code>UNION</code>:</p>
<pre><code>SELECT *
    FROM (
        ( SELECT ... with one of the LIKEs ...
              ORDER BY c.lastname, c.firstname LIMIT 20 )
        UNION DISTINCT
        ( SELECT ... with another of the LIKEs ...
              ORDER BY c.lastname, c.firstname LIMIT 20 )
        UNION DISTINCT
        ( SELECT ... with the other LIKE ...
              ORDER BY c.lastname, c.firstname LIMIT 20 )
         ) AS x
    ORDER BY lastname, firstname   -- again
    LIMIT 20      -- again
    ;
</code></pre>
<p>And more indexes (note reordering of columns:</p>
<pre><code>cc:  INDEX(number, company_id, customer_id)
c:  INDEX(firstname, lastname, id)
</code></pre>
<p>(There may be a further optimization, but give this a try first.)</p>

