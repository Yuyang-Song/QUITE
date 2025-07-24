# Ignoring apostrophes in mysql searches
[Link to question](https://stackoverflow.com/questions/4351337/ignoring-apostrophes-in-mysql-searches)
**Creation Date:** 1291425147
**Score:** 4
**Tags:** php, mysql, select
## Question Body
<p>I want to take a url that does not have any apostrophes, commas or ampersands in it and match it with a record in a database that may have one of those characters.</p>

<p>For example:</p>

<pre><code>mywebsite.com/bobs-big-boy
mywebsite.com/tom--jerry
mywebsite.com/one-two-three
</code></pre>

<p>rewrite to </p>

<pre><code>index.php?name=bobs-big-boy
index.php?name=tom--jerry
index.php?name=bobs-big-boy
</code></pre>

<p>Then in php I want to use the $_GET['name'] to match the records</p>

<pre><code>bob's big boy
tom &amp; jerry
one, two, three
</code></pre>

<p>Now my query looks like this:</p>

<pre><code>"SELECT * from the_records WHERE name=$NAME";
</code></pre>

<p>I can't change the records, because they're business names.  Is there a way I can write the query to ignore ampersands, commas and apostrophes in the db?</p>

## Answers
### Answer ID: 4351377
<p>Yes you can but I'm pretty sure it will ignore any indexes you have on the column.  And it's disgusting.</p>

<p>Something like </p>

<pre><code>SELECT * FROM the_records 
WHERE replace(replace(replace(name, '''', ''), ',', ''), '&amp;', '') = $NAME
</code></pre>

<p>By the way taking a get variable like that and injecting it into the mysql query can be ripe for sql injection as far as I know.</p>

<p>pg, I know you said you can't change/update the content in the database you're selecting from, but does anything preclude you from making a table in another database you do have write access to?  You could just make a map of urlnames to business names and it'd only be slow the first time you do the replace method.</p>

### Answer ID: 4383771
<p>Greetings,</p>

<p>This one took me a few minutes to puzzle out! There are actually a few specifics missing on you requirements, so I've tried to work through the problem with different assumptions, as stated below.</p>

<p>Here is the set of assumed input from the URL, as pulled from your example, along with a MySQL injection attack (just for giggles), and variations on the business names. The keys are the expected URLs and the values are the database values to match.</p>

<pre><code>&lt;?php
$names = array(
  'bobs-big-boy'=&gt;"bob's big boy",
  'tom--jerry'=&gt;'tom &amp; jerry',
  'tomjerry'=&gt;'tom&amp;jerry',
  'one-two-three'=&gt;'one, two, three',
  'onetwothree'=&gt;'one,two,three',
  "anything' OR 'haxor'='haxor"=&gt;'die-haxor-die',
);
?&gt;
</code></pre>

<p>One clever way to do an end-run mySQL's lack of regex replacement is to use SOUNDEX, and this approach would seem to mostly work in this case depending on the level of accuracy you need, the density of and similarity of customer names, etc. For example, this generates the soundex values for the values above:</p>

<pre><code>$soundex_test = $names;
$select = 'SELECT ';
foreach ($soundex_test as $name=&gt;$dbname) {
  echo '&lt;p&gt;'.$name.': '.soundex($name).' :: '.$dbname.': '.soundex($dbname).'&lt;/p&gt;';
  $select .= sprintf("SOUNDEX('%s'),", $name);
}
echo '&lt;pre&gt;MySQL queries with attack -- '.print_r($select,1).'&lt;/pre&gt;';
</code></pre>

<p>So, assuming that there are not customers named 'one, two, three' and separate one named 'onetwothree', this approach should work nicely.</p>

<p>To use this method, your queries would look something like this:</p>

<pre><code>$soundex_unclean = $names;
foreach ($soundex_unclean as $name=&gt;$dbname) {
  $soundex_unclean[$name] = sprintf("SELECT * from the_records WHERE name SOUNDS LIKE '%s';", $name).' /* matches name field = ['.$dbname.'] */';
}
echo '&lt;pre&gt;MySQL queries with attack -- '.print_r(array_values($soundex_unclean),1).'&lt;/pre&gt;';
</code></pre>

<p>However, here is a run that DOES deal with the injection attack (note the new line). I know this isn't the focus of the question, but ajreal mentioned the issue, so I thought to deal with it as well:</p>

<pre><code>$soundex_clean = $names;
foreach ($soundex_clean as $name=&gt;$dbname) {
  // strip out everything but alpha-numerics and dashes
  $clean_name = preg_replace('/[^[:alnum:]-]/', '', $name);
  $soundex_unclean[$name] = sprintf("SELECT * from the_records WHERE name SOUNDS LIKE '%s';", $clean_name).' /* matches name field = ['.$dbname.'] */';
}
echo '&lt;pre&gt;MySQL queries with attack cleaned -- '.print_r($soundex_unclean,1).'&lt;/pre&gt;';
</code></pre>

<p>If this approach does not suit, and you decided that the inline replacement approach is sufficient, then do remember to add a replacement for comma to the mix as well. As an example of that approach, I'm assuming here that the single quote, double quote, ampersand, and comma (i.e. ', ", &amp;, and ,) are the only four special characters are included in the database but deleted from the URL, and that any other non-alpha-numeric character, spaces included, are converted to a dash (i.e. -).</p>

<p>First, a run that does not deal with the injection attack:</p>

<pre><code>$unclean = $names;
foreach ($unclean as $name=&gt;$dbname) {
  $regex_name = preg_replace('/[-]+/', '[^[:alnum:]]+', $name);
  $unclean[$name] = sprintf("SELECT * from the_records WHERE REPLACE(REPLACE(REPLACE(REPLACE(name, ',', ''), '&amp;', ''), '\"', ''), \"'\", '') REGEXP '%s'", $regex_name);
}
echo '&lt;pre&gt;MySQL queries with attack -- '.print_r($unclean,1).'&lt;/pre&gt;';
</code></pre>

<p>Second, a run that DOES deal with the attack:</p>

<pre><code>$clean = $names;
foreach ($clean as $name=&gt;$dbname) {
  $regex_name = preg_replace('/[^[:alnum:]-]/', '', $name);
  $regex_name = preg_replace('/[-]+/', '[^[:alnum:]]+', $regex_name);
  $clean[$name] = sprintf("SELECT * from the_records WHERE REPLACE(REPLACE(REPLACE(REPLACE(name, ',', ''), '&amp;', ''), '\"', ''), \"'\", '') REGEXP '%s'", $regex_name);
}
echo '&lt;pre&gt;MySQL queries with attack cleaned -- '.print_r($clean,1).'&lt;/pre&gt;';
</code></pre>

<p>Aaaand that's enough brainstorming for me for one night! =o)</p>

### Answer ID: 4370440
<p>It's a little janky, but you could explode the GET and build a WHERE on multiple conditions.</p>

<p>Something like (untested):</p>

<pre><code>$name_array = explode("-", $_GET['name']);

$sql_str = "SELECT * FROM the_records WHERE ";

$first_time = true;
foreach($name_array as $name){
    if ($name != ""){
        if ($first_time){
            $sql_str .= "name LIKE \"%".$name."%\"";
            $first_time = false;
        }
        else {
            $sql_str .= " AND name LIKE \"%".$name."%\"";
        }
    }
}
</code></pre>

### Answer ID: 4351810
<p>Using str_replace function we will grab the $name parameter and replace </p>

<pre><code>ampersands (&amp;) with "" 
spaces (" ") with "-"
commas (",") with ""
apostrophes("'") with ""
</code></pre>

<blockquote>
  <p><strong>str_replace</strong> ( mixed $search , mixed $replace , mixed $subject [, int &amp;$count ] )</p>
  
  <p>$Search = { "&amp;", " ", ",", "'" }<br>
  $Replace = { "", "-", "", "" }</p>
</blockquote>

<pre><code>$ComparableString = str_replace($Search, $Replace, $_GET['name'])
</code></pre>

<p>After that we can do the sql query:</p>

<pre><code>$name = mysql_real_escape_string($name, $db_resource);
SELECT * from the_records WHERE name='$name'
</code></pre>

