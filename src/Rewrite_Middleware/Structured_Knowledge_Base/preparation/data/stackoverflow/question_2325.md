# PHP URL Routing - Using Database Entries in Class
[Link to question](https://stackoverflow.com/questions/29390544/php-url-routing-using-database-entries-in-class)
**Creation Date:** 1427890471
**Score:** 0
**Tags:** php, .htaccess, url
## Question Body
<p><strong>ORGINAL QUERY - Updated Query Below</strong><br><br>
I am in the process of building a custom application in PHP. I know there have been many questions asked about Routing etc. on here and I have spent many of hours reading them all. This is how I got my routing elements to work in the first place. However 1 thing I cant get to fit into my project is peoples suggestions on how to route URLs based on a database entry.</p>

<p>The application itself is working perfectly fine and I already have some URL Routing in place which works exactly how I want it. The issue I have is when I add new products into my database I have a trigger that generates a SEO Friendly URL and stores it in a field in the database.</p>

<p>All the product URLs are structured in the same way.</p>

<p>/North/productdetails/Productname<br>
/South/productdetails/Productname<br>
/NorthEast/productdetails/Productname<br></p>

<p>etc.<br><br>
What I am looking to do is not have to manually write a new URL Route into the routes.php file every time a product is added.</p>

<p>this is my .htaccess</p>

<pre><code>RewriteEngine on
RewriteBase /
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
rewriteRule ^(.+)$ index.php?uri=$1 [QSA,L]
</code></pre>

<p>and my index.php file contains:</p>

<pre><code>&lt;?php
header("Cache-Control: no-cache");
include 'System/Config/route.php';
include 'System/Config/settings.php';
connect();

$route = new Route();

include 'System/Config/routeURL.php';

$route-&gt;add('/', 'Home');
$route-&gt;add('/results', 'Results');
$route-&gt;add('/special', 'Special');
$route-&gt;gogo();

?&gt;
</code></pre>

<p>I need something like this to go in and catch every URL passed to it. It then needs to check the URL and send the relevant information to a page.</p>

<pre><code>$route-&gt;add('/results/NorthEast/productdetails/&lt;whateveryisstoredindatabse&gt;', 'productURLS');
</code></pre>

<p>The class file that I use at the min to check it is this:</p>

<pre><code>class productURLS
{
 function Item($itemID)
{
    $host = $_SERVER['SERVER_NAME'] . $_SERVER['REQUEST_URI'];
    $itemID = '0';
    if($host == host +&lt;URLStored in database&gt;) {
        $itemID = &lt;what ever id is in database&gt;;
    } else {
    $itemID = '0';

    $_POST['ShowProductDetails'] = $itemID;
}

public function __construct()
{ 
    productURLS::Item($ItemID); 
    include 'pages/productdetails.php';
}
}
</code></pre>

<p>The class I wrote above is what I use to deter the current URLS onsite, I have modified it to identify where I need help on.</p>

<p>This is the route controller:</p>

<pre><code>class Route
{

private $_uri = array();
private $_method = array();

/**
 * Builds a collection of internal URL's to look for
 * @param type $uri
 */
 public function add($uri, $method = null)
 {
     $this-&gt;_uri[] = '/' . trim($uri, '/');

     if ($method != null) {
         $this-&gt;_method[] = $method;
     }
 }

 /**
  * Triggers from start page
  */
 public function gogo()
 {
    $uriGetParam = isset($_GET['uri']) ? '/' . $_GET['uri'] : '/';

    foreach ($this-&gt;_uri as $key =&gt; $value)
    {
        if (preg_match("#^$value$#", $uriGetParam))
        {
            $usemethod = $this-&gt;_method[$key];
            new $usemethod();
        }
    }
 }
 }
</code></pre>

<p>Does anyone have any suggestions in what I can do with what I have? or will it require a complete rewrite of the routing?</p>

<p>Regards</p>

<p><strong>UPDATED</strong></p>

<p>I have left the original query in as well as this one. For anyone landing on this page I have now been able to obtain data from the database and use it to generate a route in my routing controller dynamically. This is how I did it.</p>

<p>my index.php file now looks like this:</p>

<pre><code>&lt;?php
header("Cache-Control: no-cache");
include 'System/Config/route.php';
include 'System/Config/settings.php';
connect();

$route = new Route();
include 'System/Config/routeURL.php';
$q="SELECT  `itemID`,`SEOFriendlyURL` FROM  `Products`";
$r=mysql_query($q);

$numrows = mysql_num_rows($r);
if($numrows==0) 
{ 
// Does nothing as the database is empty - Not really needed but good just in case
}
// Dynamic Routing Elements
while($row = mysql_fetch_array($r))
{
$route-&gt;add("/results" . $row['SEOFriendlyURL'] ."", 'productURLS');
}
//Static Routing Elements
$route-&gt;add('/', 'Home');
$route-&gt;add('/results', 'Results');
$route-&gt;add('/special', 'Special');
$route-&gt;gogo();

?&gt;
</code></pre>

<p>This has worked perfectly, When ever one of these URLS is called it diverts to the right page. The only thing I'm having issues with now is passing the relevant ID's via $_post</p>

<p>This is what I ended up with but its not working.</p>

<pre><code>class productURLS
{
 function clubs($ItemID)
{
    $q="SELECT  `itemID`,`SEOFriendlyURL` FROM  `products`";
    $r=mysql_query($q);

    $numrows = mysql_num_rows($r);
    if($numrows==0) 
    { 
    $ItemID = '0';
    }

    while($row = mysql_fetch_array($r))
    {
    $host = $_SERVER['REQUEST_URI'];
    $ClubID = '0';
    if($host == "/newtest/results" . $row['SEOFriendlyURL'] ."") {
        $ClubID = "'" . $row['itemID'] ."'";
    } else {
    $itemID = '0';
    }
    }
    $_POST['ShowClubDetails'] = $itemID;
    }

    public function __construct()
    { 
    productURLS::clubs($itemID); 
    include 'pages/productdetails.php';
    }
    }
</code></pre>

<p>However this doesn't work. Because the query etc. is in the index page is it really needed again here? and is it better to get the query to store the ID in a variable and use that in the function instead?</p>

<p>Regards</p>

## Answers
### Answer ID: 29410870
<p>I have managed to get this fully working. Here is what I did. May be of some use to someone else.</p>

<p><strong>Index.php</strong></p>

<pre><code>include 'System/Config/routeURL.php';
$q="SELECT  `ItemID`,`SEOFriendlyURL` FROM  `Products`";
$r=mysql_query($q);

$numrows = mysql_num_rows($r);
if($numrows==0) 
{ 
echo "There's nothing here!";
}

// Add's all SEOFriendly URL's in table into route file (Dynamic)
while($row = mysql_fetch_array($r))
{
$route-&gt;add("/results" . $row['SEOFriendlyURL'] ."", 'ProductURLS');
}
</code></pre>

<p><strong>routeURL.php</strong></p>

<pre><code>class ProductURLS
{
  public function __construct()
  { 
    $host = $_SERVER['REQUEST_URI'];
    $host = ltrim ($host, '/results');
    $host = "/$host";
    $q="SELECT `ItemID`,`SEOFriendlyURL` FROM  `Products` WHERE `SEOFriendlyURL` = '$host'";
    $r=mysql_query($q);

    if($r) {
    $row = mysql_fetch_assoc($r);
    $ItemID = $row['ItemID'];
    } else {
        $ItemID = '0';
    }
    $_POST['ShowClubDetails'] = $ItemID;
    //echo "Whole query: $ItemID"; // This is to make sure the ProductID is being passed.
    include 'pages/ProductDetails.php';
    }
}
</code></pre>

