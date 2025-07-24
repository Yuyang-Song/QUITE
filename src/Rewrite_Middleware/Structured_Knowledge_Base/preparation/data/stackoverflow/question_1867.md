# PHP PDO bug when trying to parameterize SQL LIMIT :offset, :display?
[Link to question](https://stackoverflow.com/questions/10401220/php-pdo-bug-when-trying-to-parameterize-sql-limit-offset-display)
**Creation Date:** 1335891352
**Score:** 4
**Tags:** php, mysql, pdo, rowcount
## Question Body
<p>This query returns 5 results in phpMyAdmin:</p>

<pre><code>SELECT * FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT 0,5
</code></pre>

<p>And this returns count=12 in phpMyAdmin (which is fine, because there are 12 records):</p>

<pre><code>SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT 0,5
</code></pre>

<p>This function was working fine before I added the two variables (offset, display), however now it doesn't work, and printing the variables out gives me offset=0, display=5 (so still <code>LIMIT 0,5</code>).</p>

<pre><code>function getProducts($offset, $display) {
    $sql = "SELECT * FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT ?,?;";
    $data = array((int)$offset, (int)$display);
    $rows = dbRowsCount($sql, $data);
logErrors("getProducts(".$offset.",".$display.") returned ".$rows." rows.");
    if ($rows &gt; 0) {
        dbQuery($sql, $data);
        return dbFetchAll();
    } else {
        return null;
    }
}
</code></pre>

<p>It's not working because my <code>dbRowsCount(...)</code> method was returning empty string (stupid <code>PDOStatement::fetchColumn</code>), so I changed it to return the count with <code>PDO::FETCH_ASSOC</code> and it returns count=0.</p>

<p>Here is the function which does the row-count:</p>

<pre><code>function dbRowsCount($sql, $data) {
    global $db, $query;
    $regex = '/^SELECT\s+(?:ALL\s+|DISTINCT\s+)?(?:.*?)\s+FROM\s+(.*)$/is';
    if (preg_match($regex, $sql, $output) &gt; 0) {
        $query = $db-&gt;prepare("SELECT COUNT(*) AS count FROM {$output[1]}");
logErrors("Regex output: "."SELECT COUNT(*) AS count FROM {$output[1]}");
        $query-&gt;setFetchMode(PDO::FETCH_ASSOC);
        if ($data != null) $query-&gt;execute($data); else $query-&gt;execute();
        if (!$query) {
            echo "Oops! There was an error: PDOStatement returned false.";
            exit;
        }
        $result = $query-&gt;fetch();
        return (int)$result["count"];
    } else {
logErrors("Regex did not match: ".$sql);
    }
    return -1;
}
</code></pre>

<p>My error log gives me this output from the program:</p>

<blockquote>
  <p>Regex output: SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT ?,?;<br>
  getProducts(0,5) returned 0 rows.  </p>
</blockquote>

<p>As you can see, the SQL has not been malformed, and the method input variables were 0 and 5 as expected.</p>

<p>Does anyone know what has gone wrong?</p>

<h1>Update</h1>

<p>Following a suggestion, I did try to execute the query directly, and it returned the correct result:</p>

<pre><code>function dbDebugTest() {
    global $db;
    $stmt = $db-&gt;query("SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update LIMIT 0,5;");
    $result = $stmt-&gt;fetch();
    $rows = (int)$result["count"];
    logErrors("dbDebugTest() returned rows=".$rows);
}
</code></pre>

<p>Output:</p>

<pre><code>&gt; dbDebugTest() returned rows=12
</code></pre>

<p>Following another suggestion, I changed !=null to !==null, and I also printed out the $data array:</p>

<pre><code>logErrors("Data: ".implode(",",$data));
if ($data !== null) $query-&gt;execute($data); else $query-&gt;execute();
</code></pre>

<p>Output:</p>

<pre><code>&gt; Data: 0,5
</code></pre>

<p><strong>However, the dbRowsCount($sql, $data) still returns 0 rows for this query!</strong></p>

<h1>Update 2</h1>

<p>Following advice to implement <a href="https://stackoverflow.com/a/7716896/259457">a custom PDOStatement class</a> which would allow me to output the query after the values have been binded, I found that the function would stop after $query->execute($data) and so the output would not be printed, although the custom class works for every other query in my program.</p>

<p>Updated code:</p>

<pre><code>function dbRowsCount($sql, $data) {
    global $db, $query;
    $regex = '/^SELECT\s+(?:ALL\s+|DISTINCT\s+)?(?:.*?)\s+FROM\s+(.*)$/is';
    if (preg_match($regex, $sql, $output) &gt; 0) {
        $query = $db-&gt;prepare("SELECT COUNT(*) AS count FROM {$output[1]}");
logErrors("Regex output: "."SELECT COUNT(*) AS count FROM {$output[1]}");
        $query-&gt;setFetchMode(PDO::FETCH_ASSOC);
logErrors("Data: ".implode(",",$data));
        $query-&gt;execute($data);
logErrors("queryString:".$query-&gt;queryString);
logErrors("_debugQuery():".$query-&gt;_debugQuery());
        if (!$query) {
            echo "Oops! There was an error: PDOStatement returned false.";
            exit;
        }
        $result = $query-&gt;fetch();
        return (int)$result["count"];
    } else {
logErrors("Regex did not match: ".$sql);
    }
    return -1;
}
</code></pre>

<p>Output:</p>

<blockquote>
  <p>Regex output: SELECT COUNT(<em>) AS count FROM tbl_product_category WHERE id=?;<br>
  Data: 5<br>
  queryString:SELECT COUNT(</em>) AS count FROM tbl_product_category WHERE id=?;<br>
  _debugQuery():SELECT COUNT(*) AS count FROM tbl_product_category WHERE id=?;  </p>
  
  <p>Regex output: SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT ?,?;<br>
  Data: 0,5<br>
  // function stopped and _debugQuery couldn't be output</p>
</blockquote>

<h1>Update 3</h1>

<p>Since I couldn't get the custom PDOStatement class to give me some output, I thought I'd rewrite the <code>getProducts(...)</code> class to bind the params with named placeholders instead.</p>

<pre><code>function getProducts($offset, $display) {
    $sql = "SELECT * FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT :offset, :display;";
    $data = array(':offset'=&gt;$offset, ':display'=&gt;$display);
    $rows = dbRowsCount($sql, $data);
logErrors("getProducts(".$offset.",".$display.") returned ".$rows." rows.");
    if ($rows &gt; 0) {
        dbQuery($sql, $data);
        return dbFetchAll();
    } else {
        return null;
    }
}
</code></pre>

<p>Output:  </p>

<blockquote>
  <p>Regex output: SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update DESC LIMIT :offset, :display;<br>
  Data: 0,5<br>
  // Still crashes after $query->execute($data) and so <code>logErrors("getProducts(".$offset."...))</code> wasn't printed out  </p>
</blockquote>

<h1>Update 4</h1>

<p>This dbDebugTest previously worked with declaring the limit values 0,5 directly in the SQL string. Now I've updated it to bind the parameters properly:</p>

<pre><code>function dbDebugTest($offset, $display) {
    logErrors("Beginning dbDebugTest()");
    global $db;
    $stmt = $db-&gt;prepare("SELECT COUNT(*) AS count FROM tbl_product WHERE 1 ORDER BY last_update LIMIT :offset,:display;");
    $stmt-&gt;bindParam(':offset', $offset, PDO::PARAM_INT);
    $stmt-&gt;bindParam(':display', $display, PDO::PARAM_INT);
    if ($stmt-&gt;execute()) {
      $result = $stmt-&gt;fetch();
      $rows = (int)$result["count"];
      logErrors("dbDebugTest() returned rows=".$rows);
    } else {
      logErrors("dbDebugTest() failed!");
    }
}
</code></pre>

<p>The function crashes, and only this is output:</p>

<blockquote>
  <p>Beginning dbDebugTest()</p>
</blockquote>

<h1>Update 5</h1>

<p>Following a suggestion to turn errors on (they are off by default), I did this:</p>

<pre><code>$db-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
</code></pre>

<p>That itself, made the dbDebugTest() from Update 4 work!</p>

<blockquote>
  <p>Beginning dbDebugTest()
  dbDebugTest() returned rows=12</p>
</blockquote>

<p>And now an error is generated in my webserver logs:  </p>

<blockquote>
  <p>[warn] mod_fcgid: stderr: PHP Fatal error:<br>
  Uncaught exception 'PDOException' with message 'SQLSTATE[42000]:<br>
  Syntax error or access violation: 1064 You have an error in your SQL syntax;<br>
  check the manual that corresponds to your MySQL server version for the right syntax to use<br>
  near ''0', '5'' at line 1'<br>
  in /home/linweb09/b/example.com-1050548206/user/my_program/database/dal.php:36</p>
</blockquote>

<p>Line 36 refers to <code>dbRowsCount(...)</code> method and the line is <code>$query-&gt;execute($data)</code>.</p>

<p>So the other method <code>getProducts(...)</code> still doesn't work because it uses this method of binding the data and the params turn into ''0' and '5'' (is this a bug?). A bit annoying but I'll have to create a new method in my dal.php to allow myself to bind the params in the stricter way - with <code>bindParam</code>.</p>

<p>Thanks especially to @Travesty3 and @eggyal for their help!! Much, much appreciated.</p>

## Answers
### Answer ID: 10402522
<p>Based on Update 2 in the question, where execution stops after the <code>execute</code> statement, it looks like the query is failing. After looking at <a href="http://php.net/manual/en/pdo.error-handling.php" rel="nofollow noreferrer">some PDO documentation</a>, it looks like the default error handling setting is PDO::ERRMODE_SILENT, which would result in the behavior you are seeing.</p>

<p>This is most likely due to the numbers in your LIMIT clause being put into single-quotes when passed in as parameters, as was happening in <a href="https://stackoverflow.com/q/2269840/259457">this post</a>.</p>

<p>The solution to that post was to specify the parameters as integers, using the <a href="http://php.net/manual/en/pdostatement.bindvalue.php" rel="nofollow noreferrer"><code>bindValue</code></a> method. So you will probably have to do something similar.</p>

<p>And it looks like you should also be executing your queries with try-catch blocks in order to catch the MySQL error.</p>

<hr />

<p>bindValue method:</p>

<pre><code>if ($data !== null)
{
    for ($i=0; $i&lt;count($data); $i++)
        $query-&gt;bindValue($i+1, $data[$i], PDO::PARAM_INT);
    $query-&gt;execute($data);
}
else
    $query-&gt;execute();
</code></pre>

### Answer ID: 10401588
<p>You're testing to see if <code>$data</code> is <code>NULL</code> with the equality, rather than the identity, operator (see <a href="http://www.php.net/manual/en/types.comparisons.php" rel="nofollow">the PHP manual</a> for more information on how <code>NULL</code> values are handled by the various comparison operators).  You need to either use the identity test <code>===</code> / <code>!==</code>, or else call <a href="http://php.net/manual/en/function.is-null.php" rel="nofollow"><code>is_null()</code></a>.</p>

<p>As @Travesty3 mentioned above, to test whether an array is empty, use <a href="http://php.net/manual/en/function.empty.php" rel="nofollow"><code>empty()</code></a>.</p>

