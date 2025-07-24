# PHP - Update data in databes by ID
[Link to question](https://stackoverflow.com/questions/71232498/php-update-data-in-databes-by-id)
**Creation Date:** 1645599305
**Score:** 0
**Tags:** php, mysql, database
## Question Body
<p>I need to overwrite the data in the database by ID.</p>
<p>I have a code:</p>
<p>index.php</p>
<pre><code>Databes::updateData($_POST['URL'],$_POST['title'],$_POST['label'],$_POST['content'], $id);
</code></pre>
<p>Databes.php</p>
<pre><code>public static function query ($sql, $parameters = array()){
    $query = self::$connection-&gt;prepare($sql);
    $query-&gt;execute($parameters);
    return $query;
}

public static function updateData($URL, $titel,  $label, $content, $id){
    $query = Databes::query(&quot;
    UPDATE clanky
    SET (URL, titulek, popisek, obsah)
    VALUES (?, ?, ?, ?)
    WHERE clanky.clanek_id= &quot; . $id
    , array($URL, $titel,  $label, $content));
}
</code></pre>
<p>I will get an answer:</p>
<blockquote>
<p>Fatal error: Uncaught PDOException: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near '(URL, titulek, popisek, obsah) VALUES ('uvodni-clanek', 'ÚvodníČl...' at line 2 in C:\xampp\htdocs\oop\Ukoly 5\2\tridy\databes.php:26 Stack trace: #0 C:\xampp\htdocs\oop\Ukoly 5\2\tridy\databes.php(26): PDOStatement-&gt;execute(Array) #1 C:\xampp\htdocs\oop\Ukoly 5\2\tridy\databes.php(56): Databes::query('\r\n UPDAT...', Array) #2 C:\xampp\htdocs\oop\Ukoly 5\2\administrace.php(56): Databes::updateData('uvodni-clanek', '\xC3\x9Avodn\xC3\xAD\xC4\x8Cl\xC3\xA1ne...', '\xC3\x9Avodn\xC3\xAD', 'Ahoj, v\xC3\xADtej...', 6) #3 {main} thrown in C:\xampp\htdocs\oop\Ukoly 5\2\tridy\databes.php on line 26</p>
</blockquote>
<p>But if I overwrite it directly in the database. So the database will write to me that it did this:</p>
<pre><code>UPDATE `clanky` SET `titulek` = 'ÚvodníČlánek' WHERE `clanky`.`clanek_id` = 6; 
</code></pre>
<p>I tried variously to rewrite the query into the database according to what I found on google, but it still reports an Error.</p>
<p>Please someone don't know where I'm making a mistake?</p>
<p>Thank you for answer.</p>

## Answers
### Answer ID: 71232565
<p>You're using incorrect syntax - <code>UPDATE clanky SET (...) VALUES (...)</code> is not valid. What you need to do, and what you seem to be doing manually, is:</p>
<pre><code>UPDATE clanky
   SET URL = ?
     , titulek = ?
     , popisek = ?
     , obsah = ?
 WHERE id = ?
</code></pre>
<p>Definitely do use parametrization for ID too, otherwise you're opening yourself up for SQL injection vulnerability (imagine someone passing id = 'id', you end up with WHERE id = id and all of your rows are getting updated)</p>

