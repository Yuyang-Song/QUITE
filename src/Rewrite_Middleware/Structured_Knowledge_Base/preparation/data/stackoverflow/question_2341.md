# Creating a REST API with MySQL and PHP formatted as a JSON response
[Link to question](https://stackoverflow.com/questions/30059250/creating-a-rest-api-with-mysql-and-php-formatted-as-a-json-response)
**Creation Date:** 1430846019
**Score:** 2
**Tags:** php, json, rest
## Question Body
<p>I'm trying to create a public REST API from scratch without using any framework and I've created where it retrieve all the data as JSON response when the user enter in this at the end of the address "...?list=all" However, I want to  retrieve a row by an ID or retrieving the most popular items. I know that I will probably have to change that in the query string, but how would I create the end of the address that retrieves it? like ?ID=05 (retrieving row ID 5 from database) or TOP=15 (retrieving top popular 15). If there's a better or more efficient way to rewrite my code, feel free to let me know.</p>

<pre><code>&lt;?php
    // Check Connection
if(!($db = mysqli_connect($server, $user, $password, $database))) {
    die('SQL ERROR: Connection failed: '.mysqli_error($db));
    exit;
    }
return $db;
}

    //call the passed in function
if(function_exists($_GET['list'])) {
    $_GET['list']();
} 

    //methods
function all(){
    $db = getMysqlDB();
    $query = "SELECT * FROM books;";
    $books_sql = mysqli_query($db, $query);
    $books = array();
    while($book = mysqli_fetch_array($books_sql)) {
        $books[] = $book;
    }
    $books = json_encode($books);
    echo $_GET['jsoncallback'].$books;
 }
?&gt;
</code></pre>

## Answers
### Answer ID: 42056115
<p>A simple start for a PHP based REST API would be:</p>

<pre><code>&lt;?php

// get the HTTP method, path and body of the request
$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['PATH_INFO'],'/'));
$input = json_decode(file_get_contents('php://input'),true);

// connect to the mysql database
$link = mysqli_connect('localhost', 'user', 'pass', 'dbname');
mysqli_set_charset($link,'utf8');

// retrieve the table and key from the path
$table = preg_replace('/[^a-z0-9_]+/i','',array_shift($request));
$key = array_shift($request)+0;

// escape the columns and values from the input object
$columns = preg_replace('/[^a-z0-9_]+/i','',array_keys($input));
$values = array_map(function ($value) use ($link) {
  if ($value===null) return null;
  return mysqli_real_escape_string($link,(string)$value);
},array_values($input));

// build the SET part of the SQL command
$set = '';
for ($i=0;$i&lt;count($columns);$i++) {
  $set.=($i&gt;0?',':'').'`'.$columns[$i].'`=';
  $set.=($values[$i]===null?'NULL':'"'.$values[$i].'"');
}

// create SQL based on HTTP method
switch ($method) {
  case 'GET':
    $sql = "select * from `$table`".($key?" WHERE id=$key":''); break;
  case 'PUT':
    $sql = "update `$table` set $set where id=$key"; break;
  case 'POST':
    $sql = "insert into `$table` set $set"; break;
  case 'DELETE':
    $sql = "delete `$table` where id=$key"; break;
}

// excecute SQL statement
$result = mysqli_query($link,$sql);

// die if SQL statement failed
if (!$result) {
  http_response_code(404);
  die(mysqli_error());
}

// print results, insert id or affected row count
if ($method == 'GET') {
  if (!$key) echo '[';
  for ($i=0;$i&lt;mysqli_num_rows($result);$i++) {
    echo ($i&gt;0?',':'').json_encode(mysqli_fetch_object($result));
  }
  if (!$key) echo ']';
} elseif ($method == 'POST') {
  echo mysqli_insert_id($link);
} else {
  echo mysqli_affected_rows($link);
}

// close mysql connection
mysqli_close($link);
</code></pre>

<p><a href="https://www.leaseweb.com/labs/2015/10/creating-a-simple-rest-api-in-php/" rel="nofollow noreferrer">source</a></p>

<p>For a more complete implementation check out:</p>

<p><a href="https://github.com/mevdschee/php-crud-api" rel="nofollow noreferrer">https://github.com/mevdschee/php-crud-api</a></p>

<p>Disclosure: I am the author.</p>

