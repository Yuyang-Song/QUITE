# Approach on generating sorted html/php pages
[Link to question](https://stackoverflow.com/questions/31113897/approach-on-generating-sorted-html-php-pages)
**Creation Date:** 1435575330
**Score:** 0
**Tags:** php, html
## Question Body
<p>So imagine you have online book store with a page that is a grid with 9 elements that represent book covers. Every book has a price, and when user load's page 1st time grid is generated in order that books are stored in database. Now, user has option to select option that is gonna load a grid that is in order (desc/asc). Now what is the best way to achieve this. This is what I've tried :                            </p>

<p>1) Easiest way is to make php page that is in order and simply put a link to that page in . Now this is easy, but if I had 30 different type of orders (price, popularity, year etc..) I would have to make whole bunch of sites.</p>

<p>2) I tried ajax : when user hits button I send data(how to order) to special php script that based on that data will create database query and I would then use php file manipulation to rewrite entire front page with new order , and I would simply echo that site and in ajax succes function I would do window.location.replace(sent_from_php) and that would load same site but since I changed its content it would now be in order. What wrong here is that when 1 user requests ordered site, second user will also see ordered site , not the original site.</p>

<p>So, how can I use my second approach, but in the way I isolate users . Users wants ordered site, php rewrites front page html and outputs new site. Second users gets a regular site (he doesen't get ordered site) and so on. Basically I need to isolate users, so changes one users makes to the site is not visible to any other user?  </p>

<p>My index.php:</p>

<pre><code>&lt;?php
include 'db_menager.php';

$db_handler = new DB();
$query = "SELECT `Title`, `Autor`, `Price`, `Cover`, `Brief_desc`, `id` FROM `book` ORDER BY Price DESC";
$row = array();
$rows = $db_handler-&gt;select($query);

if ($rows)
    {
    echo "&lt;ul id='main'&gt;";
    while ($row = $rows-&gt;fetch_array(MYSQLI_ASSOC))
        {
        echo '&lt;li&gt;  &lt;img src = "' . $row["Cover"] . '"/&gt;';
        echo '&lt;p&gt;Title : ' . $row["Title"] . '&lt;/p&gt;';
        echo '&lt;p&gt;Autor : ' . $row["Autor"] . '&lt;/p&gt;';
        echo '&lt;p&gt;Price : ' . $row["Price"] . '&lt;/p&gt;';
        echo '&lt;/li&gt;';
        }

    echo "&lt;/ul&gt;";
    }
?&gt;
</code></pre>

## Answers
### Answer ID: 31114586
<p>Dont ever modify php scripts from other files - thats a bad idea.<br>
There are better solutions - Fortunately the simple ones.
Just get what user need from URL string. The queries are in the <code>$_GET</code> global array. </p>

<pre><code>//default sort values
$sortby = "Price";
$order = "DESC";
if(isset($_GET['sortby'])){ //if theres a sortby query in the URL
    $sortby = mysql_real_escape_string($_GET['sortby']);
}
if(isset($_GET['order'])){ //if user provided elements order in the URL
    $order = mysql_real_escape_string($_GET['order']);
    if($order == "DESC"){
        $order = "DESC";
    }else{
        $order = "ASC";
    }
}


$db_handler = new DB();
$query = "SELECT `Title`, `Autor`, `Price`, `Cover`, `Brief_desc`, `id` FROM `book` ORDER BY $sortby $order";
</code></pre>

<p>One note for this example: <strong>ALWAYS USE ESCAPING</strong>! (The mysqli_real_escape_string is better, but requires mysqli link (reference to your db, i dont have one and i dont know what methods,variables your DB class provides)).<br>
<strong>They are preventing you from <a href="https://en.wikipedia.org/wiki/SQL_injection" rel="nofollow">SQL Injection</a></strong></p>

<p>Links will be</p>

<pre><code>&lt;a href="index.php?sort=Price&amp;order=ASC"&gt;Sort from least exspensive&lt;/a&gt; 
&lt;a href="index.php?sort=Price&amp;order=DESC"&gt;Sort from most exspensive&lt;/a&gt;
</code></pre>

