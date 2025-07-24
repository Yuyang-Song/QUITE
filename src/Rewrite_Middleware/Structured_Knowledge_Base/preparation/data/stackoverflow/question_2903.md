# MySQL, MariaDB: How do I create a child-parent hierarchical recursive query?
[Link to question](https://stackoverflow.com/questions/58030967/mysql-mariadb-how-do-i-create-a-child-parent-hierarchical-recursive-query)
**Creation Date:** 1568991965
**Score:** 0
**Tags:** mysql, sql, mariadb
## Question Body
<p>I have the following MySQL query:</p>

<pre><code>SELECT * FROM (SELECT * FROM paper ORDER BY id DESC) paper_sorted,
        (SELECT @pv := 26) initialisation
        WHERE find_in_set(id, @pv)
        AND length(@pv := concat(@pv, ',', last_id))
        ORDER BY @pv ASC LIMIT 0,15
</code></pre>

<p><a href="http://sqlfiddle.com/#!9/9e2df/24" rel="nofollow noreferrer">http://sqlfiddle.com/#!9/9e2df/24</a></p>

<p>This works perfectly fine in MySQL; however, I am working with a MariaDB database and this query is not working.  Anyway to rewrite this for it to work for both MySQL and MariaDB? </p>

<p>Database schema:</p>

<pre><code>CREATE TABLE paper (
    id INT,
    last_id INT
);

INSERT INTO paper VALUES (19, 0);
INSERT INTO paper VALUES (20, 19);
INSERT INTO paper VALUES (21, 20);
INSERT INTO paper VALUES (22, 21);
INSERT INTO paper VALUES (23, 19);
INSERT INTO paper VALUES (24, 23);
INSERT INTO paper VALUES (25, 23);
INSERT INTO paper VALUES (26, 24);
</code></pre>

<p>MariaDB v. 10.3.18;
MySQL v. 5.7.27</p>

<p>This SQL query should get all the Parent IDs. 
As in the example query, <code>@pv</code> variable is 26, and thus gets 26->24->23->19.</p>

<p>However, this is not working for MariaDB.  It's only returning one row, which is 26 in MariaDB.  How to rewrite this query to work for both MariaDB and MySQL?</p>

## Answers
### Answer ID: 58032224
<p>You should be able to rewrite the query as a <a href="https://mariadb.com/kb/en/library/recursive-common-table-expressions-overview/" rel="nofollow noreferrer">Recursive CTE</a>. These were added into MariaDB 10.2 and allow querying hierarchical data structures with SQL.</p>

<p>Something along these lines should work:</p>

<pre><code>WITH RECURSIVE p AS (
    SELECT * FROM paper WHERE id = 26
    UNION
    SELECT c.* FROM paper AS c, p WHERE p.last_id = c.id
) SELECT * FROM p ORDER BY id ASC LIMIT 15;
</code></pre>

<hr>

<p><strong>Edit:</strong> If you need the SQL to be backwards compatible with older versions, you can use a stored procedure to achieve the same result.</p>

<pre><code>DELIMITER // ;

CREATE OR REPLACE PROCEDURE p1(IN id_in INT)
BEGIN
    DECLARE i INT DEFAULT id_in;
    CREATE OR REPLACE TEMPORARY TABLE results LIKE paper;

    WHILE i IS NOT NULL DO
          INSERT INTO results SELECT p.id, p.last_id FROM paper AS p WHERE p.id = i;
          SET i = (SELECT r.last_id FROM results AS r WHERE r.id = i LIMIT 1);
    END WHILE;

    SELECT * FROM results;
    DROP TEMPORARY TABLE results;
END;
//

DELIMITER ; //
</code></pre>

