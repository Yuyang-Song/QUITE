# Using result of a PHP echo in HTML/JavaScript var for Google Maps
[Link to question](https://stackoverflow.com/questions/19126380/using-result-of-a-php-echo-in-html-javascript-var-for-google-maps)
**Creation Date:** 1380663388
**Score:** 1
**Tags:** javascript, php, mysql, google-maps, google-maps-api-3
## Question Body
<p>Long time reader, first time poster.  Hoping you all can help me out.  I'm an absolute novice to PHP and JavaScript but am strong with HTML, and have past experience with Google Maps but this is a bit of a new approach for me.  Also my first time utilizing the V3 Google Maps API.</p>

<h2>Background Information</h2>

<p>I'm trying to rewrite a mileage calculator for my company that was broken because it used an old Yahoo Maps API, and I am so close to cracking it I can taste it!  I've been able to feel myself around and learn a little about PHP from what was left behind by the past programmer but I'm having trouble finishing one last bit.</p>

<p>The code pasted below utilizes a separate PHP file (getaddress.php) and the ?cid=FOOBAR from the URL to query our MySQL database and pull the customer's address and generate a Google Map / Driving Directions page.</p>

<p>My struggle is with getting the data pulled from the database into the var "route" in the  tag for the Google Map display.   I'm able to echo it perfectly with:</p>

<pre class="lang-php prettyprint-override"><code>&lt;?php echo "Directions to " . $_GET['cid'];?&gt;
</code></pre>

<p>but I'm unable to come up with a way to get that same text echoed into the route variable.  I'm a little embarrassed in asking this because I'm certain it's something simple I'm just overlooking but it's one of those kind of "don't know what you're looking for to search for a solution" kind of things, so I'm turning to you all and your talents.</p>

<p>The "origin: '123 Easy Street' will always be hard coded, so that isn't a problem.   The problem is the "destination: " which I would like to populate with the information getaddress.php pulls from the database, which looks like "1234 Easy Street 46142" in the HTML body.</p>

<p>Does anyone have any suggestions on how I can get that address string into the "destination: " portion of the route variable in the JavaScript?</p>

<p>I graciously appreciate any alternative ideas you all can suggest.  I'm stumped.</p>

<h2>getGmap.php Code</h2>

<pre class="lang-php prettyprint-override"><code>&lt;?php require('constants.php');?&gt;
&lt;?php require('sessionHandler.php');?&gt;
&lt;?php require('dbHandler.php');?&gt;
&lt;?php if (!isset($_GET['cid']) || empty($_GET['cid'])) die('No company specified.');?&gt;

&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"&gt;
&lt;html xmlns="http://www.w3.org/1999/xhtml"  xmlns:v="urn:schemas-microsoft-com:vml"&gt;
  &lt;head&gt;
    &lt;title&gt;Driving Directions to Customer provided by Google Maps&lt;/title&gt;
    &lt;meta http-equiv="content-type" content="text/html; charset=UTF-8"/&gt;
        &lt;link type="text/css" href="./lib/default.css" rel="stylesheet"&gt;

  &lt;script type="text/javascript"
           src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCnWPIRN8X0gLNqz-c1d87gv84CwZDuzjc&amp;sensor=false"&gt;&lt;/script&gt;

  &lt;script&gt;

        function process(){
                //Main processing starts here.
                //call getAddress. 
                getAddress();
        }

        //*** Get company information from database ***
        var req;                //global http request object

        function getAddress(){
                var url="getaddress.php?ajax=1&amp;cid=&lt;?php echo $_GET['cid'];?&gt;";
                if (window.XMLHttpRequest) {    // IE/Windows ActiveX version
                req = new XMLHttpRequest();
                req.onreadystatechange = processReqChange;
                req.open("GET", url, true);
                req.send(null);
          }
          else if (window.ActiveXObject) {
                req = new ActiveXObject("Microsoft.XMLHTTP");
                if (req) {
                    req.onreadystatechange = processReqChange;
                    req.open("GET", url, true);
                    req.send();
                }
          }
          return true;
        }

        //*** End get company information from database ***

    &lt;/script&gt;
  &lt;/head&gt;

  &lt;body onload="process()"&gt;
        &lt;font class="normalText"&gt;&lt;b&gt;
        &lt;?php echo "Directions to " . $_GET['cid'];?&gt;
        &lt;span id="addressSpan"&gt;&lt;/span&gt;
        from 123 Easy Street
        &lt;/b&gt;&lt;/font&gt;
        &lt;br /&gt;
        &lt;font class="normalText10"&gt;
        &lt;div style="width: 600px;"&gt;
             &lt;div id="map" style="width: 280px; height: 400px; float: left;"&gt;&lt;/div&gt;
             &lt;div id="panel" style="width: 300px; float: right;"&gt;&lt;/div&gt;
        &lt;/div&gt;
        &lt;/font&gt;
        &lt;script type="text/javascript"&gt;

             var directionsService = new google.maps.DirectionsService();
             var directionsDisplay = new google.maps.DirectionsRenderer();

             var map = new google.maps.Map(document.getElementById('map'), {
               zoom:7,
               mapTypeId: google.maps.MapTypeId.ROADMAP
             });

             directionsDisplay.setMap(map);
             directionsDisplay.setPanel(document.getElementById('panel'));

             var route = {
               origin: '123 Easy Street',
               destination: '1234 Easy Street 46142',
               travelMode: google.maps.DirectionsTravelMode.DRIVING
             };

             directionsService.route(route, function(response, status) {
               if (status == google.maps.DirectionsStatus.OK) {
                 directionsDisplay.setDirections(response);
               }
             });
        &lt;/script&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>

<h2>getaddress.php Code</h2>

<pre class="lang-php prettyprint-override"><code>&lt;?php require('constants.php'); ?&gt;
&lt;?php require('sessionHandler.php'); ?&gt;
&lt;?php require('dbHandler.php'); ?&gt;
&lt;?php

if (isset($_GET['cid']) &amp;&amp; !empty($_GET['cid'])) {
        //we only pass 5 chars of short id - actual id may be longer
        $query="select Address1, City, State, Zipcode from companies where CompanyShortID like '".$_GET['cid']."%'";
}
else
        die('Error: No company specified.');

dbConnect();
$result=mysql_query($query);
if (!$row=mysql_fetch_array($result))   // no records returned
        echo "";
else {
        echo $row['Address1']." ".$row['Zipcode'];
}
exit;
?&gt;
</code></pre>

## Answers
### Answer ID: 19134537
<p>As promised, here is the code I was able to get working.  </p>

<h2>getGmap.php Code</h2>

<pre class="lang-php prettyprint-override"><code>&lt;?php require('constants.php');?&gt;
&lt;?php require('sessionHandler.php');?&gt;
&lt;?php require('dbHandler.php');?&gt;
&lt;?php require('getaddress.php');?&gt;

&lt;?php

if (!isset($_GET['cid']) || empty($_GET['cid']))
     die('No company specified.');
?&gt;

&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"&gt;
&lt;html xmlns="http://www.w3.org/1999/xhtml"  xmlns:v="urn:schemas-microsoft-com:vml"&gt;
  &lt;head&gt;
    &lt;title&gt;Driving Directions to Customer provided by Google Maps&lt;/title&gt;
    &lt;meta http-equiv="content-type" content="text/html; charset=UTF-8"/&gt;
        &lt;link type="text/css" href="./lib/default.css" rel="stylesheet"&gt;

        &lt;script type="text/javascript"
           src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCnWPIRN8X0gLNqz-c1d87gv84CwZDuzjc&amp;sensor=false"&gt;&lt;/script&gt;

        &lt;script&gt;

                function process(){
                        //Main processing starts here.
                        //call getAddress. When AJAX call completes it will call inititalizeMap() to show the map.
                        getAddress();
                }


        //*** Begin AJAX***
        var req;                //global http request object

        function getAddress(){
                var url="getaddress.php?ajax=1&amp;cid=&lt;?php echo $_GET['cid'];?&gt;";

                if (window.XMLHttpRequest) {    // IE/Windows ActiveX version
                req = new XMLHttpRequest();
                req.onreadystatechange = processReqChange;
                req.open("GET", url, true);
                req.send(null);
          }
          else if (window.ActiveXObject) {
                req = new ActiveXObject("Microsoft.XMLHTTP");
                if (req) {
                    req.onreadystatechange = processReqChange;
                    req.open("GET", url, true);
                    req.send();
                }
          }
          return true;
        }

        function processReqChange()
        {
            // only if req shows "complete"
            if (req.readyState == 4) {  //4=completed
                // only if "OK"
                if (req.status == 200) {        //200=OK, so processing data
                    //alert(req.responseText);

                    //parse XML
                    //var response  = req.responseXML.documentElement;
                                toAddress=req.responseText;
                                document.getElementById('addressSpan').innerHTML=" - "+toAddress;
                                initializeMap();
                }
                else {
                    alert("There was a problem retrieving the XML data:\n" + req.statusText);
                }
            }
        }
        //****** End AJAX ***
    &lt;/script&gt;
  &lt;/head&gt;

  &lt;body onload="process()"&gt;
        &lt;font class="normalText"&gt;&lt;b&gt;
        Directions to: &lt;?php echo $_GET["cid"]. "-". getAddress($_GET["cid"]); ?&gt;
        &lt;span id="addressSpan"&gt;&lt;/span&gt;
        from: My Office - 1234 Easy Street
        &lt;/b&gt;&lt;/font&gt;
        &lt;br /&gt;
        &lt;font class="normalText10"&gt;
        &lt;div style="width: 600px;"&gt;
             &lt;div id="map" style="width: 280px; height: 400px; float: left;"&gt;&lt;/div&gt;
             &lt;div id="panel" style="width: 300px; float: right;"&gt;&lt;/div&gt;
        &lt;/div&gt;
   &lt;script type="text/javascript"&gt;

             var directionsService = new google.maps.DirectionsService();
             var directionsDisplay = new google.maps.DirectionsRenderer();

             var map = new google.maps.Map(document.getElementById('map'), {
               zoom:7,
               mapTypeId: google.maps.MapTypeId.ROADMAP
             });

             directionsDisplay.setMap(map);
             directionsDisplay.setPanel(document.getElementById('panel'));

             var route = {
               origin: '1234 Easy Street',
               destination: '&lt;?php echo getAddress($_GET["cid"]); ?&gt;',
               travelMode: google.maps.DirectionsTravelMode.DRIVING
             };

             directionsService.route(route, function(response, status) {
               if (status == google.maps.DirectionsStatus.OK) {
                 directionsDisplay.setDirections(response);
               }
             });
           &lt;/script&gt;
        &lt;br/&gt;
    &lt;/font&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>

<h2>getaddress.php Code</h2>

<pre class="lang-php prettyprint-override"><code>&lt;?php

    function getAddress($cid) {

            //we only pass 5 chars of short id - actual id may be longer
            $query="select Address1, City, State, Zipcode from companies where CompanyShortID like '" . $cid . "%'";

            dbConnect();
            $result=mysql_query($query);
            if (!$row=mysql_fetch_array($result))   // no records returned
                            return "Company Not Found";
            else {
                            return $row['Address1']." ".$row['Zipcode'];
            }

            return "Company Not Found";
    }

?&gt;
</code></pre>

