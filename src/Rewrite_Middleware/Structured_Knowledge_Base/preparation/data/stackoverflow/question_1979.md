# How can I improve DELETE FROM performance on large InnoDB tables?
[Link to question](https://stackoverflow.com/questions/14284238/how-can-i-improve-delete-from-performance-on-large-innodb-tables)
**Creation Date:** 1357928167
**Score:** 26
**Tags:** mysql, performance, innodb
## Question Body
<p>I have a fairly large InnoDB table which contains about 10 million rows (and counting, it is expected to become 20 times that size). Each row is not that large (131 B on average), but from time to time I have to delete a chunk of them, and that is taking ages. This is the table structure:</p>

<pre><code> CREATE TABLE `problematic_table` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `taxid` int(10) unsigned NOT NULL,
    `blastdb_path` varchar(255) NOT NULL,
    `query` char(32) NOT NULL,
    `target` int(10) unsigned NOT NULL,
    `score` double NOT NULL,
    `evalue` varchar(100) NOT NULL,
    `log_evalue` double NOT NULL DEFAULT '-999',
    `start` int(10) unsigned DEFAULT NULL,
    `end` int(10) unsigned DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `taxid` (`taxid`),
    KEY `query` (`query`),
    KEY `target` (`target`),
    KEY `log_evalue` (`log_evalue`)
) ENGINE=InnoDB AUTO_INCREMENT=7888676 DEFAULT CHARSET=latin1;
</code></pre>

<p>Queries that delete large chunks from the table are simply like this:</p>

<pre><code>DELETE FROM problematic_table WHERE problematic_table.taxid = '57';
</code></pre>

<p>A query like this just took almost an hour to finish. I can imagine that the index rewriting overhead makes these queries very slow. </p>

<p>I am developing an application that will run on pre-existing databases. I most likely have no control over server variables unless I make changes to them mandatory (which I would prefer not to), so I'm afraid suggestions that change those are of little value.</p>

<p>I have tried to <code>INSERT ... SELECT</code> those rows that I don't want to delete into a temporary table and just dropping the rest, but as the ratio of to-delete vs. to-keep shifts towards to-keep, this is no longer a useful solution. </p>

<p>This is a table that may see frequent <code>INSERT</code>s and <code>SELECT</code>s in the future, but no <code>UPDATE</code>s. Basically, it's a logging and reference table that needs to drop parts of its content from time to time.</p>

<p>Could I improve my indexes on this table by limiting their length? Would switching to MyISAM help, which supports <code>DISABLE KEYS</code> during transactions? What else could I try to improve <code>DELETE</code> performance?</p>

<p><b>Edit:</b> One such deletion would be in the order of about one million of rows.</p>

## Answers
### Answer ID: 79073921
<p>Our solution is to create a temporary table and insert all the PKs that we need to delete to it.</p>
<p>Then we can use an inner join from our main table to that temporary table to delete.
It is hitting index nicely for us.</p>

### Answer ID: 71848488
<p>MySQL optimizer is all over the place and would run a full table scan on some environments and not others. Using some of the ideas from above my final solution was to store the PK id fields in a temp table and delete them via an inner join to the temp table. This seems to force the use of the PK index and prevent the full table scans.</p>
<pre><code>CREATE TEMPORARY TABLE d_table (id bigint);
INSERT INTO d_table SELECT id FROM my_table WHERE tax_id = 333; -- Select PK id into temp table
DELETE mt.* FROM my_table mt INNER JOIN d_table dt ON mt.id=dt.id; -- Delete by PK via JOIN to temp table to prevent full table scan
DROP TEMPORARY TABLE d_table;
</code></pre>

### Answer ID: 59929382
<p>I have an InnoDB table with around 200 million rows and I did experience the same issue.
Deleting rows took forever.</p>

<p>There are a primary key, a unique key and multiple compound indexes on the table.</p>

<p>When deleting in smaller chunks it went pretty fast, so I decided to make a stored procedure that simply deleted the rows in multiple iterations with a limit.
Kind of like Jan Larsen's answer, but with no need for separate table.</p>

<p>That made it possible to delete large chunks of data (around 500K rows) within a few minutes.</p>

<p>It seems like the transaction that InnoDB has to make to be able to rollback the changes on errors are too big, and therefor cannot fit into memory, which is causing the delete to perform very bad.</p>

<p>The procedure:</p>

<pre><code>CREATE DEFINER=`root`@`%` PROCEDURE `delete_rows`()
BEGIN
    declare v_max int unsigned default 100;
    declare v_counter int unsigned default 1;

        while v_counter &lt; v_max do
            DELETE from items where a = 'A' AND b = 'B' AND c = 'C' LIMIT 10000;
            set v_counter=v_counter+1;
        end while;
END
</code></pre>

<p>Then call it by:</p>

<pre><code>CALL delete_rows();
</code></pre>

<p>The where sentence matches a compound index starting with a,b,c-columns, which I think is important, so that MySQL do not have to make a full table scan to match the rows.</p>

### Answer ID: 59243888
<pre class="lang-sql prettyprint-override"><code>    DELETE FROM problematic_table WHERE problematic_table.taxid = '57';
</code></pre>

<p>remove Quotes, Since taxid is Integer and  Passing value in quotes makes its string, due to compare between Integer and String its doesn’t  pick Index.</p>

<pre class="lang-sql prettyprint-override"><code>    DELETE FROM problematic_table WHERE problematic_table.taxid = 57;
</code></pre>

### Answer ID: 47752860
<p>I solved a similar problem by using a stored procedure, thereby improving performance by a factor of several thousand.</p>

<p>My table had 33M rows and several indexes and I wanted to delete 10K rows. My DB was in Azure with no control over innodb_buffer_pool_size. </p>

<p>For simplicity I created a table <code>tmp_id</code> with only a primary <code>id</code> field:</p>

<pre><code>CREATE TABLE `tmp_id` (
    `id` bigint(20) NOT NULL DEFAULT '0',
    PRIMARY KEY (`id`)
)
</code></pre>

<p>I selected the set of ids I wanted to delete into <code>tmp_id</code> and ran <code>delete from my_table where id in (select id from tmp_id);</code> This did not complete in 12 hours, so I tried with only a single id in <code>tmp_id</code> and it took 25 minutes. Doing <code>delete from my_table where id = 1234</code> completed in a few milliseconds, so I decided to try doing that in a procedure instead:</p>

<pre><code>CREATE PROCEDURE `delete_ids_in_tmp`()
BEGIN
    declare finished integer default 0;
    declare v_id bigint(20);
    declare cur1 cursor for select id from tmp_id;
    declare continue handler for not found set finished=1;    
    open cur1;
    igmLoop: loop
        fetch cur1 into v_id;
        if finished = 1 then leave igmLoop; end if;
        delete from problematic_table where id = v_id;
    end loop igmLoop;
    close cur1;
END
</code></pre>

<p>Now <code>call delete_ids_in_tmp();</code> deleted all 10K rows in less than a minute.</p>

### Answer ID: 14299585
<p>This solution can provide better performance once completed, but the process may take some time to implement.</p>

<p>A new <code>BIT</code> column can be added and defaulted to <code>TRUE</code> for "active" and <code>FALSE</code> for "inactive".  If that's not enough states, you could use <code>TINYINT</code> with 256 possible values.</p>

<p>Adding this new column will probably take a long time, but once it's over, your updates should be much faster as long as you do it off the <code>PRIMARY</code> as you do with your deletes and don't index this new column.</p>

<p>The reason why InnoDB takes so long to <code>DELETE</code> on such a massive table as yours is because of the cluster index.  It physically orders your table based upon your <code>PRIMARY</code>, first <code>UNIQUE</code> it finds, or whatever it can determine as an adequate substitute if it can't find <code>PRIMARY</code> or <code>UNIQUE</code>, so when one row is deleted, it now reorders your entire table physically on the disk for speed and defragmentation.  So it's not the <code>DELETE</code> that's taking so long; it's the physical reordering after that row is removed.</p>

<p>When you create a fixed width column and update that instead of deleting, there's no need for physical reordering across your huge table because the space consumed by a row and table itself is constant.</p>

<p>During off hours, a single <code>DELETE</code> can be used to remove the unnecessary rows.  This operation will still be slow but collectively much faster than deleting individual rows.</p>

### Answer ID: 19545919
<p>I had a similar scenario with a table with 2 million rows and a delete statement, which should delete around a 100 thousand rows - it took around 10 minutes to do so.</p>

<p>After I checked the configuration, I found that MySQL Server was running with default <code>innodb_buffer_pool_size</code> = 8 MB (!).</p>

<p>After restart with <code>innodb_buffer_pool_size</code> = 1.5GB, the same scenario took 10 sec.</p>

<p>So it looks like there is a dependency if "reordering of the table" can fit in buffer_pool or not.</p>

