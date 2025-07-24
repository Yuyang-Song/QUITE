# Database query on rewrite
[Link to question](https://stackoverflow.com/questions/50659647/database-query-on-rewrite)
**Creation Date:** 1527962015
**Score:** 0
**Tags:** php, mysql, mysqli
## Question Body
<p>I  have PHP script that runs every 5 mins and gets data from an API then writes it to a MySQL table. Users (300+) of my site can query that data via data-tables and other pages present some of that data.
The PHP script get API data then </p>

<pre><code>foreach($array as $row)
{
    $query .= "INSERT INTO table_name 
    (
        col_name1, 
        col_name2, 
        col_name3, 
        col_name4, 
        col_name5
    ) 
    VALUES
    (
        '".$row["value1"]."', 
        '".$row["value2"]."', 
        '".$row["value3"]."', 
        '".$row["value4"]."', 
        '".$row["value5"]."'
    );";
}

mysqli_query($connect, "DELETE FROM table_name");

mysqli_multi_query($connect, $query);
</code></pre>

<p>DELETE then INSERT into that empty table every time the script runs.
The table has 1000 rows and this will grow over time.
I am getting reports that the data-table is empty sometimes and they would have to refresh a few times before anything shows up.</p>

<p>Is there a better way of structuring the DB, tables and/or queries.</p>

## Answers
### Answer ID: 50659853
<p>Running individual insert statements for each row will be agonizingly slow.</p>

<p>It would be more efficient to run a multi-insert, inserting multiple rows with a single statement. For example, inserting four rows with a single statement.</p>

<pre><code>INSERT INTO t (a,b,c) VALUES (?,?,?) ,(?,?,?) ,(?,?,?) ,(?,?,?)
</code></pre>

<p>One potential downside is if one the rows fails to insert due to an error, the whole statement is rolled back, and none of the rows are inserted.</p>

<p>The maximum length of the SQL statement is limited by <code>max_allowed_packet</code>. It's not necessary to insert all of the rows in a single statement. Inserting 10 rows at a pop would significantly reduce the number of statement executions.</p>

<p>Assuming the table uses the InnoDB storage engine...</p>

<p>If we disable auto-commit, and run the <code>DELETE</code> statement and the <code>INSERT</code> statements in the context of a <em>single</em> transaction, then the table wouldn't appear to be "empty" to other sessions. The other sessions would continue to see the contents of the table as it was prior to the <code>DELETE</code>... until the <code>COMMIT</code> is done. </p>

<hr>

<p>The code pattern appears to be vulnerable to SQL Injection. (And particularly open to a lot of nastiness, using multi-query. </p>

<p>Best practice for mitigating SQL Injection is to use prepared statements with bind placeholders.</p>

<p><a href="https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet" rel="nofollow noreferrer">https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet</a></p>

<hr>

<p><strong>EDIT</strong></p>

<p>As an alternative approach, if the table has a primary key or unique key, consider </p>

<p>loading a temporary table (not the target table).</p>

<p>Then run statements to apply the changes to bring the target table into sync with the temporary table. We'll refer to the temporary table by the name source. </p>

<p>-- update existing rows</p>

<pre><code> UPDATE target t 
   JOIN source s
     ON s.id = t.id
    SET t.col = s.col 
      , t.foo = s.foo
      , t.bar = s.bar
</code></pre>

<p>-- insert new rows</p>

<pre><code>INSERT INTO target
SELECT s.*
  FROM ( SELECT r.*
           FROM source r
             -- anti-join 
           LEFT
           JOIN target q
             ON q.id = r.id 
          WHERE q.id IS NULL
        ) s
</code></pre>

<p>-- remove deleted rows</p>

<pre><code> DELETE t.*
   FROM target t
     -- anti-join
   LEFT
   JOIN source s
     ON s.id = t.id
  WHERE s.id IS NULL 
</code></pre>

<p>This avoids having to "empty" the target table, so concurrent SELECT statements will still return rows while the target table is being "sync'd".</p>

<p>The DML UPDATE/INSERT/DELETE operations against the target table can be executed in the context of a single transaction.</p>

