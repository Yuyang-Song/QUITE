# Convert foreach php queries into SQL
[Link to question](https://stackoverflow.com/questions/15736415/convert-foreach-php-queries-into-sql)
**Creation Date:** 1364779014
**Score:** 0
**Tags:** php, mysql, query-optimization
## Question Body
<p>I have two php functions that perform rather slowly since i have a large database. One makes a request for category names. The other makes a subcategory count. Below, I have tried converting to SQL to speed up queries but not sure how to work around the foreach loop, or if this is the most efficient SQL query method. Your feedback is appreciated.</p>

<p>The first:</p>

<pre><code>function GetCatName($catid){
global $db, $dblang, $the_cats;

foreach($the_cats as $cat){
    if($cat-&gt;category_id == $catid &amp;&amp; $cat-&gt;category_lang == $dblang)
    {
        $x = $cat-&gt;category_name;
    }
}
return $x;
}
</code></pre>

<p>Rewrite to SQL:</p>

<pre><code>function GetCatName($catid){
global $db, $dblang;

$sql = "SELECT category_name FROM ".table_categories." where category_id = ".$catid." and category_lang = ".$dblang.";";

$x = $db-&gt;get_result($sql);

return $x;
}
</code></pre>

<p>The second:</p>

<pre><code>  function GetSubCatCount($catid){
global $db, $the_cats;

$count = 0;

foreach($the_cats as $cat){
    if(isset($cat-&gt;category_parent)){
        if($cat-&gt;category_parent == $catid &amp;&amp; $cat-&gt;category__auto_id &lt;&gt; 0 &amp;&amp; $cat-&gt;category_lang == $dblang)
        { 
            $count = $count + 1;
        }
    }
}

return $count;
}
</code></pre>

<p>Rewrite to SQL:</p>

<pre><code>function GetSubCatCount($catid){
global $db, $the_cats;

$count = 0;

foreach($the_cats as $cat){
    if(isset($cat-&gt;category_parent)){
    $sub_cateogories = $db-&gt;get_results("SELECT * FROM ".table_categories." where category_parent = ".$cat-&gt;category__auto_id." and category_order = 0 AND category__auto_id&lt;&gt;0;");
    $count = count($sub_cateogories);
    }
}

return $count;
}
</code></pre>

<p>Thanks</p>

## Answers
### Answer ID: 15736871
<p>As I mentioned in the comment you need to use <code>$catid</code>, otherwise the query has no improvement whatsoever.</p>

<p>This can be done as you did it in the first case where you replaced </p>

<pre><code>$cat-&gt;category_id == $catid &amp;&amp; $cat-&gt;category_lang == $dblang
</code></pre>

<p>through</p>

<pre><code>category_id = ".$catid." and category_lang = ".$dblang."
</code></pre>

<p>This would bring us to changing the <code>where</code> statement to</p>

<pre><code>category_parent = ".$catid." and category_order = 0 AND category_auto_id&lt;&gt;0
</code></pre>

<p>without using the foreach loop of course</p>

