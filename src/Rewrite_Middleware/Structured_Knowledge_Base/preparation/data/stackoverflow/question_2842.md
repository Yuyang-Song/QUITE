# Repetitive Postgres updates of arrays leading to bloat?
[Link to question](https://stackoverflow.com/questions/55093428/repetitive-postgres-updates-of-arrays-leading-to-bloat)
**Creation Date:** 1552260314
**Score:** 1
**Tags:** postgresql, sql-update, mvcc
## Question Body
<p>I am running a Python script which processes time-series data for a number of different metrics, and then writes the results to a Postgres database.</p>

<p>The time-series assumes 40 epochs, stored as a <code>real[40]</code> array column in the database.</p>

<p>When writing the outputs for all 40 epochs to the table in one shot, (batch update across all rows), everything seemed to work fine. i.e.</p>

<pre class="lang-sql prettyprint-override"><code>UPDATE my_table SET
  arr_col_1 = {1, 2, 3, ... 40},
  arr_col_2 = {1, 2, 3, ...40},
  ...
  arr_col_90 = {1, 2, 3, ...40};
</code></pre>

<p>However, iteratively writing the results of the respective epochs to each position in the array seems to chew up all free space on the hard drive, e.g.</p>

<pre class="lang-sql prettyprint-override"><code>UPDATE my_table SET
  arr_col_1[1] = 1,
  arr_col_2[1] = 1,
  ...
  arr_col_90[1] = 1;

UPDATE my_table SET
  arr_col_1[2] = 2,
  arr_col_2[2] = 2,
  ...
  arr_col_90[2] = 2;

-- repeat x 38 more times
</code></pre>

<p>The reason for the iterative strategy is to accommodate larger quantities of rows, for which the results for 40 epochs don't fit into memory at the same time.</p>

<p>To my knowledge, <code>UPDATE</code> queries will delete and rewrite row data in certain situations, but I'm not clear on when this happens and how this possibly relates to arrays. Is there a way to iteratively update arrays across large numbers of rows without leading to database bloat? </p>

## Answers
### Answer ID: 55096739
<p>As others have correctly mentioned, this approach is not well suited to PostgreSQL's mode of operation.</p>

<p>However, you may be able to use an optimization called HOT:</p>

<ul>
<li><p>Declare your table with a <code>fillfactor</code> less than 100 so that <code>INSERT</code>s leave free space in each block:</p>

<pre><code>ALTER TABLE my_table SET (fillfactor = 50);
</code></pre>

<p>This setting only affects future activity, you'd have to reorganize the table for it to affect existing data. If you update every row in the table, you may need a setting as low as 30 for it to be effective.</p></li>
<li><p>Make sure the columns that are updated do <em>not</em> have an index on them.</p></li>
</ul>

<p>Then PostgreSQL can use &amp;ldquo ;HOT update&rdquo; and reclaim the dead table entries on the fly, which avoids the need for autovacuum, which obviously cannot keep up on your table.</p>

<p>Check the <code>n_tup_hot_upd</code> column in the <code>pg_stat_user_tables</code> row for your table to see if it is working.</p>

### Answer ID: 55093997
<p>Postgres uses MVCC, which does copy-on-write.</p>

<p>The <code>UPDATE</code> copies the whole row to a new one and the old one is marked for deletion, but the deletion itself only takes place during a vacuum, which happens periodically by the autovacuum daemon.</p>

<p>You can free up the space yourself by running </p>

<pre><code>VACUUM
</code></pre>

<p>How much disk space do you have that it runs out?  I've never heard of such issue with a non-gigantic database.</p>

