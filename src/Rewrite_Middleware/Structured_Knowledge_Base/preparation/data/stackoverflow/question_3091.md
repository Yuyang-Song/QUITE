# Using tablenames as argument in execute prepared statement
[Link to question](https://stackoverflow.com/questions/66212591/using-tablenames-as-argument-in-execute-prepared-statement)
**Creation Date:** 1613409848
**Score:** 0
**Tags:** mysql, prepared-statement
## Question Body
<p>Working in the query-box of phpMyAdmin I want to write an outfile 'protokoll' for each table in a MySQL 5.5 database. As I have many databases that contain the same tables and are different by name only, I want the filename of the outfile to look like
/tmp/dbname_protokoll_tablename_.csv</p>
<p>This works:</p>
<pre><code>SELECT DATABASE() into @client;
SET @dir = '/tmp/';
SET @table = 'Adressen';
SET @stmt = CONCAT( 'SELECT * from ', @table, ' WHERE MarkDel=1 into outfile ''', @dir, @client , '_Protokoll_', @table , '.csv'' CHARACTER SET utf8 FIELDS TERMINATED BY '','' OPTIONALLY ENCLOSED BY ''&quot;'' LINES TERMINATED BY ''\r\n'' ');
PREPARE DoExport from @stmt;
EXECUTE DoExport;
DEALLOCATE PREPARE DoExport;
</code></pre>
<p>From what I read about prepare, I should be able to use a '?' inside the statement, like</p>
<pre><code>SET @stmt = CONCAT( 'SELECT * from ? WHERE MarkDel=1 into outfile ...
</code></pre>
<p>and then execute this with a list of arguments like</p>
<pre><code>EXECUTE DoExport USING 'Adressen', 'Familien', 'Kinder';
</code></pre>
<p>but I can't get this to work, all I receive is an unspecific syntax error. How do I have to rewrite this?</p>

