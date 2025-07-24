# array_filter and array_intersect performance improvements on large foreach loop
[Link to question](https://stackoverflow.com/questions/74027147/array-filter-and-array-intersect-performance-improvements-on-large-foreach-loop)
**Creation Date:** 1665486553
**Score:** 0
**Tags:** php, arrays
## Question Body
<p><strong>EDIT: Thanks to nice_dev for providing an excellent solution below!</strong></p>
<p>I had to rewrite part of his query for correct results:</p>
<p>From:</p>
<pre><code>$tmpmatch['unmatched'] = array_filter($deck['main_deck'],
            function ($val) use (&amp;$tmparray, &amp;$matched) {
              $matched[ $val ] = $matched [$val] ?? 0;
              $matched[ $val ]++;
              return $matched[ $val ] &lt;= $tmparray[ $val ];
            }
        );   
</code></pre>
<p>To:</p>
<pre><code>$tmpmatch['unmatched'] = array_filter($deck['main_deck'],
 function ($val) use (&amp;$tmparray) {
  return empty($tmparray[$val]) || !$tmparray[$val]++;
 }
);
</code></pre>
<p><strong>Original:</strong></p>
<p>I'm attempting to compare arrays to get a new array of matched and unmatched items. I have a loop that goes through roughly 55,000 items. The processing of this script can take upwards of 20+ minutes to attempt to complete and I've narrowed it down to both usage of <code>array_intersect</code> and <code>array_filter</code> within the foreach. Ideally, I need it to complete much faster. If I limit the foreach to 1000 items it still takes upwards of ~3 minutes to complete which is slow for the client-side experience.</p>
<p>If I remove them, the script completes almost immediately. As such, I will include only these relevant pieces in the code below.</p>
<p>I'm using a custom <code>array_intersect_fixed</code> function as regular <code>array_intersect</code> returned wrong results with duplicate values as per <a href="https://www.php.net/manual/en/function.array-intersect.php#104063" rel="nofollow noreferrer">here</a>.</p>
<p>Explanations:</p>
<p><code>totalidsarray</code> = An array of numbers such as ['11233', '35353, '3432433', '123323']. Could contain <strong>thousands</strong> of items.</p>
<p><code>$deck['main_deck']</code> = An array of numbers to compare against <code>$totalidsarray</code>. Similar structure. Max length is 60 items.</p>
<pre><code>foreach($dbdeckarray as $deck){

         $tmparray = $totalidsarray;

        //Get an array of unmatched cards between the deck and the collection
        //Collection = $tmparray
        $tmpmatch['unmatched'] = array_filter($deck['main_deck'],
            function ($val) use (&amp;$tmparray) {
                $key = array_search($val, $tmparray);
                if ( $key === false ) return true;
                unset($tmparray[$key]);
                return false;
            }
        );   

        //Get an array of matched cards between the deck and the collection
        $tmpmatch['matched'] = array_intersect_fixed($deck['main_deck'], $totalidsarray);

        //Push results to matcharray
        $matcharray[] = $tmpmatch;

}

//Built in array_intersect function returns wrong result when input arrays have duplicate values.
function array_intersect_fixed($array1, $array2) {
    $result = array();
    foreach ($array1 as $val) {
        if (($key = array_search($val, $array2, FALSE))!==false) {
            $result[] = $val;
            unset($array2[$key]);
        }
    }
    return $result;
}
</code></pre>
<p>To make matters worse, I have to do 2 further matched/unmatched checks within that same foreach loop against another array <code>extra_deck</code>, further increasing processing time.</p>
<p>Is there a more optimized approach I can take to this?</p>
<p><strong>EDIT: Explanation of what the code needs to achieve.</strong></p>
<p>The script will retrieve the user's card collection of cards that they own from a card game. This is assigned into <code>totalidsarray</code>. It will then query every deck in the database (~55,000) and compare the collection you own against the built deck of cards (<code>main_deck</code>). It then attempted to extract all owned cards (<code>matched</code>) and all un-owned cards (<code>unmatched</code>) into two arrays. Once the full foreach loop is done, the client-side returns a list of each deck alongside the matched cards/unmatched cards of each (with a % match for each).</p>

## Answers
### Answer ID: 74027709
<p>A couple of optimizations I can suggest:</p>
<ul>
<li><p>The <code>array_intersect_fixed</code> routine you have is quadratic in nature in terms of getting the result, because it is 2 nested loops under the hood. We can use <code>array_count_values</code> to optimize it to work in linear time(which uses a map).</p>
</li>
<li><p><code>json_decode()</code> doesn't need to be done twice for every deck. If you do it once and use it wherever needed, it should work just fine(unless you make any edits in place which I don't find right now) . It also needs to be decoded to an array and not to an object using the <code>true</code> flag.</p>
</li>
<li><p>For your <code>array_filter</code>, the comparison is also quadratic in nature. We will use <code>array_count_values</code> again to optimize it and use a <code>$matched</code> array. We keep counting the frequency of elements and if any of them surpasses count in <code>$tmparray</code>, we return <code>false</code>, else, we return <code>true</code>.</p>
</li>
</ul>
<p><strong>Snippet:</strong></p>
<pre><code>&lt;?php 

$tmparray = array_count_values($totalidsarray);

foreach($dbdeckarray as $deck){
        $matched = [];        
        $deck['main_deck'] = json_decode($deck['main_deck'], true);
        $tmpmatch['unmatched'] = array_filter($deck['main_deck'],
            function ($val) use (&amp;$tmparray, &amp;$matched) {
              $matched[ $val ] = $matched [$val] ?? 0;
              $matched[ $val ]++;
              return $matched[ $val ] &lt;= $tmparray[ $val ];
            }
        );   

        $tmpmatch['matched'] = array_intersect_fixed($deck['main_deck'], $tmparray);
        $matcharray[] = $tmpmatch;
}

function array_intersect_fixed($array1, $array2) {
    $result = array();
    $matched = [];
    foreach ($array1 as $val) {
        $matched[ $val ] = $matched[ $val ] ?? 0;
        $matched[ $val ]++;
        if (isset($array2[ $val ]) &amp;&amp; $matched[ $val ] &lt;= $array2[ $val ]) {
            $result[] = $val;
        }
    }
    return $result;
}
</code></pre>
<p><strong>Note:</strong> <code>array_intersect_fixed</code> expects <code>$array2</code> to be in the Hashmap way by default. If you wish to use it elsewhere, make sure to pass <code>array_count_values</code> of the array as 2nd parameter or use a third parameter to indicate a flag check otherwise.</p>

### Answer ID: 74028160
<p>Beside @nice_dev suggestion your code can be simplified.</p>
<p>The unmatched part is an array diff</p>
<pre><code>array_diff($deck['main_deck'], $tmparray);
</code></pre>
<p>The array_intersect_fixed(), if the problem are duplicated value in array, can be avoided by running array_unique() on the array (I guess is $deck['main_deck']) before calling array_intersect()</p>
<p>This will also speed up array_diff() as it will have less array element to compare.</p>

