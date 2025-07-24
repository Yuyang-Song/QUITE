# How to write a query to fetch &#39;Hello World&#39; as &#39;Hello-World&#39;
[Link to question](https://stackoverflow.com/questions/48773365/how-to-write-a-query-to-fetch-hello-world-as-hello-world)
**Creation Date:** 1518546691
**Score:** -1
**Tags:** php, mysql, .htaccess, mod-rewrite
## Question Body
<p>I'm a bit stuck here. I'm actually rewriting URL, All url who have single word seems to work fine but double word name is not working.</p>

<p>Here is my rewrite code</p>

<pre>
RewriteEngine on
RewriteRule ^cheap-flights-to-([A-Za-z0-9-]+)/?$ flight_details.php?dest=$1 [NC,L]
</pre>

<p>My MySQL Database have a table column <em>dest_name</em> with the values like for example "New York, Hong Kong, Kuala Lumpur etc."</p>

<p>Here is my Query</p>

<pre>
    $flights_query = mysql_query("SELECT * FROM `fares` WHERE `dest_name`='$to_dest' AND `dept_code`='$from_airport' AND `ticket_class`='Y/Y' AND `fare_type`='$flight_type' ORDER BY fare+tax limit 15");

    while($flights_fetch = mysql_fetch_array($flights_query)) {
        $fares = $flights_fetch['fare'] + $flights_fetch['tax'];
        $addpercent = ($fares * $percent) / 100;
        $final_fares = number_format($fares + $addpercent,2);
    }
</pre>

<p>When I output I add hyphen using PHP function... But it's not fetching data...</p>

## Answers
### Answer ID: 48773604
<p>I would process the variable before the query. So <code>$to_dest</code> would be cleaned before you used in it the query. </p>

<pre><code>$to_dest = str_replace(" ", "-", $to_dest);
</code></pre>

