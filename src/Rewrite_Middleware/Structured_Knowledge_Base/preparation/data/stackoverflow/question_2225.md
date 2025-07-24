# How can I delete duplicate rows from a table without naming columns in the query?
[Link to question](https://stackoverflow.com/questions/24685977/how-can-i-delete-duplicate-rows-from-a-table-without-naming-columns-in-the-query)
**Creation Date:** 1405025170
**Score:** 0
**Tags:** mysql, sql, database
## Question Body
<p>I am tracking history of changes to rows in a table that is filled with a trigger on update of another table. It tracks the revision history of the main table.</p>

<p>Often, my users, out of habit, will hit the SAVE button even though they have not changed anything in the record, and the system will still record a copy of that row as a revision in the history table, despite the fact that nothing has changed.</p>

<p>Lets say I have the tables with columns like this (although mine have about 40+ cols):</p>

<p>Main Data:</p>

<pre><code>id, name, phone, task, dob, timestamp, note, drivername, student, doctor, userid
</code></pre>

<p>On Update of Main Data, insert into history:</p>

<pre><code>revisionid, revisiontime, id, name, phone, task, dob, timestamp, note, drivername, student, doctor, userid
</code></pre>

<p>The solutions to find duplicate records presented in this site and on other sites all will work well, if I wanted to list out the columns by hand.</p>

<p>The problem is that there are many many columns, and that I often add columns and don't want to rewrite this query every time.</p>

<p>When the user saves, often only the timestamp will change. What I want to do is keep only the revisions where values have changed (ignoring the revisionid and revisiontime which always change).</p>

<p>In the query, I dont want to list any other column names besides the columns which i want to ignore. Is it possible?</p>

<p>Pseudo code:</p>

<pre><code>DELETE [rows, except one] FROM historytable WHERE [all columns match values] EXCEPT [these few columns which can still be different and be deleted]
</code></pre>

<p>Here are a few reference questions:</p>

<p><a href="https://stackoverflow.com/questions/1043488/deleting-duplicate-rows-from-a-table">Deleting duplicate rows from a table</a></p>

<p><a href="https://stackoverflow.com/questions/6454805/how-to-check-for-duplicates-in-mysql-table-over-multiple-columns">How to check for duplicates in mysql table over multiple columns</a></p>

<p><a href="https://stackoverflow.com/questions/1651999/mysql-remove-duplicates-from-big-database-quick">MySQL remove duplicates from big database quick</a></p>

## Answers
### Answer ID: 24687663
<p>My thought process is as following..</p>

<ol>
<li><p>List all the column names (with an exclusion list)</p>

<p>SELECT <code>COLUMN_NAME</code> 
FROM <code>INFORMATION_SCHEMA</code>.<code>COLUMNS</code> 
WHERE <code>TABLE_SCHEMA</code>='db' 
    AND <code>TABLE_NAME</code>='table'
    AND <code>COLUMN_NAME</code> NOT IN ('columnToIgnore')</p></li>
<li><p>Store the names as rows in a temporary table</p>

<p>CREATE TEMPORARY TABLE IF NOT EXISTS columnNames AS (<em>step1</em>);</p></li>
<li><p>Fetch all records from temporary table 'columnNames' and store in a variable.</p>

<p>SELECT GROUP_CONCAT(COLUMN_NAME) into @cols FROM columnNames;</p></li>
<li><p>Prepare the final statement, list all the redundant rows. (I used SELECT for checking)</p>

<p>SET @sql = CONCAT('SELECT CONCAT_WS(" ",',@cols,')  AS allColumns FROM targetTable GROUP BY allcolumns');</p></li>
</ol>

<p>To sum up,</p>

<pre><code>CREATE TEMPORARY TABLE IF NOT EXISTS columnNames AS (SELECT `COLUMN_NAME` 
FROM `INFORMATION_SCHEMA`.`COLUMNS` 
WHERE `TABLE_SCHEMA`='dbName' 
    AND `TABLE_NAME`='tableName'
    AND `COLUMN_NAME` NOT IN ('columnNameToIgnore'));

SELECT GROUP_CONCAT(COLUMN_NAME) into @cols FROM columnNames;

SET @sql = CONCAT('SELECT CONCAT_WS(" ",',@cols,')  AS allColumns FROM targetTable GROUP BY allcolumns');

PREPARE stmt FROM @sql;
EXECUTE stmt;
</code></pre>

<p>Who says we can't use chainsaw to slice a bread ;)</p>

### Answer ID: 24686418
<p>No, it isn't possible to delete duplicates from a table without specifying the columns.</p>

<p>The only way I know of to use a SQL statement to trim a table of dups without specifying an explicit column list is to do the following. Create a new copy with only distinct records:</p>

<pre><code>create table T_UNIQUES as select distinct * from T;
</code></pre>

<p>You'd have to create a new table, rename the old one and then rename the new one into place. This is sometimes done on data warehouses when a DELETE operation is too slow. However, this doesn't ignore any timestamp columns, so it may not be adequate.</p>

<p>The only way I know to write a prune your history table with something automatic and extensible is to extract the columns from the data dictionary (INFORMATION_SCHEMA). This only automates it, but doesn't avoid specifying the columns in question. </p>

<p>My approach would be to fix the trigger. It sounds broken / inadequate; I would rewrite it to do an "UPSERT" instead of a blind INSERT.</p>

