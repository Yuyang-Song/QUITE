# MethodNotFound behaviour in PHP 5.3
[Link to question](https://stackoverflow.com/questions/63799678/methodnotfound-behaviour-in-php-5-3)
**Creation Date:** 1599589715
**Score:** 0
**Tags:** php, postgresql
## Question Body
<p>I am not a PHP developer, but I've been handed some legacy PHP code that I have to bug fix. I'm going to rewrite this code in C#, so I just need to understand why it's not failing when I think it should.</p>
<p>First, a database object is instantiated and a SQL query is built:</p>
<pre class="lang-php prettyprint-override"><code>$dbh = new PDO('pgsql:dbname=' . $dbname . ';host=' . $host, $dbuser, $dbpass, array(
    PDO::ATTR_PERSISTENT =&gt; true
));

$db2 = new PDO('pgsql:dbname=' . $dbname . ';host=' . $host, $dbuser, $dbpass, array(
    PDO::ATTR_PERSISTENT =&gt; true
));
$sql = &quot;select b.uniqueid,b.name,&quot;;
$sql .= &quot; a.id,a.servertime,a.devicetime,a.latitude,a.longitude,speed,course,accuracy&quot;;
$sql .= &quot; from tc_positions a, tc_devices b&quot;;
$sql .= &quot; where a.deviceid = b.id and a.processed = 0&quot;;
$sql .= &quot; order by a.devicetime&quot;;
</code></pre>
<p>Then, the SQL query is executed, and the records are processed individually:</p>
<pre class="lang-php prettyprint-override"><code>$stmt = $dbh-&gt;query($sql);
$x = 0;
while ($data = $stmt-&gt;fetch(PDO::FETCH_ASSOC)) {
    $x++;
    try {
        $gps = new GpsDevice(array('identity' =&gt; $data['uniqueid']));
    } catch (fNotFoundException $e) {
        $gps = new GpsDevice();
        $gps-&gt;setIdentity($data['uniqueid']);
        $gps-&gt;setComments('Tracker-&gt;' . $data['name']);
        $gps-&gt;store();
    }

    // begin functions under question
    $loc = new GpsDeviceLocation();
    $loc-&gt;setGpsDeviceId($gps-&gt;getGpsDeviceId());
    $loc-&gt;setCreated($data['devicetime'] . ' +00');
    $loc-&gt;setReceived($data['servertime'] . ' +00');
    $loc-&gt;setLat($data['latitude']);
    $loc-&gt;setLon($data['longitude']);
    $loc-&gt;setHeading($data['course']);
    $loc-&gt;setSpeed($data['speed'] / 1.60934);
    $loc-&gt;setAccuracy($data['accuracy']);
    // end functions in question

    $loc-&gt;store();
    $loc-&gt;free();
    $loc = null;
    $gps-&gt;free();
    $gps = null;
    print($data['uniqueid'] . &quot;\n&quot;);


    $sql2 = 'update tc_positions set processed = 1 where id = ' . $data['id'];

    $db2-&gt;query($sql2);
}
</code></pre>
<p>As I'm not a PHP developer, I'm relying on my very limited PHP knowledge and PHPStorm to help me understand what is happening. <code>$loc</code> is set to a new instance of <code>GpsDeviceLocation</code>, which is a class, built like this:</p>
<pre class="lang-php prettyprint-override"><code>// using flourish-classes
class GpsDeviceLocation extends fActiveRecord { }
</code></pre>
<p>The part I don't understand is when this bit is called, <code>$loc-&gt;setGpsDeviceId($gps-&gt;getGpsDeviceId());</code> (as well as the other methods in question), there's no matching method. Normally, in Python or C#, there would be an exception thrown at execution or compile time, but the code isn't throwing any errors, and the script is running as intended, I've verified in the downstream database that records are getting processed as intended. I've searched the code base and there isn't a single reference to any of those methods except in that file.</p>
<p>I feel like there should be an exception thrown, but there isn't. From what I can tell, this code should fail, but it's not, and I don't understand why. What is the behaviour of missing methods in PHP 5.3?</p>

## Answers
### Answer ID: 63799931
<p>By the name of methods and conventions its problably using Symfony 1 or something similar. Its a PHP framework, it has some custom functions, like getGpsDeviceId, the framework understand that it need to return the field gps_device_id or id_device_gps, they use an old ORM, the functions are created automatically. PHP Storm will probably not tell where the code is because its a very old thing and people didn't developed a plugin to backtrace this. To know what application is doing I recommend you to find the files that describe the architecture like a composer.json or a require() function, after you find the framework you can check the documentation on official website.</p>
<p>Example of Symfony 1:
<a href="https://symfony.com/legacy/doc/gentle-introduction/1_4/en/01-Introducing-Symfony" rel="nofollow noreferrer">https://symfony.com/legacy/doc/gentle-introduction/1_4/en/01-Introducing-Symfony</a></p>

