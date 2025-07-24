# Using PDO, do I really need to run two separate prepared statements to get the number of rows returned?
[Link to question](https://stackoverflow.com/questions/17897289/using-pdo-do-i-really-need-to-run-two-separate-prepared-statements-to-get-the-n)
**Creation Date:** 1374924815
**Score:** 1
**Tags:** php, select, pdo
## Question Body
<p>What is the preferred method for getting the number of rows that are returned for a SELECT state when using PDO with prepared statements? </p>

<p>I am currently using rowCount() but the docs say I shouldn't be using that since "most databases" don't support it (It is actually working just fine for me, so I'm tempted to keep using it. I can't find any sources that list exactly which databases do not support it, but apparently mine is fine).</p>

<p>Instead they recommend I use fetchColumn() but that requires writing a completely separate SQL statement that includes the COUNT(*) in my sql statement.</p>

<p>This is what they propose (<a href="http://php.net/manual/en/pdostatement.rowcount.php#example-1038" rel="nofollow">http://php.net/manual/en/pdostatement.rowcount.php#example-1038</a>):</p>

<pre><code>//SQL TO GET ROWS TO OUTPUT
$sql = 'SELECT *
  FROM properties
  WHERE lister_id = :lister_id
  AND lister_type = "landlord"';

$result = $dbh-&gt;prepare($sql);
$result-&gt;bindParam(':lister_id', $_SESSION['loggedin_lister_id'], PDO::PARAM_INT);
$result-&gt;execute();

//SQL TO GET NUMBER OF RETURNED ROWS
$row_num_sql = 'SELECT COUNT(*)
  FROM properties
  WHERE lister_id = :lister_id
  AND lister_type = "landlord"';

$row_num_result = $dbh-&gt;prepare($row_num_sql);
$row_num_result-&gt;bindParam(':lister_id', $_SESSION['loggedin_lister_id'], PDO::PARAM_INT);
$row_num_result-&gt;execute();
$num_rows = $row_num_result-&gt;fetchColumn();

if($num_rows &gt; 0) {
  while($row = $result-&gt;fetch(PDO::FETCH_ASSOC)) {
    echo $row['name'];
  }
}
</code></pre>

<p>I find this method that requires me to write a separate and nearly identical sql statement to be redundant and a serious pain when using prepared statements. I can understand how this approach might be acceptable when using a short SQL statement with a basic query, but not in the case of a prepared statement.</p>

<blockquote>
  <p><strong>1.</strong> Is there any other way I can use the fetchColumn() approach
  without having to rewrite what is almost exactly the same code? </p>
  
  <p><strong>2.</strong> Where can I find an official list of which databases
  rowCount() supports when using a SELECT statement? And since it is
  working on the database I am currently using, can I assume it is safe
  to use(assuming I am not updating my database anytime soon)?</p>
</blockquote>

## Answers
### Answer ID: 17897573
<p>If you don't want to use <code>rowCount</code> I'm think you should two query, or you can use <code>fetchAll</code> and <code>count(fetchAll)</code> for <code>rowCount</code></p>

<p>the second way, Use <code>SELECT *,COUNT(*) ...</code></p>

