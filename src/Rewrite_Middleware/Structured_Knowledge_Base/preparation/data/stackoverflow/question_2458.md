# PHP MySQL Get Connection From Require() File
[Link to question](https://stackoverflow.com/questions/35122611/php-mysql-get-connection-from-require-file)
**Creation Date:** 1454297427
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>I usually am immersed in the Microsoft Stack but dabble in PHP from time to time. A long standing question I've had with PHP that I've never seem to be able to find the answer to is how do you apply your already declared <code>require("dbConnect.php")</code> database connection to your mysql_query()? For clarification please see my code example below:</p>

<pre><code>        require("dbConnect.php"); 

        $db_host = 'localhost';
        $db_user = 'UserName';
        $db_pwd = 'Password';

        $database = 'DbName';
        $table = 'tblQuote';

        if (!mysql_connect($db_host, $db_user, $db_pwd))
            die("Can't connect to database");

        if (!mysql_select_db($database))
            die("Can't select database");

        // sending query
        $result = mysql_query("SELECT QuoteID, FirstName, LastName, PhoneNumber, Email, QuoteDate FROM tblQuote ORDER BY QuoteDate DESC");
        if (!$result) {
            die("Query to show fields from table failed");
        }

        $fields_num = mysql_num_fields($result);
</code></pre>

<p>So in looking at this you can see the standard require() declaration at the top... which already holds my connection info. But every single MySQL Query example I've ever found always creates it's own connection... which I get for demonstration purposes... but I've never been able to figure out how I can use my already existing connection thereby bypassing rewriting the exact same connection info over and over again when it comes to writing queries. I know for you PHP developers this question is like 101 but I've not been able to find an answer to this seemingly basic question... admittedly I may be asking the question wrong so any help would be appreciated!</p>

## Answers
### Answer ID: 35122769
<p>From the PHP documentation:  <a href="http://php.net/manual/en/function.mysql-query.php" rel="nofollow">http://php.net/manual/en/function.mysql-query.php</a></p>

<pre><code>mixed mysql_query ( string $query [, resource $link_identifier = NULL ] )
</code></pre>

<blockquote>
  <p>link_identifier
  The MySQL connection. If the link identifier is not specified, the last link opened by mysql_connect() is assumed. If no such link is found, it will try to create one as if mysql_connect() was called with no arguments.</p>
</blockquote>

<p>So since you've already created one in your dbConnect.php, the one you just made will be used (It won't create a new one for every query). To pass it explicitly into your <code>mysql_query</code> function call, you can return the MySQL resource that was returned from your mysql_connect call like so:</p>

<p>dbConnect.php</p>

<pre><code>return mysql_connect(....);
</code></pre>

<p>Then in the code you pasted above:</p>

<pre><code>$mysql_conn = require('dbConnect.php');
...
$result = mysql_query('...', $mysql_conn);
</code></pre>

<p>Then you will explicitly have the connection and pass it to your query - there will be no mistaking it, regardless of how large your codebase becomes. When you require the file, you'll have access to the connection variable, but in the above example, how you get the connection is more semantically clear.</p>

<hr>

<p><strong><em>Also, notice that this function has been deprecated in PHP>=5.5, so you'll want to use PDOs or MySQLi which have future support.</em></strong></p>

<p>Hope this helps!</p>

