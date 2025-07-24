# How to optimize writing this data to a postgres database
[Link to question](https://stackoverflow.com/questions/12111327/how-to-optimize-writing-this-data-to-a-postgres-database)
**Creation Date:** 1345818434
**Score:** 1
**Tags:** c++, sql, database, postgresql, optimization
## Question Body
<p>I'm parsing poker hand histories, and storing the data in a postgres database. Here's a quick view of that:
<img src="https://i.sstatic.net/fA0nP.png" alt="enter image description here"></p>

<p>I'm getting a relatively bad performance, and parsing files will take several hours. I can see that the database part takes 97% of the total program time. So only a little optimization would make this a lot quicker.</p>

<p>The way I have it set-up now is as follows:</p>

<ol>
<li>Read next file into a string.</li>
<li>Parse one game and store it into object GameData.</li>
<li>For every player, check if we have his name in the std::map. If so; store the playerids in an array and go to 5.</li>
<li>Insert the player, add it to the std::map, store the playerids in an array.</li>
<li>Using the playerids array, insert the moves for this betting round, store the moveids in an array.</li>
<li>Using the moveids array, insert a movesequence, store the movesequenceids in an array.</li>
<li>If this isn't the last round played, go to 5.</li>
<li>Using the movesequenceids array, insert a game.</li>
<li>If this was not the final game, go to 2.</li>
<li>If this was not the last file, go to 1.</li>
</ol>

<p>Since I'm sending queries for every move, for every movesequence, for every game, I'm obviously doing too many queries. How should I bundle them for best performance? I don't mind rewriting a bit of code, so don't hold back. :)</p>

<p>Thanks in advance.</p>

<p>CX</p>

## Answers
### Answer ID: 12118658
<p>It's very hard to answer this without any queries, schema, or a Pg version.</p>

<p>In general, though, the answer to these problems is to batch the work into bigger coarser batches to avoid repeating lots of work, and, most importantly, by doing it all in one transaction.</p>

<p>You haven't said anything about <strong>transactions</strong>, so I'm wondering if you're doing all this in autocommit mode. Bad plan. Try wrapping the whole process in a <code>BEGIN</code> and <code>COMMIT</code>. If it's a seriously long-running process the <code>COMMIT</code> every few minutes / tens of games / whatever, write a checkpoint file or DB entry your program can use to resume the import from that point, and open a new transaction to carry on.</p>

<p>It'll help to use <strong>multi-valued inserts</strong> where you're inserting multiple rows to the same table. Eg:</p>

<pre><code>INSERT INTO some_table(col1, col2, col3) VALUES
('a','b','c'),
('1','2','3'),
('bork','spam','eggs');
</code></pre>

<p>You can improve commit rates with <code>synchronous_commit=off</code> and a <code>commit_delay</code>, but that's not very useful if you're batching work into bigger transactions.</p>

<p>One very good option will be to insert your new data into <strong><code>UNLOGGED</code> tables</strong> (PostgreSQL 9.1 or newer) or <code>TEMPORARY</code> tables (all versions, but lost when session disconnects), then at the end of the process copy all the new rows into the main tables and drop the import tables with commands like:</p>

<pre><code>INSERT INTO the_table
SELECT * FROM the_table_import;
</code></pre>

<p>When doing this, <a href="http://www.postgresql.org/docs/current/static/sql-createtable.html" rel="nofollow"><code>CREATE TABLE ... LIKE</code></a> is useful.</p>

<p>Another option - really a more extreme version of the above - is to <strong>write your results to CSV flat files</strong> as you read and convert them, then <strong><a href="http://www.postgresql.org/docs/current/static/sql-copy.html" rel="nofollow"><code>COPY</code></a></strong> them into the database. Since you're working in C++ I'm assuming you're using <code>libpq</code> - in which case you're hopefully also using <a href="http://pgfoundry.org/projects/libpqtypes/" rel="nofollow"><code>libpqtypes</code></a>. <a href="http://www.postgresql.org/docs/current/static/libpq-copy.html" rel="nofollow"><code>libpq</code> offers access to the <code>COPY</code> api for bulk-loading</a>, so your app wouldn't need to call out to <code>psql</code> to load the CSV data once it'd produced it.</p>

