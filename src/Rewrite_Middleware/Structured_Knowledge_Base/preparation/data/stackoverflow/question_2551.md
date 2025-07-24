# New PDO::query while fetching other query
[Link to question](https://stackoverflow.com/questions/39527096/new-pdoquery-while-fetching-other-query)
**Creation Date:** 1474015109
**Score:** 1
**Tags:** php, pdo
## Question Body
<p>There is a sample of old PHP code (not real code, just for understading of problem).</p>

<pre><code>    $q = mysql_query("SELECT MILLIONS ROWS FROM TABLES");
    while($row = mysql_fetch_assoc($q)) {
        // other different queries (SELECT, INSERT, DELETE, UPDATE) &amp; other complex logic 
        $q2 = mysql_query("SELECT SOME DATA");
        $data = mysql_fetch_assoc($q2);
        $q3 = mysql_query("UPDATE SOME ROWS");
        $q4 = mysql_query("SELECT SOME OTHER DATA");
        // many other code, that works with DataBase and do many other things
        // ...
    }
</code></pre>

<p>This old code works fine.
But I need to move this code to PHP7 and PDO (instead of mysql_).
In the project about 3000 places of code like this. </p>

<p>I tryed to rewrite code like this:</p>

<pre><code>    $pdo = new PDO('connection string');
    $q = $pdo-&gt;query("SELECT MILLIONS ROWS FROM TABLES");
    while($row = $q-&gt;fetch()) {
        // other different queries (SELECT, INSERT, DELETE, UPDATE) &amp; other complex logic 
        $q2 = $pdo-&gt;query("SELECT SOME DATA");
        $data = $q2-&gt;fetch();
        $q3 = $pdo-&gt;query("UPDATE SOME ROWS");
        $q4 = $pdo-&gt;query("SELECT SOME OTHER DATA");
        // many other code, that works with DataBase and do many other things
        // ...
    }
</code></pre>

<p>It does not work: the loop executes one time, though rows in a table a few million.
This is natural, because it is written in the manual:</p>

<blockquote>
  <p>If you do not fetch all of the data in a result set before issuing your next call to PDO::query(), your call may fail. Call PDOStatement::closeCursor() to release the database resources associated with the PDOStatement object before issuing your next call to PDO::query(). </p>
</blockquote>

<p>I can rewrite the code using fetchAll, then it will work. </p>

<pre><code>    $pdo = new PDO('connection string');
    $q = $pdo-&gt;query("SELECT MILLIONS ROWS FROM TABLES");
    $rows = $q-&gt;fetchAll();
    foreach($rows as $row) {
         // other different queries (SELECT, INSERT, DELETE, UPDATE) &amp; other complex logic 
        $q2 = $pdo-&gt;query("SELECT SOME DATA");
        $data = $q2-&gt;fetch();
        $q3 = $pdo-&gt;query("UPDATE SOME ROWS");
        $q4 = $pdo-&gt;query("SELECT SOME OTHER DATA");
        // many other code, that works with DataBase and do many other things
        // ...
    }
</code></pre>

<p>But this option does not suit me, because fetchAll eats all memory and the script fails. </p>

<p>Also, i can rewrite code like this:</p>

<pre><code>    $pdo = new PDO('connection string');
    for($i=0; $&lt;=10000; $i++) {
        $offset = $i * 1000;
        $q = $pdo-&gt;query("SELECT ROWS FROM TABLES LIMIT $offset, 1000");
        $rows = $q-&gt;fetchAll();
        foreach($rows as $row) {
            // other different queries (SELECT, INSERT, DELETE, UPDATE) &amp; other complex logic 
            $q2 = $pdo-&gt;query("SELECT SOME DATA");
            $data = $q2-&gt;fetch();
            $q3 = $pdo-&gt;query("UPDATE SOME ROWS");
            $q4 = $pdo-&gt;query("SELECT SOME OTHER DATA");
            // many other code, that works with DataBase and do many other things
            // ...
        }
    }
</code></pre>

<p>But this method does not suit me, because i have to rewrite a lot of code in the project and i don't want do this.</p>

<p>How to move this code to PDO? 
Is there other way to make PDO queries while fetching data by the first query ?</p>

## Answers
### Answer ID: 39527229
<p>Try next approach:</p>

<pre><code>$q = PDO::query("SELECT Table2.* FROM Table1 JOIN Table2 ON Table2.id=Table1.id");
while($data = $q-&gt;fetch()) {
    // some code here
}
</code></pre>

### Answer ID: 39527180
<p>Can't you put in in 1 query?</p>

<pre><code>SELECT `Table2`.* FROM `Table2`
JOIN `Table1`
ON `Table1`.`id` = `Table2`.`id`
</code></pre>

<p>This will be more performant, and give the results you want.</p>

