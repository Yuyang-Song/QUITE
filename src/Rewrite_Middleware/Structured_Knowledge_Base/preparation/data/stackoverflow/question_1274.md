# Complete db schema transformation - how to test rewritten queries?
[Link to question](https://stackoverflow.com/questions/6777598/complete-db-schema-transformation-how-to-test-rewritten-queries)
**Creation Date:** 1311258205
**Score:** 4
**Tags:** sql, database-migration, database-testing
## Question Body
<p>Our database is poorly designed all the way around (we inherited it). I've reworked the schema to something useable and maintainable.  Quite a few tables and columns have been dropped, many columns have moved and most tables and columns have been renamed.  Some datatypes have been changed also.</p>

<p>I've extracted all the queries from our webapps and we've started rewriting them.  Our DBA is able to migrate the old data to the new schema, we think.  To be sure we need to test each query by comparing the old results with the new.</p>

<p>How can we test such a wholesale migration?  I need to be able to specify parameters, and map old tables/columns to new tables/columns.  With hundreds of queries this is a daunting task.  I could write something myself but I already have a lot of demands on my time so using an existing tool is preferable.</p>

<p>Thanks!</p>

## Answers
### Answer ID: 7517145
<p>I've had to do this ... and well it was easy because i rewrote the entire application ;)</p>

<p>Many queries sounds like basic operations such as select,insert,updates have not been abstracted in functions - maybe that can help clean up the mess before adapting.</p>

<p>Now for the testing:</p>

<p>You need a test script that will
a) run all your queries
b) store output of all selects for comparison</p>

<ol>
<li><p>backup your test db @ state 0, clear the general query log</p></li>
<li><p>play around your application using all the deletes, selects and updates, </p></li>
<li><p>copy paste that log, take every single select and precede it with a "Create table temptable_xyz" (or of course SELECT into temptable_xyz .. depends on the available syntax)</p></li>
<li><p>run on both databases, test db @ state 0 and test db @ state 0 after migration script</p></li>
<li><p>compare</p></li>
</ol>

<p>This should do it if you can make sure you used every feature in every app.</p>

<p>GL - nothing like making existing stuff better ;)</p>

### Answer ID: 6905805
<p>This would be my approach:</p>

<ol>
<li>Restore a test db that has data, run all the known queries.</li>
<li>Restore another test db, run all the new queries.</li>
<li><p>Create a sql script that joins each database's table and compare the results.  This could be done off information_schema or other system tables (depending on the vendor.)</p>

<p>insert into temp table
select (select count(1) from db1..name)
     , (select count(1) from db2..name)
     , (Select count(1) from db1.name t1 join db2.name t2 on t1.col1 = t2.col1 and t1.colx = t2.colx)
     , tablename</p></li>
</ol>

<p>You could then run through the queries that have the tablename in the query.  It would give you starting point of where to look.</p>

### Answer ID: 6778962
<p>Sometimes simple solutions do the job.</p>

<p>If it is just SELECTs, you could just put the new and old queries in text files, run them with a script and diff the output.</p>

<pre><code>cd newqueries
for queryfile in *; do
    psql -f $queryfile migrateddb &gt; /tmp/newresult
    psql -f ../oldqueries/$queryfile olddb &gt; /tmp/oldresult

    if ! diff /tmp/oldresult /tmp/newresult; then
        echo "Difference in $queryfile"
        exit 1
    fi
done
</code></pre>

<p>Or you could write a unit test based result comparison</p>

