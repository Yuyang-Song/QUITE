# Migrating from xamp to raspberry pi apache server
[Link to question](https://stackoverflow.com/questions/50218713/migrating-from-xamp-to-raspberry-pi-apache-server)
**Creation Date:** 1525710659
**Score:** 0
**Tags:** php, html, xampp, raspberry-pi3
## Question Body
<p>I'm currently working on a project. It's almost done, there's only one big problem. I tested my code all the time with a xamp server on my computer, which worked perfectly fine. the goal is to run it (apache server, mysql database) on my raspberry pi. Now my project is finished, I came figured out the problem why my code doesn't work on my raspberry (at least not as I expected). </p>

<p>I turned on error reporting in PHP and came to this error message: </p>

<blockquote>
  <p>Notice: Trying to get property of non-object in /var/www/html/test.php on line 41</p>
</blockquote>

<p>I use this function for all my SQL queries. Can someone provide a solution so I don't have to rewrite the whole code? Thanks in advance! </p>

<p>PS: this is just a piece of the code (the function where I pull the data out of the database + example of one of my queries)</p>

<pre><code>&lt;?php

// Enable debugging
error_reporting(E_ALL);
ini_set('display_errors', true);


$servername = "localhost"; 
$username = "root";
$password = "*****";  // I just dont want to give my sql database password its nothing wrong ;)
$dbname = "test";




// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);


if ($conn-&gt;connect_error) {
    die("Connection failed: " . $conn-&gt;connect_error);
} else {
    print_r("ok connection");

    function sqlquery ($sql, $conn, $naamtabel) {
        global $myArray;
        global $stateLoop;

        $stateLoop = "0";

        $result = $conn-&gt;query($sql);

        if ($result-&gt;num_rows &gt; 0) {  //line 41 in my code ==&gt; do a while loop to fetch all data to an array
            // output data of each row
            while($row = $result-&gt;fetch_assoc()) {
                $myArray[] = $row["$naamtabel"]; //alle data van kolom "tijd" in een array
            }
            $stateLoop = "1";
        } 
        else { // if there are no results
        }
    }

    $sql1 = "SELECT stopTijd FROM gespeeldeTijd WHERE naam = 'thomas' ORDER BY ID DESC LIMIT 1";   // get data with SQL query
    sqlquery($sql1,$conn,"stopTijd");

    if ( $stateLoop == "1") {
        print_r("ok loop");
        $date1 = $myArray["0"];
        print_r($date1);        
        $myArray = [];
        $stateLoop == "0";
    }
}
?&gt;
</code></pre>

## Answers
### Answer ID: 50241344
<p>It pretty much looks like you have some sql error in your query; check if your field names in your database match those on the raspberry.</p>

<p>Seeing through your code it seems like you are pretty new to programming (which is no bad thing, I was once, too). So I made a few more modifications to your code showing you the prettiness of PHP</p>

<ul>
<li>use "return" in function sqlquery instead of globals</li>
<li>check for errors after executing the code</li>
<li>use only one variable to check if data was loaded</li>
</ul>

<p>I commented everything I changed</p>

<pre><code>&lt;?php
    // Enable debugging
    error_reporting(E_ALL);
    ini_set('display_errors', true);

    $servername = "localhost"; 
    $username   = "root";
    $password   = "*****";
    $dbname     = "test";

    // Your function with some modifications
    function sqlquery($sql, $conn, $naamtabel) {
        $result = $conn-&gt;query($sql);

        // Check for errors after execution
        if(!$result)
            die('mysqli error: '. htmlentities(mysqli_error($con)));

        // If we have no data, we simply return an empty array
        if($result-&gt;num_rows == 0)
            return array();

        // This is a variable we store the data we processed in
        // We will return it at the end of our function 
        $myArray = null;

        // Read all field data and store it $myArray
        while($row = $result-&gt;fetch_assoc())
            $myArray[] = $row[$naamtabel]; // if you use "$naamtabel" here, PHP first needs to interpret the string (= slower)

        return $myArray;
    }

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn-&gt;connect_error)
        die("Connection failed: " . $conn-&gt;connect_error);
    // Because we use "die" above we don't need an "else"-clause

    print_r("ok connection");

    $sql = "SELECT `stopTijd` FROM `gespeeldeTijd` WHERE `naam` = 'thomas' ORDER BY `ID` DESC LIMIT 1";
    $data = sqlquery($sql, $conn, "stopTijd");
    // $data will contain $myArray (see "return $myArray" in function sqlquery)

    // Instead checking for $stateLoop being "1" we check if $data contains any values
    // If so, we fetched some data
    if(sizeof($data) &gt;= 1) {
        print_r("ok loop");
        $date1 = $data[0]; // No "0", because we are trying to get index 0
        print_r($date1);        
        $data = array(); // Are you sure this is nessecary?
    } else {
        echo 'No data returned from query!';
    }
?&gt;
</code></pre>

<p>Note: code tipped on my smartphone -> untested!<br>
If you don't want to adapt the code I wrote, the important part for this question is:</p>

<pre><code>if(!$result)
    die('mysqli error: '. htmlentities(mysqli_error($con)));
</code></pre>

<p>Your error <code>Notice: Trying to get property of non-object</code> means "you are trying to get <code>num_rows</code> from <code>$result</code>, but <code>$result</code> is not an object, so it can't contain this property".<br>
So to figure out why <code>$result</code> is not an object, you need to get the error from <code>$conn-&gt;query</code> - my code above probably won't fix your error, but it will display you one you can work with (+ it's too long for a comment)</p>

<p>If you have a more detailed error message and you can't solve it on your own, feel free to comment; I will update my answer!</p>

