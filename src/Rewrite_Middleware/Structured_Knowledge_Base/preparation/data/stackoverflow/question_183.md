# Oracle external tables. Optimising select queries
[Link to question](https://stackoverflow.com/questions/1596209/oracle-external-tables-optimising-select-queries)
**Creation Date:** 1256060639
**Score:** 2
**Tags:** sql, oracle-database, plsql, external-tables
## Question Body
<p>I have to perform many selects from an Oracle external table.</p>
<p>I have 10 cursors that look a lot like this (ext_temp is the external table)</p>
<pre><code>CURSOR F_CURSOR (day IN varchar,code Number,orig Number)
    IS
    select NVL(sum(table_4.f),0) 
     from ext_temp table_4
    where
      --couple of conditions here, irrelevant for the question at hand.
      AND TO_CHAR(table_4.day,'YYYYMMDD') = day
      AND table_4.CODE = code
      AND table_4.ORIG = orig;
</code></pre>
<p>And the external table has about 22659 registers.</p>
<p>My script main loop looks like this</p>
<pre><code>   for each register in some_query: --22659 registers
       open F_cursor(register.day,register.code,register.orig);
       --open 9 more cursors

       fetch F_cursor into some_var;  
       --fetch 9 more cursors, with the same structure
</code></pre>
<p>Queries are taking way to much. And I know from <a href="http://www.orafaq.com/node/848" rel="nofollow noreferrer">here</a> that i can't have any indexes or DML.</p>
<p>So, is there a way of getting it to run faster? I can rewrite my plsql script, but i don't think I have time left.</p>
<h1>Update: missed an important detail.</h1>
<p>I'm not the owner or DBA of the database. That guy doesn't want any extra info (its about 3gb of data) in his database, and external tables is all we could get out of him. He doesnt allow us to create temporary tables. I don't pretend to question his reasons, but external tables is not the solution for this. So, we are stuck with them.</p>

## Answers
### Answer ID: 1597474
<p>While totally agreeing with Quassnoi's suggestion that external tables do not appear to be the proper solution here, as well as DCookie's analogy that you're being bound and tossed overboard and asked to swim, there may at least be a way to structure your program so that the external table is only read once.  My belief from your description is that all 10 cursors are reading from the external table, meaning that you are forcing Oracle to scan the external table 10 times.</p>

<p>Assuming this inference is correct, the simplest answer is likely to make the external table the driving cursor, similar to what IronGoofy suggested.  Depending on what <code>some_query</code> in the code snippet below is doing, </p>

<pre><code>for each register in some_query
</code></pre>

<p>and assuming that the fact that the query returns the same number of rows that are in the external table is not a coincidence, the simplest option would be to do something like</p>

<pre><code>FOR register in (select * from ext_temp)
LOOP
  -- Figure out if the row should have been part of cursor 1
  IF( &lt;&lt;set of conditions&gt;&gt; ) 
  THEN
    &lt;&lt;do something&gt;&gt;
  -- Figure out if the row should have been part of cursor 2
  ELSIF( ... )
  ...
END LOOP;
</code></pre>

<p>or</p>

<pre><code>FOR register in (select * 
                   from ext_temp a, 
                        (&lt;&lt;some query&gt;&gt;) b 
                  where a.column_name = b.column_name )
LOOP
  -- Figure out if the row should have been part of cursor 1
  IF( &lt;&lt;set of conditions&gt;&gt; ) 
  THEN
    &lt;&lt;do something&gt;&gt;
  -- Figure out if the row should have been part of cursor 2
  ELSIF( ... )
  ...
END LOOP;
</code></pre>

<p>It should be more efficient to take things a step further and move logic out of the cursors (and IF statements) and into the driving cursor.  Using the simpler of the code snippets above (you could, of course, join <code>some_query</code> to these examples</p>

<pre><code>FOR register in (select a.*,
                        NVL(sum( (case when condition1 and condition2
                                       then table_4.f
                                       else 0
                                       end) ),
                             0) f_cursor_sum
                  from ext_temp table_4)
LOOP
  &lt;&lt;do something&gt;&gt;
END LOOP;
</code></pre>

<p>If, even after doing this, you still find that you are doing some row-by-row processing, you could even go one more step forward and do a BULK COLLECT from the driving cursor into a locally declared collection and operate on that collection.  You almost certainly don't want to fetch 3 GB of data into a local collection (though crushing the PGA might lead the DBA to conclude that temporary tables aren't such a bad thing, it's not something I would advise), fetching a few hundred rows at a time using the LIMIT clause should make things a bit more efficient.</p>

### Answer ID: 1597107
<p>It's really tough if you have to work around restrictions that don't make sense but that you can't change ...</p>

<p>You should be better off reading through the external table once, and then build the required data in an index-like data structure in your code (basically an array with one element for each register you are looking for).</p>

<p>So your cursor would look like this:</p>

<pre><code>CURSOR F_CURSOR (day IN varchar, orig IN Number)
    IS
    select NVL(sum(table_4.f),0) value, table_4.CODE register
     from ext_temp table_4
    where
      --couple of conditions here, irrelevant for the question at hand.
      AND TO_CHAR(table_4.day,'YYYYMMDD') = day
      -- AND table_4.CODE = code -- don't use this condition!
      AND table_4.ORIG = orig;
</code></pre>

<p>And your register-loop would turn into a cursor-loop:</p>

<pre><code>open F_cursor(register.day,register.orig);
LOOP
    fetch F_cursor into some_var;
    EXIT WHEN F_cursor%NOT_FOUND
    result (some_var.register) := some_var.value;
END LOOP;
</code></pre>

<p>As a result, instead of a loop through the external table for each register, you just need one loop for all registers.</p>

<p>This can be extended for the ten cursors you mentioned.</p>

### Answer ID: 1596233
<p>Make them <code>Oracle</code> tables.</p>

<p>External tables are there to replace <code>SQL*LOADER</code>, not to work with them on a daily basis.</p>

<p>Just run an importing script whenever you underlying file changes which would load the contents of an external table into an <code>Oracle</code> table.</p>

<p>Here's what your namesake thinks of it (stolen from <a href="http://asktom.oracle.com/pls/asktom/f?p=100:11:0::::P11_QUESTION_ID:6611962171229" rel="nofollow noreferrer"><strong>here</strong></a>):</p>

<blockquote>
  <p>you are using external tables <em>instead of</em> <code>sqlldr</code>.</p>
  
  <p>with external tables you can</p>
  
  <ul>
  <li>merge a flat file with an existing table in one statement.</li>
  <li>sort a flat file on the way into a table you want compressed nicely.</li>
  <li>do a parallel direct path load -- without splitting up the input file, writing 
  umpteen scripts and so on</li>
  <li>run <code>sqlldr</code> in effect from a stored procedure or trigger (insert is not <code>sqlldr</code>)</li>
  <li>do multi-table inserts</li>
  <li>flow the data through a pipelined plsql function for cleansing/transformation</li>
  </ul>
  
  <p>and so on.  they are <em>instead of</em> <code>sqlldr</code> -- to get data into the database without having to use <code>sqlldr</code> in the first place.</p>
  
  <p>You would not normally query them day to day in an operational system, you use them to load data. </p>
</blockquote>

<p><strong>Update:</strong></p>

<p>You won't ever get decent performance with a <code>3GB</code> table, since <code>Oracle</code> will have to do a <code>3GB</code> fullscan on each query, and it will be a first-class disk-reading spindle-moving fullscan, not a cheap cached imitation which you can see in the plan but can barely notice in the actual execution time.</p>

<p>Try to convince the guy to create a temporary table for you which you could use to work with the data and just load the data from the external table whenever your session begins.</p>

<p>This is not the best solution since it will need to keep the separate copy of the table for each session in the temporary tablespace but it's much better performance-wise.</p>

### Answer ID: 1596232
<p>You could write your external table data to a <a href="http://www.dba-oracle.com/t_temporary_tables_sql.htm" rel="nofollow noreferrer">temporary</a> indexed (if you want) table, and then perform your multiple queries against it.</p>

<pre><code>create your_temp_table as select * from ext_temp;
create index your_desired_index on your_temp_table(indexed_field);
</code></pre>

<p>Then do all your queries directly using your_temp_table.</p>

