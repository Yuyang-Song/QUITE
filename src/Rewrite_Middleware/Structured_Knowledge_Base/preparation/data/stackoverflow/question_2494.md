# prepared statement PDO Probably small mistake
[Link to question](https://stackoverflow.com/questions/37047262/prepared-statement-pdo-probably-small-mistake)
**Creation Date:** 1462441238
**Score:** -1
**Tags:** php, pdo
## Question Body
<p>im rewriting all my database queries so that they are prepared and with PDO (before I used mysqli) so that they are save against sql injections. Now I'm new to PDO so its probably a small mistake that I dont see, so I hope u guys can help me out because this code doesnt work.  </p>

<pre><code> &lt;?php

        function getUserBalance($steamid)
        {
            include 'settings.php';

            $conn = new PDO("mysql:host="$servername";dbname="$dbname"", $username, $password);
            $conn-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); 



            $sql = $conn-&gt;prepare("SELECT balance FROM users WHERE steamid= :steamid");


            $stmt = $conn-&gt;prepare($sql); 
            $stmt-&gt;bind_param(":steamid", $steamid, PDO::PARAM_STR);
            $stmt-&gt;execute(); 



            while($row = $stmt-&gt;fetch(PDO::FETCH_ASSOC)) 
            { 
                return $row['balance'];
            } 

        }
         $stmt-&gt;close();


    ?&gt;
</code></pre>

## Answers
### Answer ID: 37047471
<p><strong>Change this line</strong></p>

<pre><code>$conn = new PDO("mysql:host="$servername";dbname="$dbname"", $username, $password);
</code></pre>

<p><strong>to this</strong></p>

<pre><code>$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
</code></pre>

### Answer ID: 37047995
<p>Okey so now I changed it to new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);, moved the  $stmt->close(); within the function (oops) , and changed bind_param to bindParam, Thx guys its working now</p>

<pre><code>&lt;?php
    include 'ChromePhp.php';

    function getUserBalance($steamid)
    {
        include 'settings.php';
        $db = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
        $db-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); 


        $sql = "SELECT balance FROM users WHERE steamid= :steamid";
        $stmt = $db-&gt;prepare($sql); 

        $stmt-&gt;bindParam(':steamid', $steamid, PDO::PARAM_STR); 

        $stmt-&gt;execute(); 



        while($row = $stmt-&gt;fetch(PDO::FETCH_ASSOC)) 
    { 
        return $row['balance'];
    } 
        $stmt-&gt;close();

    }


?&gt;
</code></pre>

