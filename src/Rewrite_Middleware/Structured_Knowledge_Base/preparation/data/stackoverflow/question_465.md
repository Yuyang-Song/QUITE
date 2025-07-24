# C/PHP: How do I convert the following PHP JSON API script into a C plugin for apache?
[Link to question](https://stackoverflow.com/questions/2733566/c-php-how-do-i-convert-the-following-php-json-api-script-into-a-c-plugin-for-ap)
**Creation Date:** 1272493957
**Score:** 0
**Tags:** php, c, apache
## Question Body
<p>I have a JSON API that I need to provide super fast access to my data through.</p>

<p>The JSON API makes a simply query against the database based on the GET parameters provided.</p>

<p>I've already optimized my database, so please don't recommend that as an answer.</p>

<p>I'm using PHP-APC, which helps PHP by saving the bytecode, BUT - for a JSON API that is being called literally dozens of times per second (as indicated by my logs), I need to reduce the massive RAM consumption PHP is consuming ... as well as rewrite my JSON API in a language that execute much faster than PHP.</p>

<p>My code is below. As you can see, is fairly straight forward.</p>

<pre><code>&lt;?php

define(ALLOWED_HTTP_REFERER, 'example.com');

if ( stristr($_SERVER['HTTP_REFERER'], ALLOWED_HTTP_REFERER) ) {

 try {
  $conn_str = DB . ':host=' . DB_HOST . ';dbname=' . DB_NAME;
  $dbh = new PDO($conn_str, DB_USERNAME, DB_PASSWORD);
  $params = array();

  $sql = 'SELECT  homes.home_id,
      address,
      city,
      state,
      zip
    FROM homes
    WHERE homes.display_status = true
    AND homes.geolat BETWEEN :geolatLowBound AND :geolatHighBound 
    AND homes.geolng BETWEEN :geolngLowBound AND :geolngHighBound';

  $params[':geolatLowBound'] = $_GET['geolatLowBound'];
  $params[':geolatHighBound'] = $_GET['geolatHighBound'];
  $params[':geolngLowBound'] =$_GET['geolngLowBound'];
  $params[':geolngHighBound'] = $_GET['geolngHighBound'];

  if ( isset($_GET['min_price']) &amp;&amp; isset($_GET['max_price']) ) {
    $sql = $sql . ' AND homes.price BETWEEN :min_price AND :max_price ';
    $params[':min_price'] = $_GET['min_price'];
    $params[':max_price'] = $_GET['max_price'];
  }

  if ( isset($_GET['min_beds']) &amp;&amp; isset($_GET['max_beds']) ) {
    $sql = $sql . ' AND homes.num_of_beds BETWEEN :min_beds AND :max_beds ';
    $params['min_beds'] = $_GET['min_beds'];
    $params['max_beds'] = $_GET['max_beds'];
  }

  if ( isset($_GET['min_sqft']) &amp;&amp; isset($_GET['max_sqft']) ) {
    $sql = $sql . ' AND homes.sqft BETWEEN :min_sqft AND :max_sqft ';
    $params['min_sqft'] = $_GET['min_sqft'];
    $params['max_sqft'] = $_GET['max_sqft'];
  }

  $stmt = $dbh-&gt;prepare($sql);

  $stmt-&gt;execute($params);
  $result_set = $stmt-&gt;fetchAll(PDO::FETCH_ASSOC);

  /* output a JSON representation of the home listing data retrieved */
  ob_start("ob_gzhandler"); // compress the output
  header('Content-type: text/javascript');
  print "{'homes' : ";

  array_walk_recursive($result_set, "cleanOutputFromXSS");
  print json_encode( $result_set );

  print '}';

  $dbh = null;
 } catch (PDOException $e) {
  die('Unable to retreive home listing information');
 }

}


function cleanOutputFromXSS(&amp;$value) {
 $value = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
}


?&gt;
</code></pre>

<p>How would I begin converting this PHP code over to C, since C is both better on memory management (since you do it yourself) and much, much faster to execute?</p>

<p><strong>UPDATE</strong>:</p>

<p>Would <a href="http://github.com/facebook/hiphop-php" rel="nofollow noreferrer">Facebooks HipHop</a> do all of this automatically for me?</p>

## Answers
### Answer ID: 2733598
<p>There are better solutions than rewriting this in c. Memcached, adding more memory, tuning php all come to mind.  </p>

<p>You need to profile your app to see how much memory is from the php interpreter, and how much is from compressing the output, and pulling the whole sql result set into memory.</p>

<p>Remember that little site called facebook? They use php and get way more traffic than your API. Keep that in mind.</p>

<p>Also think about the maintenance and stability hit you will take compiling this. Any change will now take orders of magnitude longer, and you have to take down the server to deploy. Maybe not an issue, but something to ponder.</p>

<p>I'd bet there are better ways to optimize than what you are thinking. Profiling is the key.</p>

### Answer ID: 2733591
<p>You can write your own Apache module.</p>

<p>Here is a tutorial:
<a href="http://threebit.net/tutorials/apache2_modules/tut1/tutorial1.html" rel="nofollow noreferrer">http://threebit.net/tutorials/apache2_modules/tut1/tutorial1.html</a></p>

