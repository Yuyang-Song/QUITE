# Moving Rows up and down using Mysqli in PHP (Update SQL)
[Link to question](https://stackoverflow.com/questions/20538317/moving-rows-up-and-down-using-mysqli-in-php-update-sql)
**Creation Date:** 1386836424
**Score:** 0
**Tags:** php, mysql, sql, mysqli
## Question Body
<p>So,
I found this Script on this Website:
<a href="http://www.webdesignerforum.co.uk/topic/15011-moving-rows-in-a-database-up-or-down-with-php/" rel="nofollow">http://www.webdesignerforum.co.uk/topic/15011-moving-rows-in-a-database-up-or-down-with-php/</a></p>

<p>And thought I would try to rewrite it so it works with Mysqli.</p>

<p>However, I'm not really strong with SQL Querys, and I'm currently struggeling on how to get the last part of the script done, the last part where you insert the values to the DB again.</p>

<p>So far, I've managed to rewrite the first part, or atleast I think I have.</p>

<pre><code>&lt;?php
   $mysqli = new mysqli("localhost", "name", "password", "db");

   /* check connection */
   if (mysqli_connect_errno()) {
       printf("Connect failed: %s\n", mysqli_connect_error());
       exit();
   }
   $result = $mysqli-&gt;query("SELECT min(pos) FROM category");
   $row = $result-&gt;fetch_row();
   $minOrder = $row[0];

   $result = $mysqli-&gt;query("SELECT max(pos) FROM category");
   $row = $result-&gt;fetch_row();
   $maxOrder = $row[0];

   $result = $mysqli-&gt;query("select * from category order BY pos asc");
   $news=$result;
   while ($row = $news-&gt;fetch_assoc()) {

      $order = $row['pos'];
      $name = $row['navn'];

      echo "Name $name:&lt;br&gt;";
      if($order &gt; $minOrder) { // was $up, can be optimised??
          $tmp_up = $order-1;
          echo "&lt;a href=\"move_cat.php?a=$order&amp;amp;b=$tmp_up\"&gt;Move Up&lt;/a&gt;";
      }
      if($order &lt; $maxOrder) { // was $down, can be optimised??
         $tmp_down = $order+1;
         echo "&lt;a href=\"move_cat.php?a=$order&amp;amp;b=$tmp_down\"&gt;Move Down&lt;/a&gt;";
      }
   }
   $mysqli-&gt;close();
?&gt;
</code></pre>

<p>I think this part is okay, but the part following, is the one that I'm struggeling with:</p>

<pre><code>&lt;?php
   include("config.php");
   $a = $_GET["a"];
   $b = $_GET["b"];
   /* Check numeric --- this is stronger than just isset and ensures no SQL injection occurs */
   if (is_numeric($a) &amp;&amp; is_numeric($b)) {
      $result = mysql_query("UPDATE links SET `order`=(CASE `order` WHEN $a THEN $b ELSE $a END) WHERE `order`=$a OR `order`=$b", $db);
   }
   /* Always redirect back using HTTP response */
   header("Location: links2.php");
?&gt;
</code></pre>

<p>This is the one I need help rewriting, as I do not know, how I would use Prepared Statements with such a SQL Query.</p>

<p>Hope all this is understandable, if not do not hessitate to ask :)</p>

## Answers
### Answer ID: 20538568


<p>Using your current <code>UPDATE</code> statement:</p>

<pre class="lang-php prettyprint-override"><code>$update = $mysqli-&gt;prepare('
  UPDATE links
  SET    `order`=(CASE `order` WHEN ? THEN ? ELSE ? END)
  WHERE  `order`=? OR `order`=?
');
$update-&gt;bind_param('iiiii', $a, $b, $a, $a, $b);
$update-&gt;execute();
</code></pre>

<p>However, I'd be tempted to do something more like this (which allows one to shift items an arbitrary number of places):</p>

<pre class="lang-php prettyprint-override"><code>$update = $mysqli-&gt;prepare('
  UPDATE links
  SET    `order`= `order` '.($a &lt; $b ? '+' : '-').' 1
  WHERE  `order` BETWEEN ? AND ?
');
$update-&gt;bind_param('ii', min($a,$b), max($a,$b));
$update-&gt;execute();
</code></pre>

