# How to run a PDO/ODBC/PHP query with double quote in it?
[Link to question](https://stackoverflow.com/questions/30559118/how-to-run-a-pdo-odbc-php-query-with-double-quote-in-it)
**Creation Date:** 1433085895
**Score:** 0
**Tags:** php, pdo, escaping, odbc, quote
## Question Body
<p>When I run the following simple query inside Microsoft Access:  </p>

<pre><code>select * from movie where moviename like 'batman'  
</code></pre>

<p>it works. </p>

<p>Also using double quotes around the string works:  </p>

<pre><code>select * from movie where moviename like "batman"
</code></pre>

<p>I have a website where the user can type in <em>any</em> select query which PHP will then run and returning the record results to the user. I use PDO/ODBC to connect to the Access database. If the user types in query 1 it works, but query 2 fails with:</p>

<blockquote>
  <p>[Microsoft][ODBC Microsoft Access Driver] Too few parameters. Expected 1. (SQLExecute[-3010] at ext\pdo_odbc\odbc_stmt.c:254)</p>
</blockquote>

<p>The documentation says about quote() function:  </p>

<blockquote>
  <p>"Not all PDO drivers implement this method (notably PDO_ODBC). Consider using prepared statements instead."</p>
</blockquote>

<p>but I can't use prepared statement as I don't know what query the user will type in. Sometimes they use '...' around a string and sometimes "...". </p>

<p>To reproduce you only need an Access (.mdb/.accdb) database with at least one table called 'film' and a column 'titel'. Put some records in it. At least 1 with 'Batman'. Use the following testscript:  </p>

<pre><code>//also using a older Access version of the database "film.mdb" didn't work
//be sure to use full/absolute pathname
$dbnameFile="C:\\wamp\\www\\elearning2\\databases\\film.accdb";
$username="";
$password="";
$accessdriver="{Microsoft Access Driver (*.mdb, *.accdb)}";
$dbDB = new PDO("odbc:Driver=$accessdriver;Dbq=$dbnameFile", $username, $password, 
                array(PDO::ATTR_ERRMODE =&gt; PDO::ERRMODE_EXCEPTION));

//Testcases, comment all but one
//Testcase 1: works
$sql="select * from film where titel like 'Batman'";

//Testcase 2: works
$sql='select * from film where titel like \'Batman\'';

//Testcase 3: COUNT field incorrect: -3010 [Microsoft][ODBC Microsoft Access Driver] Too few parameters. Expected 1.
$sql="select * from film where titel like \"Batman\"";

//Testcase 4: COUNT field incorrect: -3010 [Microsoft][ODBC Microsoft Access Driver] Too few parameters. Expected 1.
$sql='select * from film where titel like "Batman"';

//Testcase 5: Syntax error (missing operator) in query expression 'titel like \[Batman\] 
$sql='select * from film where titel like \"Batman\"';

//Testcase 6: Syntax error (missing operator) in query expression 'titel like []Batman[]
$sql='select * from film where titel like ""Batman""';

$result=$dbDB-&gt;query($sql);
$rows=$result-&gt;fetchAll(PDO::FETCH_ASSOC);  
$result-&gt;closeCursor();

foreach($rows as $row) {
  echo $row["TITEL"]."\n";
  echo "&lt;br&gt;";
}

$dbDB=null;
</code></pre>

<p>How can I properly escape a user given SQL query for PHP/PDO/ODBC/Access? Or is it just not possible to use a "..." string delimiter, despite working in Access?</p>

<p>I also find the error messages for testcase 5 and 6 odd. It looks like the double quote is changed into a <code>[</code> or <code>]</code>??</p>

<p>I can't use bind parameters, prepared statements or rewrite the query because the query is totally unknown and given by the user and can also contain syntax error(s). I can't modify this user query and just want it to be executed by PDO/ODBC but how?</p>

<p>I use Apache 2.4.9 and PHP 5.5.12 running locally on a Windows 7 SP1 machine.</p>

<p>I posted an official <a href="https://bugs.php.net/bug.php?id=69736" rel="nofollow noreferrer">PHP bug report</a>  </p>

<p>Here's proof that query 1 and 2 both work in Access:
<img src="https://i.sstatic.net/KGP42.png" alt="enter image description here"></p>

