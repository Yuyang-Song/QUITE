# Avoiding failed inserts to avoid spurious autoincrement
[Link to question](https://stackoverflow.com/questions/10600010/avoiding-failed-inserts-to-avoid-spurious-autoincrement)
**Creation Date:** 1337082295
**Score:** 4
**Tags:** mysql, sql, innodb, auto-increment
## Question Body
<p>My problem is the same as <a href="https://stackoverflow.com/q/2787910/">Why does MySQL autoincrement increase on failed inserts?</a>, but instead of increasing my <code>id</code> field, I would prefer just to rewrite the <code>INSERT</code> query that is causing me trouble. Pretend I have a database with two fields, <code>id</code> and <code>username</code>, where <code>id</code> is a primary key and <code>username</code> is a unique key. I'm essentially looking for syntax that would do <code>INSERT...IF NOT EXISTS</code>. Right now, I do </p>

<pre><code>INSERT INTO `table`(`username`) 
    VALUES ('foo') 
    ON DUPLICATE KEY UPDATE `id`=`id`
</code></pre>

<p>I only have one thread writing to the database, so I don't need any sort of concurrency protection. Suggestions?</p>

## Answers
### Answer ID: 29266665
<p>you can simply reset the auto increment field after the failed insert</p>

<p>ALTER TABLE table_name AUTO_INCREMENT =1;</p>

<p>this will not reset the auto increment to 1 but will reset it to the current maximum plus one</p>

<p>also note that the user you are connected with to the DB should has alter privilege to the targeted table</p>

### Answer ID: 26780692
<p>You can also check before insert that user if it was inserted before, it will cost an extra call into your DB but, if the user already exists, you can return the information that you found and a fake insert is avoided.</p>

### Answer ID: 10600531
<p>You should use this:</p>

<pre><code>INSERT INTO tableX (username) 
  SELECT 'foo' AS username
  FROM dual
  WHERE NOT EXISTS
        ( SELECT *
          FROM tableX 
          WHERE username = 'foo'
        ) ;
</code></pre>

<p>If you want to include values for more columns:</p>

<pre><code>INSERT INTO tableX (username, dateColumn) 
  SELECT 'foo'                       --- the aliases are not needed             
       , NOW()                       --- actually
  FROM dual
  WHERE NOT EXISTS
        ( SELECT *
          FROM tableX 
          WHERE username = 'foo'
        ) ;                      
</code></pre>

### Answer ID: 10600542
<p>I don't think you can prevent the counter from being incremented, for the reasons given in the answers the question to which you've linked.</p>

<p>You have three options:</p>

<ol>
<li><p>Live with skipped identifiers; do you really expect to use up 64-bits?</p></li>
<li><p>Check for existence of the existing record prior to attempting the <code>INSERT</code>:</p>

<pre><code>DELIMITER ;;

IF NOT EXISTS (SELECT * FROM `table` WHERE username = 'foo') THEN
  INSERT INTO `table` (username) VALUES ('foo');
END IF;;

DELIMITER ;
</code></pre>

<p>Or, better yet, use the <code>FROM dual WHERE NOT EXISTS ...</code> form suggested by @ypercube.</p></li>
<li><p>Reset the counter after each insert.  If performing the <code>INSERT</code> operation within a stored procedure, you could do this using a handler for duplicate key errors:</p>

<pre><code>DELIMITER ;;

CREATE PROCEDURE TEST(IN uname CHAR(16) CHARSET latin1) BEGIN
  DECLARE CONTINUE HANDLER FOR SQLSTATE '23000' BEGIN
    -- WARNING: THIS IS NOT SAFE FOR CONCURRENT CONNECTIONS
    SET @qry = CONCAT(
      'ALTER TABLE `table` AUTO_INCREMENT = ',
      (SELECT MAX(id) FROM `table`)
    );
    PREPARE stmt FROM @qry;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    SET @qry = NULL;
  END;
  INSERT INTO `table` (username) VALUES (uname);
END;;
DELIMITER ;
</code></pre>

<p>Bearing in mind the (valid) concerns @ypercube raised in his comments beneath regarding this strategy, you might instead use:</p>

<pre><code>SELECT AUTO_INCREMENT - 1
FROM   INFORMATION_SCHEMA.TABLES
WHERE  table_schema = 'db_name' AND table_name = 'table';
</code></pre></li>
</ol>

### Answer ID: 10600070
<p>use <code>INSERT IGNORE INTO table</code>. Check the below post</p>

<p><a href="http://bogdan.org.ua/2007/10/18/mysql-insert-if-not-exists-syntax.html" rel="nofollow">http://bogdan.org.ua/2007/10/18/mysql-insert-if-not-exists-syntax.html</a></p>

<p>You can do it like:</p>

<pre><code>INSERT INTO `table`(`username`) 
VALUES ('foo')      
ON DUPLICATE KEY UPDATE `username`= 'foo' 
</code></pre>

<p>OR</p>

<pre><code>INSERT IGNORE INTO `table`
SET `username` = 'foo'
</code></pre>

